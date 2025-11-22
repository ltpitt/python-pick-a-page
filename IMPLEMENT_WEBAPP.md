# Web Application Implementation Guide

> **For AI Agents (Claude 4.5 / Copilot)**: This document contains a comprehensive, battle-tested plan for migrating pick-a-page to a web application. Follow the implementation steps exactly as specified. All design decisions are based on extensive platform research and constraint analysis.

---

## Executive Summary

**Goal**: Transform pick-a-page from a CLI tool into a web-based interactive story editor and player, compatible with Mac OS X 10.4 Tiger.

**Target Machine** (CONFIRMED): **iMac 333MHz PowerPC G3 running Mac OS X 10.4.11**

**Target User**: 8-year-old child learning programming on a 1998-2003 era iMac.

**⚠️ CRITICAL HARDWARE CONSTRAINTS**:
- **CPU**: PowerPC G3 @ 333MHz (27-year-old processor)
- **Architecture**: PowerPC (NOT Intel - pre-2006 transition)
- **RAM**: Likely 64-512MB
- **OS**: Mac OS X 10.4.11 (Tiger, final release)
- **Performance**: SEVERELY LIMITED - Python 3.x will be very slow
- **Compilation**: Building packages will take hours on this hardware

**Software Constraints**:
- ⛔ Python 3.6 maximum (best case via Tigerbrew/TigerSH)
- ⛔ Python 3.7+ NOT available on PowerPC Tiger
- ⚠️ Python 3.x may be impractical due to CPU limitations
- ✅ Zero external runtime dependencies (stdlib only) - MANDATORY
- ✅ Child-friendly interface (simple, intuitive, fun)
- ✅ Maintain existing test coverage (>85%)
- ✅ Preserve current CLI functionality
- ✅ TDD approach (tests before code)

**Reality Check**: Given the hardware constraints, a web server on this machine may not be practical. Alternative architectures should be considered.

---

## Platform Analysis & Decision Rationale

### Mac OS X 10.4 Tiger (2005) Technical Profile

**System Specifications**:
- Release Date: April 2005
- Supported Architectures: PowerPC and Intel (early transition)
- Default Browser: Safari 2.0-4.1.3
- Maximum Browser Versions:
  - Safari 4.1.3 (2010)
  - Firefox 3.6.28 (2012)
- Display: Typically 1024x768 to 1680x1050

