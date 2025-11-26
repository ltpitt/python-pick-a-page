"""
Page rendering router - serves Jinja2 templates.
"""

from flask import Blueprint, render_template

bp = Blueprint('pages', __name__)


@bp.route("/")
def index():
    """Render main page (shows all three tabs)."""
    return render_template("index.html")
