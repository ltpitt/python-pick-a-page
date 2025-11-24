# Pick-a-Page

A simple Python tool for creating interactive story books, designed for children learning programming.

Convert Markdown-style stories with choices into playable web apps and printable books!

## Features

- 📝 Simple Markdown-based story format with `[[choice]]` syntax
- 🌐 **Web GUI for children** - No command line needed!
- 🎮 Interactive web-based story player (Squiffy-style scrolling narrative)
- 🖨️ Print-friendly CSS for PDF output
- 🖼️ Support for images with Base64 embedding
- 📦 Single HTML file + ZIP package distribution
- ✅ Test-driven development with 92 tests and 77%+ code coverage
- 🎯 Zero external dependencies (Python stdlib only)
- 🌍 Multi-language support (English, Dutch, Italian)
- 🖥️ Runs locally or on cloud servers

## Requirements

- Python 3.10+ (compatible with Mac OS X 10.5 via Tigerbrew)
- pytest (for development)

## Quick Start

### Option 1: Web GUI (Recommended for Children)

```bash
# Start the web server
python -m pick_a_page serve

# Your browser will open automatically to http://127.0.0.1:8000
# Click on stories, edit them, and play them - all in the browser!
```

**For cloud servers:**
```bash
# Allow network access
python -m pick_a_page serve --host 0.0.0.0 --port 8000
```

### Option 2: Command Line

```bash
# Install dependencies
make install

# Run tests
make test

# Try compiling an example story
python -m pick_a_page compile stories/dragon_quest_en.txt
# Output will be in: output/dragon_quest_en.html
# The story will automatically open in your default browser!

# To compile without opening the browser
python -m pick_a_page compile stories/dragon_quest_en.txt --no-open

# Create a new story from template
python -m pick_a_page init my_story

# Validate a story (check for broken links)
python -m pick_a_page validate my_story.txt
```

## Language Support

Pick-a-Page supports multiple languages for the CLI interface. Available languages:
- 🇬🇧 English (`en`) - Default
- 🇳🇱 Dutch (`nl`)
- 🇮🇹 Italian (`it`)

### Setting the Language

**Using Environment Variable (Recommended)**

Set the `PICK_A_PAGE_LANG` environment variable to change the language:

```bash
# Set language for the current session
export PICK_A_PAGE_LANG=nl

# All commands will now use Dutch
python -m pick_a_page initialiseren mijn-verhaal
python -m pick_a_page compileren mijn-verhaal.txt
python -m pick_a_page valideren mijn-verhaal.txt

# Or set it for a single command
PICK_A_PAGE_LANG=it python -m pick_a_page inizializza mia-storia
```

**Tip for Young Learners**: Add this to your shell profile (`.bashrc`, `.zshrc`, etc.) to make it permanent:
```bash
# Always use Dutch for Pick-a-Page
export PICK_A_PAGE_LANG=nl
```

### Localized Commands

Commands are translated in each language. When you set a language, you must use the localized command names:

| English | Dutch | Italian | Description |
|---------|-------|---------|-------------|
| `init` | `initialiseren` | `inizializza` | Create a new story |
| `compile` | `compileren` | `compila` | Compile story to HTML |
| `validate` | `valideren` | `valida` | Validate story format |

**Examples:**
```bash
# English (default)
python -m pick_a_page init my_story
python -m pick_a_page compile my_story.txt
python -m pick_a_page validate my_story.txt

# Dutch
export PICK_A_PAGE_LANG=nl
python -m pick_a_page initialiseren mijn-verhaal
python -m pick_a_page compileren mijn-verhaal.txt
python -m pick_a_page valideren mijn-verhaal.txt

# Italian
export PICK_A_PAGE_LANG=it
python -m pick_a_page inizializza mia-storia
python -m pick_a_page compila mia-storia.txt
python -m pick_a_page valida mia-storia.txt
```

**Note**: All messages, help text, and generated story templates will also be in the selected language. The generated HTML will have the appropriate `lang` attribute (e.g., `<html lang="nl">` for Dutch).

## Story Format

Stories are written in plain text with simple markup:

```markdown
---
title: My First Adventure
author: Your Name
---

[[beginning]]

You wake up in a mysterious forest. The sun is shining through the tall trees.

What do you want to do?

[[Explore the forest]]
[[Follow the path]]

---

[[Explore the forest]]

You venture deeper into the forest and discover a sparkling stream.

[[Follow the stream]]
[[Go back|beginning]]

---

[[Follow the path]]

The path leads you to a small cottage with smoke coming from the chimney.

You found a safe place!

---

[[Follow the stream]]

You follow the stream and find a treasure chest filled with gold!

You won!
```

