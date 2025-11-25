# Backend - FastAPI + Jinja2 Production Application

Production-ready web application for Pick-a-Page story tool, built with FastAPI and Jinja2.

## ⚠️ CRITICAL: Always Use Virtual Environment

**NEVER install dependencies globally. ALWAYS use the virtual environment:**

```bash
# Navigate to project root
cd /Users/xt41vb/Desktop/DevData/gitclones/python-pick-a-page

# Activate virtual environment (REQUIRED for all operations)
source .venv/bin/activate

# Verify you're in venv (should show .venv path)
which python
```

## Installation

```bash
# 1. Activate virtual environment (REQUIRED)
source .venv/bin/activate

# 2. Install backend dependencies
pip install -r backend/requirements.txt

# 3. Verify installation
python -c "import fastapi; print(fastapi.__version__)"
```

## Running the Server

```bash
# ALWAYS activate venv first
source .venv/bin/activate

# Development mode (auto-reload on file changes)
python -m backend.main

# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

The server will start on **http://localhost:8001** (POC runs on 8000).

## API Endpoints

### Pages
- `GET /` - Main web interface (3-tab SPA)
- `GET /health` - Health check

### Stories
- `GET /api/stories` - List all stories with metadata
- `GET /api/story/{filename}` - Get raw story content
- `POST /api/save` - Save story file
- `POST /api/delete` - Delete story file

### Compilation
- `POST /api/compile` - Compile story to HTML
- `POST /api/validate` - Validate story structure
- `GET /play/{story_name}` - Serve compiled story

### Internationalization
- `GET /api/languages` - List available languages (15 total)
- `GET /api/translations/{lang}` - Get translations for language

## Testing

```bash
# ALWAYS activate venv first
source .venv/bin/activate

# Run backend tests
pytest tests/backend/ -v

# With coverage
pytest tests/backend/ --cov=backend --cov-report=html
```

## Development Workflow

```bash
# 1. Start POC server (for comparison)
source .venv/bin/activate
python -m pick_a_page serve --port 8000  # Terminal 1

# 2. Start new backend server
source .venv/bin/activate
python -m backend.main                    # Terminal 2 (port 8001)

# 3. Compare functionality side-by-side
open http://localhost:8000  # POC
open http://localhost:8001  # New backend
```

## Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── api/
│   └── routers/
│       ├── stories.py      # Story CRUD operations
│       ├── compile_router.py # Story compilation
│       ├── i18n.py         # Internationalization
│       └── pages.py        # Page rendering
├── services/               # Business logic (pending)
├── templates/              # Jinja2 HTML (pending)
└── static/
    ├── css/                # Modular CSS (pending)
    └── js/                 # Modular JavaScript (pending)
```

## Dependencies

All dependencies install in virtual environment only:
- **FastAPI** - Modern async web framework
- **Uvicorn** - ASGI server with auto-reload
- **Jinja2** - Template engine (like Thymeleaf)
- **Pydantic** - Request/response validation
- **pytest-asyncio** - Async test support
- **httpx** - TestClient for API testing

## Security Features

- CORS middleware (configured for development)
- Security headers (X-Content-Type-Options, X-Frame-Options, CSP)
- Path traversal prevention (`is_safe_path` validation)
- Filename sanitization (regex-based)

## Migration Status

✅ **Completed:**
- Directory structure
- FastAPI app setup (main.py)
- API routers (stories, compile, i18n, pages)
- Dependencies installed in venv

⏳ **Pending:**
- Jinja2 templates (base.html, library.html, editor.html, player.html)
- Modular CSS (8 files: variables, base, book, bookmarks, library, editor, messages, mobile)
- Modular JavaScript (5 files: app, library, editor, i18n, utils)
- Test migration (port 160 tests to FastAPI TestClient)

## Troubleshooting

### Import Errors
```bash
# Solution: Activate venv
source .venv/bin/activate
```

### Port Already in Use
```bash
# Check what's running on port 8001
lsof -i :8001

# Kill process if needed
kill -9 <PID>
```

### Module Not Found
```bash
# Reinstall dependencies IN VENV
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Key Differences from POC

| Feature | POC (server.py) | Backend (FastAPI) |
|---------|----------------|-------------------|
| Framework | stdlib http.server | FastAPI + Uvicorn |
| Templates | 2000-line string | Modular Jinja2 files |
| CSS | Embedded (~400 lines) | 8 modular files |
| JavaScript | Embedded (~600 lines) | 5 ES6 modules |
| Port | 8000 | 8001 |
| Auto-reload | Manual restart | --reload flag |
| API docs | None | Automatic OpenAPI |
| Testing | Basic | FastAPI TestClient |

## Next Steps

1. ✅ ~~Install dependencies in venv~~
2. Create Jinja2 templates
3. Extract CSS to modular files
4. Extract JavaScript to ES6 modules
5. Port tests to FastAPI TestClient
6. Side-by-side functionality testing
7. Performance comparison
8. Production deployment plan
