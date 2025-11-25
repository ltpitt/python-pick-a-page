"""
Page rendering router - serves Jinja2 templates.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

backend_dir = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=str(backend_dir / "templates"))

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render main page (shows all three tabs)."""
    return templates.TemplateResponse(request, "index.html")
