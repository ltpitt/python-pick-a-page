# Claude Prompt: Generate Pick-a-Page Story Tool

Create a complete educational web application called "Pick-a-Page" that helps children (ages 8+) create interactive "Choose Your Own Adventure" stories. The app transforms simple text files into beautiful, playable HTML stories with a modern scrolling narrative interface.

## Technical Stack
- **Backend**: FastAPI 0.122.0+ (Python 3.10+, async ASGI)
- **Server**: Uvicorn (ASGI server)
- **Frontend**: Vanilla JavaScript (ES6+), CSS3 (mobile-first responsive)
- **Testing**: pytest 8.3.4+, pytest-cov, httpx
- **Templating**: Jinja2 (server-side rendering)

## Core Requirements

### 1. API-First Architecture (FastAPI)

Create a REST API with these endpoints:

**Stories API** (`backend/api/routers/stories.py`):
- `GET /api/stories` - List all stories with metadata
- `GET /api/story/{filename}` - Get story content
- `POST /api/story` - Save/update story
- `DELETE /api/story/{filename}` - Delete story

**Compilation API** (`backend/api/routers/compile_router.py`):
- `POST /api/compile` - Compile story text to HTML
- `POST /api/validate` - Validate story structure
- `GET /play/{story_id}` - Serve compiled story HTML

**i18n API** (`backend/api/routers/i18n.py`):
- `GET /api/languages` - List 15 supported languages
- `GET /api/translations/{lang}` - Get translations for language

**Template API** (`backend/api/routers/template.py`):
- `POST /api/template/init` - Initialize new story from template

**Pages** (`backend/api/routers/pages.py`):
- `GET /` - Serve main web interface

### 2. Story Format & Parser

**Story Syntax** (`backend/core/compiler.py`):
```
---
title: Story Title
author: Author Name
---

[[section-name]]
Story text here with **bold** and *italic*.

[[Choice 1 text]]
[[Choice 2|custom-section]]

---

[[custom-section]]
More story content...
```

**Parser must**:
- Extract YAML metadata (title, author)
- Parse sections with `[[section-name]]` headers
- Parse choices: `[[text]]` links to normalized "text", `[[display|target]]` for custom targets
- Support Markdown: `**bold**`, `*italic*`, `![alt](image.jpg)`
- Normalize section names: "Section Name" → "section-name"
- Validate: detect broken links, orphaned sections
- Embed images as Base64 in final HTML

### 3. HTML Generator

**Generate single-file HTML** (`backend/core/generator.py`):
- Embed all CSS (from backend/static/css/)
- Embed all JavaScript
- Embed images as Base64
- Squiffy-style scrolling: new sections append to bottom
- Choice buttons disable after click (reading history)
- Print-friendly styles for PDF export

### 4. Internationalization (i18n)

**Support 15 languages** (`backend/core/i18n.py`):
English (en), Dutch (nl), Italian (it), Spanish (es), French (fr), Portuguese (pt), German (de), Russian (ru), Chinese (zh), Hindi (hi), Arabic (ar), Bengali (bn), Urdu (ur), Indonesian (id), Bulgarian (bg)

**Translation keys**:
```python
TRANSLATIONS = {
    "en": {
        "web_tab_library": "Story Library",
        "web_tab_editor": "Story Editor",
        "web_btn_play": "Play Story",
        "web_btn_save": "Save",
        "web_btn_compile": "Compile & Play",
        # ... all UI strings
    },
    # ... 14 more languages
}
```

### 5. Frontend (Mobile-First, Vanilla JS)

**CSS Architecture** (`backend/static/css/`):
- `variables.css` - Design tokens (colors, spacing, fonts)
- `base.css` - CSS reset, global styles
- `book.css` - Book container with spine effect
- `bookmarks.css` - Tab navigation
- `library.css` - Story grid/cards
- `editor.css` - Textarea, buttons
- `messages.css` - Success/error notifications
- `mobile.css` - Mobile overrides (<768px)

