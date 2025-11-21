"""
Internationalization (i18n) module for pick-a-page.

Provides translations for English, Dutch, and Italian.
Uses simple dictionary-based approach with Python stdlib only.
"""

import os
from typing import Dict

# Current language (defaults to English)
_current_language = 'en'

# Translation strings organized by language
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'en': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Create interactive story books',
        'cli_command_help': 'Command to run',
        
        # Commands
        'cmd_compile': 'compile',
        'cmd_compile_help': 'Compile a story to HTML',
        'cmd_validate': 'validate',
        'cmd_validate_help': 'Validate a story file',
        'cmd_init': 'init',
        'cmd_init_help': 'Initialize a new story',
        
        # Arguments
        'arg_input_help': 'Input story file',
        'arg_output_help': 'Output directory (default: output/)',
        'arg_no_zip_help': 'Do not create ZIP file',
        'arg_name_help': 'Story name',
        'arg_directory_help': 'Output directory',
        'arg_lang_help': 'Language (en, nl, it)',
        
        # Messages - compile command
        'msg_file_not_found': 'File not found',
        'msg_reading_story': 'Reading story from {path}...',
        'msg_parsing_story': 'Parsing story...',
        'msg_parse_error': 'Parse error',
        'msg_validating_story': 'Validating story...',
        'msg_validation_errors': 'Validation errors found',
        'msg_generating_html': 'Generating HTML...',
        'msg_created': 'Created',
        'msg_creating_zip': 'Creating ZIP archive: {path}',
        'msg_compile_success': '✓ Story compiled successfully!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Parse error',
        'msg_validation_error_count': '✗ Found {count} validation error(s)',
        'msg_story_valid': '✓ Story is valid!',
        'msg_title': 'Title',
        'msg_author': 'Author',
        'msg_sections': 'Sections',
        
        # Messages - init command
        'msg_directory_exists': 'Directory already exists',
        'msg_project_created': '✓ Created new story project: {directory}',
        'msg_story_file': 'Story file',
        'msg_images_directory': 'Images directory',
        'msg_next_steps': 'Next steps',
        'msg_step_edit': 'Edit {file}',
        'msg_step_add_images': 'Add images to {directory}/',
        'msg_step_compile': 'Run: python -m pick_a_page compile {file}',
        
        # Story template
        'template_welcome': 'Welcome to your new story!',
        'template_beginning': 'This is the beginning. What happens next is up to you.',
        'template_continue': 'Continue',
        'template_body': 'Write your story here. Use **bold** and *italic* for emphasis.',
        'template_add_images': 'Add images with: ![Description](images/your-image.jpg)',
        'template_choices': 'Create choices by writing: [[Choice text]]',
        'template_end': 'The end.',
        'template_author': 'Your Name',
        
        # Errors
        'error_generic': 'Error',
    },
    'nl': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Maak interactieve verhalenboeken',
        'cli_command_help': 'Commando om uit te voeren',
        
        # Commands
        'cmd_compile': 'compileren',
        'cmd_compile_help': 'Compileer een verhaal naar HTML',
        'cmd_validate': 'valideren',
        'cmd_validate_help': 'Valideer een verhaalbestand',
        'cmd_init': 'initialiseren',
        'cmd_init_help': 'Initialiseer een nieuw verhaal',
        
        # Arguments
        'arg_input_help': 'Invoer verhaalbestand',
        'arg_output_help': 'Uitvoermap (standaard: output/)',
        'arg_no_zip_help': 'Geen ZIP-bestand maken',
        'arg_name_help': 'Verhaalnaam',
        'arg_directory_help': 'Uitvoermap',
        'arg_lang_help': 'Taal (en, nl, it)',
        
        # Messages - compile command
        'msg_file_not_found': 'Bestand niet gevonden',
        'msg_reading_story': 'Verhaal lezen van {path}...',
        'msg_parsing_story': 'Verhaal analyseren...',
        'msg_parse_error': 'Analysefout',
        'msg_validating_story': 'Verhaal valideren...',
        'msg_validation_errors': 'Validatiefouten gevonden',
        'msg_generating_html': 'HTML genereren...',
        'msg_created': 'Gemaakt',
        'msg_creating_zip': 'ZIP-archief maken: {path}',
        'msg_compile_success': '✓ Verhaal succesvol gecompileerd!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Analysefout',
        'msg_validation_error_count': '✗ {count} validatiefout(en) gevonden',
        'msg_story_valid': '✓ Verhaal is geldig!',
        'msg_title': 'Titel',
        'msg_author': 'Auteur',
        'msg_sections': 'Secties',
        
        # Messages - init command
        'msg_directory_exists': 'Map bestaat al',
        'msg_project_created': '✓ Nieuw verhaalproject gemaakt: {directory}',
        'msg_story_file': 'Verhaalbestand',
        'msg_images_directory': 'Afbeeldingenmap',
        'msg_next_steps': 'Volgende stappen',
        'msg_step_edit': 'Bewerk {file}',
        'msg_step_add_images': 'Voeg afbeeldingen toe aan {directory}/',
        'msg_step_compile': 'Uitvoeren: python -m pick_a_page compileren {file}',
        
        # Story template
        'template_welcome': 'Welkom bij je nieuwe verhaal!',
        'template_beginning': 'Dit is het begin. Wat er hierna gebeurt, bepaal jij.',
        'template_continue': 'Doorgaan',
        'template_body': 'Schrijf hier je verhaal. Gebruik **vet** en *cursief* voor nadruk.',
        'template_add_images': 'Voeg afbeeldingen toe met: ![Beschrijving](images/jouw-afbeelding.jpg)',
        'template_choices': 'Maak keuzes door te schrijven: [[Keuzestekst]]',
        'template_end': 'Het einde.',
        'template_author': 'Jouw Naam',
        
        # Errors
        'error_generic': 'Fout',
    },
    'it': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Crea libri di storie interattive',
        'cli_command_help': 'Comando da eseguire',
        
        # Commands
        'cmd_compile': 'compila',
        'cmd_compile_help': 'Compila una storia in HTML',
        'cmd_validate': 'valida',
        'cmd_validate_help': 'Valida un file storia',
        'cmd_init': 'inizializza',
        'cmd_init_help': 'Inizializza una nuova storia',
        
        # Arguments
        'arg_input_help': 'File storia di input',
        'arg_output_help': 'Directory di output (predefinita: output/)',
        'arg_no_zip_help': 'Non creare file ZIP',
        'arg_name_help': 'Nome della storia',
        'arg_directory_help': 'Directory di output',
        'arg_lang_help': 'Lingua (en, nl, it)',
        
        # Messages - compile command
        'msg_file_not_found': 'File non trovato',
        'msg_reading_story': 'Lettura storia da {path}...',
        'msg_parsing_story': 'Analisi storia in corso...',
        'msg_parse_error': 'Errore di analisi',
        'msg_validating_story': 'Validazione storia in corso...',
        'msg_validation_errors': 'Errori di validazione trovati',
        'msg_generating_html': 'Generazione HTML in corso...',
        'msg_created': 'Creato',
        'msg_creating_zip': 'Creazione archivio ZIP: {path}',
        'msg_compile_success': '✓ Storia compilata con successo!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Errore di analisi',
        'msg_validation_error_count': '✗ Trovati {count} errori di validazione',
        'msg_story_valid': '✓ La storia è valida!',
        'msg_title': 'Titolo',
        'msg_author': 'Autore',
        'msg_sections': 'Sezioni',
        
        # Messages - init command
        'msg_directory_exists': 'La directory esiste già',
        'msg_project_created': '✓ Nuovo progetto storia creato: {directory}',
        'msg_story_file': 'File storia',
        'msg_images_directory': 'Directory immagini',
        'msg_next_steps': 'Prossimi passi',
        'msg_step_edit': 'Modifica {file}',
        'msg_step_add_images': 'Aggiungi immagini a {directory}/',
        'msg_step_compile': 'Esegui: python -m pick_a_page compila {file}',
        
        # Story template
        'template_welcome': 'Benvenuto nella tua nuova storia!',
        'template_beginning': "Questo è l'inizio. Cosa succede dopo dipende da te.",
        'template_continue': 'Continua',
        'template_body': 'Scrivi qui la tua storia. Usa **grassetto** e *corsivo* per enfatizzare.',
        'template_add_images': 'Aggiungi immagini con: ![Descrizione](images/tua-immagine.jpg)',
        'template_choices': 'Crea scelte scrivendo: [[Testo scelta]]',
        'template_end': 'La fine.',
        'template_author': 'Il Tuo Nome',
        
        # Errors
        'error_generic': 'Errore',
    }
}


def set_language(lang: str) -> None:
    """
    Set the current language for translations.
    
    Args:
        lang: Language code ('en', 'nl', or 'it')
    """
    global _current_language
    
    if lang not in TRANSLATIONS:
        # Fall back to English if unsupported language
        lang = 'en'
    
    _current_language = lang


def get_language() -> str:
    """
    Get the current language code.
    
    Returns:
        Current language code ('en', 'nl', or 'it')
    """
    return _current_language


def _(key: str, **kwargs) -> str:
    """
    Get translated string for the given key.
    
    Args:
        key: Translation key
        **kwargs: Optional formatting arguments
        
    Returns:
        Translated and formatted string
    """
    # Get translation for current language, fall back to English
    translations = TRANSLATIONS.get(_current_language, TRANSLATIONS['en'])
    text = translations.get(key, key)
    
    # Format with any provided arguments
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            # If formatting fails, return unformatted text
            pass
    
    return text


def init_language_from_env() -> None:
    """
    Initialize language from environment variable PICK_A_PAGE_LANG.
    
    Checks for PICK_A_PAGE_LANG environment variable and sets the language
    if it's a supported language code.
    """
    lang = os.environ.get('PICK_A_PAGE_LANG', 'en')
    set_language(lang)
