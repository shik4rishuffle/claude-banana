# claude-banana

MCP server for [Nano Banana](https://deepmind.google/models/gemini-image/) — Google's Gemini image generation and editing models.

## Tools

| Tool | Description |
|------|-------------|
| `generate_image` | Text → image using Nano Banana 2 or Pro |
| `edit_image` | Image + prompt → edited image |
| `combine_images` | Two images + prompt → merged/composited image |
| `describe_image` | Image → detailed text description or Q&A |

## Setup

### 1. Get a Gemini API key

Go to [Google AI Studio](https://aistudio.google.com/apikey) and create a key. Free tier is available.

### 2. Install dependencies

```bash
cd claude-banana
pip install -r requirements.txt
```

Or with a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add to Claude Code

Add to your `~/.claude/settings.json` (or project-level `.claude/settings.json`):

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "python",
      "args": ["/absolute/path/to/claude-banana/server.py"],
      "env": {
        "GEMINI_API_KEY": "your-key-here"
      }
    }
  }
}
```

If using a virtualenv, point to the venv's Python:

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "/absolute/path/to/claude-banana/.venv/bin/python",
      "args": ["/absolute/path/to/claude-banana/server.py"],
      "env": {
        "GEMINI_API_KEY": "your-key-here"
      }
    }
  }
}
```

### 4. Add to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "python",
      "args": ["/absolute/path/to/claude-banana/server.py"],
      "env": {
        "GEMINI_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Usage examples

Once connected, you can ask Claude:

- *"Generate an image of a narrowboat at sunrise on the Kennet and Avon canal"*
- *"Edit ~/photos/boat.jpg — make it look like an oil painting"*
- *"Combine ~/img/cat.jpg and ~/img/garden.jpg — place the cat in the garden"*
- *"Describe ~/screenshots/design.png — what UI elements are visible?"*

## Models

| Key | Model | Notes |
|-----|-------|-------|
| `flash` | `gemini-3.1-flash-image-preview` | Default. Nano Banana 2 — fast, high quality |
| `pro` | `gemini-3.0-pro-image` | Nano Banana Pro — max fidelity, slower |

Pass `"model": "pro"` in tool arguments to use the Pro model for `generate_image` or `edit_image`.

## Output

- Images are returned inline to the MCP client (base64) **and** saved to disk
- If no `output_path` is specified, images are saved to a system temp file
- All generated images include an invisible SynthID watermark (Google's AI content ID)

## Troubleshooting

**`GEMINI_API_KEY environment variable is not set`**
→ Add the env var to your MCP server config or export it in your shell before running.

**`FileNotFoundError: Image not found`**
→ Use absolute paths or `~/` prefixed paths for image inputs.

**No image returned from edit/combine**
→ Some prompts trigger safety filters. Try rephrasing. The model's text response will be returned instead.