**Design System**:
```css
:root {
    /* Purple gradient primary */
    --color-primary-start: #667eea;
    --color-primary-end: #764ba2;
    
    /* Green gradient secondary */
    --color-success-start: #48bb78;
    --color-success-end: #38a169;
    
    /* Paper background */
    --color-bg-paper: #faf8f3;
    
    /* Spacing (8px grid) */
    --spacing-xs: 8px;
    --spacing-md: 16px;
    --spacing-xl: 24px;
    
    /* Font sizes */
    --font-size-base: 1rem;
    --font-size-xl: 1.3rem;
    --font-size-3xl: 2.5rem;
}
```

**Button Styles**:
- `.btn-primary` - Purple gradient (main actions)
- `.btn-secondary` - Green gradient (secondary actions)
- Shine effect on hover, lift animation, touch-friendly (48px min)

**JavaScript Modules** (`backend/static/js/`):
- `api-service.js` - API calls (fetch wrapper)
- `i18n-service.js` - Translation management
- `story-manager.js` - Story CRUD operations
- `ui-controller.js` - Page switching, button states
- `app.js` - Main initialization

**Web Interface** (`backend/templates/`):
- `base.html` - Base template with CSS/JS includes
- `index.html` - Three-page book interface:
  1. **Library**: Story grid with cards, play/edit/new buttons
  2. **Editor**: Textarea with validate/save/compile buttons
  3. **Player**: Iframe showing compiled story

### 6. Security

**File Operations** (`backend/utils/file_utils.py`):
```python
def is_safe_path(base_dir: Path, requested_path: Path) -> bool:
    """Prevent directory traversal (../ attacks)."""
    
def sanitize_filename(filename: str, extension: str = ".txt") -> str:
    """Remove dangerous characters from filenames."""
```

**Always**:
- Validate all file paths before operations
- Sanitize user-provided filenames
- Use Pydantic models for API input validation

### 7. Testing (TDD Approach)

**Test Structure** (`tests/`):
- `tests/core/test_compiler.py` - Parser, validator (42 tests)
- `tests/core/test_generator.py` - HTML generation (28 tests)
- `tests/core/test_i18n.py` - Translations (15 tests)
- `tests/core/test_integration.py` - End-to-end (18 tests)
- `tests/api/test_basic.py` - Health, pages (12 tests)
- `tests/api/test_stories.py` - Story CRUD (15 tests)

**Test fixtures** (`tests/fixtures/`):
- `valid_story.txt` - Complete valid story
- `broken_links.txt` - Story with broken links
- `with_images.txt` - Story with image embeds

**Requirements**:
- Use pytest with async support (`pytest-asyncio`)
- Test cleanup: Delete created files after tests
- Aim for >85% coverage

### 8. Project Structure

```
python-pick-a-page/
├── backend/
│   ├── main.py                    # FastAPI app, middleware, health check
│   ├── core/                      # Business logic (no HTTP concerns)
│   │   ├── compiler.py            # Parser, validator
│   │   ├── generator.py           # HTML/CSS/JS generator
│   │   ├── i18n.py               # 15-language translations
│   │   └── templates.py           # Story templates
│   ├── api/routers/               # REST API endpoints
│   │   ├── stories.py             # Story CRUD
│   │   ├── compile_router.py     # Compilation
│   │   ├── i18n.py               # Translation endpoints
│   │   ├── pages.py              # Frontend serving
│   │   └── template.py            # Story initialization
│   ├── utils/                     # Shared utilities
│   │   └── file_utils.py         # Security: path validation
│   ├── static/                    # Frontend assets
│   │   ├── css/                  # 8 CSS files
│   │   └── js/                   # 5 JS modules
│   └── templates/                 # Jinja2 templates
│       ├── base.html
│       └── index.html
├── tests/                         # 135+ tests (91% coverage)
│   ├── core/
│   ├── api/
│   └── fixtures/
├── stories/                       # Example stories
├── output/                        # Compiled HTML (gitignored)
├── requirements.txt               # Dev dependencies
├── backend/requirements.txt       # Backend dependencies
├── Makefile                       # Development shortcuts
└── README.md                      # Documentation
```

### 9. Key Files Content

