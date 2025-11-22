# Hybrid Architecture Plan: CLI + Remote Web Editor

> **For AI Agents (Claude 4.5 / Copilot)**: This document outlines the hybrid architecture approach that combines the existing CLI tool with a remote web editor, based on user's successful Python 3.10 installation via Tigerbrew on Mac OS X 10.4.11 Tiger.

---

## Executive Summary

**Objective**: Build a hybrid solution that:
1. ✅ Preserves 100% CLI functionality on iMac Tiger (write in text editor → compile to HTML → play in browser)
2. ✅ Adds optional web editor on modern computer (FastAPI-based, lightweight, good UX/UI)
3. ✅ Accessible from iMac Tiger via network (Safari 4.1.3 compatible)
4. ✅ Not resource-intensive (considerate of 333MHz PowerPC)
5. ✅ Backward compatible (CLI always works, webapp is optional enhancement)

**User's Correction**: Python 3.10 successfully installed via Tigerbrew on Tiger! 🎉

---

## Architecture Overview

### Two-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Tier 1: CLI Tool (Standalone - Local on iMac)             │
│  ────────────────────────────────────────────────────────   │
│                                                             │
│  iMac 333MHz PowerPC (Tiger 10.4.11)                       │
│  ├─ Python 3.10 (via Tigerbrew) ✅                         │
│  ├─ pick-a-page CLI (existing)                             │
│  ├─ Text editor (TextEdit, BBEdit, etc)                    │
│  └─ Safari 4.1.3 (play stories)                            │
│                                                             │
│  Workflow:                                                  │
│  1. Write story in text editor                             │
│  2. python -m pick_a_page compile story.txt                │
│  3. Open story.html in Safari                              │
│                                                             │
│  Status: ✅ Already implemented and working                │
└─────────────────────────────────────────────────────────────┘

                            │
                    Optional Enhancement
                            │
                            ▼

