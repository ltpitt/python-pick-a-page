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
- ✅ **Battle-tested** - 135 tests, 91% code coverage
- 🚀 **Modern API** - FastAPI backend with REST endpoints

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ltpitt/python-pick-a-page.git
cd python-pick-a-page

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt          # Dev dependencies (pytest, etc.)
pip install -r backend/requirements.txt  # Backend dependencies (FastAPI, etc.)
```

### Requirements

- Python 3.13+ (or Python 3.10+)
- FastAPI 0.122.0+
- Uvicorn (ASGI server)
- pytest, pytest-cov, httpx (development only)

### 🎨 Web Interface (Recommended!)

Perfect for kids - no command line needed!

```bash
# Start the FastAPI backend server
cd backend
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

# Or use the Makefile shortcut
make serve
```

Your browser opens at `http://127.0.0.1:8001` with:
- 📚 **Library** - Browse and play existing stories
- ✏️ **Editor** - Write and edit stories with live validation
- 🎮 **Player** - Play stories with smooth scrolling
- 🌍 **Multi-language** - 15 languages with dropdown selector

**Sharing on network:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001
# Access from any device: http://your-ip:8001
```

**Using Makefile shortcuts:**
```bash
make serve         # Start FastAPI server on port 8001
make test          # Run all tests with coverage (135 tests)
make test-watch    # Continuous testing during development
make coverage      # Detailed HTML coverage report (91%)
make lint          # Check code style
```

## 🌍 Multi-Language Support

Pick-a-Page speaks **15 languages**! Perfect for teaching programming worldwide.

**Available Languages:**
🇬🇧 English • 🇳🇱 Dutch • 🇮🇹 Italian • 🇪🇸 Spanish • 🇫🇷 French • 🇵🇹 Portuguese • 🇩🇪 German • 🇷🇺 Russian • 🇨🇳 Chinese • 🇮🇳 Hindi • 🇸🇦 Arabic • 🇧🇩 Bengali • 🇵🇰 Urdu • 🇮🇩 Indonesian • 🇧🇬 Bulgarian

### Web Interface

The web GUI automatically detects your browser's language preference and lets you switch between all 15 languages with a dropdown selector! All UI messages, story templates, and navigation adapt to your chosen language.

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
make test          # Run 135 tests (91% coverage)
make test-watch    # Continuous testing (great for TDD!)
make coverage      # Detailed HTML coverage report
make lint          # Check code style
```

**Coverage by module:**
- `backend/core/compiler.py` - 97% (story parsing & validation)
- `backend/core/generator.py` - 90% (HTML generation)
- `backend/core/i18n.py` - 93% (15 language translations)
- `backend/api/routers/` - 86% (REST API endpoints)
- `backend/utils/` - 95% (shared utilities, security)

### Project Structure

```
python-pick-a-page/
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI application entry point
│   ├── core/                # Core business logic
│   │   ├── compiler.py      # 130 lines - Story parser & validator
│   │   ├── generator.py     # 72 lines - HTML/CSS/JS generator
│   │   ├── i18n.py         # 27 lines - 15-language translations
│   │   └── templates.py     # Story templates
│   ├── api/routers/         # REST API endpoints
│   │   ├── stories.py       # Story CRUD operations
│   │   ├── compile_router.py # Story compilation
│   │   ├── i18n.py         # Translation endpoints
│   │   ├── pages.py        # Frontend page serving
│   │   └── template.py      # Story initialization
│   ├── utils/               # Shared utilities
│   │   └── file_utils.py   # Security (path validation, sanitization)
│   ├── static/              # Frontend assets
│   │   ├── css/            # 8 CSS files (841 lines)
│   │   └── js/             # 5 JS modules (888 lines)
│   └── templates/           # Jinja2 templates
│       ├── base.html        # Base layout
│       └── index.html       # Main app interface
├── tests/                   # 135 tests (91% coverage)
│   ├── core/               # Core module tests
│   │   ├── test_compiler.py   # Parser validation
│   │   ├── test_generator.py  # HTML generation
│   │   ├── test_i18n.py      # Translations
│   │   └── test_integration.py # End-to-end
│   ├── api/                # API endpoint tests
│   │   ├── test_basic.py     # Health, pages, i18n
│   │   ├── test_stories.py   # Story CRUD, compilation
│   │   └── test_template.py  # Story initialization
│   └── fixtures/           # Test data
├── stories/                 # Example stories (EN, NL, IT)
└── output/                  # Compiled HTML (auto-cleaned after tests)
```

### Design Principles

Following the project's core values:

1. **🎯 Simplicity First** - Easy enough for 8-year-olds
2. **🚀 API-First** - FastAPI backend with REST endpoints
3. **✅ TDD Always** - Red → Green → Refactor (135 tests, 91% coverage)
4. **📱 Mobile-First** - Responsive design for all devices
5. **🏗️ SOLID Principles** - Clean architecture, DRY, single responsibility
6. **🎨 Modern UX** - Squiffy-inspired scrolling narrative
7. **🔒 Security-First** - Path validation, filename sanitization

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
# Basic usage (development with auto-reload)
cd backend
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

