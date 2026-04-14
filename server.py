#!/usr/bin/env python3
"""
Nano Banana MCP Server
Google Gemini image generation and editing via Model Context Protocol.
"""

import asyncio
import base64
import os
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from google import genai
from google.genai import types as genai_types
from PIL import Image

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

app = Server("claude-banana")

# Model aliases
MODELS = {
    "flash": "gemini-3.1-flash-image-preview",   # Nano Banana 2 — fast, high quality
    "pro":   "gemini-3.0-pro-image",              # Nano Banana Pro — max fidelity
}
DEFAULT_MODEL = "flash"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Get a key at https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=api_key)


def resolve_model(key: str | None) -> str:
    return MODELS.get(key or DEFAULT_MODEL, MODELS[DEFAULT_MODEL])


def load_image(path: str) -> Image.Image:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return Image.open(p)


def image_to_base64(image: Image.Image) -> str:
    buf = BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def get_output_dir() -> Path:
    d = Path.home() / ".claude-banana" / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_image(image: Image.Image, output_path: str | None) -> str:
    if output_path:
        p = Path(output_path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        image.save(p)
        return str(p)
    else:
        d = get_output_dir()
        f = tempfile.NamedTemporaryFile(dir=d, suffix=".png", prefix="banana_", delete=False)
        image.save(f.name)
        f.close()
        return f.name


def extract_image(response) -> Image.Image | None:
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return Image.open(BytesIO(part.inline_data.data))
    return None


def extract_text(response) -> str:
    parts = []
    for part in response.candidates[0].content.parts:
        if part.text:
            parts.append(part.text)
    return "\n".join(parts)


def image_result(image: Image.Image, saved_path: str, has_output_path: bool) -> list:
    if has_output_path:
        return [
            types.TextContent(type="text", text=f"Image saved to {saved_path}"),
        ]
    return [
        types.TextContent(type="text", text=f"Saved to: {saved_path}"),
        types.ImageContent(type="image", data=image_to_base64(image), mimeType="image/png"),
    ]


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="generate_image",
            description=(
                "Generate an image from a text prompt using Nano Banana "
                "(Google's Gemini image model). Returns the image and saves it to disk."
            ),
            inputSchema={
                "type": "object",
                "required": ["prompt"],
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": (
                            "Detailed description of the image to generate. "
                            "More detail = better results. "
                            "Example: 'A cinematic photo of a canal boat at dusk, "
                            "warm golden light reflecting on the water, highly detailed.'"
                        ),
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional file path to save the image (e.g. ~/Desktop/output.png). "
                                       "Defaults to a temp file if omitted.",
                    },
                    "model": {
                        "type": "string",
                        "enum": ["flash", "pro"],
                        "description": (
                            "'flash' = Nano Banana 2 (fast, great quality, default). "
                            "'pro' = Nano Banana Pro (max fidelity, slower)."
                        ),
                    },
                },
            },
        ),
        types.Tool(
            name="edit_image",
            description=(
                "Edit an existing image using a natural language prompt. "
                "Supports style changes, object replacement, background swaps, "
                "text overlay, restoration, localisation, and more."
            ),
            inputSchema={
                "type": "object",
                "required": ["image_path", "prompt"],
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute or ~ path to the input image.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": (
                            "Description of the edit. Be specific. "
                            "Examples: 'Make it look like a watercolour painting', "
                            "'Replace the sky with a dramatic sunset', "
                            "'Restore this old damaged photo', "
                            "'Add the text OPEN in bold red above the door'."
                        ),
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional path to save the result.",
                    },
                    "model": {
                        "type": "string",
                        "enum": ["flash", "pro"],
                        "description": "'flash' (default) or 'pro' for maximum fidelity.",
                    },
                },
            },
        ),
        types.Tool(
            name="combine_images",
            description=(
                "Merge or blend two images together using a text prompt. "
                "Useful for compositing, placing objects into scenes, "
                "applying a style from one image to another, or fusing concepts."
            ),
            inputSchema={
                "type": "object",
                "required": ["image_path_1", "image_path_2", "prompt"],
                "properties": {
                    "image_path_1": {
                        "type": "string",
                        "description": "Path to the first (primary) image.",
                    },
                    "image_path_2": {
                        "type": "string",
                        "description": "Path to the second image.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": (
                            "How to combine them. "
                            "Examples: 'Place the cat from image 1 into the living room in image 2', "
                            "'Apply the colour palette from image 2 to image 1', "
                            "'Merge these two portraits into one composite face'."
                        ),
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional path to save the result.",
                    },
                },
            },
        ),
        types.Tool(
            name="describe_image",
            description=(
                "Analyse an image and return a detailed description or answer a "
                "specific question about it. Uses Gemini's vision capabilities."
            ),
            inputSchema={
                "type": "object",
                "required": ["image_path"],
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image to analyse.",
                    },
                    "question": {
                        "type": "string",
                        "description": (
                            "Specific question to ask about the image. "
                            "Defaults to a general detailed description if omitted. "
                            "Examples: 'What text is visible?', "
                            "'What objects are in the foreground?', "
                            "'Is this AI-generated?'"
                        ),
                    },
                },
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list:
    client = get_client()

    # --- generate_image ---
    if name == "generate_image":
        prompt = arguments["prompt"]
        model = resolve_model(arguments.get("model"))
        output_path = arguments.get("output_path")

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            ),
        )

        image = extract_image(response)
        if image is None:
            return [types.TextContent(type="text", text=f"No image generated. Model said: {extract_text(response)}")]

        saved = save_image(image, output_path)
        return image_result(image, saved, bool(output_path))

    # --- edit_image ---
    elif name == "edit_image":
        input_image = load_image(arguments["image_path"])
        prompt = arguments["prompt"]
        model = resolve_model(arguments.get("model"))
        output_path = arguments.get("output_path")

        response = client.models.generate_content(
            model=model,
            contents=[prompt, input_image],
            config=genai_types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            ),
        )

        image = extract_image(response)
        if image is None:
            return [types.TextContent(type="text", text=f"No image returned. Model said: {extract_text(response)}")]

        saved = save_image(image, output_path)
        return image_result(image, saved, bool(output_path))

    # --- combine_images ---
    elif name == "combine_images":
        img1 = load_image(arguments["image_path_1"])
        img2 = load_image(arguments["image_path_2"])
        prompt = arguments["prompt"]
        output_path = arguments.get("output_path")

        response = client.models.generate_content(
            model=resolve_model("flash"),
            contents=[prompt, img1, img2],
            config=genai_types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            ),
        )

        image = extract_image(response)
        if image is None:
            return [types.TextContent(type="text", text=f"No image returned. Model said: {extract_text(response)}")]

        saved = save_image(image, output_path)
        return image_result(image, saved, bool(output_path))

    # --- describe_image ---
    elif name == "describe_image":
        input_image = load_image(arguments["image_path"])
        question = arguments.get("question") or (
            "Please describe this image in detail. Include: main subjects, "
            "composition, colours, mood, style, any visible text, and any notable details."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[question, input_image],
        )

        return [types.TextContent(type="text", text=extract_text(response))]

    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
