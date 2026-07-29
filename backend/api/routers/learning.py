"""
Learning router - guided tutorial and child-friendly Markdown reference.

Exposes the content from :mod:`backend.core.learning` over HTTP so the web UI
(and any other client) can render an optional tutorial and an always-available
Markdown cheatsheet.
"""

from flask import Blueprint, jsonify, request

from backend.core.i18n import LANGUAGE_INFO
from backend.core.learning import (
    DEFAULT_LANGUAGE,
    get_markdown_help,
    get_tutorial,
    get_ui_labels,
)

bp = Blueprint('learning', __name__)


def _resolve_language() -> str:
    """Resolve the requested language, falling back to English."""
    lang = request.args.get('lang', DEFAULT_LANGUAGE)
    return lang if lang in LANGUAGE_INFO else DEFAULT_LANGUAGE


@bp.route("/tutorial")
def tutorial():
    """Return the guided tutorial steps for the requested language."""
    lang = _resolve_language()
    labels = get_ui_labels(lang)
    return jsonify({
        "language": lang,
        "heading": labels["tutorial_heading"],
        "cta": labels["tutorial_cta"],
        "done": labels["tutorial_done"],
        "steps": get_tutorial(lang),
    })


@bp.route("/help/markdown")
def markdown_help():
    """Return the child-friendly Markdown reference for the requested language."""
    lang = _resolve_language()
    labels = get_ui_labels(lang)
    return jsonify({
        "language": lang,
        "summary": labels["help_summary"],
        "items": get_markdown_help(lang),
    })
