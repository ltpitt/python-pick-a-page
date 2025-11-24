# 📖 Pick-a-Page

**Create interactive "Choose Your Own Adventure" stories with Python!**

A simple tool designed for teaching programming to children. Write stories in plain text, compile them to beautiful web pages, and share them with friends!

## ✨ Features

- 📝 **Super simple syntax** - Just `[[choices]]` and plain text
- 🌐 **Child-friendly web interface** - No command line needed!
- 🎮 **Modern story player** - Smooth scrolling like Squiffy/Twine
- 🖼️ **Image support** - Embed images directly in your stories
- 🌍 **15 languages** - English, Dutch, Italian, Spanish, French, Portuguese, German, Russian, Chinese, Hindi, Arabic, Bengali, Urdu, Indonesian, Bulgarian
- 📦 **Portable** - Single HTML file output, works offline
- ✅ **Battle-tested** - 160 tests, 81% code coverage
- 🎯 **Zero dependencies** - Pure Python stdlib only

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ltpitt/python-pick-a-page.git
cd python-pick-a-page

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dev dependencies (optional, for testing)
pip install -r requirements.txt
```

### Requirements

- Python 3.10+ (compatible with Mac OS X 10.5 via Tigerbrew)
- No runtime dependencies (uses only Python standard library)
- pytest, pytest-cov (development only)

### 🎨 Option 1: Web Interface (Recommended!)

Perfect for kids - no command line needed!

```bash
python -m pick_a_page serve
```

Your browser opens automatically at `http://127.0.0.1:8000` with:
- 📚 **Library** - Browse and play existing stories
- ✏️ **Editor** - Write and edit stories with live validation
- 🎮 **Player** - Play stories with one click

**Sharing on network:**
```bash
python -m pick_a_page serve --host 0.0.0.0 --port 8000
# Access from any device on your network!
```

### ⌨️ Option 2: Command Line

For power users and automation:

```bash
# Compile a story to HTML (opens in browser automatically)
python -m pick_a_page compile stories/dragon_quest_en.txt

# Compile without opening browser
python -m pick_a_page compile story.txt --no-open

# Create a new story from template
python -m pick_a_page init my_adventure

# Validate story structure (check for broken links)
python -m pick_a_page validate my_adventure.txt
```

**Using Makefile shortcuts:**
```bash
make test          # Run all tests with coverage
make test-watch    # Continuous testing during development
make coverage      # Detailed coverage report
make lint          # Check code style
```

## 🌍 Multi-Language Support

Pick-a-Page speaks **15 languages**! Perfect for teaching programming worldwide.

**Available Languages:**
🇬🇧 English • 🇳🇱 Dutch • 🇮🇹 Italian • 🇪🇸 Spanish • 🇫🇷 French • 🇵🇹 Portuguese • 🇩🇪 German • 🇷🇺 Russian • 🇨🇳 Chinese • 🇮🇳 Hindi • 🇸🇦 Arabic • 🇧🇩 Bengali • 🇵🇰 Urdu • 🇮🇩 Indonesian • 🇧🇬 Bulgarian

### Quick Setup

```bash
# Set your language (permanent)
export PICK_A_PAGE_LANG=nl  # Dutch
echo 'export PICK_A_PAGE_LANG=nl' >> ~/.zshrc  # Make it permanent

# Or just for one command
PICK_A_PAGE_LANG=it python -m pick_a_page inizializza mia-storia
```

### Web Interface

The web GUI automatically detects your language preference and lets you switch between all 15 languages with a dropdown selector!

### Localized Commands

Commands change based on language:

| English | Dutch | Italian | Spanish | French |
|---------|-------|---------|---------|--------|
| `init` | `initialiseren` | `inizializza` | `inicializar` | `initialiser` |
| `compile` | `compileren` | `compila` | `compilar` | `compiler` |
| `validate` | `valideren` | `valida` | `validar` | `valider` |

