Set up the nano-banana MCP server for image generation. Here's what to do:

**1. Clone the repo:**
```
git clone https://github.com/shik4rishuffle/claude-banana.git ~/Documents/GitHub/claude-banana
```

**2. Install dependencies:**
The project requires Python 3.10+. Install the requirements:
```
pip install -r requirements.txt
````
If pip fails because the active Python is below 3.10, find or install a 3.10+ version (e.g. via pyenv) and use that instead. Note the absolute path to that Python binary - you'll need it for the config.

**3. Get a Gemini API key:**
Ask me for my Gemini API key. If I don't have one, point me to https://aistudio.google.com/apikey to create one. Do not proceed until you have the key.

**4. Add the MCP server to Claude Code config (`~/.claude/settings.json`):**
Add this to the `mcpServers` object (create it if it doesn't exist):
```json
"nano-banana": {
  "command": "<absolute path to python 3.10+ binary>",
  "args": ["<absolute path to>/claude-banana/server.py"],
  "env": {
    "GEMINI_API_KEY": "<the key>"
  }
}
```

**5. Add the MCP server to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):**
Same config block as above, added to the `mcpServers` object. Create the file if it doesn't exist.

**6. Add image generation instructions to `~/.claude/CLAUDE.md`:**
Append this section:
```
## Image Generation

When the user asks to create, generate, draw, design, or make an image, logo, illustration, picture, icon, graphic, or visual of any kind, use the nano-banana MCP server tools. This includes phrases like "create me an image", "draw me a", "make a logo", "generate a picture of", "I want an image of", "design an icon", etc.

Available tools:
- generate_image - create images from text prompts
- edit_image - modify existing images via natural language
- combine_images - merge or blend two images together
- describe_image - analyse an image and answer questions about it
```

After setup, remind me to restart the Claude Desktop app for the changes to take effect.
