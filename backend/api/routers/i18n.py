"""
Internationalization (i18n) router - language and translation endpoints.
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException

from backend.core.i18n import get_available_languages, TRANSLATIONS

router = APIRouter()

@router.get("/languages")
async def get_languages():
    """Get list of available languages with metadata."""
    languages = get_available_languages()
    return {"languages": languages}

@router.get("/translations/{lang}")
async def get_translations(lang: str):
    """Get translations for a specific language (web UI keys only)."""
    if lang not in TRANSLATIONS:
        raise HTTPException(status_code=404, detail=f"Language not found: {lang}")
    
    translations = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    web_translations = {k: v for k, v in translations.items() if k.startswith('web_')}
    
    return {"language": lang, "translations": web_translations}