All UI messages, help text, and story templates adapt to your chosen language!

## 📝 Story Format

Super simple! Just plain text with `[[choices]]`.

### Complete Example

```markdown
---
title: The Dragon's Secret
author: Young Inventor
---

[[beginning]]

You find a glowing scale on your windowsill. It hums softly.

Your friend Alex bursts in: "Did you see the lightning? It hit the old tower!"

[[Investigate the tower]]
[[Study the scale first|examine-scale]]

---

[[Investigate the tower]]

The tower looms ahead. You hear something big moving inside!

[[Enter bravely]]
[[Go back|examine-scale]]

---

[[examine-scale]]

Through your magnifying glass, you see tiny symbols: "Dragon in danger. Help."

[[Rush to the tower|Enter bravely]]

---

[[Enter bravely]]

Inside, a magnificent dragon sits trapped in chains! Time to help!

🎉 Adventure begins!
```

### Syntax Reference

| Syntax | What it does |
|--------|-------------|
| `---`<br>`title: Story Title`<br>`author: Your Name`<br>`---` | **Metadata** (required at top) |
| `[[section-name]]` | **Define a section** (normalized: "Section Name" → "section-name") |
| `[[Choice text]]` | **Create a button** (links to section "choice-text") |
| `[[Display\|target]]` | **Custom button text** (shows "Display", goes to "target") |
| `---` | **Section separator** |
| `![Alt text](image.jpg)` | **Embed image** (Base64 encoded in output) |
| `**bold**` • `*italic*` | **Text formatting** |

**Pro tips:**
- Sections without choices = story endings
- First section in file = starting point
- Broken links are caught during validation!

## 🛠️ Development

Built with **Test-Driven Development (TDD)** for rock-solid reliability!

### Test Suite

```bash
make test          # Run 160 tests (81% coverage)
make test-watch    # Continuous testing (great for TDD!)
make coverage      # Detailed coverage report
make lint          # Check code style
```

**Coverage by module:**
- `compiler.py` - 97% (story parsing & validation)
- `generator.py` - 90% (HTML generation)
- `i18n.py` - 93% (translations)
- `__main__.py` - 80% (CLI interface)
- `server.py` - 70% (web server)

### Project Structure

```
pick_a_page/
├── pick_a_page/              # Main package
│   ├── compiler.py           # 130 lines - Story parser & validator
│   ├── generator.py          # 72 lines - HTML/CSS/JS generator
│   ├── i18n.py              # 27 lines - 15-language translations
│   ├── server.py            # 279 lines - Web GUI server
│   ├── templates.py         # 3 lines - Story templates
│   └── __main__.py          # 168 lines - CLI commands
├── tests/                   # 160 tests
│   ├── test_compiler.py     # Parser tests
│   ├── test_generator.py   # HTML generator tests
│   ├── test_i18n.py        # Translation tests
│   ├── test_cli.py         # CLI tests
│   ├── test_server.py      # Web server tests
│   └── test_integration.py # End-to-end tests
├── stories/                 # Example stories (EN, NL, IT)
└── output/                  # Compiled HTML (gitignored)
```

### Design Principles

Following the project's core values:

1. **🎯 Simplicity First** - Easy enough for 8-year-olds
2. **📦 Zero Dependencies** - Pure Python stdlib (runtime)
3. **✅ TDD Always** - Red → Green → Refactor
4. **🎨 Modern UX** - Squiffy-inspired scrolling narrative
5. **🧪 Battle-Tested** - High coverage, real-world usage

## 🎨 Web Interface

Beautiful, book-styled interface designed for children!

**Features:**
- 📚 **Story Library** - Card-based story browser with metadata
- ✏️ **Live Editor** - Real-time validation and syntax highlighting
- 🎮 **Embedded Player** - Play stories without leaving the app
- 🌍 **Language Switcher** - All 15 languages, one click
- 🎨 **Gorgeous Design** - Purple gradient with book metaphor

