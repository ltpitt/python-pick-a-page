"""
Command-line interface for pick-a-page.

Provides commands for compiling stories, validating them, and initializing new projects.
"""

import sys
import argparse
from pathlib import Path
import zipfile
import shutil
from .compiler import StoryCompiler, ValidationError
from .generator import HTMLGenerator
from .i18n import _, init_language_from_env, set_language


def main():
    """Main CLI entry point."""
    # Initialize language from environment
    init_language_from_env()
    
    parser = argparse.ArgumentParser(
        description=_('cli_description'),
        prog='pick-a-page'
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('--lang', choices=['en', 'nl', 'it'], help=_('arg_lang_help'))
    
    subparsers = parser.add_subparsers(dest='command', help=_('cli_command_help'))
    
    # Compile command
    compile_parser = subparsers.add_parser(_('cmd_compile'), help=_('cmd_compile_help'))
    compile_parser.add_argument('input', type=Path, help=_('arg_input_help'))
    compile_parser.add_argument('-o', '--output', type=Path, help=_('arg_output_help'))
    compile_parser.add_argument('--no-zip', action='store_true', help=_('arg_no_zip_help'))
    
    # Validate command
    validate_parser = subparsers.add_parser(_('cmd_validate'), help=_('cmd_validate_help'))
    validate_parser.add_argument('input', type=Path, help=_('arg_input_help'))
    
    # Init command
    init_parser = subparsers.add_parser(_('cmd_init'), help=_('cmd_init_help'))
    init_parser.add_argument('name', help=_('arg_name_help'))
    init_parser.add_argument('-d', '--directory', type=Path, help=_('arg_directory_help'))
    
    args = parser.parse_args()
    
    # Apply language from command line if specified
    if hasattr(args, 'lang') and args.lang:
        set_language(args.lang)
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        # Map localized command names to handlers
        if args.command in [_('cmd_compile'), 'compile']:
            return compile_story(args)
        elif args.command in [_('cmd_validate'), 'validate']:
            return validate_story_file(args)
        elif args.command in [_('cmd_init'), 'init']:
            return init_story(args)
    except Exception as e:
        print(f"{_('error_generic')}: {e}", file=sys.stderr)
        return 1
    
    return 0


def compile_story(args):
    """Compile a story file to HTML."""
    input_file = args.input
    
    if not input_file.exists():
        print(f"{_('error_generic')}: {_('msg_file_not_found')}: {input_file}", file=sys.stderr)
        return 1
    
    # Read story
    print(_('msg_reading_story', path=input_file))
    content = input_file.read_text()
    
    # Parse and validate
    print(_('msg_parsing_story'))
    compiler = StoryCompiler()
    try:
        story = compiler.parse(content)
    except ValidationError as e:
        print(f"{_('msg_parse_error')}: {e}", file=sys.stderr)
        return 1
    
    print(_('msg_validating_story'))
    errors = compiler.validate(story)
    if errors:
        print(f"{_('msg_validation_errors')}:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    
    # Generate HTML
    print(_('msg_generating_html'))
    generator = HTMLGenerator()
    html = generator.generate(story, base_path=input_file.parent)
    
    # Determine output directory
    output_dir = args.output if args.output else Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write HTML file
    story_name = input_file.stem
    html_file = output_dir / f"{story_name}.html"
    html_file.write_text(html)
    print(f"{_('msg_created')}: {html_file}")
    
    # Create ZIP if requested
    if not args.no_zip:
        zip_file = output_dir / f"{story_name}.zip"
        print(_('msg_creating_zip', path=zip_file))
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add HTML file
            zf.write(html_file, f"{story_name}.html")
            
            # Add source story file
            zf.write(input_file, f"{story_name}.txt")
            
            # Add any images referenced in the story
            for section in story.sections:
                for image in section.images:
                    image_path = input_file.parent / image.path
                    if image_path.exists():
                        zf.write(image_path, image.path)
        
        print(f"{_('msg_created')}: {zip_file}")
    
    print(f"\n{_('msg_compile_success')}")
    return 0


def validate_story_file(args):
    """Validate a story file."""
    input_file = args.input
    
    if not input_file.exists():
        print(f"{_('error_generic')}: {_('msg_file_not_found')}: {input_file}", file=sys.stderr)
        return 1
    
    # Read and parse
    content = input_file.read_text()
    compiler = StoryCompiler()
    
    try:
        story = compiler.parse(content)
    except ValidationError as e:
        print(f"{_('msg_validate_parse_error')}: {e}", file=sys.stderr)
        return 1
    
    # Validate
    errors = compiler.validate(story)
    
    if errors:
        print(f"{_('msg_validation_error_count', count=len(errors))}:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    
    print(_('msg_story_valid'))
    print(f"  {_('msg_title')}: {story.metadata.title}")
    if story.metadata.author:
        print(f"  {_('msg_author')}: {story.metadata.author}")
    print(f"  {_('msg_sections')}: {len(story.sections)}")
    
    return 0


def init_story(args):
    """Initialize a new story project."""
    story_name = args.name
    directory = args.directory if args.directory else Path(story_name)
    
    if directory.exists():
        print(f"{_('error_generic')}: {_('msg_directory_exists')}: {directory}", file=sys.stderr)
        return 1
    
    # Create directory structure
    directory.mkdir(parents=True)
    images_dir = directory / 'images'
    images_dir.mkdir()
    
    # Create template story file
    template = f"""---
title: {story_name.replace('-', ' ').replace('_', ' ').title()}
author: {_('template_author')}
---

[[start]]

{_('template_welcome')}

{_('template_beginning')}

[[{_('template_continue')}]]

---

[[{_('template_continue')}]]

{_('template_body')}

{_('template_add_images')}

{_('template_choices')}

{_('template_end')}
"""
    
    story_file = directory / f"{story_name}.txt"
    story_file.write_text(template)
    
    print(_('msg_project_created', directory=directory))
    print(f"  {_('msg_story_file')}: {story_file}")
    print(f"  {_('msg_images_directory')}: {images_dir}")
    print(f"\n{_('msg_next_steps')}:")
    print(f"  1. {_('msg_step_edit', file=story_file)}")
    print(f"  2. {_('msg_step_add_images', directory=images_dir)}")
    print(f"  3. {_('msg_step_compile', file=story_file)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
