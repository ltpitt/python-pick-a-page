"""
Tests for the i18n (internationalization) module.
"""

import os
import pytest
from pick_a_page.i18n import (
    set_language,
    get_language,
    _,
    init_language_from_env,
    TRANSLATIONS
)


@pytest.fixture(autouse=True)
def reset_language():
    """Automatically reset language to English after each test."""
    yield
    set_language('en')


class TestLanguageSelection:
    """Tests for language selection functionality."""
    
    def test_default_language_is_english(self):
        """By default, language should be English."""
        set_language('en')
        assert get_language() == 'en'
    
    def test_set_language_to_dutch(self):
        """Should be able to set language to Dutch."""
        set_language('nl')
        assert get_language() == 'nl'
    
    def test_set_language_to_italian(self):
        """Should be able to set language to Italian."""
        set_language('it')
        assert get_language() == 'it'
    
    def test_unsupported_language_falls_back_to_english(self):
        """Unsupported language codes should fall back to English."""
        set_language('xx')  # 'xx' is not a supported language
        assert get_language() == 'en'


class TestTranslationRetrieval:
    """Tests for retrieving translations."""
    
    def test_get_english_translation(self):
        """Should retrieve English translation."""
        set_language('en')
        assert _('cli_description') == 'Pick-a-Page: Create interactive story books'
    
    def test_get_dutch_translation(self):
        """Should retrieve Dutch translation."""
        set_language('nl')
        assert _('cli_description') == 'Pick-a-Page: Maak interactieve verhalenboeken'
    
    def test_get_italian_translation(self):
        """Should retrieve Italian translation."""
        set_language('it')
        assert _('cli_description') == 'Pick-a-Page: Crea libri di storie interattive'
    
    def test_missing_key_returns_key(self):
        """Missing translation key should return the key itself."""
        set_language('en')
        assert _('nonexistent_key') == 'nonexistent_key'
    
    def test_translation_with_formatting(self):
        """Should format translations with parameters."""
        set_language('en')
        result = _('msg_reading_story', path='/path/to/file.txt')
        assert 'Reading story from /path/to/file.txt' in result


class TestTranslationFormatting:
    """Tests for translation string formatting."""
    
    def test_format_with_single_parameter(self):
        """Should format string with single parameter."""
        set_language('en')
        result = _('msg_created')
        assert result == 'Created'
    
    def test_format_with_path_parameter(self):
        """Should format path-containing messages."""
        set_language('nl')
        result = _('msg_reading_story', path='verhaal.txt')
        assert 'verhaal.txt' in result
    
    def test_format_with_count_parameter(self):
        """Should format count-containing messages."""
        set_language('en')
        result = _('msg_validation_error_count', count=3)
        assert '3' in result


class TestEnvironmentVariableInit:
    """Tests for environment variable initialization."""
    
    def test_init_from_env_with_dutch(self, monkeypatch):
        """Should initialize language from environment variable."""
        monkeypatch.setenv('PICK_A_PAGE_LANG', 'nl')
        init_language_from_env()
        assert get_language() == 'nl'
    
    def test_init_from_env_with_italian(self, monkeypatch):
        """Should initialize language from environment variable."""
        monkeypatch.setenv('PICK_A_PAGE_LANG', 'it')
        init_language_from_env()
        assert get_language() == 'it'
    
    def test_init_from_env_default_to_english(self, monkeypatch):
        """Should default to English if env var not set."""
        monkeypatch.delenv('PICK_A_PAGE_LANG', raising=False)
        init_language_from_env()
        assert get_language() == 'en'


class TestTranslationCompleteness:
    """Tests to ensure all languages have the same keys."""
    
    def test_all_languages_have_same_keys(self):
        """All language translations should have the same keys."""
        en_keys = set(TRANSLATIONS['en'].keys())
        nl_keys = set(TRANSLATIONS['nl'].keys())
        it_keys = set(TRANSLATIONS['it'].keys())
        
        assert en_keys == nl_keys, f"Dutch missing keys: {en_keys - nl_keys}, Extra: {nl_keys - en_keys}"
        assert en_keys == it_keys, f"Italian missing keys: {en_keys - it_keys}, Extra: {it_keys - en_keys}"
    
    def test_no_empty_translations(self):
        """No translation value should be empty."""
        for lang, translations in TRANSLATIONS.items():
            for key, value in translations.items():
                assert value.strip(), f"Empty translation for '{key}' in language '{lang}'"


class TestCommandTranslations:
    """Tests for command-specific translations."""
    
    def test_compile_command_messages_exist(self):
        """Compile command messages should exist in all languages."""
        for lang in ['en', 'nl', 'it']:
            set_language(lang)
            assert _('msg_reading_story') is not None
            assert _('msg_parsing_story') is not None
            assert _('msg_validating_story') is not None
            assert _('msg_generating_html') is not None
    
    def test_validate_command_messages_exist(self):
        """Validate command messages should exist in all languages."""
        for lang in ['en', 'nl', 'it']:
            set_language(lang)
            assert _('msg_story_valid') is not None
            assert _('msg_validate_parse_error') is not None
    
    def test_init_command_messages_exist(self):
        """Init command messages should exist in all languages."""
        for lang in ['en', 'nl', 'it']:
            set_language(lang)
            assert _('msg_project_created') is not None
            assert _('msg_next_steps') is not None
            assert _('template_welcome') is not None