**Server Options:**
```bash
# Basic usage (auto-opens browser)
python -m pick_a_page serve

# Custom configuration
python -m pick_a_page serve --host 0.0.0.0 --port 8080 \
  --stories my_stories --output compiled --no-open
```

**Deploy Anywhere:**
Works on any server with Python 3.10+ (no external deps!):
```bash
# Cloud server
python -m pick_a_page serve --host 0.0.0.0 --port 8000

# Access from network: http://your-server-ip:8000
```

## 🔧 How It Works

### Architecture

```
Story Text → Parser → Validator → Generator → HTML File
                ↓                      ↓
            Data Model           Single File
         (Story, Sections)    (HTML+CSS+JS+Images)
```

**Core Components:**

1. **Parser** (`compiler.py`, 130 lines)
   - Extracts metadata, sections, choices, images
   - Normalizes section names (`"Go Home"` → `"go-home"`)
   - Validates all links point to real sections

2. **Validator** (built into parser)
   - Checks for broken links
   - Detects orphaned sections
   - Ensures story structure is sound

3. **Generator** (`generator.py`, 72 lines)
   - Creates single HTML file with embedded:
     - CSS (Squiffy-inspired responsive design)
     - JavaScript (event delegation for navigation)
     - Images (Base64 encoded)
   - Print-ready styles for PDF export

4. **Web Server** (`server.py`, 279 lines)
   - Pure Python `http.server` (no dependencies!)
   - REST API for CRUD operations
   - Child-friendly interface with validation

5. **i18n** (`i18n.py`, 27 lines)
   - Dictionary-based translations
   - 15 languages, environment-aware
   - Web UI + CLI support

### Story Navigation

**Squiffy-style chronological scrolling:**
- First visit: `appendChild()` moves section to end
- Revisit: `cloneNode(true)` creates fresh copy with enabled buttons
- Buttons in current section disabled after click (reading history)

This creates a natural reading flow even with complex branching!

## ✅ Status

**Production Ready!**

- ✅ 160 tests passing (81% coverage)
- ✅ 15 languages fully translated
- ✅ Web GUI battle-tested
- ✅ TDD workflow established
- ✅ Zero external runtime dependencies
- ✅ Example stories in 3 languages
- ✅ Comprehensive documentation

**Roadmap:**
- 📚 More example stories (community contributions welcome!)
- 🎨 Additional story templates
- 🌍 More language translations
- 📖 Video tutorials for kids
- 🔌 Plugin system for advanced users

## 🤝 Contributing

We love contributions! This project is perfect for learning TDD.

**Guidelines:**
1. 🔴 **Write tests first** (TDD: Red → Green → Refactor)
2. ✅ **All tests must pass** (`make test`)
3. 📊 **Maintain >85% coverage** (`make coverage`)
4. 🎨 **Follow PEP 8** (`make lint`)
5. 📦 **Stdlib only** (no new runtime dependencies!)

**Great starter contributions:**
- 📚 Add example stories in different languages
- 🌍 Translate UI to new languages (we have 15, let's add more!)
- 📖 Write tutorials or documentation
- 🐛 Fix bugs or improve error messages
- ✨ Add tests for uncovered code

See `AGENTS.md` for detailed development guidelines.

## 📄 License

MIT License - See LICENSE file for details.

## 💝 Credits

Created by a parent teaching programming to their 8-year-old daughter.

**Inspired by:**
- [Squiffy](https://github.com/textadventures/squiffy) - Scrolling narrative style
- [Twine](https://twinery.org/) - Interactive fiction
- Classic "Choose Your Own Adventure" books

**Built with:**
- ❤️ Love for education
- 🧪 Test-Driven Development
- 🎯 Simplicity as a feature
- 🌍 Accessibility for all

---

**Made with ❤️ for young programmers everywhere!**

*"The best way to learn programming is to build something fun." — Anonymous Parent-Teacher*