┌─────────────────────────────────────────────────────────────┐
│  Tier 2: Web Editor (Optional - Remote Server)             │
│  ────────────────────────────────────────────────────────   │
│                                                             │
│  Modern Computer (Parent's laptop/desktop)                 │
│  ├─ Python 3.10+ ✅                                        │
│  ├─ FastAPI Web Server                                     │
│  ├─ Lightweight web UI (ES5 for Safari 4.1.3)             │
│  └─ File storage & management                              │
│                                                             │
│  Network accessible:                                        │
│  http://192.168.1.x:8080                                    │
│                                                             │
│  iMac accesses via Safari 4.1.3:                           │
│  ├─ Write stories in browser (textarea)                    │
│  ├─ Live preview (iframe)                                  │
│  ├─ Save/Load stories                                      │
│  └─ Export to HTML                                         │
│                                                             │
│  Status: 🔨 To be implemented                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### 1. CLI-First (Core Principle)
- **CLI tool is PRIMARY interface** - must always work standalone
- Web editor is OPTIONAL enhancement, not replacement
- If webapp is unavailable, CLI still 100% functional
- No dependencies on network or modern computer

### 2. Lightweight & Compatible
- **Minimal HTML/CSS/JS** sent to iMac
- **ES5 JavaScript only** (Safari 4.1.3 compatible)
- **No heavy frameworks** on client side (no React, Vue)
- **Small page sizes** (< 100KB per page)
- **Simple forms** (standard HTML inputs, minimal processing)

### 3. Resource-Conscious
- **Server does heavy lifting** (Python compilation on modern computer)
- **iMac only renders UI** (minimal CPU usage)
- **No real-time features** requiring constant polling
- **Static assets cached** (reduce network traffic)

### 4. Backward Compatible
- **Same story format** (.txt files with [[section]] syntax)
- **Same compiler** (shared code between CLI and webapp)
- **Same output** (identical HTML files)
- **Interchangeable** (stories created in CLI work in webapp and vice versa)

---

## Implementation Plan

### Phase 1: Core Web Server (Week 1)

**Goal**: Basic FastAPI server with story management

**Components**:
1. **FastAPI application** (`pick_a_page/webapp_server.py`)
   - Story CRUD endpoints (Create, Read, Update, Delete)
   - Compilation endpoint (reuse existing compiler)
   - Static file serving
   - CORS support for network access

2. **Storage layer** (`pick_a_page/storage.py`)
   - File-based storage (simple, reliable)
   - Story list/search
   - Story versioning (optional)

3. **API Endpoints**:
   ```python
   GET  /api/stories           # List all stories
   GET  /api/stories/{id}      # Get story content
   POST /api/stories           # Create new story
   PUT  /api/stories/{id}      # Update story
   DELETE /api/stories/{id}    # Delete story
   POST /api/compile/{id}      # Compile to HTML
   GET  /api/export/{id}       # Download HTML
   ```

**Testing**:
- Unit tests for all endpoints
- Integration tests with existing compiler
- Performance tests (response time < 100ms)

**Timeline**: 2-3 days

---

### Phase 2: Web UI (Week 1-2)

**Goal**: Simple, fast web interface for Safari 4.1.3

**Components**:
1. **Homepage** (`templates/index.html`)
   - List of stories (table/cards)
   - Create new story button
   - Search/filter stories
   - Child-friendly design

2. **Editor Page** (`templates/editor.html`)
   - Split-pane layout:
     - Left: Textarea for story content
     - Right: Live preview iframe
   - Toolbar: Save, Validate, Export buttons
   - Auto-save (every 30 seconds)
   - Syntax highlighting (simple, optional)

3. **Preview Page** (`templates/preview.html`)
   - Embedded iframe showing compiled story
   - Refresh on save

**Browser Compatibility**:
```javascript
// ES5 only - Safari 4.1.3 compatible
var storyId = getStoryId();

function saveStory() {
    var content = document.getElementById('story-content').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/stories/' + storyId, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            showMessage('Story saved!');
            refreshPreview();
        }
    };
    xhr.send(JSON.stringify({ content: content }));
}

// Auto-save every 30 seconds
setInterval(function() {
    saveStory();
}, 30000);
```

**CSS Guidelines**:
- CSS 2.1 (avoid flexbox, grid)
- Simple layouts (floats, tables)
- Large fonts (14px minimum)
- High contrast colors
- Minimal animations

**Timeline**: 3-4 days

---

### Phase 3: Integration & Polish (Week 2)

**Goal**: Seamless integration between CLI and webapp

**Features**:
1. **Shared Story Format**
   - CLI and webapp use identical .txt format
   - Stories created in CLI visible in webapp
   - Stories created in webapp work with CLI

2. **File Sync** (optional)
   - Network share (SMB/AFP)
   - USB drive sync
   - Dropbox/iCloud (if available)

3. **Export Options**
   - HTML file (same as CLI)
   - ZIP package (HTML + images + source)
   - PDF (future enhancement)

4. **User Management** (optional, simple)
   - Single user mode (default)
   - Multi-user (if needed)
   - No authentication required on local network

**Timeline**: 2-3 days

---

### Phase 4: Testing & Documentation (Week 3)

**Goal**: Ensure reliability and usability

**Testing**:
1. **Safari 4.1.3 Compatibility**
   - Manual testing on Tiger iMac
   - All features work correctly
   - No JavaScript errors
   - Acceptable performance

2. **Network Testing**
   - Access from iMac on local network
   - Latency tests (< 200ms acceptable)
   - Concurrent access (if multiple users)

3. **CLI Compatibility**
   - Stories from CLI work in webapp
   - Stories from webapp work in CLI
   - Same output from both methods

**Documentation**:
1. **User Guide**
   - How to start the web server
   - How to access from iMac
   - Basic usage instructions
   - Troubleshooting

2. **Developer Guide**
   - Architecture overview
   - API documentation
   - Extending the system
   - Testing procedures

**Timeline**: 2-3 days

---

## File Structure

```
pick_a_page/
├── pick_a_page/
│   ├── __init__.py
│   ├── __main__.py              # CLI entry (existing)
│   ├── compiler.py              # Story compiler (existing)
│   ├── generator.py             # HTML generator (existing)
│   ├── templates.py             # HTML templates (existing)
│   ├── i18n.py                  # Internationalization (existing)
│   │
│   ├── webapp_server.py         # NEW - FastAPI application
│   ├── storage.py               # NEW - File storage management
│   ├── web_api.py               # NEW - API endpoints
│   │
│   └── web_templates/           # NEW - Web UI templates
│       ├── base.html           # Base template
│       ├── index.html          # Story list
│       ├── editor.html         # Story editor
│       └── preview.html        # Preview page
│
├── static/                      # NEW - Static assets
│   ├── css/
│   │   └── style.css           # ES5-compatible styles
│   ├── js/
│   │   └── app.js              # ES5 JavaScript
│   └── img/
│       └── logo.png
│
├── tests/
│   ├── test_compiler.py         # Existing tests
│   ├── test_generator.py        # Existing tests
│   ├── test_integration.py      # Existing tests
│   ├── test_i18n.py             # Existing tests
│   │
│   ├── test_webapp_server.py    # NEW - Server tests
│   ├── test_storage.py          # NEW - Storage tests
│   └── test_web_api.py          # NEW - API tests
│
├── stories/                     # NEW - Story storage directory
│   ├── my_adventure.txt
│   └── treasure_hunt.txt
│
├── requirements.txt             # Existing dev dependencies
├── requirements-webapp.txt      # NEW - Web server dependencies
├── Makefile                     # Existing
├── README.md                    # Existing - update with webapp docs
└── HYBRID_ARCHITECTURE_PLAN.md  # This document
```

---

## Technology Stack

### Backend (Modern Computer)
- **Framework**: FastAPI (user's preference)
- **Python**: 3.10+ (modern features, type hints)
- **Server**: Uvicorn (ASGI server)
- **Storage**: File system (simple, reliable)
- **Validation**: Pydantic models

### Frontend (Safari 4.1.3 Compatible)
- **HTML**: HTML5 with HTML4 fallbacks
- **CSS**: CSS 2.1 (no flexbox, grid)
- **JavaScript**: ES5 only (no arrow functions, no const/let)
- **AJAX**: XMLHttpRequest (not Fetch API)
- **Templating**: Jinja2 (server-side)

### Development
- **Testing**: pytest (existing)
- **Linting**: flake8 (existing)
- **Type Checking**: mypy (optional)
- **Documentation**: Markdown

---

## CLI Commands

### Existing Commands (Unchanged)
```bash
# Initialize new story
python -m pick_a_page init my_story

# Compile story to HTML
python -m pick_a_page compile my_story.txt

# Validate story
python -m pick_a_page validate my_story.txt
```

### New Commands (Added)
```bash
# Start web server
python -m pick_a_page serve

# Start web server with options
python -m pick_a_page serve --host 0.0.0.0 --port 8080

# Start web server (production mode)
python -m pick_a_page serve --production
```

### Installation
```bash
# Install CLI dependencies (existing)
pip install -r requirements.txt

# Install web server dependencies (new, optional)
pip install -r requirements-webapp.txt
```

---

## Usage Scenarios

### Scenario 1: CLI Only (Default - Works Offline)
```bash
# On iMac Tiger
cd ~/stories
python -m pick_a_page init treasure_hunt
vim treasure_hunt.txt          # Write story
python -m pick_a_page compile treasure_hunt.txt
open output/treasure_hunt.html # Play in Safari
```

**Advantages**:
- ✅ No network required
- ✅ Fast and simple
- ✅ Full control
- ✅ Works when modern computer unavailable

---

### Scenario 2: Web Editor (Enhanced UX)
```bash
# On modern computer
cd ~/pick_a_page
python -m pick_a_page serve --host 0.0.0.0

# Open in browser on iMac
# http://192.168.1.100:8080
```

**Workflow**:
1. Child opens Safari on iMac
2. Navigates to modern computer's IP
3. Sees list of stories
4. Clicks "New Story"
5. Types story in web editor
6. Preview updates automatically
7. Clicks "Save"
8. Clicks "Export" to download HTML
9. Opens HTML in Safari to play

**Advantages**:
- ✅ Better UI/UX
- ✅ Live preview
- ✅ Auto-save (no lost work)
- ✅ Story management (list, search)
- ✅ Faster compilation (modern CPU)

---

### Scenario 3: Hybrid (Best of Both)
```bash
# Parent starts web server in morning
python -m pick_a_page serve --host 0.0.0.0

# Child uses web editor during day
# (Opens Safari, edits stories)

# Web server stopped in evening
# Child switches to CLI if needed
python -m pick_a_page compile story.txt
```

**Advantages**:
- ✅ Flexibility
- ✅ Gradual adoption
- ✅ Fallback to CLI always available
- ✅ Learn both interfaces

---

## API Specification

### Story Management

#### List Stories
```http
GET /api/stories
Response: 200 OK
{
  "stories": [
    {
      "id": "treasure-hunt",
      "title": "Treasure Hunt",
      "author": "Alice",
      "created": "2025-01-15T10:30:00Z",
      "modified": "2025-01-15T14:20:00Z"
    }
  ]
}
```

#### Get Story
```http
GET /api/stories/{id}
Response: 200 OK
{
  "id": "treasure-hunt",
  "title": "Treasure Hunt",
  "author": "Alice",
  "content": "---\ntitle: Treasure Hunt\nauthor: Alice\n---\n\n[[start]]: ...",
  "created": "2025-01-15T10:30:00Z",
  "modified": "2025-01-15T14:20:00Z"
}
```

#### Create Story
```http
POST /api/stories
Content-Type: application/json
{
  "title": "New Adventure",
  "author": "Bob",
  "content": "---\ntitle: New Adventure\nauthor: Bob\n---\n\n[[start]]: ..."
}

Response: 201 Created
{
  "id": "new-adventure",
  "message": "Story created successfully"
}
```

#### Update Story
```http
PUT /api/stories/{id}
Content-Type: application/json
{
  "content": "---\ntitle: Updated Story\nauthor: Bob\n---\n\n[[start]]: ..."
}

Response: 200 OK
{
  "message": "Story updated successfully"
}
```

#### Delete Story
```http
DELETE /api/stories/{id}
Response: 200 OK
{
  "message": "Story deleted successfully"
}
```

### Compilation

#### Compile Story
```http
POST /api/compile/{id}
Response: 200 OK
{
  "html": "<html>...</html>",
  "message": "Story compiled successfully"
}
```

#### Validate Story
```http
POST /api/validate
Content-Type: application/json
{
  "content": "---\ntitle: Story\n---\n\n[[start]]: ..."
}

Response: 200 OK
{
  "valid": true,
  "errors": []
}

OR

Response: 400 Bad Request
{
  "valid": false,
  "errors": [
    "Section 'start' has broken link to 'missing-section'",
    "Section 'orphaned' is never referenced"
  ]
}
```

#### Export Story
```http
GET /api/export/{id}
Response: 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="treasure-hunt.html"

<html>...</html>
```

---

## Security Considerations

### Network Security
- **Local network only** (bind to 192.168.x.x, not 0.0.0.0)
- **No authentication** (trusted home network)
- **CORS configured** for iMac access only
- **No HTTPS** (local network, not needed)

### File System Security
- **Path traversal protection** (sanitize filenames)
- **File size limits** (max 1MB per story)
- **Allowed extensions** (.txt only)
- **Story directory isolation** (no access outside stories/)

### Input Validation
- **Story content validation** (check format)
- **XSS prevention** (escape HTML in preview)
- **SQL injection N/A** (no database)

---

## Performance Optimization

### Server-Side
- **Caching compiled stories** (avoid recompilation)
- **Lazy loading** (stories loaded on demand)
- **Compression** (gzip for text responses)
- **Static file caching** (CSS/JS/images)

### Client-Side
- **Minimal JavaScript** (reduce parsing time on 333MHz)
- **Debounced auto-save** (don't save on every keystroke)
- **Lazy preview updates** (compile on save, not on every change)
- **Small payloads** (< 100KB per page)

### Network
- **Keep-alive connections** (reduce TCP overhead)
- **Batched requests** (group API calls when possible)
- **CDN N/A** (local network)

---

## Testing Strategy

### Unit Tests
```python
# test_webapp_server.py
def test_list_stories():
    """GET /api/stories should return list of stories"""
    response = client.get("/api/stories")
    assert response.status_code == 200
    assert "stories" in response.json()

def test_create_story():
    """POST /api/stories should create new story"""
    story = {
        "title": "Test Story",
        "author": "Test",
        "content": "[[start]]: Hello"
    }
    response = client.post("/api/stories", json=story)
    assert response.status_code == 201
    assert "id" in response.json()
```

### Integration Tests
```python
# test_web_integration.py
def test_cli_to_webapp():
    """Stories created in CLI should appear in webapp"""
    # Create story using CLI
    subprocess.run(["python", "-m", "pick_a_page", "init", "test-story"])
    
    # List stories via API
    response = client.get("/api/stories")
    stories = response.json()["stories"]
    
    # Verify story appears
    assert any(s["id"] == "test-story" for s in stories)

def test_webapp_to_cli():
    """Stories created in webapp should work with CLI"""
    # Create story via API
    client.post("/api/stories", json={
        "title": "Test",
        "author": "Test",
        "content": "[[start]]: Hello"
    })
    
    # Compile using CLI
    result = subprocess.run(
        ["python", "-m", "pick_a_page", "compile", "stories/test.txt"],
        capture_output=True
    )
    
    # Verify compilation succeeds
    assert result.returncode == 0
```

### Browser Compatibility Tests
```markdown
# Manual Test Checklist (Safari 4.1.3 on Tiger)

## Homepage
- [ ] Page loads in < 3 seconds
- [ ] Story list displays correctly
- [ ] "New Story" button works
- [ ] Search box filters stories
- [ ] No JavaScript errors in console

## Editor
- [ ] Editor page loads in < 3 seconds
- [ ] Textarea is editable
- [ ] Save button saves content
- [ ] Auto-save works every 30 seconds
- [ ] Preview iframe updates after save
- [ ] Export button downloads HTML
- [ ] No JavaScript errors

## Compatibility
- [ ] No CSS layout issues
- [ ] Text is readable (14px minimum)
- [ ] Buttons are clickable (44px minimum)
- [ ] Forms submit correctly
- [ ] AJAX requests work
```

---

## Deployment

### Development Mode
```bash
# On modern computer
cd ~/pick_a_page
pip install -r requirements-webapp.txt
python -m pick_a_page serve --debug

# Access from iMac
# http://192.168.1.100:8080
```

### Production Mode
```bash
# With systemd (Linux)
sudo systemctl enable pick-a-page-webapp
sudo systemctl start pick-a-page-webapp

# With launchd (macOS)
cp pick-a-page.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/pick-a-page.plist

# Manual
nohup python -m pick_a_page serve --production &
```

---

## Timeline Summary

| Phase | Tasks | Duration | Deliverables |
|-------|-------|----------|--------------|
| **Phase 1** | Core web server, API endpoints, storage | 2-3 days | Working FastAPI server |
| **Phase 2** | Web UI, editor, preview | 3-4 days | Browser-accessible interface |
| **Phase 3** | Integration, polish, export | 2-3 days | Seamless CLI/webapp sync |
| **Phase 4** | Testing, docs, Safari testing | 2-3 days | Production-ready system |
| **TOTAL** | Full hybrid system | **9-13 days** | **~2 weeks** |

---

## Success Criteria

### Must Have ✅
1. CLI tool works 100% standalone (existing functionality preserved)
2. Web server accessible from iMac on local network
3. Story editor works in Safari 4.1.3 on Tiger
4. Stories created in CLI work in webapp and vice versa
5. Same story format and compilation output
6. Auto-save prevents data loss
7. Export to HTML works correctly
8. > 85% test coverage maintained

### Should Have 🎯
1. Live preview updates on save
2. Story list/search functionality
3. Simple, child-friendly UI
4. Response time < 1 second (on modern server)
5. Page load time < 3 seconds (on iMac)
6. Validation feedback in UI
7. Multi-language support (existing i18n)

### Nice to Have 🌟
1. Syntax highlighting in editor
2. Story templates
3. Undo/redo functionality
4. Keyboard shortcuts (Ctrl+S to save)
5. Drag-and-drop for images
6. Story statistics (word count, sections)
7. Export to PDF

---

## Risks & Mitigation

### Risk 1: Safari 4.1.3 Compatibility
**Impact**: High
**Mitigation**: 
- Strict ES5 JavaScript only
- Test frequently on Tiger iMac
- Fallback to simple forms if AJAX fails

### Risk 2: Network Latency
**Impact**: Medium
**Mitigation**:
- Debounced auto-save
- Local caching where possible
- Optimistic UI updates

### Risk 3: Server Availability
**Impact**: Low
**Mitigation**:
- CLI always works as fallback
- Clear documentation on starting server
- Simple error messages

### Risk 4: Python 3.10 on Tiger
**Impact**: Low (already working!)
**Mitigation**:
- Document Tigerbrew installation
- Test on actual hardware
- Provide Python version checks

---

## Future Enhancements

### Version 2.0
- **Collaborative editing** (multiple users)
- **Version history** (story revisions)
- **Templates library** (pre-made story structures)
- **Image management** (upload, organize)
- **Story analytics** (which paths players take)

### Version 3.0
- **Cloud sync** (Dropbox, iCloud, Google Drive)
- **Mobile app** (iOS, Android)
- **AI assistance** (story suggestions, grammar check)
- **Social features** (share stories, community)

---

## Conclusion

This hybrid architecture provides:
- ✅ **100% backward compatibility** with CLI
- ✅ **Enhanced UX** with optional web editor
- ✅ **FastAPI** as requested by user
- ✅ **Lightweight and performant** for Tiger iMac
- ✅ **Gradual adoption** (start with CLI, add webapp later)
- ✅ **Flexible deployment** (modern computer as server)

The user gets the best of both worlds:
1. Reliable CLI tool that always works
2. Modern web editor when available
3. Same story format throughout
4. Professional development practices for child to learn

---

**Document Version**: 1.0
**Created**: 2025-11-22
**Author**: AI Agent (Copilot)
**Based On**: User's successful Python 3.10 installation on Tiger
**Target**: Hybrid CLI + Web Editor architecture
**Implementation**: ~2 weeks (9-13 days)
**Confidence**: Very High ✅
