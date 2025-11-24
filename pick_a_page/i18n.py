"""
Internationalization (i18n) module for pick-a-page.

Provides translations for English, Dutch, Italian, Spanish, French, Portuguese,
German, Russian, Mandarin Chinese, Hindi, Arabic, Bengali, Urdu, Indonesian, and Bulgarian.
Uses simple dictionary-based approach with Python stdlib only.
"""

import os
from typing import Dict

# Current language (defaults to English)
_current_language = 'en'

# Language metadata with native names and flags
LANGUAGE_INFO: Dict[str, Dict[str, str]] = {
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'nl': {'name': 'Nederlands', 'flag': '🇳🇱'},
    'it': {'name': 'Italiano', 'flag': '🇮🇹'},
    'es': {'name': 'Español', 'flag': '🇪🇸'},
    'fr': {'name': 'Français', 'flag': '🇫🇷'},
    'pt': {'name': 'Português', 'flag': '🇵🇹'},
    'de': {'name': 'Deutsch', 'flag': '🇩🇪'},
    'ru': {'name': 'Русский', 'flag': '🇷🇺'},
    'zh': {'name': '中文', 'flag': '🇨🇳'},
    'hi': {'name': 'हिन्दी', 'flag': '🇮🇳'},
    'ar': {'name': 'العربية', 'flag': '🇸🇦'},
    'bn': {'name': 'বাংলা', 'flag': '🇧🇩'},
    'ur': {'name': 'اردو', 'flag': '🇵🇰'},
    'id': {'name': 'Indonesia', 'flag': '🇮🇩'},
    'bg': {'name': 'Български', 'flag': '🇧🇬'},
}

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
        'arg_lang_help': 'Language',
        
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
        
        # Web UI - Navigation
        'web_tab_library': '📚 Story Library',
        'web_tab_editor': '✏️ Story Editor',
        'web_tab_reader': '📖 Story Reader',
        
        # Web UI - Titles
        'web_title_library': '📖 My Story Collection',
        'web_title_editor': '✨ Create Your Story',
        
        # Web UI - Buttons
        'web_btn_play': 'Play Story',
        'web_btn_edit': 'Edit Story',
        'web_btn_new': 'New Story',
        'web_btn_validate': 'Validate',
        'web_btn_save': 'Save',
        'web_btn_compile': 'Compile & Play',
        
        # Web UI - Messages
        'web_loading_stories': 'Loading your stories...',
        'web_empty_title': 'No stories yet',
        'web_empty_text': 'Click "New Story" to create your first adventure!',
        'web_by': 'by',
        'web_sections': 'sections',
        'web_editing': 'Editing',
        'web_msg_loading': 'Loading story...',
        'web_msg_errors': 'Errors',
        'web_msg_error': 'Error',
        'web_msg_loaded': 'Loaded',
        'web_msg_ready': 'Ready to write a new story!',
        'web_msg_empty': 'Editor is empty!',
        'web_msg_valid': 'Story is valid! Found',
        'web_msg_validation_errors': 'Validation errors',
        'web_msg_saved': 'Saved as',
        'web_msg_unknown_error': 'Unknown error',
        'web_msg_compiling': 'Compiling story...',
        'web_msg_compilation_errors': 'Compilation errors',
        
        # Web UI - Prompts
        'web_prompt_save': 'Save as:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'My New Adventure',
        'web_new_story_author': 'Your Name',
        'web_new_story_content': 'Write your story here...',
        'web_new_story_choice': 'Make a choice',
        'web_new_story_continue': 'Continue your adventure!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Write your adventure here...\n\nExample format:\n\n---\ntitle: My Adventure\nauthor: Your Name\n---\n\n[[beginning]]\n\nYou wake up in a mysterious place...\n\n[[Explore]]\n[[Go back to sleep]]\n\n---\n\n[[Explore]]\n\nYou discover something amazing!',
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
        'arg_lang_help': 'Taal',
        
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
        
        # Web UI - Navigation
        'web_tab_library': '📚 Verhalenbibliotheek',
        'web_tab_editor': '✏️ Verhalen Editor',
        'web_tab_reader': '📖 Verhaal Lezer',
        
        # Web UI - Titles
        'web_title_library': '📖 Mijn Verhalencollectie',
        'web_title_editor': '✨ Maak Je Verhaal',
        
        # Web UI - Buttons
        'web_btn_play': 'Verhaal Spelen',
        'web_btn_edit': 'Verhaal Bewerken',
        'web_btn_new': 'Nieuw Verhaal',
        'web_btn_validate': 'Valideren',
        'web_btn_save': 'Opslaan',
        'web_btn_compile': 'Compileren & Spelen',
        
        # Web UI - Messages
        'web_loading_stories': 'Je verhalen laden...',
        'web_empty_title': 'Nog geen verhalen',
        'web_empty_text': 'Klik op "Nieuw Verhaal" om je eerste avontuur te maken!',
        'web_by': 'door',
        'web_sections': 'secties',
        'web_editing': 'Bewerken',
        'web_msg_loading': 'Verhaal laden...',
        'web_msg_errors': 'Fouten',
        'web_msg_error': 'Fout',
        'web_msg_loaded': 'Geladen',
        'web_msg_ready': 'Klaar om een nieuw verhaal te schrijven!',
        'web_msg_empty': 'Editor is leeg!',
        'web_msg_valid': 'Verhaal is geldig! Gevonden',
        'web_msg_validation_errors': 'Validatiefouten',
        'web_msg_saved': 'Opgeslagen als',
        'web_msg_unknown_error': 'Onbekende fout',
        'web_msg_compiling': 'Verhaal compileren...',
        'web_msg_compilation_errors': 'Compilatiefouten',
        
        # Web UI - Prompts
        'web_prompt_save': 'Opslaan als:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Mijn Nieuwe Avontuur',
        'web_new_story_author': 'Jouw Naam',
        'web_new_story_content': 'Schrijf hier je verhaal...',
        'web_new_story_choice': 'Maak een keuze',
        'web_new_story_continue': 'Ga verder met je avontuur!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Schrijf hier je avontuur...\n\nVoorbeeld formaat:\n\n---\ntitle: Mijn Avontuur\nauthor: Jouw Naam\n---\n\n[[beginning]]\n\nJe wordt wakker op een mysterieuze plek...\n\n[[Verkennen]]\n[[Ga terug slapen]]\n\n---\n\n[[Verkennen]]\n\nJe ontdekt iets verbazingwekkends!',
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
        'arg_lang_help': 'Lingua',
        
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
        
        # Web UI - Navigation
        'web_tab_library': '📚 Biblioteca Storie',
        'web_tab_editor': '✏️ Editor Storie',
        'web_tab_reader': '📖 Lettore Storie',
        
        # Web UI - Titles
        'web_title_library': '📖 La Mia Collezione di Storie',
        'web_title_editor': '✨ Crea La Tua Storia',
        
        # Web UI - Buttons
        'web_btn_play': 'Gioca Storia',
        'web_btn_edit': 'Modifica Storia',
        'web_btn_new': 'Nuova Storia',
        'web_btn_validate': 'Valida',
        'web_btn_save': 'Salva',
        'web_btn_compile': 'Compila & Gioca',
        
        # Web UI - Messages
        'web_loading_stories': 'Caricamento delle tue storie...',
        'web_empty_title': 'Ancora nessuna storia',
        'web_empty_text': 'Clicca su "Nuova Storia" per creare la tua prima avventura!',
        'web_by': 'di',
        'web_sections': 'sezioni',
        'web_editing': 'Modifica',
        'web_msg_loading': 'Caricamento storia...',
        'web_msg_errors': 'Errori',
        'web_msg_error': 'Errore',
        'web_msg_loaded': 'Caricato',
        'web_msg_ready': 'Pronto per scrivere una nuova storia!',
        'web_msg_empty': 'Editor vuoto!',
        'web_msg_valid': 'Storia valida! Trovate',
        'web_msg_validation_errors': 'Errori di validazione',
        'web_msg_saved': 'Salvato come',
        'web_msg_unknown_error': 'Errore sconosciuto',
        'web_msg_compiling': 'Compilazione storia...',
        'web_msg_compilation_errors': 'Errori di compilazione',
        
        # Web UI - Prompts
        'web_prompt_save': 'Salva come:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'La Mia Nuova Avventura',
        'web_new_story_author': 'Il Tuo Nome',
        'web_new_story_content': 'Scrivi qui la tua storia...',
        'web_new_story_choice': 'Fai una scelta',
        'web_new_story_continue': 'Continua la tua avventura!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Scrivi qui la tua avventura...\n\nFormato esempio:\n\n---\ntitle: La Mia Avventura\nauthor: Il Tuo Nome\n---\n\n[[beginning]]\n\nTi svegli in un luogo misterioso...\n\n[[Esplora]]\n[[Torna a dormire]]\n\n---\n\n[[Esplora]]\n\nScopri qualcosa di incredibile!',
    },
    'es': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Crea libros de historias interactivas',
        'cli_command_help': 'Comando a ejecutar',
        
        # Commands
        'cmd_compile': 'compilar',
        'cmd_compile_help': 'Compilar una historia a HTML',
        'cmd_validate': 'validar',
        'cmd_validate_help': 'Validar un archivo de historia',
        'cmd_init': 'inicializar',
        'cmd_init_help': 'Inicializar una nueva historia',
        
        # Arguments
        'arg_input_help': 'Archivo de historia de entrada',
        'arg_output_help': 'Directorio de salida (predeterminado: output/)',
        'arg_no_zip_help': 'No crear archivo ZIP',
        'arg_name_help': 'Nombre de la historia',
        'arg_directory_help': 'Directorio de salida',
        'arg_lang_help': 'Idioma',
        
        # Messages - compile command
        'msg_file_not_found': 'Archivo no encontrado',
        'msg_reading_story': 'Leyendo historia desde {path}...',
        'msg_parsing_story': 'Analizando historia...',
        'msg_parse_error': 'Error de análisis',
        'msg_validating_story': 'Validando historia...',
        'msg_validation_errors': 'Errores de validación encontrados',
        'msg_generating_html': 'Generando HTML...',
        'msg_created': 'Creado',
        'msg_creating_zip': 'Creando archivo ZIP: {path}',
        'msg_compile_success': '✓ ¡Historia compilada exitosamente!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Error de análisis',
        'msg_validation_error_count': '✗ Se encontraron {count} error(es) de validación',
        'msg_story_valid': '✓ ¡La historia es válida!',
        'msg_title': 'Título',
        'msg_author': 'Autor',
        'msg_sections': 'Secciones',
        
        # Messages - init command
        'msg_directory_exists': 'El directorio ya existe',
        'msg_project_created': '✓ Nuevo proyecto de historia creado: {directory}',
        'msg_story_file': 'Archivo de historia',
        'msg_images_directory': 'Directorio de imágenes',
        'msg_next_steps': 'Próximos pasos',
        'msg_step_edit': 'Editar {file}',
        'msg_step_add_images': 'Agregar imágenes a {directory}/',
        'msg_step_compile': 'Ejecutar: python -m pick_a_page compilar {file}',
        
        # Story template
        'template_welcome': '¡Bienvenido a tu nueva historia!',
        'template_beginning': 'Este es el comienzo. Lo que sucede después depende de ti.',
        'template_continue': 'Continuar',
        'template_body': 'Escribe tu historia aquí. Usa **negrita** y *cursiva* para énfasis.',
        'template_add_images': 'Agrega imágenes con: ![Descripción](images/tu-imagen.jpg)',
        'template_choices': 'Crea opciones escribiendo: [[Texto de opción]]',
        'template_end': 'El fin.',
        'template_author': 'Tu Nombre',
        
        # Errors
        'error_generic': 'Error',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Biblioteca de Historias',
        'web_tab_editor': '✏️ Editor de Historias',
        'web_tab_reader': '📖 Lector de Historias',
        
        # Web UI - Titles
        'web_title_library': '📖 Mi Colección de Historias',
        'web_title_editor': '✨ Crea Tu Historia',
        
        # Web UI - Buttons
        'web_btn_play': 'Jugar Historia',
        'web_btn_edit': 'Editar Historia',
        'web_btn_new': 'Nueva Historia',
        'web_btn_validate': 'Validar',
        'web_btn_save': 'Guardar',
        'web_btn_compile': 'Compilar y Jugar',
        
        # Web UI - Messages
        'web_loading_stories': 'Cargando tus historias...',
        'web_empty_title': 'Aún no hay historias',
        'web_empty_text': '¡Haz clic en "Nueva Historia" para crear tu primera aventura!',
        'web_by': 'por',
        'web_sections': 'secciones',
        'web_editing': 'Editando',
        'web_msg_loading': 'Cargando historia...',
        'web_msg_errors': 'Errores',
        'web_msg_error': 'Error',
        'web_msg_loaded': 'Cargado',
        'web_msg_ready': '¡Listo para escribir una nueva historia!',
        'web_msg_empty': '¡El editor está vacío!',
        'web_msg_valid': '¡Historia válida! Encontradas',
        'web_msg_validation_errors': 'Errores de validación',
        'web_msg_saved': 'Guardado como',
        'web_msg_unknown_error': 'Error desconocido',
        'web_msg_compiling': 'Compilando historia...',
        'web_msg_compilation_errors': 'Errores de compilación',
        
        # Web UI - Prompts
        'web_prompt_save': 'Guardar como:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Mi Nueva Aventura',
        'web_new_story_author': 'Tu Nombre',
        'web_new_story_content': 'Escribe tu historia aquí...',
        'web_new_story_choice': 'Hacer una elección',
        'web_new_story_continue': '¡Continúa tu aventura!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Escribe tu aventura aquí...\n\nFormato de ejemplo:\n\n---\ntitle: Mi Aventura\nauthor: Tu Nombre\n---\n\n[[beginning]]\n\nDespertas en un lugar misterioso...\n\n[[Explorar]]\n[[Volver a dormir]]\n\n---\n\n[[Explorar]]\n\n¡Descubres algo increíble!',
    },
    'fr': {
        # CLI main description
        'cli_description': 'Pick-a-Page : Créez des livres d\'histoires interactives',
        'cli_command_help': 'Commande à exécuter',
        
        # Commands
        'cmd_compile': 'compiler',
        'cmd_compile_help': 'Compiler une histoire en HTML',
        'cmd_validate': 'valider',
        'cmd_validate_help': 'Valider un fichier d\'histoire',
        'cmd_init': 'initialiser',
        'cmd_init_help': 'Initialiser une nouvelle histoire',
        
        # Arguments
        'arg_input_help': 'Fichier d\'histoire d\'entrée',
        'arg_output_help': 'Répertoire de sortie (par défaut : output/)',
        'arg_no_zip_help': 'Ne pas créer de fichier ZIP',
        'arg_name_help': 'Nom de l\'histoire',
        'arg_directory_help': 'Répertoire de sortie',
        'arg_lang_help': 'Langue',
        
        # Messages - compile command
        'msg_file_not_found': 'Fichier non trouvé',
        'msg_reading_story': 'Lecture de l\'histoire depuis {path}...',
        'msg_parsing_story': 'Analyse de l\'histoire...',
        'msg_parse_error': 'Erreur d\'analyse',
        'msg_validating_story': 'Validation de l\'histoire...',
        'msg_validation_errors': 'Erreurs de validation trouvées',
        'msg_generating_html': 'Génération du HTML...',
        'msg_created': 'Créé',
        'msg_creating_zip': 'Création de l\'archive ZIP : {path}',
        'msg_compile_success': '✓ Histoire compilée avec succès !',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Erreur d\'analyse',
        'msg_validation_error_count': '✗ {count} erreur(s) de validation trouvée(s)',
        'msg_story_valid': '✓ L\'histoire est valide !',
        'msg_title': 'Titre',
        'msg_author': 'Auteur',
        'msg_sections': 'Sections',
        
        # Messages - init command
        'msg_directory_exists': 'Le répertoire existe déjà',
        'msg_project_created': '✓ Nouveau projet d\'histoire créé : {directory}',
        'msg_story_file': 'Fichier d\'histoire',
        'msg_images_directory': 'Répertoire d\'images',
        'msg_next_steps': 'Prochaines étapes',
        'msg_step_edit': 'Modifier {file}',
        'msg_step_add_images': 'Ajouter des images à {directory}/',
        'msg_step_compile': 'Exécuter : python -m pick_a_page compiler {file}',
        
        # Story template
        'template_welcome': 'Bienvenue dans votre nouvelle histoire !',
        'template_beginning': 'C\'est le début. Ce qui arrive ensuite dépend de vous.',
        'template_continue': 'Continuer',
        'template_body': 'Écrivez votre histoire ici. Utilisez **gras** et *italique* pour l\'emphase.',
        'template_add_images': 'Ajoutez des images avec : ![Description](images/votre-image.jpg)',
        'template_choices': 'Créez des choix en écrivant : [[Texte du choix]]',
        'template_end': 'La fin.',
        'template_author': 'Votre Nom',
        
        # Errors
        'error_generic': 'Erreur',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Bibliothèque d\'Histoires',
        'web_tab_editor': '✏️ Éditeur d\'Histoires',
        'web_tab_reader': '📖 Lecteur d\'Histoires',
        
        # Web UI - Titles
        'web_title_library': '📖 Ma Collection d\'Histoires',
        'web_title_editor': '✨ Créez Votre Histoire',
        
        # Web UI - Buttons
        'web_btn_play': 'Jouer l\'Histoire',
        'web_btn_edit': 'Modifier l\'Histoire',
        'web_btn_new': 'Nouvelle Histoire',
        'web_btn_validate': 'Valider',
        'web_btn_save': 'Enregistrer',
        'web_btn_compile': 'Compiler et Jouer',
        
        # Web UI - Messages
        'web_loading_stories': 'Chargement de vos histoires...',
        'web_empty_title': 'Pas encore d\'histoires',
        'web_empty_text': 'Cliquez sur "Nouvelle Histoire" pour créer votre première aventure !',
        'web_by': 'par',
        'web_sections': 'sections',
        'web_editing': 'Édition',
        'web_msg_loading': 'Chargement de l\'histoire...',
        'web_msg_errors': 'Erreurs',
        'web_msg_error': 'Erreur',
        'web_msg_loaded': 'Chargé',
        'web_msg_ready': 'Prêt à écrire une nouvelle histoire !',
        'web_msg_empty': 'L\'éditeur est vide !',
        'web_msg_valid': 'Histoire valide ! Trouvé',
        'web_msg_validation_errors': 'Erreurs de validation',
        'web_msg_saved': 'Enregistré sous',
        'web_msg_unknown_error': 'Erreur inconnue',
        'web_msg_compiling': 'Compilation de l\'histoire...',
        'web_msg_compilation_errors': 'Erreurs de compilation',
        
        # Web UI - Prompts
        'web_prompt_save': 'Enregistrer sous :',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Ma Nouvelle Aventure',
        'web_new_story_author': 'Votre Nom',
        'web_new_story_content': 'Écrivez votre histoire ici...',
        'web_new_story_choice': 'Faire un choix',
        'web_new_story_continue': 'Continuez votre aventure !',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Écrivez votre aventure ici...\n\nFormat d\'exemple :\n\n---\ntitle: Mon Aventure\nauthor: Votre Nom\n---\n\n[[beginning]]\n\nVous vous réveillez dans un endroit mystérieux...\n\n[[Explorer]]\n[[Retourner dormir]]\n\n---\n\n[[Explorer]]\n\nVous découvrez quelque chose d\'incroyable !',
    },
    'pt': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Crie livros de histórias interativas',
        'cli_command_help': 'Comando a executar',
        
        # Commands
        'cmd_compile': 'compilar',
        'cmd_compile_help': 'Compilar uma história para HTML',
        'cmd_validate': 'validar',
        'cmd_validate_help': 'Validar um arquivo de história',
        'cmd_init': 'inicializar',
        'cmd_init_help': 'Inicializar uma nova história',
        
        # Arguments
        'arg_input_help': 'Arquivo de história de entrada',
        'arg_output_help': 'Diretório de saída (padrão: output/)',
        'arg_no_zip_help': 'Não criar arquivo ZIP',
        'arg_name_help': 'Nome da história',
        'arg_directory_help': 'Diretório de saída',
        'arg_lang_help': 'Idioma',
        
        # Messages - compile command
        'msg_file_not_found': 'Arquivo não encontrado',
        'msg_reading_story': 'Lendo história de {path}...',
        'msg_parsing_story': 'Analisando história...',
        'msg_parse_error': 'Erro de análise',
        'msg_validating_story': 'Validando história...',
        'msg_validation_errors': 'Erros de validação encontrados',
        'msg_generating_html': 'Gerando HTML...',
        'msg_created': 'Criado',
        'msg_creating_zip': 'Criando arquivo ZIP: {path}',
        'msg_compile_success': '✓ História compilada com sucesso!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Erro de análise',
        'msg_validation_error_count': '✗ Encontrados {count} erro(s) de validação',
        'msg_story_valid': '✓ A história é válida!',
        'msg_title': 'Título',
        'msg_author': 'Autor',
        'msg_sections': 'Seções',
        
        # Messages - init command
        'msg_directory_exists': 'O diretório já existe',
        'msg_project_created': '✓ Novo projeto de história criado: {directory}',
        'msg_story_file': 'Arquivo de história',
        'msg_images_directory': 'Diretório de imagens',
        'msg_next_steps': 'Próximos passos',
        'msg_step_edit': 'Editar {file}',
        'msg_step_add_images': 'Adicionar imagens a {directory}/',
        'msg_step_compile': 'Executar: python -m pick_a_page compilar {file}',
        
        # Story template
        'template_welcome': 'Bem-vindo à sua nova história!',
        'template_beginning': 'Este é o começo. O que acontece a seguir depende de você.',
        'template_continue': 'Continuar',
        'template_body': 'Escreva sua história aqui. Use **negrito** e *itálico* para ênfase.',
        'template_add_images': 'Adicione imagens com: ![Descrição](images/sua-imagem.jpg)',
        'template_choices': 'Crie escolhas escrevendo: [[Texto da escolha]]',
        'template_end': 'O fim.',
        'template_author': 'Seu Nome',
        
        # Errors
        'error_generic': 'Erro',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Biblioteca de Histórias',
        'web_tab_editor': '✏️ Editor de Histórias',
        'web_tab_reader': '📖 Leitor de Histórias',
        
        # Web UI - Titles
        'web_title_library': '📖 Minha Coleção de Histórias',
        'web_title_editor': '✨ Crie Sua História',
        
        # Web UI - Buttons
        'web_btn_play': 'Jogar História',
        'web_btn_edit': 'Editar História',
        'web_btn_new': 'Nova História',
        'web_btn_validate': 'Validar',
        'web_btn_save': 'Salvar',
        'web_btn_compile': 'Compilar e Jogar',
        
        # Web UI - Messages
        'web_loading_stories': 'Carregando suas histórias...',
        'web_empty_title': 'Ainda não há histórias',
        'web_empty_text': 'Clique em "Nova História" para criar sua primeira aventura!',
        'web_by': 'por',
        'web_sections': 'seções',
        'web_editing': 'Editando',
        'web_msg_loading': 'Carregando história...',
        'web_msg_errors': 'Erros',
        'web_msg_error': 'Erro',
        'web_msg_loaded': 'Carregado',
        'web_msg_ready': 'Pronto para escrever uma nova história!',
        'web_msg_empty': 'O editor está vazio!',
        'web_msg_valid': 'História válida! Encontradas',
        'web_msg_validation_errors': 'Erros de validação',
        'web_msg_saved': 'Salvo como',
        'web_msg_unknown_error': 'Erro desconhecido',
        'web_msg_compiling': 'Compilando história...',
        'web_msg_compilation_errors': 'Erros de compilação',
        
        # Web UI - Prompts
        'web_prompt_save': 'Salvar como:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Minha Nova Aventura',
        'web_new_story_author': 'Seu Nome',
        'web_new_story_content': 'Escreva sua história aqui...',
        'web_new_story_choice': 'Fazer uma escolha',
        'web_new_story_continue': 'Continue sua aventura!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Escreva sua aventura aqui...\n\nFormato de exemplo:\n\n---\ntitle: Minha Aventura\nauthor: Seu Nome\n---\n\n[[beginning]]\n\nVocê acorda em um lugar misterioso...\n\n[[Explorar]]\n[[Voltar a dormir]]\n\n---\n\n[[Explorar]]\n\nVocê descobre algo incrível!',
    },
    'de': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Erstellen Sie interaktive Geschichtenbücher',
        'cli_command_help': 'Auszuführender Befehl',
        
        # Commands
        'cmd_compile': 'kompilieren',
        'cmd_compile_help': 'Eine Geschichte zu HTML kompilieren',
        'cmd_validate': 'validieren',
        'cmd_validate_help': 'Eine Geschichtendatei validieren',
        'cmd_init': 'initialisieren',
        'cmd_init_help': 'Eine neue Geschichte initialisieren',
        
        # Arguments
        'arg_input_help': 'Eingabe-Geschichtendatei',
        'arg_output_help': 'Ausgabeverzeichnis (Standard: output/)',
        'arg_no_zip_help': 'Keine ZIP-Datei erstellen',
        'arg_name_help': 'Geschichtenname',
        'arg_directory_help': 'Ausgabeverzeichnis',
        'arg_lang_help': 'Sprache',
        
        # Messages - compile command
        'msg_file_not_found': 'Datei nicht gefunden',
        'msg_reading_story': 'Geschichte wird gelesen von {path}...',
        'msg_parsing_story': 'Geschichte wird analysiert...',
        'msg_parse_error': 'Analysefehler',
        'msg_validating_story': 'Geschichte wird validiert...',
        'msg_validation_errors': 'Validierungsfehler gefunden',
        'msg_generating_html': 'HTML wird generiert...',
        'msg_created': 'Erstellt',
        'msg_creating_zip': 'ZIP-Archiv wird erstellt: {path}',
        'msg_compile_success': '✓ Geschichte erfolgreich kompiliert!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Analysefehler',
        'msg_validation_error_count': '✗ {count} Validierungsfehler gefunden',
        'msg_story_valid': '✓ Die Geschichte ist gültig!',
        'msg_title': 'Titel',
        'msg_author': 'Autor',
        'msg_sections': 'Abschnitte',
        
        # Messages - init command
        'msg_directory_exists': 'Das Verzeichnis existiert bereits',
        'msg_project_created': '✓ Neues Geschichtenprojekt erstellt: {directory}',
        'msg_story_file': 'Geschichtendatei',
        'msg_images_directory': 'Bilderverzeichnis',
        'msg_next_steps': 'Nächste Schritte',
        'msg_step_edit': '{file} bearbeiten',
        'msg_step_add_images': 'Bilder hinzufügen zu {directory}/',
        'msg_step_compile': 'Ausführen: python -m pick_a_page kompilieren {file}',
        
        # Story template
        'template_welcome': 'Willkommen zu Ihrer neuen Geschichte!',
        'template_beginning': 'Dies ist der Anfang. Was als nächstes passiert, liegt bei Ihnen.',
        'template_continue': 'Weiter',
        'template_body': 'Schreiben Sie hier Ihre Geschichte. Verwenden Sie **fett** und *kursiv* zur Betonung.',
        'template_add_images': 'Bilder hinzufügen mit: ![Beschreibung](images/ihr-bild.jpg)',
        'template_choices': 'Erstellen Sie Auswahlmöglichkeiten mit: [[Auswahltext]]',
        'template_end': 'Das Ende.',
        'template_author': 'Ihr Name',
        
        # Errors
        'error_generic': 'Fehler',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Geschichtenbibliothek',
        'web_tab_editor': '✏️ Geschichten-Editor',
        'web_tab_reader': '📖 Geschichten-Leser',
        
        # Web UI - Titles
        'web_title_library': '📖 Meine Geschichtensammlung',
        'web_title_editor': '✨ Erstellen Sie Ihre Geschichte',
        
        # Web UI - Buttons
        'web_btn_play': 'Geschichte spielen',
        'web_btn_edit': 'Geschichte bearbeiten',
        'web_btn_new': 'Neue Geschichte',
        'web_btn_validate': 'Validieren',
        'web_btn_save': 'Speichern',
        'web_btn_compile': 'Kompilieren & Spielen',
        
        # Web UI - Messages
        'web_loading_stories': 'Ihre Geschichten werden geladen...',
        'web_empty_title': 'Noch keine Geschichten',
        'web_empty_text': 'Klicken Sie auf "Neue Geschichte", um Ihr erstes Abenteuer zu erstellen!',
        'web_by': 'von',
        'web_sections': 'Abschnitte',
        'web_editing': 'Bearbeitung',
        'web_msg_loading': 'Geschichte wird geladen...',
        'web_msg_errors': 'Fehler',
        'web_msg_error': 'Fehler',
        'web_msg_loaded': 'Geladen',
        'web_msg_ready': 'Bereit, eine neue Geschichte zu schreiben!',
        'web_msg_empty': 'Editor ist leer!',
        'web_msg_valid': 'Geschichte ist gültig! Gefunden',
        'web_msg_validation_errors': 'Validierungsfehler',
        'web_msg_saved': 'Gespeichert als',
        'web_msg_unknown_error': 'Unbekannter Fehler',
        'web_msg_compiling': 'Geschichte wird kompiliert...',
        'web_msg_compilation_errors': 'Kompilierungsfehler',
        
        # Web UI - Prompts
        'web_prompt_save': 'Speichern als:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Mein Neues Abenteuer',
        'web_new_story_author': 'Ihr Name',
        'web_new_story_content': 'Schreiben Sie hier Ihre Geschichte...',
        'web_new_story_choice': 'Eine Wahl treffen',
        'web_new_story_continue': 'Setzen Sie Ihr Abenteuer fort!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Schreiben Sie hier Ihr Abenteuer...\n\nBeispielformat:\n\n---\ntitle: Mein Abenteuer\nauthor: Ihr Name\n---\n\n[[beginning]]\n\nSie wachen an einem geheimnisvollen Ort auf...\n\n[[Erkunden]]\n[[Weiterschlafen]]\n\n---\n\n[[Erkunden]]\n\nSie entdecken etwas Erstaunliches!',
    },
    'ru': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Создавайте интерактивные книги историй',
        'cli_command_help': 'Команда для выполнения',
        
        # Commands
        'cmd_compile': 'компилировать',
        'cmd_compile_help': 'Скомпилировать историю в HTML',
        'cmd_validate': 'проверить',
        'cmd_validate_help': 'Проверить файл истории',
        'cmd_init': 'инициализировать',
        'cmd_init_help': 'Инициализировать новую историю',
        
        # Arguments
        'arg_input_help': 'Входной файл истории',
        'arg_output_help': 'Выходная директория (по умолчанию: output/)',
        'arg_no_zip_help': 'Не создавать ZIP-файл',
        'arg_name_help': 'Название истории',
        'arg_directory_help': 'Выходная директория',
        'arg_lang_help': 'Язык',
        
        # Messages - compile command
        'msg_file_not_found': 'Файл не найден',
        'msg_reading_story': 'Чтение истории из {path}...',
        'msg_parsing_story': 'Анализ истории...',
        'msg_parse_error': 'Ошибка анализа',
        'msg_validating_story': 'Проверка истории...',
        'msg_validation_errors': 'Найдены ошибки проверки',
        'msg_generating_html': 'Генерация HTML...',
        'msg_created': 'Создано',
        'msg_creating_zip': 'Создание ZIP-архива: {path}',
        'msg_compile_success': '✓ История успешно скомпилирована!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Ошибка анализа',
        'msg_validation_error_count': '✗ Найдено {count} ошибок проверки',
        'msg_story_valid': '✓ История действительна!',
        'msg_title': 'Название',
        'msg_author': 'Автор',
        'msg_sections': 'Разделы',
        
        # Messages - init command
        'msg_directory_exists': 'Директория уже существует',
        'msg_project_created': '✓ Создан новый проект истории: {directory}',
        'msg_story_file': 'Файл истории',
        'msg_images_directory': 'Директория изображений',
        'msg_next_steps': 'Следующие шаги',
        'msg_step_edit': 'Редактировать {file}',
        'msg_step_add_images': 'Добавить изображения в {directory}/',
        'msg_step_compile': 'Выполнить: python -m pick_a_page компилировать {file}',
        
        # Story template
        'template_welcome': 'Добро пожаловать в вашу новую историю!',
        'template_beginning': 'Это начало. Что произойдет дальше, зависит от вас.',
        'template_continue': 'Продолжить',
        'template_body': 'Напишите свою историю здесь. Используйте **жирный** и *курсив* для выделения.',
        'template_add_images': 'Добавьте изображения с помощью: ![Описание](images/ваше-изображение.jpg)',
        'template_choices': 'Создавайте выборы, написав: [[Текст выбора]]',
        'template_end': 'Конец.',
        'template_author': 'Ваше Имя',
        
        # Errors
        'error_generic': 'Ошибка',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Библиотека Историй',
        'web_tab_editor': '✏️ Редактор Историй',
        'web_tab_reader': '📖 Читатель Историй',
        
        # Web UI - Titles
        'web_title_library': '📖 Моя Коллекция Историй',
        'web_title_editor': '✨ Создайте Свою Историю',
        
        # Web UI - Buttons
        'web_btn_play': 'Играть Историю',
        'web_btn_edit': 'Редактировать Историю',
        'web_btn_new': 'Новая История',
        'web_btn_validate': 'Проверить',
        'web_btn_save': 'Сохранить',
        'web_btn_compile': 'Скомпилировать и Играть',
        
        # Web UI - Messages
        'web_loading_stories': 'Загрузка ваших историй...',
        'web_empty_title': 'Пока нет историй',
        'web_empty_text': 'Нажмите "Новая История", чтобы создать ваше первое приключение!',
        'web_by': 'от',
        'web_sections': 'разделы',
        'web_editing': 'Редактирование',
        'web_msg_loading': 'Загрузка истории...',
        'web_msg_errors': 'Ошибки',
        'web_msg_error': 'Ошибка',
        'web_msg_loaded': 'Загружено',
        'web_msg_ready': 'Готов написать новую историю!',
        'web_msg_empty': 'Редактор пуст!',
        'web_msg_valid': 'История действительна! Найдено',
        'web_msg_validation_errors': 'Ошибки проверки',
        'web_msg_saved': 'Сохранено как',
        'web_msg_unknown_error': 'Неизвестная ошибка',
        'web_msg_compiling': 'Компиляция истории...',
        'web_msg_compilation_errors': 'Ошибки компиляции',
        
        # Web UI - Prompts
        'web_prompt_save': 'Сохранить как:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Мое Новое Приключение',
        'web_new_story_author': 'Ваше Имя',
        'web_new_story_content': 'Напишите свою историю здесь...',
        'web_new_story_choice': 'Сделать выбор',
        'web_new_story_continue': 'Продолжите ваше приключение!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Напишите свое приключение здесь...\n\nПример формата:\n\n---\ntitle: Мое Приключение\nauthor: Ваше Имя\n---\n\n[[beginning]]\n\nВы просыпаетесь в таинственном месте...\n\n[[Исследовать]]\n[[Вернуться ко сну]]\n\n---\n\n[[Исследовать]]\n\nВы обнаруживаете что-то удивительное!',
    },
    'zh': {
        # CLI main description
        'cli_description': 'Pick-a-Page：创建互动故事书',
        'cli_command_help': '要运行的命令',
        
        # Commands
        'cmd_compile': '编译',
        'cmd_compile_help': '将故事编译为HTML',
        'cmd_validate': '验证',
        'cmd_validate_help': '验证故事文件',
        'cmd_init': '初始化',
        'cmd_init_help': '初始化新故事',
        
        # Arguments
        'arg_input_help': '输入故事文件',
        'arg_output_help': '输出目录（默认：output/）',
        'arg_no_zip_help': '不创建ZIP文件',
        'arg_name_help': '故事名称',
        'arg_directory_help': '输出目录',
        'arg_lang_help': '语言',
        
        # Messages - compile command
        'msg_file_not_found': '文件未找到',
        'msg_reading_story': '正在从{path}读取故事...',
        'msg_parsing_story': '正在解析故事...',
        'msg_parse_error': '解析错误',
        'msg_validating_story': '正在验证故事...',
        'msg_validation_errors': '发现验证错误',
        'msg_generating_html': '正在生成HTML...',
        'msg_created': '已创建',
        'msg_creating_zip': '正在创建ZIP存档：{path}',
        'msg_compile_success': '✓ 故事编译成功！',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ 解析错误',
        'msg_validation_error_count': '✗ 发现{count}个验证错误',
        'msg_story_valid': '✓ 故事有效！',
        'msg_title': '标题',
        'msg_author': '作者',
        'msg_sections': '章节',
        
        # Messages - init command
        'msg_directory_exists': '目录已存在',
        'msg_project_created': '✓ 已创建新故事项目：{directory}',
        'msg_story_file': '故事文件',
        'msg_images_directory': '图片目录',
        'msg_next_steps': '下一步',
        'msg_step_edit': '编辑{file}',
        'msg_step_add_images': '将图片添加到{directory}/',
        'msg_step_compile': '运行：python -m pick_a_page 编译 {file}',
        
        # Story template
        'template_welcome': '欢迎来到你的新故事！',
        'template_beginning': '这是开始。接下来发生什么取决于你。',
        'template_continue': '继续',
        'template_body': '在这里写你的故事。使用**粗体**和*斜体*来强调。',
        'template_add_images': '添加图片：![描述](images/你的图片.jpg)',
        'template_choices': '创建选择：[[选择文本]]',
        'template_end': '结束。',
        'template_author': '你的名字',
        
        # Errors
        'error_generic': '错误',
        
        # Web UI - Navigation
        'web_tab_library': '📚 故事库',
        'web_tab_editor': '✏️ 故事编辑器',
        'web_tab_reader': '📖 故事阅读器',
        
        # Web UI - Titles
        'web_title_library': '📖 我的故事集',
        'web_title_editor': '✨ 创建你的故事',
        
        # Web UI - Buttons
        'web_btn_play': '播放故事',
        'web_btn_edit': '编辑故事',
        'web_btn_new': '新故事',
        'web_btn_validate': '验证',
        'web_btn_save': '保存',
        'web_btn_compile': '编译并播放',
        
        # Web UI - Messages
        'web_loading_stories': '正在加载你的故事...',
        'web_empty_title': '还没有故事',
        'web_empty_text': '点击"新故事"创建你的第一个冒险！',
        'web_by': '作者',
        'web_sections': '章节',
        'web_editing': '编辑中',
        'web_msg_loading': '正在加载故事...',
        'web_msg_errors': '错误',
        'web_msg_error': '错误',
        'web_msg_loaded': '已加载',
        'web_msg_ready': '准备写新故事！',
        'web_msg_empty': '编辑器是空的！',
        'web_msg_valid': '故事有效！找到',
        'web_msg_validation_errors': '验证错误',
        'web_msg_saved': '保存为',
        'web_msg_unknown_error': '未知错误',
        'web_msg_compiling': '正在编译故事...',
        'web_msg_compilation_errors': '编译错误',
        
        # Web UI - Prompts
        'web_prompt_save': '保存为：',
        
        # Web UI - New Story Template
        'web_new_story_title': '我的新冒险',
        'web_new_story_author': '你的名字',
        'web_new_story_content': '在这里写你的故事...',
        'web_new_story_choice': '做出选择',
        'web_new_story_continue': '继续你的冒险！',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': '在这里写你的冒险...\n\n示例格式：\n\n---\ntitle: 我的冒险\nauthor: 你的名字\n---\n\n[[beginning]]\n\n你在一个神秘的地方醒来...\n\n[[探索]]\n[[继续睡觉]]\n\n---\n\n[[探索]]\n\n你发现了一些惊人的东西！',
    },
    'hi': {
        # CLI main description
        'cli_description': 'Pick-a-Page: इंटरैक्टिव कहानी की किताबें बनाएं',
        'cli_command_help': 'चलाने के लिए कमांड',
        
        # Commands
        'cmd_compile': 'संकलित करें',
        'cmd_compile_help': 'कहानी को HTML में संकलित करें',
        'cmd_validate': 'मान्य करें',
        'cmd_validate_help': 'कहानी फ़ाइल को मान्य करें',
        'cmd_init': 'आरंभ करें',
        'cmd_init_help': 'नई कहानी आरंभ करें',
        
        # Arguments
        'arg_input_help': 'इनपुट कहानी फ़ाइल',
        'arg_output_help': 'आउटपुट निर्देशिका (डिफ़ॉल्ट: output/)',
        'arg_no_zip_help': 'ZIP फ़ाइल न बनाएं',
        'arg_name_help': 'कहानी का नाम',
        'arg_directory_help': 'आउटपुट निर्देशिका',
        'arg_lang_help': 'भाषा',
        
        # Messages - compile command
        'msg_file_not_found': 'फ़ाइल नहीं मिली',
        'msg_reading_story': '{path} से कहानी पढ़ी जा रही है...',
        'msg_parsing_story': 'कहानी का विश्लेषण किया जा रहा है...',
        'msg_parse_error': 'विश्लेषण त्रुटि',
        'msg_validating_story': 'कहानी को मान्य किया जा रहा है...',
        'msg_validation_errors': 'मान्यता त्रुटियां मिलीं',
        'msg_generating_html': 'HTML उत्पन्न किया जा रहा है...',
        'msg_created': 'बनाया गया',
        'msg_creating_zip': 'ZIP संग्रह बनाया जा रहा है: {path}',
        'msg_compile_success': '✓ कहानी सफलतापूर्वक संकलित हुई!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ विश्लेषण त्रुटि',
        'msg_validation_error_count': '✗ {count} मान्यता त्रुटि(यां) मिलीं',
        'msg_story_valid': '✓ कहानी मान्य है!',
        'msg_title': 'शीर्षक',
        'msg_author': 'लेखक',
        'msg_sections': 'अनुभाग',
        
        # Messages - init command
        'msg_directory_exists': 'निर्देशिका पहले से मौजूद है',
        'msg_project_created': '✓ नई कहानी परियोजना बनाई गई: {directory}',
        'msg_story_file': 'कहानी फ़ाइल',
        'msg_images_directory': 'चित्र निर्देशिका',
        'msg_next_steps': 'अगले कदम',
        'msg_step_edit': '{file} संपादित करें',
        'msg_step_add_images': '{directory}/ में चित्र जोड़ें',
        'msg_step_compile': 'चलाएं: python -m pick_a_page संकलित करें {file}',
        
        # Story template
        'template_welcome': 'अपनी नई कहानी में आपका स्वागत है!',
        'template_beginning': 'यह शुरुआत है। आगे क्या होता है यह आप पर निर्भर करता है।',
        'template_continue': 'जारी रखें',
        'template_body': 'यहां अपनी कहानी लिखें। जोर देने के लिए **बोल्ड** और *इटैलिक* का उपयोग करें।',
        'template_add_images': 'चित्र जोड़ें: ![विवरण](images/आपका-चित्र.jpg)',
        'template_choices': 'विकल्प बनाएं: [[विकल्प पाठ]]',
        'template_end': 'समाप्त।',
        'template_author': 'आपका नाम',
        
        # Errors
        'error_generic': 'त्रुटि',
        
        # Web UI - Navigation
        'web_tab_library': '📚 कहानी पुस्तकालय',
        'web_tab_editor': '✏️ कहानी संपादक',
        'web_tab_reader': '📖 कहानी पाठक',
        
        # Web UI - Titles
        'web_title_library': '📖 मेरा कहानी संग्रह',
        'web_title_editor': '✨ अपनी कहानी बनाएं',
        
        # Web UI - Buttons
        'web_btn_play': 'कहानी चलाएं',
        'web_btn_edit': 'कहानी संपादित करें',
        'web_btn_new': 'नई कहानी',
        'web_btn_validate': 'मान्य करें',
        'web_btn_save': 'सहेजें',
        'web_btn_compile': 'संकलित करें और चलाएं',
        
        # Web UI - Messages
        'web_loading_stories': 'आपकी कहानियां लोड हो रही हैं...',
        'web_empty_title': 'अभी तक कोई कहानी नहीं',
        'web_empty_text': 'अपना पहला साहसिक कार्य बनाने के लिए "नई कहानी" पर क्लिक करें!',
        'web_by': 'द्वारा',
        'web_sections': 'अनुभाग',
        'web_editing': 'संपादन',
        'web_msg_loading': 'कहानी लोड हो रही है...',
        'web_msg_errors': 'त्रुटियां',
        'web_msg_error': 'त्रुटि',
        'web_msg_loaded': 'लोड किया गया',
        'web_msg_ready': 'नई कहानी लिखने के लिए तैयार!',
        'web_msg_empty': 'संपादक खाली है!',
        'web_msg_valid': 'कहानी मान्य है! मिला',
        'web_msg_validation_errors': 'मान्यता त्रुटियां',
        'web_msg_saved': 'इस रूप में सहेजा गया',
        'web_msg_unknown_error': 'अज्ञात त्रुटि',
        'web_msg_compiling': 'कहानी संकलित की जा रही है...',
        'web_msg_compilation_errors': 'संकलन त्रुटियां',
        
        # Web UI - Prompts
        'web_prompt_save': 'इस रूप में सहेजें:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'मेरा नया साहसिक कार्य',
        'web_new_story_author': 'आपका नाम',
        'web_new_story_content': 'यहां अपनी कहानी लिखें...',
        'web_new_story_choice': 'एक विकल्प चुनें',
        'web_new_story_continue': 'अपना साहसिक कार्य जारी रखें!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'यहां अपना साहसिक कार्य लिखें...\n\nउदाहरण प्रारूप:\n\n---\ntitle: मेरा साहसिक कार्य\nauthor: आपका नाम\n---\n\n[[beginning]]\n\nआप एक रहस्यमय स्थान पर जागते हैं...\n\n[[अन्वेषण करें]]\n[[वापस सोएं]]\n\n---\n\n[[अन्वेषण करें]]\n\nआप कुछ अद्भुत खोजते हैं!',
    },
    'ar': {
        # CLI main description
        'cli_description': 'Pick-a-Page: إنشاء كتب قصص تفاعلية',
        'cli_command_help': 'الأمر المراد تنفيذه',
        
        # Commands
        'cmd_compile': 'ترجمة',
        'cmd_compile_help': 'ترجمة قصة إلى HTML',
        'cmd_validate': 'التحقق',
        'cmd_validate_help': 'التحقق من صحة ملف القصة',
        'cmd_init': 'التهيئة',
        'cmd_init_help': 'تهيئة قصة جديدة',
        
        # Arguments
        'arg_input_help': 'ملف القصة المدخل',
        'arg_output_help': 'دليل الإخراج (الافتراضي: output/)',
        'arg_no_zip_help': 'عدم إنشاء ملف ZIP',
        'arg_name_help': 'اسم القصة',
        'arg_directory_help': 'دليل الإخراج',
        'arg_lang_help': 'اللغة',
        
        # Messages - compile command
        'msg_file_not_found': 'الملف غير موجود',
        'msg_reading_story': 'قراءة القصة من {path}...',
        'msg_parsing_story': 'تحليل القصة...',
        'msg_parse_error': 'خطأ في التحليل',
        'msg_validating_story': 'التحقق من القصة...',
        'msg_validation_errors': 'تم العثور على أخطاء في التحقق',
        'msg_generating_html': 'إنشاء HTML...',
        'msg_created': 'تم الإنشاء',
        'msg_creating_zip': 'إنشاء أرشيف ZIP: {path}',
        'msg_compile_success': '✓ تمت ترجمة القصة بنجاح!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ خطأ في التحليل',
        'msg_validation_error_count': '✗ تم العثور على {count} خطأ في التحقق',
        'msg_story_valid': '✓ القصة صحيحة!',
        'msg_title': 'العنوان',
        'msg_author': 'المؤلف',
        'msg_sections': 'الأقسام',
        
        # Messages - init command
        'msg_directory_exists': 'الدليل موجود بالفعل',
        'msg_project_created': '✓ تم إنشاء مشروع قصة جديد: {directory}',
        'msg_story_file': 'ملف القصة',
        'msg_images_directory': 'دليل الصور',
        'msg_next_steps': 'الخطوات التالية',
        'msg_step_edit': 'تحرير {file}',
        'msg_step_add_images': 'إضافة صور إلى {directory}/',
        'msg_step_compile': 'تشغيل: python -m pick_a_page ترجمة {file}',
        
        # Story template
        'template_welcome': 'مرحبًا بك في قصتك الجديدة!',
        'template_beginning': 'هذه هي البداية. ما يحدث بعد ذلك يعتمد عليك.',
        'template_continue': 'متابعة',
        'template_body': 'اكتب قصتك هنا. استخدم **غامق** و*مائل* للتأكيد.',
        'template_add_images': 'أضف صورًا باستخدام: ![الوصف](images/صورتك.jpg)',
        'template_choices': 'أنشئ خيارات بكتابة: [[نص الخيار]]',
        'template_end': 'النهاية.',
        'template_author': 'اسمك',
        
        # Errors
        'error_generic': 'خطأ',
        
        # Web UI - Navigation
        'web_tab_library': '📚 مكتبة القصص',
        'web_tab_editor': '✏️ محرر القصص',
        'web_tab_reader': '📖 قارئ القصص',
        
        # Web UI - Titles
        'web_title_library': '📖 مجموعة قصصي',
        'web_title_editor': '✨ أنشئ قصتك',
        
        # Web UI - Buttons
        'web_btn_play': 'تشغيل القصة',
        'web_btn_edit': 'تحرير القصة',
        'web_btn_new': 'قصة جديدة',
        'web_btn_validate': 'التحقق',
        'web_btn_save': 'حفظ',
        'web_btn_compile': 'ترجمة وتشغيل',
        
        # Web UI - Messages
        'web_loading_stories': 'تحميل قصصك...',
        'web_empty_title': 'لا توجد قصص بعد',
        'web_empty_text': 'انقر على "قصة جديدة" لإنشاء مغامرتك الأولى!',
        'web_by': 'بواسطة',
        'web_sections': 'أقسام',
        'web_editing': 'التحرير',
        'web_msg_loading': 'تحميل القصة...',
        'web_msg_errors': 'أخطاء',
        'web_msg_error': 'خطأ',
        'web_msg_loaded': 'تم التحميل',
        'web_msg_ready': 'جاهز لكتابة قصة جديدة!',
        'web_msg_empty': 'المحرر فارغ!',
        'web_msg_valid': 'القصة صحيحة! تم العثور على',
        'web_msg_validation_errors': 'أخطاء التحقق',
        'web_msg_saved': 'تم الحفظ باسم',
        'web_msg_unknown_error': 'خطأ غير معروف',
        'web_msg_compiling': 'ترجمة القصة...',
        'web_msg_compilation_errors': 'أخطاء الترجمة',
        
        # Web UI - Prompts
        'web_prompt_save': 'حفظ باسم:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'مغامرتي الجديدة',
        'web_new_story_author': 'اسمك',
        'web_new_story_content': 'اكتب قصتك هنا...',
        'web_new_story_choice': 'اتخذ خيارًا',
        'web_new_story_continue': 'تابع مغامرتك!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'اكتب مغامرتك هنا...\n\nتنسيق المثال:\n\n---\ntitle: مغامرتي\nauthor: اسمك\n---\n\n[[beginning]]\n\nتستيقظ في مكان غامض...\n\n[[استكشف]]\n[[عد للنوم]]\n\n---\n\n[[استكشف]]\n\nتكتشف شيئًا مذهلاً!',
    },
    'bn': {
        # CLI main description
        'cli_description': 'Pick-a-Page: ইন্টারঅ্যাক্টিভ গল্পের বই তৈরি করুন',
        'cli_command_help': 'চালানোর জন্য কমান্ড',
        
        # Commands
        'cmd_compile': 'সংকলন করুন',
        'cmd_compile_help': 'গল্পটি HTML-এ সংকলন করুন',
        'cmd_validate': 'যাচাই করুন',
        'cmd_validate_help': 'গল্প ফাইল যাচাই করুন',
        'cmd_init': 'আরম্ভ করুন',
        'cmd_init_help': 'নতুন গল্প আরম্ভ করুন',
        
        # Arguments
        'arg_input_help': 'ইনপুট গল্প ফাইল',
        'arg_output_help': 'আউটপুট ডিরেক্টরি (ডিফল্ট: output/)',
        'arg_no_zip_help': 'ZIP ফাইল তৈরি করবেন না',
        'arg_name_help': 'গল্পের নাম',
        'arg_directory_help': 'আউটপুট ডিরেক্টরি',
        'arg_lang_help': 'ভাষা',
        
        # Messages - compile command
        'msg_file_not_found': 'ফাইল পাওয়া যায়নি',
        'msg_reading_story': '{path} থেকে গল্প পড়া হচ্ছে...',
        'msg_parsing_story': 'গল্প বিশ্লেষণ করা হচ্ছে...',
        'msg_parse_error': 'বিশ্লেষণ ত্রুটি',
        'msg_validating_story': 'গল্প যাচাই করা হচ্ছে...',
        'msg_validation_errors': 'যাচাই ত্রুটি পাওয়া গেছে',
        'msg_generating_html': 'HTML তৈরি করা হচ্ছে...',
        'msg_created': 'তৈরি হয়েছে',
        'msg_creating_zip': 'ZIP আর্কাইভ তৈরি করা হচ্ছে: {path}',
        'msg_compile_success': '✓ গল্প সফলভাবে সংকলিত হয়েছে!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ বিশ্লেষণ ত্রুটি',
        'msg_validation_error_count': '✗ {count} যাচাই ত্রুটি পাওয়া গেছে',
        'msg_story_valid': '✓ গল্প বৈধ!',
        'msg_title': 'শিরোনাম',
        'msg_author': 'লেখক',
        'msg_sections': 'বিভাগ',
        
        # Messages - init command
        'msg_directory_exists': 'ডিরেক্টরি ইতিমধ্যে বিদ্যমান',
        'msg_project_created': '✓ নতুন গল্প প্রকল্প তৈরি হয়েছে: {directory}',
        'msg_story_file': 'গল্প ফাইল',
        'msg_images_directory': 'ছবি ডিরেক্টরি',
        'msg_next_steps': 'পরবর্তী পদক্ষেপ',
        'msg_step_edit': '{file} সম্পাদনা করুন',
        'msg_step_add_images': '{directory}/ এ ছবি যোগ করুন',
        'msg_step_compile': 'চালান: python -m pick_a_page সংকলন করুন {file}',
        
        # Story template
        'template_welcome': 'আপনার নতুন গল্পে স্বাগতম!',
        'template_beginning': 'এটি শুরু। পরবর্তী কী ঘটে তা আপনার উপর নির্ভর করে।',
        'template_continue': 'চালিয়ে যান',
        'template_body': 'এখানে আপনার গল্প লিখুন। জোর দেওয়ার জন্য **গাঢ়** এবং *তির্যক* ব্যবহার করুন।',
        'template_add_images': 'ছবি যোগ করুন: ![বর্ণনা](images/আপনার-ছবি.jpg)',
        'template_choices': 'পছন্দ তৈরি করুন: [[পছন্দ পাঠ্য]]',
        'template_end': 'শেষ।',
        'template_author': 'আপনার নাম',
        
        # Errors
        'error_generic': 'ত্রুটি',
        
        # Web UI - Navigation
        'web_tab_library': '📚 গল্প লাইব্রেরি',
        'web_tab_editor': '✏️ গল্প সম্পাদক',
        'web_tab_reader': '📖 গল্প পাঠক',
        
        # Web UI - Titles
        'web_title_library': '📖 আমার গল্প সংগ্রহ',
        'web_title_editor': '✨ আপনার গল্প তৈরি করুন',
        
        # Web UI - Buttons
        'web_btn_play': 'গল্প খেলুন',
        'web_btn_edit': 'গল্প সম্পাদনা করুন',
        'web_btn_new': 'নতুন গল্প',
        'web_btn_validate': 'যাচাই করুন',
        'web_btn_save': 'সংরক্ষণ করুন',
        'web_btn_compile': 'সংকলন ও খেলুন',
        
        # Web UI - Messages
        'web_loading_stories': 'আপনার গল্প লোড হচ্ছে...',
        'web_empty_title': 'এখনও কোনও গল্প নেই',
        'web_empty_text': 'আপনার প্রথম অভিযান তৈরি করতে "নতুন গল্প" ক্লিক করুন!',
        'web_by': 'দ্বারা',
        'web_sections': 'বিভাগ',
        'web_editing': 'সম্পাদনা',
        'web_msg_loading': 'গল্প লোড হচ্ছে...',
        'web_msg_errors': 'ত্রুটি',
        'web_msg_error': 'ত্রুটি',
        'web_msg_loaded': 'লোড হয়েছে',
        'web_msg_ready': 'নতুন গল্প লেখার জন্য প্রস্তুত!',
        'web_msg_empty': 'সম্পাদক খালি!',
        'web_msg_valid': 'গল্প বৈধ! পাওয়া গেছে',
        'web_msg_validation_errors': 'যাচাই ত্রুটি',
        'web_msg_saved': 'হিসাবে সংরক্ষিত',
        'web_msg_unknown_error': 'অজানা ত্রুটি',
        'web_msg_compiling': 'গল্প সংকলন করা হচ্ছে...',
        'web_msg_compilation_errors': 'সংকলন ত্রুটি',
        
        # Web UI - Prompts
        'web_prompt_save': 'হিসাবে সংরক্ষণ করুন:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'আমার নতুন অভিযান',
        'web_new_story_author': 'আপনার নাম',
        'web_new_story_content': 'এখানে আপনার গল্প লিখুন...',
        'web_new_story_choice': 'একটি পছন্দ করুন',
        'web_new_story_continue': 'আপনার অভিযান চালিয়ে যান!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'এখানে আপনার অভিযান লিখুন...\n\nউদাহরণ বিন্যাস:\n\n---\ntitle: আমার অভিযান\nauthor: আপনার নাম\n---\n\n[[beginning]]\n\nআপনি একটি রহস্যময় স্থানে জেগে উঠেছেন...\n\n[[অন্বেষণ করুন]]\n[[আবার ঘুমান]]\n\n---\n\n[[অন্বেষণ করুন]]\n\nআপনি কিছু আশ্চর্যজনক আবিষ্কার করেছেন!',
    },
    'ur': {
        # CLI main description
        'cli_description': 'Pick-a-Page: انٹرایکٹو کہانی کی کتابیں بنائیں',
        'cli_command_help': 'چلانے کے لیے کمانڈ',
        
        # Commands
        'cmd_compile': 'مرتب کریں',
        'cmd_compile_help': 'کہانی کو HTML میں مرتب کریں',
        'cmd_validate': 'تصدیق کریں',
        'cmd_validate_help': 'کہانی کی فائل کی تصدیق کریں',
        'cmd_init': 'شروع کریں',
        'cmd_init_help': 'نئی کہانی شروع کریں',
        
        # Arguments
        'arg_input_help': 'ان پٹ کہانی فائل',
        'arg_output_help': 'آؤٹ پٹ ڈائریکٹری (ڈیفالٹ: output/)',
        'arg_no_zip_help': 'ZIP فائل نہ بنائیں',
        'arg_name_help': 'کہانی کا نام',
        'arg_directory_help': 'آؤٹ پٹ ڈائریکٹری',
        'arg_lang_help': 'زبان',
        
        # Messages - compile command
        'msg_file_not_found': 'فائل نہیں ملی',
        'msg_reading_story': '{path} سے کہانی پڑھی جا رہی ہے...',
        'msg_parsing_story': 'کہانی کا تجزیہ کیا جا رہا ہے...',
        'msg_parse_error': 'تجزیہ کی خرابی',
        'msg_validating_story': 'کہانی کی تصدیق کی جا رہی ہے...',
        'msg_validation_errors': 'تصدیق کی خرابیاں ملیں',
        'msg_generating_html': 'HTML بنایا جا رہا ہے...',
        'msg_created': 'بنایا گیا',
        'msg_creating_zip': 'ZIP آرکائیو بنایا جا رہا ہے: {path}',
        'msg_compile_success': '✓ کہانی کامیابی سے مرتب ہوئی!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ تجزیہ کی خرابی',
        'msg_validation_error_count': '✗ {count} تصدیق کی خرابیاں ملیں',
        'msg_story_valid': '✓ کہانی درست ہے!',
        'msg_title': 'عنوان',
        'msg_author': 'مصنف',
        'msg_sections': 'حصے',
        
        # Messages - init command
        'msg_directory_exists': 'ڈائریکٹری پہلے سے موجود ہے',
        'msg_project_created': '✓ نیا کہانی پروجیکٹ بنایا گیا: {directory}',
        'msg_story_file': 'کہانی فائل',
        'msg_images_directory': 'تصاویر کی ڈائریکٹری',
        'msg_next_steps': 'اگلے قدم',
        'msg_step_edit': '{file} میں ترمیم کریں',
        'msg_step_add_images': '{directory}/ میں تصاویر شامل کریں',
        'msg_step_compile': 'چلائیں: python -m pick_a_page مرتب کریں {file}',
        
        # Story template
        'template_welcome': 'اپنی نئی کہانی میں خوش آمدید!',
        'template_beginning': 'یہ آغاز ہے۔ آگے کیا ہوتا ہے یہ آپ پر منحصر ہے۔',
        'template_continue': 'جاری رکھیں',
        'template_body': 'یہاں اپنی کہانی لکھیں۔ زور دینے کے لیے **بولڈ** اور *اٹیلک* استعمال کریں۔',
        'template_add_images': 'تصاویر شامل کریں: ![تفصیل](images/آپ-کی-تصویر.jpg)',
        'template_choices': 'انتخاب بنائیں: [[انتخاب کا متن]]',
        'template_end': 'اختتام۔',
        'template_author': 'آپ کا نام',
        
        # Errors
        'error_generic': 'خرابی',
        
        # Web UI - Navigation
        'web_tab_library': '📚 کہانی لائبریری',
        'web_tab_editor': '✏️ کہانی ایڈیٹر',
        'web_tab_reader': '📖 کہانی ریڈر',
        
        # Web UI - Titles
        'web_title_library': '📖 میرا کہانی کا مجموعہ',
        'web_title_editor': '✨ اپنی کہانی بنائیں',
        
        # Web UI - Buttons
        'web_btn_play': 'کہانی چلائیں',
        'web_btn_edit': 'کہانی میں ترمیم کریں',
        'web_btn_new': 'نئی کہانی',
        'web_btn_validate': 'تصدیق کریں',
        'web_btn_save': 'محفوظ کریں',
        'web_btn_compile': 'مرتب کریں اور چلائیں',
        
        # Web UI - Messages
        'web_loading_stories': 'آپ کی کہانیاں لوڈ ہو رہی ہیں...',
        'web_empty_title': 'ابھی تک کوئی کہانیاں نہیں',
        'web_empty_text': 'اپنا پہلا مہم بنانے کے لیے "نئی کہانی" پر کلک کریں!',
        'web_by': 'بذریعہ',
        'web_sections': 'حصے',
        'web_editing': 'ترمیم',
        'web_msg_loading': 'کہانی لوڈ ہو رہی ہے...',
        'web_msg_errors': 'خرابیاں',
        'web_msg_error': 'خرابی',
        'web_msg_loaded': 'لوڈ ہوا',
        'web_msg_ready': 'نئی کہانی لکھنے کے لیے تیار!',
        'web_msg_empty': 'ایڈیٹر خالی ہے!',
        'web_msg_valid': 'کہانی درست ہے! ملا',
        'web_msg_validation_errors': 'تصدیق کی خرابیاں',
        'web_msg_saved': 'بطور محفوظ کیا گیا',
        'web_msg_unknown_error': 'نامعلوم خرابی',
        'web_msg_compiling': 'کہانی مرتب کی جا رہی ہے...',
        'web_msg_compilation_errors': 'ترتیب کی خرابیاں',
        
        # Web UI - Prompts
        'web_prompt_save': 'بطور محفوظ کریں:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'میری نئی مہم',
        'web_new_story_author': 'آپ کا نام',
        'web_new_story_content': 'یہاں اپنی کہانی لکھیں...',
        'web_new_story_choice': 'انتخاب کریں',
        'web_new_story_continue': 'اپنی مہم جاری رکھیں!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'یہاں اپنی مہم لکھیں...\n\nمثال کی شکل:\n\n---\ntitle: میری مہم\nauthor: آپ کا نام\n---\n\n[[beginning]]\n\nآپ ایک پراسرار جگہ میں جاگتے ہیں...\n\n[[تلاش کریں]]\n[[واپس سو جائیں]]\n\n---\n\n[[تلاش کریں]]\n\nآپ کچھ حیرت انگیز دریافت کرتے ہیں!',
    },
    'id': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Buat buku cerita interaktif',
        'cli_command_help': 'Perintah untuk dijalankan',
        
        # Commands
        'cmd_compile': 'kompilasi',
        'cmd_compile_help': 'Kompilasi cerita ke HTML',
        'cmd_validate': 'validasi',
        'cmd_validate_help': 'Validasi file cerita',
        'cmd_init': 'inisialisasi',
        'cmd_init_help': 'Inisialisasi cerita baru',
        
        # Arguments
        'arg_input_help': 'File cerita input',
        'arg_output_help': 'Direktori output (default: output/)',
        'arg_no_zip_help': 'Jangan buat file ZIP',
        'arg_name_help': 'Nama cerita',
        'arg_directory_help': 'Direktori output',
        'arg_lang_help': 'Bahasa',
        
        # Messages - compile command
        'msg_file_not_found': 'File tidak ditemukan',
        'msg_reading_story': 'Membaca cerita dari {path}...',
        'msg_parsing_story': 'Menganalisis cerita...',
        'msg_parse_error': 'Kesalahan analisis',
        'msg_validating_story': 'Memvalidasi cerita...',
        'msg_validation_errors': 'Kesalahan validasi ditemukan',
        'msg_generating_html': 'Membuat HTML...',
        'msg_created': 'Dibuat',
        'msg_creating_zip': 'Membuat arsip ZIP: {path}',
        'msg_compile_success': '✓ Cerita berhasil dikompilasi!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Kesalahan analisis',
        'msg_validation_error_count': '✗ Ditemukan {count} kesalahan validasi',
        'msg_story_valid': '✓ Cerita valid!',
        'msg_title': 'Judul',
        'msg_author': 'Penulis',
        'msg_sections': 'Bagian',
        
        # Messages - init command
        'msg_directory_exists': 'Direktori sudah ada',
        'msg_project_created': '✓ Proyek cerita baru dibuat: {directory}',
        'msg_story_file': 'File cerita',
        'msg_images_directory': 'Direktori gambar',
        'msg_next_steps': 'Langkah selanjutnya',
        'msg_step_edit': 'Edit {file}',
        'msg_step_add_images': 'Tambahkan gambar ke {directory}/',
        'msg_step_compile': 'Jalankan: python -m pick_a_page kompilasi {file}',
        
        # Story template
        'template_welcome': 'Selamat datang di cerita baru Anda!',
        'template_beginning': 'Ini adalah awal. Apa yang terjadi selanjutnya terserah Anda.',
        'template_continue': 'Lanjutkan',
        'template_body': 'Tulis cerita Anda di sini. Gunakan **tebal** dan *miring* untuk penekanan.',
        'template_add_images': 'Tambahkan gambar dengan: ![Deskripsi](images/gambar-anda.jpg)',
        'template_choices': 'Buat pilihan dengan menulis: [[Teks pilihan]]',
        'template_end': 'Tamat.',
        'template_author': 'Nama Anda',
        
        # Errors
        'error_generic': 'Kesalahan',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Perpustakaan Cerita',
        'web_tab_editor': '✏️ Editor Cerita',
        'web_tab_reader': '📖 Pembaca Cerita',
        
        # Web UI - Titles
        'web_title_library': '📖 Koleksi Cerita Saya',
        'web_title_editor': '✨ Buat Cerita Anda',
        
        # Web UI - Buttons
        'web_btn_play': 'Mainkan Cerita',
        'web_btn_edit': 'Edit Cerita',
        'web_btn_new': 'Cerita Baru',
        'web_btn_validate': 'Validasi',
        'web_btn_save': 'Simpan',
        'web_btn_compile': 'Kompilasi & Mainkan',
        
        # Web UI - Messages
        'web_loading_stories': 'Memuat cerita Anda...',
        'web_empty_title': 'Belum ada cerita',
        'web_empty_text': 'Klik "Cerita Baru" untuk membuat petualangan pertama Anda!',
        'web_by': 'oleh',
        'web_sections': 'bagian',
        'web_editing': 'Mengedit',
        'web_msg_loading': 'Memuat cerita...',
        'web_msg_errors': 'Kesalahan',
        'web_msg_error': 'Kesalahan',
        'web_msg_loaded': 'Dimuat',
        'web_msg_ready': 'Siap menulis cerita baru!',
        'web_msg_empty': 'Editor kosong!',
        'web_msg_valid': 'Cerita valid! Ditemukan',
        'web_msg_validation_errors': 'Kesalahan validasi',
        'web_msg_saved': 'Disimpan sebagai',
        'web_msg_unknown_error': 'Kesalahan tidak diketahui',
        'web_msg_compiling': 'Mengompilasi cerita...',
        'web_msg_compilation_errors': 'Kesalahan kompilasi',
        
        # Web UI - Prompts
        'web_prompt_save': 'Simpan sebagai:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Petualangan Baru Saya',
        'web_new_story_author': 'Nama Anda',
        'web_new_story_content': 'Tulis cerita Anda di sini...',
        'web_new_story_choice': 'Buat pilihan',
        'web_new_story_continue': 'Lanjutkan petualangan Anda!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Tulis petualangan Anda di sini...\n\nContoh format:\n\n---\ntitle: Petualangan Saya\nauthor: Nama Anda\n---\n\n[[beginning]]\n\nAnda terbangun di tempat misterius...\n\n[[Jelajahi]]\n[[Kembali tidur]]\n\n---\n\n[[Jelajahi]]\n\nAnda menemukan sesuatu yang menakjubkan!',
    },
    'bg': {
        # CLI main description
        'cli_description': 'Pick-a-Page: Създавайте интерактивни книги с истории',
        'cli_command_help': 'Команда за изпълнение',
        
        # Commands
        'cmd_compile': 'компилирай',
        'cmd_compile_help': 'Компилирайте история в HTML',
        'cmd_validate': 'валидирай',
        'cmd_validate_help': 'Валидирайте файл с история',
        'cmd_init': 'инициализирай',
        'cmd_init_help': 'Инициализирайте нова история',
        
        # Arguments
        'arg_input_help': 'Входен файл с история',
        'arg_output_help': 'Изходна директория (по подразбиране: output/)',
        'arg_no_zip_help': 'Не създавайте ZIP файл',
        'arg_name_help': 'Име на историята',
        'arg_directory_help': 'Изходна директория',
        'arg_lang_help': 'Език',
        
        # Messages - compile command
        'msg_file_not_found': 'Файлът не е намерен',
        'msg_reading_story': 'Четене на история от {path}...',
        'msg_parsing_story': 'Анализиране на историята...',
        'msg_parse_error': 'Грешка при анализ',
        'msg_validating_story': 'Валидиране на историята...',
        'msg_validation_errors': 'Намерени грешки при валидация',
        'msg_generating_html': 'Генериране на HTML...',
        'msg_created': 'Създадено',
        'msg_creating_zip': 'Създаване на ZIP архив: {path}',
        'msg_compile_success': '✓ Историята е компилирана успешно!',
        
        # Messages - validate command
        'msg_validate_parse_error': '✗ Грешка при анализ',
        'msg_validation_error_count': '✗ Намерени са {count} грешки при валидация',
        'msg_story_valid': '✓ Историята е валидна!',
        'msg_title': 'Заглавие',
        'msg_author': 'Автор',
        'msg_sections': 'Раздели',
        
        # Messages - init command
        'msg_directory_exists': 'Директорията вече съществува',
        'msg_project_created': '✓ Създаден е нов проект с история: {directory}',
        'msg_story_file': 'Файл с история',
        'msg_images_directory': 'Директория с изображения',
        'msg_next_steps': 'Следващи стъпки',
        'msg_step_edit': 'Редактирайте {file}',
        'msg_step_add_images': 'Добавете изображения към {directory}/',
        'msg_step_compile': 'Изпълнете: python -m pick_a_page компилирай {file}',
        
        # Story template
        'template_welcome': 'Добре дошли във вашата нова история!',
        'template_beginning': 'Това е началото. Какво се случва след това зависи от вас.',
        'template_continue': 'Продължете',
        'template_body': 'Напишете историята си тук. Използвайте **удебелен** и *курсив* за акцент.',
        'template_add_images': 'Добавете изображения с: ![Описание](images/вашето-изображение.jpg)',
        'template_choices': 'Създайте избори, като напишете: [[Текст на избора]]',
        'template_end': 'Краят.',
        'template_author': 'Вашето Име',
        
        # Errors
        'error_generic': 'Грешка',
        
        # Web UI - Navigation
        'web_tab_library': '📚 Библиотека с Истории',
        'web_tab_editor': '✏️ Редактор на Истории',
        'web_tab_reader': '📖 Четец на Истории',
        
        # Web UI - Titles
        'web_title_library': '📖 Моята Колекция от Истории',
        'web_title_editor': '✨ Създайте Вашата История',
        
        # Web UI - Buttons
        'web_btn_play': 'Пусни Историята',
        'web_btn_edit': 'Редактирай Историята',
        'web_btn_new': 'Нова История',
        'web_btn_validate': 'Валидирай',
        'web_btn_save': 'Запази',
        'web_btn_compile': 'Компилирай и Пусни',
        
        # Web UI - Messages
        'web_loading_stories': 'Зареждане на вашите истории...',
        'web_empty_title': 'Все още няма истории',
        'web_empty_text': 'Кликнете на "Нова История", за да създадете първото си приключение!',
        'web_by': 'от',
        'web_sections': 'раздели',
        'web_editing': 'Редактиране',
        'web_msg_loading': 'Зареждане на историята...',
        'web_msg_errors': 'Грешки',
        'web_msg_error': 'Грешка',
        'web_msg_loaded': 'Заредено',
        'web_msg_ready': 'Готово за писане на нова история!',
        'web_msg_empty': 'Редакторът е празен!',
        'web_msg_valid': 'Историята е валидна! Намерени',
        'web_msg_validation_errors': 'Грешки при валидация',
        'web_msg_saved': 'Запазено като',
        'web_msg_unknown_error': 'Неизвестна грешка',
        'web_msg_compiling': 'Компилиране на историята...',
        'web_msg_compilation_errors': 'Грешки при компилация',
        
        # Web UI - Prompts
        'web_prompt_save': 'Запази като:',
        
        # Web UI - New Story Template
        'web_new_story_title': 'Моето Ново Приключение',
        'web_new_story_author': 'Вашето Име',
        'web_new_story_content': 'Напишете историята си тук...',
        'web_new_story_choice': 'Направете избор',
        'web_new_story_continue': 'Продължете приключението си!',
        
        # Web UI - Editor Placeholder
        'web_editor_placeholder': 'Напишете приключението си тук...\n\nПримерен формат:\n\n---\ntitle: Моето Приключение\nauthor: Вашето Име\n---\n\n[[beginning]]\n\nСъбуждате се на мистериозно място...\n\n[[Изследвайте]]\n[[Върнете се да спите]]\n\n---\n\n[[Изследвайте]]\n\nОткривате нещо невероятно!',
    }
}


def set_language(lang: str) -> None:
    """
    Set the current language for translations.
    
    Args:
        lang: Language code ('en', 'nl', 'it', 'es', 'fr', 'pt', 'de', 'ru', 'zh', 'hi', 'ar', 'bn', 'ur', 'id', 'bg')
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
        Current language code ('en', 'nl', 'it', 'es', 'fr', 'pt', 'de', 'ru', 'zh', 'hi', 'ar', 'bn', 'ur', 'id', 'bg')
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


def get_available_languages() -> Dict[str, Dict[str, str]]:
    """
    Get all available languages with their metadata.
    
    Returns:
        Dictionary mapping language codes to their info (name and flag)
    """
    return LANGUAGE_INFO.copy()


def get_language_codes() -> list[str]:
    """
    Get list of all available language codes.
    
    Returns:
        List of language codes sorted alphabetically
    """
    return sorted(LANGUAGE_INFO.keys())