# Production deployment
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4

# Using Makefile
make serve  # Development mode with auto-reload
```

**Deploy Anywhere:**
```bash
# Cloud server (DigitalOcean, AWS, etc.)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4

# Access from network: http://your-server-ip:8001
# API docs: http://your-server-ip:8001/docs
```

## 🔧 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                      │
│                  (Port 8001, Async)                     │
├─────────────────────────────────────────────────────────┤
│  API Layer (backend/api/routers/)                       │
│  ├─ stories.py      - Story CRUD operations            │
│  ├─ compile_router.py - Story compilation              │
│  ├─ i18n.py         - Translation endpoints            │
│  ├─ pages.py        - Frontend serving                 │
│  └─ template.py     - Story initialization             │
├─────────────────────────────────────────────────────────┤
│  Core Logic (backend/core/)                             │
│  ├─ compiler.py     - Parser + Validator               │
│  ├─ generator.py    - HTML/CSS/JS generator            │
│  ├─ i18n.py         - 15 language support              │
│  └─ templates.py    - Story templates                  │
├─────────────────────────────────────────────────────────┤
│  Utilities (backend/utils/)                             │
│  └─ file_utils.py   - Security (paths, filenames)     │
├─────────────────────────────────────────────────────────┤
│  Frontend (backend/static/ & templates/)                │
│  ├─ CSS (8 files)   - Responsive, mobile-first        │
│  ├─ JS (5 modules)  - Event handling, navigation      │
│  └─ Jinja2          - Server-side rendering           │
└─────────────────────────────────────────────────────────┘
```

**Core Components:**

1. **FastAPI Backend** (`backend/main.py`)
   - Async REST API on port 8001
   - CORS-enabled for development
   - Serves static files and Jinja2 templates
   - Automatic OpenAPI docs at `/docs`

2. **Parser & Validator** (`backend/core/compiler.py`, 130 lines)
   - Extracts metadata, sections, choices, images
   - Normalizes section names (`"Go Home"` → `"go-home"`)
   - Validates all links point to real sections
   - Detects broken links and orphaned sections

3. **HTML Generator** (`backend/core/generator.py`, 72 lines)
   - Creates single HTML file with embedded:
     - CSS (Squiffy-inspired responsive design)
     - JavaScript (event delegation for navigation)
     - Images (Base64 encoded)
   - Print-ready styles for PDF export

4. **REST API** (`backend/api/routers/`)
   - Story CRUD: GET, POST, PUT, DELETE operations
   - Compilation: Text → HTML conversion
   - Validation: Check story structure
   - Templates: Initialize new stories
   - i18n: Get translations for all 15 languages

5. **Security Layer** (`backend/utils/file_utils.py`)
   - Path validation (prevents directory traversal)
   - Filename sanitization (removes dangerous characters)
   - Used by all file operations

6. **Internationalization** (`backend/core/i18n.py`, 27 lines)
   - Dictionary-based translations
   - 15 languages supported
   - Auto-detection from browser
   - Dropdown language switcher in UI

### Story Navigation

**Squiffy-style chronological scrolling:**
- First visit: `appendChild()` moves section to end
- Revisit: `cloneNode(true)` creates fresh copy with enabled buttons
- Buttons in current section disabled after click (reading history)

This creates a natural reading flow even with complex branching!

## ✅ Status

**Production Ready!**

- ✅ 135 tests passing (91% coverage)
- ✅ 15 languages fully translated
- ✅ FastAPI backend battle-tested
- ✅ TDD workflow established (RED → GREEN → REFACTOR)
- ✅ Mobile-first responsive design
- ✅ SOLID principles throughout codebase
- ✅ Security-first (path validation, sanitization)
- ✅ Example stories in 3 languages
- ✅ Comprehensive documentation
- ✅ Automatic test cleanup (no leftover files)

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
2. ✅ **All tests must pass** (`make test` - 135 tests)
3. 📊 **Maintain >85% coverage** (`make coverage` - currently 91%)
4. 🎨 **Follow PEP 8** (`make lint`)
5. 🚀 **API-first design** - REST endpoints for all features
6. 📱 **Mobile-first** - Test on small screens
7. 🏗️ **SOLID principles** - Clean architecture, DRY code
8. 🧹 **Clean up after tests** - Use cleanup fixtures

**Great starter contributions:**
- 📚 Add example stories in different languages
- 🌍 Translate UI to new languages (we have 15, let's add more!)
- 📖 Write tutorials or documentation
- 🐛 Fix bugs or improve error messages
- ✨ Add tests for uncovered code (aiming for 95%+)
- 🎨 Improve CSS/JS frontend
- 🚀 Add new API endpoints

See `.github/copilot-instructions.md` for detailed development guidelines.

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
