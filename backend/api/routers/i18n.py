"""
Internationalization (i18n) router - language and translation endpoints.
"""

from flask import Blueprint, jsonify, abort

from backend.core.i18n import get_available_languages, TRANSLATIONS

bp = Blueprint('i18n', __name__)


@bp.route("/languages")
def get_languages():
    """Get list of available languages with metadata."""
    languages = get_available_languages()
    return jsonify({"languages": languages})


@bp.route("/translations/<lang>")
def get_translations(lang: str):
    """Get translations for a specific language (web UI keys only)."""
    if lang not in TRANSLATIONS:
        abort(404, description=f"Language not found: {lang}")
    
    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    web_translations = {k: v for k, v in translations.items() if k.startswith('web_')}
    
    return jsonify({"language": lang, "translations": web_translations})
