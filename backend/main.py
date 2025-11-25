"""Main Flask application for Pick-a-Page.

Serves Jinja2 templates with modular CSS/JS, reusing existing core modules.
"""

from pathlib import Path
from flask import Flask, jsonify

# Create Flask app
backend_dir = Path(__file__).parent
app = Flask(
    __name__,
    static_folder=str(backend_dir / "static"),
    static_url_path="/static",
    template_folder=str(backend_dir / "templates")
)

# Configure app
app.config['JSON_SORT_KEYS'] = False

# Import and register blueprints
from backend.api.routers import stories, compile_router, i18n, pages, template

app.register_blueprint(pages.bp)
app.register_blueprint(stories.bp, url_prefix="/api")
app.register_blueprint(compile_router.bp, url_prefix="/api")
app.register_blueprint(compile_router.play_bp)  # Serve compiled stories without /api prefix
app.register_blueprint(i18n.bp, url_prefix="/api")
app.register_blueprint(template.bp, url_prefix="/api")


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"  # Allow iframes from same origin
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'"
    return response


@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "version": "2.0.0"})


if __name__ == "__main__":
    # Development server only - use gunicorn for production:
    # gunicorn backend.main:app --bind 0.0.0.0:8001 --workers 4
    app.run(
        host="127.0.0.1",  # Only bind to localhost for development
        port=8001,
        debug=True  # nosec B201 - debug mode only for local development
    )