**main.py**:
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pick-a-Page Story Tool", version="2.0.0")

# CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Mount static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="backend/templates")

# Include routers
from backend.api.routers import stories, compile_router, i18n, pages, template
app.include_router(pages.router)
app.include_router(stories.router, prefix="/api", tags=["stories"])
app.include_router(compile_router.router, prefix="/api", tags=["compile"])
app.include_router(i18n.router, prefix="/api", tags=["i18n"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}
```

**Makefile**:
```makefile
.PHONY: install serve test coverage clean

install:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r backend/requirements.txt

serve:
	source .venv/bin/activate && uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload

test:
	pytest -v --cov=backend --cov-report=term-missing

coverage:
	pytest --cov=backend --cov-report=html

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage output/
```

**requirements.txt** (dev):
```
pytest>=8.3.4
pytest-cov>=6.0.0
pytest-asyncio>=0.24.0
httpx>=0.27.0
pytest-watch>=4.2.0
```

**backend/requirements.txt**:
```
fastapi>=0.122.0
uvicorn[standard]>=0.34.0
jinja2>=3.1.5
python-multipart>=0.0.20
pydantic>=2.10.5
aiofiles>=24.1.0
Pillow>=11.0.0
PyYAML>=6.0.2
```

### 10. Example Stories

Include 3 example stories in `stories/`:
1. `dragon_quest_en.txt` - Simple branching story (English)
2. `dragon_quest_it.txt` - Same story in Italian
3. `markdown_demo.txt` - Demonstrates all Markdown features

### 11. Critical Implementation Details

**Story Compilation Flow**:
1. Parse story text → extract metadata, sections, choices
2. Validate → check broken links, orphaned sections
3. Generate HTML → embed CSS/JS, Base64 images
4. Return single-file HTML (works offline)

**Story Player (Squiffy-style)**:
- First visit to section: `appendChild()` to end
- Revisit section: `cloneNode(true)` with fresh buttons
- Clicked buttons disable (visual reading history)
- Scroll to new section automatically

**Mobile-First CSS**:
```css
/* Base: Mobile (320px+) */
.story-card { width: 100%; padding: 1rem; }

/* Tablet (768px+) */
@media (min-width: 768px) {
    .story-card { width: 48%; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .story-card { width: 32%; }
}
```

**Error Handling**:
- Use FastAPI's `HTTPException` with proper status codes
- Return structured JSON errors: `{"detail": "Error message"}`
- Log errors server-side

### 12. .gitignore

```
__pycache__/
*.pyc
.venv/
.pytest_cache/
htmlcov/
.coverage
*.egg-info/
output/
output/*.html
.DS_Store
```

## Success Criteria

1. ✅ `make install` creates venv and installs dependencies
2. ✅ `make serve` starts server on http://127.0.0.1:8001
3. ✅ Web interface loads with 3 tabs (Library, Editor, Player)
4. ✅ Can create, edit, save, play stories
5. ✅ Language switcher changes UI to any of 15 languages
6. ✅ Story compilation generates single HTML file
7. ✅ Compiled stories work offline with scrolling narrative
8. ✅ `make test` runs 135+ tests with >85% coverage
9. ✅ Mobile-responsive (works at 320px width)
10. ✅ Security validated (path traversal, filename sanitization)

## Development Principles

1. **API-First**: All features exposed via REST API before UI
2. **Mobile-First**: CSS works on 320px screens before desktop
3. **TDD**: Write tests first (RED → GREEN → REFACTOR)
4. **SOLID**: Single responsibility, DRY, clean architecture
5. **Security**: Validate all inputs, sanitize all outputs
6. **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation
7. **Performance**: Async I/O, lazy loading, minimize reflows

## Output Requirements

Generate complete, production-ready code for all files listed above. Ensure:
- All API endpoints return proper JSON responses
- All CSS follows mobile-first approach
- All JavaScript uses modern ES6+ features
- All tests use pytest async patterns
- All security checks implemented
- All 15 languages fully translated
- Complete Makefile for development workflow
- Comprehensive README.md with setup instructions

The application should be fully functional and ready to run with just `make install && make serve`.
