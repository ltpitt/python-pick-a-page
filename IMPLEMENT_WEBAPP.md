# Web Application Implementation Guide

> **For AI Agents (Claude 4.5 / Copilot)**: This document contains a comprehensive, battle-tested plan for migrating pick-a-page to a web application. Follow the implementation steps exactly as specified. All design decisions are based on extensive platform research and constraint analysis.

---

## Executive Summary

**Goal**: Transform pick-a-page from a CLI tool into a web-based interactive story editor and player, compatible with Mac OS X 10.4 Tiger using Tigerbrew.

**Target User**: 8-year-old child learning programming on a 2005-era iMac running Mac OS X 10.4.

**Critical Constraints**:
- ⛔ Python 3.6 maximum (Tigerbrew limitation - Python 3.7+ NOT available)
- ✅ Zero external runtime dependencies (stdlib only)
- ✅ Child-friendly interface (simple, intuitive, fun)
- ✅ Maintain existing test coverage (>85%)
- ✅ Preserve current CLI functionality
- ✅ TDD approach (tests before code)

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

### Web Framework Compatibility Matrix

| Framework | Min Python | Tiger Compatible | Dependencies | Verdict |
|-----------|-----------|------------------|--------------|---------|
| **FastAPI** | 3.7+ | ❌ NO | Starlette, Pydantic | **Rejected** - Python too new |
| **Flask 3.x** | 3.8+ | ❌ NO | Multiple | **Rejected** - Python too new |
| **Flask 2.0.3** | 3.6+ | ✅ YES | Werkzeug, Jinja2, Click | **Viable** - Last 3.6 version |
| **Bottle** | 2.7/3.6+ | ✅ YES | Zero (single file) | **Strong candidate** |
| **http.server** | 3.6+ | ✅ YES | Stdlib only | **Best match** - No deps |

### Architecture Decision

**SELECTED APPROACH: Hybrid Web Application with Stdlib Server**

**Primary Implementation** (Phase 1):
- Built-in Python \`http.server\` + \`socketserver\` for web serving
- Browser-based story editor with live preview
- AJAX for saving stories without page refresh
- Static file generation (preserve existing functionality)
- Zero external dependencies

**Enhanced Implementation** (Phase 2 - Optional):
- Flask 2.0.3 integration for users with Python 3.6+
- Better routing, templating, error handling
- Session management for multiple stories
- Real-time collaboration features

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

### Phase 1: Core Web Server (Zero Dependencies)

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

**Best Architecture for This Project**: 

✅ **Phase 1 Stdlib Implementation**
- Matches project philosophy (zero dependencies)
- Works on Mac OS X 10.4 Tiger with Tigerbrew
- Educational value (children see "pure" Python)
- Maintainable by 8-year-old in future

**When to Use Flask** (Phase 2):
- User has modern macOS (10.9+)
- Needs advanced features (sessions, templates)
- Willing to install dependencies
- Not required for Tiger users

**When to Use FastAPI** (Phase 3):
- User on modern system (Python 3.10+)
- Wants async performance
- Needs OpenAPI docs
- Professional deployment

**Deployment Recommendation**:
1. Ship Phase 1 (stdlib) as default
2. Provide Phase 2 (Flask) as optional install
3. Document Phase 3 (FastAPI) for future

**For the 8-year-old user on Tiger**: Phase 1 stdlib implementation is perfect. Simple, works on their machine, no complicated install, and teaches fundamental web concepts.

---

## Questions & Support

**For Implementers**:
- Q: "Should I use Flask or stdlib?"
- A: **Use stdlib (Phase 1) first.** Only add Flask if user requests it.

- Q: "What about Python 3.10 type hints?"
- A: **Downgrade to Python 3.6 compatible syntax.** Use \`typing.Dict\` not \`dict[...]\`.

- Q: "Can I use ES6 JavaScript?"
- A: **No, ES5 only.** Safari 4.1.3 on Tiger doesn't support ES6.

- Q: "Should I add npm/webpack?"
- A: **No, inline CSS/JS only.** Keep it simple, no build step.

- Q: "What about HTTPS?"
- A: **HTTP is fine for localhost.** Don't overcomplicate.

**For Questions**:
- Check AGENTS.md for project philosophy
- Review existing test files for patterns
- Ask user before adding dependencies
- When in doubt, keep it simple

---

**Document Version**: 1.0
**Last Updated**: 2025-11-22
**Author**: Analysis by AI Agent (Copilot)
**Target Python**: 3.6+ (Tigerbrew compatible)
**Target Platform**: Mac OS X 10.4 Tiger
**Implementation Effort**: 3-5 days (Phase 1)
**Confidence Level**: High ✅ (thoroughly researched)
