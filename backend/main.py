"""Main FastAPI application for Pick-a-Page.

Serves Jinja2 templates with modular CSS/JS, reusing existing core modules.
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routers import stories, compile_router, i18n, pages, template

app = FastAPI(
    title="Pick-a-Page Story Tool",
    description="Create interactive Choose Your Own Adventure stories",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'"
    return response

# Mount static files
backend_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(backend_dir / "static")), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(backend_dir / "templates"))

# Include routers
app.include_router(pages.router)
app.include_router(stories.router, prefix="/api", tags=["stories"])
app.include_router(compile_router.router, prefix="/api", tags=["compile"])
app.include_router(i18n.router, prefix="/api", tags=["i18n"])
app.include_router(template.router, tags=["templates"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000, 
        reload=True,
        log_level="info"
    )