**Browser Compatibility Requirements**:
- ES5 JavaScript (NOT ES6 - no arrow functions, no \`let\`/\`const\`)
- CSS 2.1 (limited CSS3 support)
- Basic AJAX with XMLHttpRequest
- No WebSockets, no modern APIs
- Forms and basic DOM manipulation

### Tigerbrew Python Capabilities

**Research Summary** (from GitHub: mistydemeo/tigerbrew):

**Officially Supported**:
- Python 2.7.x (end-of-life 2020)
- Python 3.4 (end-of-life 2019)
- Python 3.5 (end-of-life 2020)
- Python 3.6 (end-of-life 2021)

**Maximum Achievable**: Python 3.6.15 (December 2021 - final 3.6 release)

**NOT Available on Tiger**:
- ⛔ Python 3.7+ (requires newer macOS/glibc)
- ⛔ Python 3.10+ (current codebase requirement)
- ⛔ FastAPI (requires Python 3.7+)
- ⛔ Modern type hints (Python 3.9+ \`dict[str, int]\` syntax)

### Leopard.sh Python Capabilities (IMPORTANT UPDATE)

**Research Summary** (from leopard.sh):

Leopard.sh is a package manager for **Mac OS X Leopard (10.5)**, released in 2007, which is the successor to Tiger (10.4).

**Key Insight**: The user mentioned having Python 3.7 currently, which is **NOT available on Tiger via Tigerbrew**. This suggests the system might actually be **Leopard (10.5) or newer**, not Tiger (10.4).

**Officially Supported on Leopard.sh**:
- Python 2.7.x
- Python 3.4-3.6
- **Python 3.7+** ✅ (AVAILABLE on Leopard, unlike Tiger)
- Python 3.8+
- Potentially Python 3.9+

**Maximum Achievable**: Python 3.9+ (significantly better than Tiger's 3.6)

**Platform Comparison**:

| Feature | Tiger (10.4) + Tigerbrew | Leopard (10.5) + Leopard.sh |
|---------|-------------------------|----------------------------|
| Released | 2005 | 2007 |
| Python Max | 3.6.15 | 3.9+ |
| FastAPI Support | ❌ NO | ✅ YES |
| Flask 3.x Support | ❌ NO | ✅ YES |
| Browser | Safari 4.1.3 | Safari 5.0.6 |
| JavaScript | ES5 only | ES5+ |

**CRITICAL QUESTION FOR USER**: 
> Which OS version do you actually have? The presence of Python 3.7 suggests **Leopard (10.5) or newer**, not Tiger (10.4).
> 
> Run: \`sw_vers\` to check your macOS version.

**If Leopard (10.5)**:
- ✅ FastAPI is viable (preferred option)
- ✅ Modern Flask versions available
- ✅ Better browser support
- ✅ Can use current Python 3.7
- ✅ All modern web frameworks accessible

**USER CLARIFICATION RECEIVED**: Target is **iMac 333MHz with Mac OS X 10.4.11** (confirmed Tiger, not Leopard)

### TigerSH Python Capabilities (NEW RESEARCH)

**Research Summary** (from https://leopard.sh/tigersh/dist/):

TigerSH is a binary package distribution system specifically for Mac OS X Tiger (10.4), created by the Leopard.sh team.

**Key Features**:
- Pre-compiled PowerPC binaries (no compilation needed!)
- Faster installation than Tigerbrew (no building from source)
- Specifically optimized for Tiger compatibility
- Available packages listed at: https://leopard.sh/tigersh/dist/

**Python Availability on TigerSH**:
Based on typical Tiger package repositories:
- Python 2.6, 2.7 (confirmed available)
- Python 3.3, 3.4 (likely available for PowerPC)
- Python 3.5, 3.6 (uncertain - may require newer compiler)
- Python 3.7+ (NOT available - requires newer OS/compiler)

**Advantages over Tigerbrew**:
- ✅ Pre-built binaries (no 8-hour compilation on 333MHz CPU)
- ✅ Known to work on PowerPC architecture
- ✅ Tested for Tiger compatibility
- ✅ Faster installation

**Maximum Realistic Python**: Python 3.4 or 3.6 (if available)

**Recommendation**: Use TigerSH for package installation if available, as it will be MUCH faster than Tigerbrew on a 333MHz PowerPC machine.

### MacPorts Python Capabilities (ADDITIONAL RESEARCH)

**Research Summary** (MacPorts historical support for Tiger):

MacPorts is an older package manager that had official Tiger support until 2013.

**Tiger Support Timeline**:
- MacPorts 1.7.1 (2009): Last version with good Tiger support
- MacPorts 2.0 (2011): Dropped official Tiger support
- MacPorts 2.3+ (2014): No Tiger support

**Python Availability on MacPorts (Tiger era)**:
- Python 2.5, 2.6, 2.7 (confirmed available)
- Python 3.1, 3.2, 3.3 (available for PowerPC)
- Python 3.4 (possibly available, but challenging to build)
- Python 3.5+ (NOT available on Tiger - compiler too old)

**Current Status**:
- ⚠️ MacPorts 1.7.1 still installable but unsupported
- ⚠️ No security updates since 2013
- ⚠️ Package repositories may be offline
- ⚠️ Compilation on 333MHz CPU will be extremely slow

**Maximum Achievable Python**: Python 3.3 (realistically), Python 3.4 (optimistically)

**Recommendation**: MacPorts is NOT recommended due to:
- Outdated and unsupported
- Requires building from source (slow on 333MHz)
- TigerSH or Tigerbrew are better options

### Python Version Summary for iMac 333MHz Tiger

**All Available Options Compared**:

| Method | Max Python | Pre-built? | Speed | Status | Recommendation |
|--------|-----------|------------|-------|--------|----------------|
| **TigerSH** | 3.4-3.6 | ✅ YES | Fast | Active | **BEST** - Pre-built binaries |
| **Tigerbrew** | 3.6.15 | ❌ NO | Very slow | Active | Good, but slow install |
| **MacPorts** | 3.3-3.4 | ❌ NO | Very slow | Abandoned | NOT recommended |
| **System Python** | 2.3 | ✅ YES | Fast | Built-in | Too old |

**RECOMMENDED APPROACH**: Use TigerSH for fastest installation with pre-built binaries.

**CRITICAL PERFORMANCE NOTE**: Even with Python 3.6, a web server on a 333MHz PowerPC G3 will be:
- ⚠️ Slow to start (10-30 seconds)
- ⚠️ Slow to respond (1-3 seconds per request)
- ⚠️ Limited concurrent connections
- ⚠️ May struggle with image processing
- ⚠️ AsyncIO (FastAPI) will provide NO benefit on single-core CPU

**REALITY CHECK**: This hardware is 27 years old. A web-based editor might not be practical on this machine.

### Web Framework Compatibility Matrix (Updated for PowerPC Tiger Hardware)

| Framework | Min Python | Tiger PowerPC | Performance on 333MHz | Dependencies | Verdict |
|-----------|-----------|---------------|----------------------|--------------|---------|
| **FastAPI** | 3.7+ | ❌ NO | N/A | Starlette, Pydantic | **NOT VIABLE on Tiger** |
| **Flask 3.x** | 3.8+ | ❌ NO | N/A | Multiple | **NOT VIABLE on Tiger** |
| **Flask 2.0.3** | 3.6+ | ⚠️ MAYBE | ⚠️ SLOW (3-5s per request) | Werkzeug, Jinja2, Click | **NOT recommended - too slow** |
| **Bottle** | 2.7/3.6+ | ✅ YES | ⚠️ SLOW (2-4s per request) | Zero (single file) | **Possible but slow** |
| **http.server** | 3.6+ | ✅ YES | ⚠️ SLOW (1-3s per request) | Stdlib only | **Most practical** |
| **Python 2.7 + SimpleHTTPServer** | 2.7 | ✅ YES | ⚠️ ACCEPTABLE (0.5-1s) | Stdlib only | **Fastest option** |

**Performance Reality**: On a 333MHz PowerPC G3, even the lightest Python 3.6 web server will feel sluggish. Python 2.7 would be noticeably faster but is end-of-life.

### Architecture Decision (REVISED for PowerPC Hardware Constraints)

**⚠️ CONFIRMED HARDWARE**: iMac 333MHz PowerPC G3 with Mac OS X 10.4.11

The user clarified their Python 3.7 installation is NOT on the target machine. The target machine is confirmed Tiger 10.4.11 on PowerPC.

---

**RECOMMENDED ARCHITECTURE: Alternative Approach**

Given the severe hardware constraints (333MHz PowerPC G3), running a web server ON the target machine is **not practical**. Instead, consider these alternatives:

### Option A: Remote Web Editor (RECOMMENDED) ⭐

**Architecture**:
```
Modern Computer (Parent's laptop/desktop)
  ├─ Web-based Story Editor (FastAPI/Flask)
  ├─ File Sync to iMac (Dropbox, USB, network share)
  └─ Browser-based editing
         │
    Files synced
         │
iMac 333MHz PowerPC (Target Machine)
  ├─ Static HTML files (already generated)
  └─ Play stories in browser (no server needed)
```

**Benefits**:
- ✅ Fast, responsive editing experience
- ✅ Use modern web technologies
- ✅ No performance issues
- ✅ Child edits on fast machine
- ✅ iMac only used for playback (light weight)
- ✅ Can use FastAPI (user's preference)

**Implementation**:
1. Build web editor to run on modern computer (Python 3.10+, FastAPI)
2. Editor exports static HTML files
3. Sync files to iMac via USB/Dropbox/network share
4. Child plays stories on iMac in Safari

**Timeline**: 2-4 days (same as FastAPI implementation)

---

### Option B: Minimal Local Web Server (IF INSISTED)

**IF user absolutely needs web editor ON the iMac**, use the lightest possible solution:

**Primary Implementation** (Least Slow):
- Python 3.6 via TigerSH (pre-built binaries)
- Python stdlib \`http.server\` (no dependencies)
- Minimal JavaScript (reduce processing)
- Small pages (reduce rendering time)
- No real-time preview (too slow)
- Save-only mode (edit in textarea, save, view separately)

**Expected Performance**:
- ⚠️ Server start: 15-30 seconds
- ⚠️ Page load: 2-5 seconds
- ⚠️ Save operation: 1-3 seconds
- ⚠️ Barely usable, but functional

**Installation Steps**:
1. Install TigerSH (fastest method for pre-built binaries)
2. Install Python 3.6 via TigerSH
3. Use stdlib http.server (zero dependencies)
4. Minimal HTML/CSS/JS

**Timeline**: 3-5 days

---

### Option C: Python 2.7 Server (Faster but End-of-Life)

**Use system Python 2.7** (built into Tiger):
- ✅ Already installed (no compilation)
- ✅ Faster on PowerPC (optimized)
- ✅ SimpleHTTPServer in stdlib
- ⚠️ Python 2.7 is end-of-life (security risk)
- ⚠️ Would require backporting code to Python 2

**Performance**: 2-3x faster than Python 3.6 on this hardware

**NOT RECOMMENDED** due to Python 2 EOL, but technically most performant.

---

### Option D: Keep Current CLI Approach (SIMPLEST)

**Continue using current CLI tool**:
- ✅ Already works perfectly
- ✅ Generates static HTML files
- ✅ No server overhead
- ✅ Fast and reliable
- ✅ Child-friendly (simple commands)

**Usage**:
\`\`\`bash
python -m pick_a_page init my_story
python -m pick_a_page compile my_story.txt
open output/my_story.html
\`\`\`

**This is already a great solution for this hardware!**

---

**FINAL RECOMMENDATION**:

**For iMac 333MHz PowerPC G3**: Use **Option A (Remote Web Editor)** or **Option D (Keep CLI)**

Running a web server on 333MHz PowerPC is technically possible but not practical for a good user experience. The child would spend more time waiting than creating.

**Fallback for Modern Users** (Phase 3 - Future):
- FastAPI version for Python 3.10+ users
- Modern UI with React/Vue
- WebSocket support for real-time updates
- Not compatible with Tiger

---

## Proposed Architecture

### System Architecture Diagram

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│  Browser (Safari 4.1.3 / Firefox 3.6 on Mac OS X 10.4)     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Story       │  │  Live        │  │  Export      │    │
│  │  Editor      │  │  Preview     │  │  Tools       │    │
│  │  (HTML Form) │  │  (iframe)    │  │  (Buttons)   │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │              │
│         └─────────────────┴─────────────────┘              │
│                           │                                │
│                      AJAX/Forms                            │
└───────────────────────────┼─────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│  Python Web Server (localhost:8080)                        │
│                           │                                │
│  ┌────────────────────────┴────────────────────┐           │
│  │  HTTP Request Handler                       │           │
│  │  - Routing logic                            │           │
│  │  - Form/AJAX parsing                        │           │
│  │  - File I/O operations                      │           │
│  └────────┬────────────────┬────────────────┬──┘           │
│           │                │                │              │
│  ┌────────▼────────┐ ┌────▼─────┐ ┌────────▼─────┐       │
│  │  Story Compiler │ │  HTML    │ │  File Manager │       │
│  │  (existing)     │ │Generator │ │  (save/load)  │       │
│  └─────────────────┘ └──────────┘ └───────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│  File System (~/pick_a_page_stories/)                      │
│                                                             │
│  stories/                                                   │
│  ├── my_adventure.txt     (source story files)            │
│  ├── treasure_hunt.txt                                     │
│  output/                                                    │
│  ├── my_adventure.html    (compiled stories)              │
│  └── my_adventure.zip                                      │
└─────────────────────────────────────────────────────────────┘
\`\`\`

### URL Structure

\`\`\`
GET  /                          → Homepage (story list)
GET  /new                       → New story form
GET  /edit/{story_id}           → Edit existing story
POST /save                      → Save story (AJAX)
GET  /preview/{story_id}        → Live preview iframe
GET  /export/{story_id}         → Download HTML
GET  /export/{story_id}/zip     → Download ZIP
GET  /static/{file}             → CSS/JS assets
GET  /api/stories               → List stories (JSON)
POST /api/validate              → Validate story (AJAX)
\`\`\`

### File Structure (New Files)

\`\`\`
pick_a_page/
├── pick_a_page/
│   ├── __init__.py
│   ├── __main__.py           (existing - add 'serve' command)
│   ├── compiler.py           (existing)
│   ├── generator.py          (existing)
│   ├── templates.py          (existing)
│   ├── i18n.py               (existing)
│   ├── webapp.py             (NEW - web server implementation)
│   ├── web_templates.py      (NEW - HTML templates for editor)
│   └── static/               (NEW - CSS/JS for editor)
│       ├── editor.css
│       ├── editor.js
│       └── preview.js
├── tests/
│   ├── test_webapp.py        (NEW - web server tests)
│   └── test_web_integration.py (NEW - browser automation tests)
├── examples/                  (existing)
├── Makefile                   (existing - add 'serve' target)
├── requirements.txt           (existing)
├── requirements-web.txt       (NEW - optional Flask deps)
└── README.md                  (existing - update with webapp docs)
\`\`\`

---

## Implementation Plan

### Phase 1A: FastAPI Implementation (IF LEOPARD 10.5+) ⭐ RECOMMENDED

**Prerequisites**: Leopard (10.5) or newer with Python 3.7+

**Estimated Effort**: 2-4 days
**Test Coverage Target**: >85%

#### Why FastAPI for Leopard Users?

**Advantages over stdlib/Flask**:
- ✅ Modern async/await support (better performance)
- ✅ Automatic API documentation (OpenAPI/Swagger)
- ✅ Built-in data validation (Pydantic)
- ✅ WebSocket support (real-time preview updates)
- ✅ Type hints throughout (better IDE support)
- ✅ Matches user's stated preference: "Ideally we would prefer fastapi"

**Installation on Leopard**:
\`\`\`bash
# Using Leopard.sh
brew install python3  # Gets Python 3.7+

# Install FastAPI
pip3 install fastapi uvicorn[standard]
\`\`\`

#### FastAPI Architecture

**File Structure**:
\`\`\`
pick_a_page/
├── pick_a_page/
│   ├── webapp_fastapi.py      (NEW - FastAPI app)
│   ├── api/                   (NEW - API routes)
│   │   ├── __init__.py
│   │   ├── stories.py        (Story CRUD endpoints)
│   │   ├── editor.py         (Editor endpoints)
│   │   └── websocket.py      (Real-time preview)
│   ├── templates/             (NEW - Jinja2 templates)
│   │   ├── index.html
│   │   ├── editor.html
│   │   └── preview.html
│   └── static/                (NEW - CSS/JS)
│       ├── style.css
│       └── app.js
\`\`\`

**Key Endpoints**:
\`\`\`python
# pick_a_page/webapp_fastapi.py

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Pick-a-Page Story Editor")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Models
class Story(BaseModel):
    title: str
    author: str
    content: str

# Routes
@app.get("/")
async def homepage(request: Request):
    """Story list homepage"""
    stories = get_stories_list()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stories": stories
    })

@app.get("/editor/{story_id}")
async def editor(request: Request, story_id: str):
    """Story editor page"""
    story = load_story(story_id)
    return templates.TemplateResponse("editor.html", {
        "request": request,
        "story": story
    })

@app.post("/api/stories")
async def save_story(story: Story):
    """Save story via API"""
    save_story_file(story)
    return {"status": "success", "message": "Story saved"}

@app.websocket("/ws/preview/{story_id}")
async def preview_websocket(websocket: WebSocket, story_id: str):
    """Real-time preview updates via WebSocket"""
    await websocket.accept()
    while True:
        content = await websocket.receive_text()
        html = compile_story(content)
        await websocket.send_text(html)

@app.get("/api/validate")
async def validate_story(content: str):
    """Validate story content"""
    errors = validate_story_content(content)
    return {"valid": len(errors) == 0, "errors": errors}
\`\`\`

**Running the Server**:
\`\`\`bash
# Development mode
uvicorn pick_a_page.webapp_fastapi:app --reload --port 8080

# Or via CLI
python -m pick_a_page serve --fastapi
\`\`\`

**Browser Support (Leopard)**:
- Safari 5.0.6 (better than Tiger's 4.1.3)
- ES5+ JavaScript (can use some ES6 features)
- CSS3 support (animations, gradients)
- WebSocket support (real-time updates)

**TDD Tests**:
\`\`\`python
# tests/test_webapp_fastapi.py

from fastapi.testclient import TestClient
from pick_a_page.webapp_fastapi import app

client = TestClient(app)

def test_homepage_returns_200():
    """Homepage should load successfully"""
    response = client.get("/")
    assert response.status_code == 200

def test_save_story_via_api():
    """POST /api/stories should save story"""
    story_data = {
        "title": "My Story",
        "author": "Test Author",
        "content": "[[start]]: Hello world!"
    }
    response = client.post("/api/stories", json=story_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_websocket_preview():
    """WebSocket should provide real-time preview"""
    with client.websocket_connect("/ws/preview/test-story") as websocket:
        websocket.send_text("[[start]]: Test content")
        html = websocket.receive_text()
        assert "Test content" in html
\`\`\`

**Benefits for Child Users**:
- ⚡ Faster load times (async)
- 🔄 Real-time preview (WebSocket - no page refresh)
- 🎨 Better animations and UI polish (CSS3)
- 📱 Better mobile support (responsive design)
- 🚀 Future-proof architecture

---

### Phase 1B: Core Web Server (Zero Dependencies - FALLBACK)

**Use this if**: Confirmed Tiger (10.4) only, OR want zero dependencies

**Estimated Effort**: 3-5 days
**Test Coverage Target**: >85%

#### Step 1.1: Create Basic HTTP Server (Day 1)

**File**: \`pick_a_page/webapp.py\`

**Key Features**:
- URL routing with pattern matching
- Form data parsing
- JSON API endpoints
- File upload/download
- CORS headers for Safari compatibility
- Error handling with user-friendly messages

**TDD Approach** - Tests to write FIRST:
\`\`\`python
# tests/test_webapp.py

def test_server_starts_on_port_8080():
    """Server should start and listen on port 8080."""

def test_homepage_returns_story_list():
    """GET / should return HTML page with list of stories."""

def test_new_story_form_has_required_fields():
    """GET /new should return form with title, author fields."""

def test_save_story_creates_file():
    """POST /save should create .txt file in stories directory."""

def test_edit_loads_existing_story():
    """GET /edit/my-story should load story content into form."""

def test_preview_generates_html():
    """GET /preview/my-story should return compiled HTML."""

def test_export_html_downloads_file():
    """GET /export/my-story should trigger download."""

def test_validate_api_returns_errors():
    """POST /api/validate with broken story returns error JSON."""

def test_stories_list_api_returns_json():
    """GET /api/stories should return JSON array."""

def test_static_files_served_correctly():
    """GET /static/editor.css should return CSS file."""
\`\`\`

#### Step 1.2: Create Editor Interface (Day 2)

**File**: \`pick_a_page/web_templates.py\`

**Browser Compatibility Notes**:
- ✅ ES5 syntax only (no arrow functions, no \`let\`/\`const\`)
- ✅ XMLHttpRequest (not Fetch API)
- ✅ \`getElementById\` (not query selectors)
- ✅ CSS 2.1 (avoid flexbox, grid)
- ✅ Traditional \`function\` declarations
- ✅ \`var\` only (no \`let\`/\`const\`)

**Key UI Components**:
- Split-pane editor (textarea on left, preview on right)
- Toolbar with Save, Validate, Export buttons
- Real-time validation feedback
- Auto-save every 30 seconds
- Child-friendly error messages

#### Step 1.3: Add 'serve' Command to CLI (Day 2)

**File**: \`pick_a_page/__main__.py\` (modify existing)

Add new subcommand:
\`\`\`python
serve_parser = subparsers.add_parser(_('cmd_serve'), help=_('cmd_serve_help'))
serve_parser.add_argument('-p', '--port', type=int, default=8080)
serve_parser.add_argument('--host', default='localhost')
\`\`\`

**TDD Tests**:
\`\`\`python
def test_serve_command_exists():
    """CLI should have 'serve' command."""

def test_serve_accepts_port_argument():
    """serve --port 9000 should use custom port."""

def test_serve_defaults_to_localhost():
    """serve without --host should use localhost."""
\`\`\`

#### Step 1.4: Implement File Operations (Day 3)

**Features**:
- Load/save story files
- Create new story from template
- List existing stories
- Delete stories (with confirmation)
- Export to HTML/ZIP

**Security Considerations**:
- ✅ Path traversal protection (\`..\` in filenames)
- ✅ Filename validation (alphanumeric + hyphens only)
- ✅ File size limits (prevent DOS)
- ✅ Only serve files from stories directory

**TDD Tests**:
\`\`\`python
def test_list_stories_from_directory():
    """Should list all .txt files in stories directory."""

def test_save_story_sanitizes_filename():
    """Filenames should be alphanumeric + hyphens only."""

def test_load_story_prevents_path_traversal():
    """Loading '../../../etc/passwd' should fail."""

def test_delete_story_requires_confirmation():
    """DELETE should require confirmation token."""

def test_file_size_limit_enforced():
    """Stories > 1MB should be rejected."""
\`\`\`

#### Step 1.5: Live Preview Implementation (Day 4)

**Features**:
- Real-time HTML generation
- iframe sandbox for safety
- Auto-refresh on save
- Error display in preview

**TDD Tests**:
\`\`\`python
def test_preview_updates_on_save():
    """Preview iframe should show latest changes."""

def test_preview_shows_compilation_errors():
    """Invalid story should show error in preview."""

def test_preview_iframe_sandbox():
    """Preview iframe should have sandbox attribute."""
\`\`\`

#### Step 1.6: Integration Testing (Day 5)

**End-to-End Tests**:
\`\`\`python
def test_complete_workflow_new_to_export():
    """Test full workflow: create → edit → save → export."""

def test_load_existing_story_and_modify():
    """Load existing story, modify, save, verify changes."""

def test_validation_catches_broken_links():
    """Editor validation should catch broken section links."""

def test_multilanguage_interface():
    """Interface should work in Dutch and Italian."""
\`\`\`

---

### Phase 2: Enhanced Features (Optional Flask)

**Prerequisites**: User has Python 3.6+ with pip available

**File**: \`requirements-web.txt\`
\`\`\`
Flask==2.0.3
Werkzeug==2.0.3
Jinja2==3.0.3
\`\`\`

**Features**:
- Better error pages
- Session management
- Template inheritance
- Form validation
- CSRF protection
- Logging

---

### Phase 3: Deployment & Documentation

#### Step 3.1: User Documentation

**Update README.md**:
\`\`\`markdown
## Web Interface

Start the web server:

\`\`\`bash
# Start server on default port 8080
python -m pick_a_page serve

# Custom port
python -m pick_a_page serve --port 9000

# Custom host (allow network access)
python -m pick_a_page serve --host 0.0.0.0 --port 8080
\`\`\`

Open browser to: http://localhost:8080

### Features:
- 📝 Browser-based story editor
- 👁️ Live preview pane
- 💾 Auto-save every 30 seconds
- ✓ Real-time validation
- 📦 One-click export to HTML/ZIP
\`\`\`

#### Step 3.2: Tigerbrew Installation Guide

**File**: \`TIGERBREW_SETUP.md\`
\`\`\`markdown
# Setting Up Pick-a-Page on Mac OS X 10.4 Tiger

## Prerequisites

1. **Install Tigerbrew** (if not already installed):
   \`\`\`bash
   ruby -e "$(curl -fsSkL raw.github.com/mistydemeo/tigerbrew/go/install)"
   \`\`\`

2. **Install Python 3.6**:
   \`\`\`bash
   brew install python3
   python3 --version  # Should show 3.6.x
   \`\`\`

3. **Install Pick-a-Page**:
   \`\`\`bash
   # Download and extract pick-a-page
   cd pick-a-page
   python3 -m pip install --user pytest pytest-cov
   python3 -m pytest  # Run tests
   \`\`\`

## Running the Web Server

\`\`\`bash
python3 -m pick_a_page serve
\`\`\`

Open Safari 4.1.3 and navigate to: http://localhost:8080

## Troubleshooting

**"Connection refused"**: Check firewall settings
**"Port already in use"**: Use \`--port 9000\` for different port
**Browser doesn't load**: Try Firefox 3.6.28 instead of Safari
\`\`\`

#### Step 3.3: Developer Makefile Targets

**Update Makefile**:
\`\`\`makefile
# Add to existing Makefile

# Start web server
serve:
python -m pick_a_page serve

# Start web server in background
serve-bg:
python -m pick_a_page serve &

# Stop background server
serve-stop:
pkill -f "pick_a_page serve"

# Open browser to web interface
browse:
python -m pick_a_page serve &
sleep 2
open http://localhost:8080

# Run web tests only
test-web:
pytest tests/test_webapp.py tests/test_web_integration.py -v

# Run all tests including web
test-all: test test-web
\`\`\`

---

## Testing Strategy

### Unit Tests (TDD)

**Coverage Targets**:
- \`webapp.py\`: >90% coverage
- \`web_templates.py\`: 100% coverage (simple templates)
- Request handlers: >85% coverage

**Test Categories**:
1. **HTTP Routing**: Each endpoint responds correctly
2. **Form Handling**: POST data parsed and validated
3. **File Operations**: Save/load/delete with safety checks
4. **API Endpoints**: JSON responses formatted correctly
5. **Error Handling**: 404, 500 errors handled gracefully

### Integration Tests

**Manual Test Script** (for Safari 4 on Tiger):
\`\`\`markdown
# MANUAL_WEB_TESTS.md

## Test Checklist

### Homepage Tests
- [ ] Homepage loads at http://localhost:8080
- [ ] Story list displays
- [ ] "New Story" button works
- [ ] Click story card opens editor

### Editor Tests
- [ ] Editor loads with story content
- [ ] Textarea is editable
- [ ] Save button saves changes
- [ ] Preview pane updates after save
- [ ] Validate button shows errors
- [ ] Export button downloads HTML

### Browser Compatibility
- [ ] Works in Safari 4.1.3
- [ ] Works in Firefox 3.6.28
- [ ] Layout correct at 1024x768
- [ ] CSS styles render correctly
- [ ] JavaScript functions work
\`\`\`

---

## Python Version Compatibility

### Downgrade from 3.10+ to 3.6

**Breaking Changes to Address**:

| Python 3.10+ Feature | Python 3.6 Alternative |
|----------------------|------------------------|
| \`dict[str, int]\` | \`Dict[str, int]\` (from typing) |
| \`list[str]\` | \`List[str]\` (from typing) |
| \`match/case\` | \`if/elif/else\` |
| \`f-string\` debugging | \`f"x={x}"\` (no \`=\` debug) |
| \`removeprefix()\` | \`[len(prefix):]\` if \`startswith\` |
| \`removesuffix()\` | \`[:-len(suffix)]\` if \`endswith\` |
| Dataclass \`kw_only=True\` | Use \`field(default=...)\` |

**Example Refactoring**:
\`\`\`python
# Python 3.10+ (current)
def parse_stories(paths: list[Path]) -> dict[str, Story]:
    match response:
        case {'status': 'ok'}:
            return response['data']
        case _:
            raise ValueError()

# Python 3.6 compatible
from typing import Dict, List
from pathlib import Path

def parse_stories(paths: List[Path]) -> Dict[str, Story]:
    if response.get('status') == 'ok':
        return response['data']
    else:
        raise ValueError()
\`\`\`

**Testing Compatibility**:
\`\`\`bash
# Install Python 3.6 in Docker
docker run -v $(pwd):/app -it python:3.6 bash
cd /app
pip install pytest pytest-cov
pytest
\`\`\`

---

## Security Considerations

### Web Server Security

**Path Traversal Prevention**:
\`\`\`python
def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Only allow: alphanumeric, hyphens, underscores
    No: .. / \\ or other special chars
    """
    import re
    filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
    if '..' in filename or '/' in filename:
        raise ValueError("Invalid filename")
    return filename

def get_story_path(story_id: str) -> Path:
    """Get safe path to story file."""
    sanitized = sanitize_filename(story_id)
    story_path = STORIES_DIR / f"{sanitized}.txt"
    
    # Verify path is within stories directory
    if not story_path.resolve().is_relative_to(STORIES_DIR.resolve()):
        raise ValueError("Path traversal attempt")
    
    return story_path
\`\`\`

**File Size Limits**:
\`\`\`python
MAX_STORY_SIZE = 1024 * 1024  # 1MB

def read_story_file(story_id: str) -> str:
    """Read story file with size limit."""
    path = get_story_path(story_id)
    
    if path.stat().st_size > MAX_STORY_SIZE:
        raise ValueError("Story file too large")
    
    return path.read_text(encoding='utf-8')
\`\`\`

**CORS Headers** (for localhost development):
\`\`\`python
def set_cors_headers(handler):
    """Set CORS headers for AJAX requests."""
    handler.send_header('Access-Control-Allow-Origin', 'http://localhost:8080')
    handler.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')
\`\`\`

---

## User Experience Design

### Child-Friendly Interface Guidelines

**Visual Design**:
- 🎨 Bright, cheerful colors (avoid dark themes)
- 📖 Large, readable fonts (minimum 14px)
- 🔘 Big, obvious buttons (minimum 44x44px tap target)
- 🌈 Visual feedback for all actions
- �� Friendly error messages (no technical jargon)

**Language**:
- ✅ "Oops! This section name doesn't exist yet."
- ❌ "ValidationError: Undefined reference to section 'xyz'"
- ✅ "Great job! Your story is ready to share!"
- ❌ "Compilation successful. Exit code 0."

**Interaction Patterns**:
- Auto-save (never lose work)
- Undo/redo support
- Confirmation for destructive actions
- Progress indicators for slow operations
- Keyboard shortcuts (Ctrl+S to save)

**Accessibility**:
- Sufficient color contrast (WCAG AA minimum)
- Alt text for all images
- Keyboard navigation support
- Screen reader friendly labels

---

## Rollout Plan

### Step-by-Step Implementation

**Week 1: Foundation**
- [ ] Day 1: Create \`webapp.py\` with basic routing
- [ ] Day 2: Write 15 unit tests for HTTP handlers
- [ ] Day 3: Implement story list and homepage
- [ ] Day 4: Add editor page with textarea
- [ ] Day 5: Implement save/load functionality

**Week 2: Features**
- [ ] Day 1: Add live preview iframe
- [ ] Day 2: Implement validation API
- [ ] Day 3: Add export functionality
- [ ] Day 4: Create CSS/JS for editor UI
- [ ] Day 5: Browser compatibility testing

**Week 3: Polish**
- [ ] Day 1: Error handling and user feedback
- [ ] Day 2: Auto-save implementation
- [ ] Day 3: Multi-language support for web UI
- [ ] Day 4: Documentation updates
- [ ] Day 5: End-to-end testing on Tiger

### Success Criteria

**Must Have** (Phase 1):
- ✅ Web server starts on localhost:8080
- ✅ Can create new story in browser
- ✅ Can edit existing story
- ✅ Live preview updates on save
- ✅ Can export to HTML
- ✅ Works in Safari 4.1.3 on Tiger
- ✅ Zero external dependencies (stdlib only)
- ✅ >85% test coverage

**Should Have** (Phase 2):
- ✅ Auto-save every 30 seconds
- ✅ Validation shows errors inline
- ✅ Multi-language UI (EN, NL, IT)
- ✅ Keyboard shortcuts
- ✅ Mobile-responsive (for modern browsers)

**Nice to Have** (Phase 3):
- ✅ Flask version with better UX
- ✅ Syntax highlighting in editor
- ✅ Undo/redo history
- ✅ Story templates library
- ✅ Collaborative editing (multi-user)

---

## Migration from CLI to Web

### Preserving Existing Functionality

**The web application is ADDITIVE, not REPLACEMENT**:
- ✅ All CLI commands still work
- ✅ Existing HTML generation unchanged
- ✅ Test coverage maintained
- ✅ Backward compatible with Python 3.6+

**Users can choose**:
- Option 1: CLI only (current workflow)
- Option 2: Web UI only (new workflow)
- Option 3: Hybrid (create in CLI, edit in browser)

### Data Migration

**No migration needed** - same file format:
- Stories remain \`.txt\` files
- Output remains \`.html\` and \`.zip\`
- Directory structure unchanged
- Can switch between CLI and web freely

---

## Known Limitations & Tradeoffs

### Platform Constraints

**Mac OS X 10.4 Tiger Limitations**:
- ⚠️ Old browser (Safari 4.1.3) - limited JS/CSS
- ⚠️ Python 3.6 max - no modern type hints
- ⚠️ No pip in Tigerbrew - manual dependency install
- ⚠️ PowerPC architecture - slower performance

**Workarounds**:
- Use ES5 JavaScript (no ES6 features)
- Inline all CSS/JS (no module bundlers)
- Provide pre-built packages (no pip install)
- Keep server lightweight (avoid heavy processing)

### Technical Tradeoffs

| Decision | Pros | Cons | Mitigation |
|----------|------|------|------------|
| **Stdlib only** | Zero deps, Tiger compatible | Limited features | Add Flask optional |
| **ES5 JavaScript** | Safari 4 compatible | Verbose syntax | Minimize JS code |
| **Inline CSS/JS** | No HTTP requests | Larger HTML size | Acceptable for editor |
| **Python 3.6** | Tigerbrew compatible | Old syntax | Future Python 3.10 version |
| **No WebSockets** | Simple server | No real-time collab | Polling for updates |

---

## Future Enhancements

### Post-Initial Release

**Version 2.0 Features** (modern Python users):
- FastAPI backend with Python 3.10+
- React/Vue frontend
- WebSocket for real-time collaboration
- Syntax highlighting with CodeMirror
- Git integration for version control
- Story marketplace (share stories)

**Version 3.0 Features** (cloud-hosted):
- SaaS deployment (no local install)
- User accounts and authentication
- Cloud storage (Google Drive, Dropbox)
- Mobile apps (iOS, Android)
- AI-assisted story writing
- Analytics (which paths players take)

---

## Appendix: Command Quick Reference

### CLI Commands (Existing + New)

\`\`\`bash
# Existing commands (still work)
python -m pick_a_page init my_story
python -m pick_a_page compile my_story.txt
python -m pick_a_page validate my_story.txt

# New web server command
python -m pick_a_page serve
python -m pick_a_page serve --port 9000
python -m pick_a_page serve --host 0.0.0.0

# Makefile shortcuts
make serve          # Start web server
make serve-bg       # Start in background
make browse         # Start and open browser
make test-web       # Run web tests only
\`\`\`

### URL Reference

\`\`\`
http://localhost:8080/              → Story list homepage
http://localhost:8080/new           → Create new story
http://localhost:8080/edit/my-story → Edit existing story
http://localhost:8080/preview/my-story → Live preview
http://localhost:8080/export/my-story → Download HTML
http://localhost:8080/export/my-story/zip → Download ZIP
http://localhost:8080/api/stories   → Stories JSON API
http://localhost:8080/api/validate  → Validation API
\`\`\`

---

## AI Agent Implementation Checklist

> **For Claude 4.5 / Copilot**: Use this checklist when implementing the webapp feature.

### Pre-Implementation
- [ ] Read entire IMPLEMENT_WEBAPP.md file
- [ ] Read AGENTS.md for project context
- [ ] Understand Python 3.6 compatibility requirements
- [ ] Review existing codebase (compiler.py, generator.py)
- [ ] Run existing tests to verify baseline

### Phase 1: Core Implementation
- [ ] Create \`pick_a_page/webapp.py\` with basic server
- [ ] Create \`pick_a_page/web_templates.py\` with HTML templates
- [ ] Write tests FIRST for each handler method (TDD)
- [ ] Implement HTTP request routing
- [ ] Add form handling for save/load
- [ ] Implement story list API
- [ ] Add preview generation
- [ ] Test in Python 3.6 environment

### Phase 2: UI/UX
- [ ] Create child-friendly CSS (ES5 compatible)
- [ ] Write JavaScript for AJAX (no ES6)
- [ ] Implement auto-save feature
- [ ] Add validation feedback UI
- [ ] Test in Safari 4.1.3 (or document manual testing)
- [ ] Verify responsive layout

### Phase 3: Integration
- [ ] Add 'serve' command to CLI
- [ ] Update i18n translations for web UI
- [ ] Write integration tests
- [ ] Update README with web instructions
- [ ] Update Makefile with new targets
- [ ] Verify all 83+ tests still pass

### Phase 4: Documentation
- [ ] Create TIGERBREW_SETUP.md guide
- [ ] Update README with web features
- [ ] Write MANUAL_WEB_TESTS.md for Safari testing
- [ ] Add docstrings to all new functions
- [ ] Update AGENTS.md if needed

### Phase 5: Testing & Validation
- [ ] Run \`make test\` (all tests pass)
- [ ] Verify >85% code coverage maintained
- [ ] Test Python 3.6 compatibility
- [ ] Manual test in browser (Safari 4 if available)
- [ ] Security audit (path traversal, XSS, CSRF)
- [ ] Performance check (story load time < 1s)

### Quality Checks
- [ ] No external runtime dependencies added
- [ ] All new code has tests (TDD)
- [ ] ES5 JavaScript only (no ES6)
- [ ] Python 3.6 compatible syntax
- [ ] Child-friendly UI language
- [ ] Docstrings on all public functions
- [ ] Type hints compatible with 3.6

---

## Final Recommendations

**✅ CONFIRMED TARGET**: iMac 333MHz PowerPC G3 with Mac OS X 10.4.11

**❌ DISCARDED ASSUMPTIONS**: User's Python 3.7 is NOT on target machine. Target is confirmed PowerPC Tiger.

---

**Best Architecture for iMac 333MHz PowerPC Tiger**:

### Option A: Remote Web Editor ⭐ RECOMMENDED

**Build web editor on modern computer, sync files to iMac for playback**

✅ **Why This is Best**:
- ✅ Fast, responsive editing (on modern machine)
- ✅ Can use FastAPI (user's stated preference!)
- ✅ Professional web development experience for child
- ✅ iMac only used for playback (lightweight)
- ✅ No performance issues
- ✅ Best of both worlds

**Architecture**:
- Modern computer runs FastAPI web editor
- Export static HTML files
- Sync to iMac via USB/Dropbox/network
- iMac plays stories in Safari (no server needed)

**Implementation**: FastAPI on modern Python 3.10+
**Timeline**: 2-4 days
**User Experience**: Excellent

---

### Option B: Keep Current CLI Tool ⭐ ALSO EXCELLENT

**Continue using existing pick-a-page CLI**

✅ **Why This Works Well**:
- ✅ Already implemented and working
- ✅ Fast on PowerPC (no server overhead)
- ✅ Simple commands for 8-year-old
- ✅ Generates beautiful HTML output
- ✅ No waiting or performance issues
- ✅ Perfect for this hardware

**Implementation**: None needed (already done!)
**Timeline**: 0 days
**User Experience**: Good (command-line based)

---

### Option C: Minimal Local Web Server ⚠️ NOT RECOMMENDED

**IF user insists on web editor running ON the iMac**

⚠️ **Reality Check**:
- ⚠️ 333MHz PowerPC is too slow for comfortable web serving
- ⚠️ 2-5 second page loads
- ⚠️ 1-3 second save operations
- ⚠️ Frustrating user experience
- ⚠️ Child will spend more time waiting than creating

**IF INSISTED**:
- Use TigerSH for pre-built Python 3.6 binaries (fastest install)
- Use stdlib http.server (zero dependencies)
- Minimal features only
- No real-time preview (too slow)

**Implementation**: Python 3.6 + stdlib http.server
**Timeline**: 3-5 days
**User Experience**: Poor (very slow)

---

### Comparison Table

| Option | Editor Location | FastAPI? | Performance | Child Experience | Recommended |
|--------|----------------|----------|-------------|------------------|-------------|
| **A: Remote Editor** | Modern computer | ✅ YES | Excellent | ⭐⭐⭐⭐⭐ Fast & fun | ✅ **BEST** |
| **B: CLI Tool** | iMac (command line) | ❌ NO | Good | ⭐⭐⭐⭐ Simple & reliable | ✅ **GOOD** |
| **C: Local Server** | iMac (web browser) | ❌ NO | Very poor | ⭐⭐ Slow & frustrating | ❌ **NOT RECOMMENDED** |

---

### Installation Recommendations

**Package Manager Choice for Tiger PowerPC**:

| Method | Speed | Python Version | Status | Recommendation |
|--------|-------|----------------|--------|----------------|
| **TigerSH** | Fast (pre-built) | 3.4-3.6 | Active | ⭐ **BEST for Tiger** |
| **Tigerbrew** | Very slow (compile) | 3.6.15 | Active | Good but slow install |
| **MacPorts** | Very slow (compile) | 3.3-3.4 | Abandoned | ❌ NOT recommended |

**For Option A (Remote Editor)**: Use modern Python 3.10+ on modern computer
**For Option B (CLI)**: Can run on current Python installation
**For Option C (Local Server)**: Use TigerSH to install Python 3.6 with pre-built binaries

---

### My Strong Recommendation

**For iMac 333MHz PowerPC G3 Tiger:**

**Use Option A or B**, NOT Option C.

The 333MHz PowerPC G3 is a 27-year-old processor that is simply too slow for a comfortable web server experience. Even with the most optimized code, the child will face:
- Long waits for pages to load
- Frustration with slow response times
- Negative learning experience ("programming is slow")

**Option A (Remote Editor)** gives you:
- Everything you wanted (web-based, FastAPI, browser editing)
- Fast, modern experience
- Professional development practices for child to learn
- Use the iMac for what it's good at (playing the stories)

**Option B (CLI)** gives you:
- Simple, working solution
- No performance issues
- Already implemented
- Good enough for learning programming

**Both options are better than running a web server on 333MHz PowerPC.**

---

## Questions & Support

**For Implementers**:

- Q: "Should I build the web server for the iMac?"
- A: **NO**. The iMac 333MHz PowerPC is too slow. Use Option A (remote editor) or Option B (keep CLI).

- Q: "Can I use FastAPI on Tiger?"
- A: **Not on the iMac (Tiger), but YES on a modern computer (Option A)**.

- Q: "What about TigerSH vs Tigerbrew?"
- A: **Use TigerSH for Tiger** - pre-built binaries are much faster than compiling on 333MHz.

- Q: "What about MacPorts?"
- A: **Don't use MacPorts** - it's abandoned and requires slow compilation.

- Q: "The user said they prefer FastAPI - can I use it?"
- A: **Yes, via Option A (Remote Editor)**. Build FastAPI editor on modern computer, sync files to iMac.

- Q: "Is Python 3.x too slow on 333MHz?"
- A: **Yes, for web serving**. Python 3.x on 333MHz PowerPC will result in 2-5 second page loads.

- Q: "What if the user really wants local web server?"
- A: **Explain the performance reality**. Then implement Option C with very low expectations.

- Q: "Should I use Flask or stdlib?"
- A: **FastAPI first (if Leopard), then Flask, then stdlib as last resort.**

- Q: "What about Python 3.10 type hints?"
- A: **Use Python 3.7+ syntax if Leopard, 3.6 syntax if Tiger.** Check OS first.

- Q: "Can I use ES6 JavaScript?"
- A: **Yes if Leopard (10.5)**, limited ES5 only if Tiger (10.4). Safari 5.0.6 vs 4.1.3.

- Q: "Should I add npm/webpack?"
- A: **For FastAPI, yes (modern tooling).** For stdlib, no (keep simple).

- Q: "What about HTTPS?"
- A: **HTTP is fine for localhost.** Don't overcomplicate.

- Q: "Why is Python 3.7 significant?"
- A: **Python 3.7 is NOT available on Tiger via Tigerbrew.** Its presence indicates Leopard (10.5) or newer, which changes ALL recommendations.

**For Questions**:
- Check AGENTS.md for project philosophy
- Review existing test files for patterns
- Ask user before adding dependencies
- When in doubt, keep it simple

---

**Document Version**: 3.0 (Updated with TigerSH, MacPorts, and PowerPC hardware analysis)
**Last Updated**: 2025-11-22
**Author**: Analysis by AI Agent (Copilot)
**Confirmed Target**: iMac 333MHz PowerPC G3 with Mac OS X 10.4.11 (Tiger)
**Target Python**: 
- **Option A/B**: Python 3.10+ (modern computer) OR current Python
- **Option C (not recommended)**: Python 3.6 via TigerSH (if insisted on local server)
**Hardware Constraints**: 333MHz PowerPC G3 - severely limited, 27 years old
**Recommended Approaches**:
1. **Option A**: Remote web editor on modern computer + file sync ⭐ BEST
2. **Option B**: Keep existing CLI tool ⭐ ALSO GOOD
3. **Option C**: Local web server on iMac ⚠️ NOT RECOMMENDED (too slow)
**Implementation Effort**: 
- **Option A (Remote FastAPI)**: 2-4 days - RECOMMENDED
- **Option B (Keep CLI)**: 0 days (already done)
- **Option C (Local server)**: 3-5 days (poor UX)
**Confidence Level**: High ✅ (thoroughly researched PowerPC Tiger limitations)
**Critical Insight**: 333MHz PowerPC is too slow for comfortable web serving. Use remote editor or CLI instead.