**Key syntax:**
- `[[section-name]]` - Defines a new section (simple, no colon needed!)
- `[[Choice text]]` - Creates a button that links to section "Choice text"
- `[[Display text|target-section]]` - Custom button text linking to different section
- `---` - Separates sections
- Sections with no choices are story endings

### Adding Images

```markdown
![Description](image.jpg)
```

Images will be embedded in the final HTML file.

## Development

This project follows Test-Driven Development (TDD) principles:

```bash
# Run tests
make test

# Run tests with coverage report
make coverage

# Run tests in watch mode
make test-watch

# Lint code
make lint

# Clean build artifacts
make clean
```

## Project Structure

```
pick_a_page/
├── pick_a_page/           # Main package
│   ├── __init__.py
│   ├── __main__.py        # CLI interface
│   ├── compiler.py        # Story parser and validator
│   ├── generator.py       # HTML generator
│   ├── templates.py       # CSS/JS templates
│   ├── server.py          # Web GUI server (NEW!)
│   └── i18n.py            # Internationalization (translations)
├── tests/                 # Test suite (92 tests, 77% coverage)
│   ├── fixtures/          # Sample story files
│   │   ├── valid_story.txt
│   │   ├── broken_links.txt
│   │   ├── with_images.txt
│   │   └── images/
│   ├── test_compiler.py   # Parser tests (21 tests)
│   ├── test_generator.py  # Generator tests (18 tests)
│   ├── test_i18n.py       # Translation tests (20 tests)
│   ├── test_cli.py        # CLI tests (9 tests)
│   └── test_integration.py # E2E tests (24 tests)
├── stories/               # Example stories (EN/NL/IT)
│   ├── dragon_quest_en.txt
│   ├── dragon_quest_nl.txt
│   └── dragon_quest_it.txt
├── output/                # Compiled stories output here
├── Makefile              # Build automation
├── requirements.txt      # Dev dependencies
├── STORY_GUIDE.md        # User guide in 3 languages
└── README.md
```

## Web GUI

The web interface provides a **child-friendly** way to create and play stories without using the command line:

- 📚 **Story Library**: Browse and select stories
- ✏️ **Editor**: Create and edit stories with live validation
- ▶️ **Play**: Compile and play stories with one click
- 💾 **Save**: Save stories directly from the browser
- 🎨 **Beautiful UI**: Colorful, gradient design perfect for kids

**Server Options:**
```bash
# Start server (opens browser automatically)
python -m pick_a_page serve

# Don't open browser
python -m pick_a_page serve --no-open

# Allow network access (for other devices)
python -m pick_a_page serve --host 0.0.0.0

# Use different port
python -m pick_a_page serve --port 3000

# Custom story directory
python -m pick_a_page serve --stories my_stories --output my_output
```

**Cloud Deployment:**

The server uses only Python stdlib (`http.server`), so it works on any server with Python 3.10+:

```bash
# On cloud server
python -m pick_a_page serve --host 0.0.0.0 --port 8000

# Access from anywhere
http://your-server-ip:8000
```

## How It Works

1. **Parser** (`compiler.py`): Reads story text, extracts sections and choices, validates all links
2. **Generator** (`generator.py`): Converts parsed story into single HTML file with embedded CSS/JavaScript
3. **Server** (`server.py`): Provides web GUI with REST API for story management (stdlib only!)
4. **Internationalization** (`i18n.py`): Provides translations for CLI in English, Dutch, and Italian
5. **Navigation**: Squiffy-style scrolling where sections append as you make choices
6. **Backtracking**: When revisiting a section, it's cloned with fresh choices at the end
7. **Output**: Single standalone HTML file + ZIP package with images and source

## Current Status

✅ **Implemented:**
- **Web GUI server** with child-friendly interface (NEW!)
- Story parser with validation (97% coverage, 21 tests)
- HTML/CSS/JS generator (90% coverage, 18 tests)
- CLI commands: compile, validate, init, serve
- Multi-language support (English, Dutch, Italian) with 20 tests
- Squiffy-style scrolling navigation
- Section cloning for backtracking
- Image embedding (Base64)
- Integration tests (24 tests covering all paths)
- Print-friendly CSS
- Browser auto-open feature (9 CLI tests)

📋 **TODO:**
- Additional example stories in `stories/` directory
- Additional story templates
- Additional language translations (contributions welcome!)

## Contributing

Contributions welcome! Please:

1. Write tests first (TDD approach)
2. Ensure all tests pass (`make test`)
3. Maintain >85% code coverage
4. Follow existing code style (PEP 8)
5. Use Python stdlib only (no external runtime dependencies)

## License

MIT License - See LICENSE file for details

## Credits

Created for teaching programming to an 8-year-old daughter.

Inspired by Squiffy and other interactive fiction tools.
