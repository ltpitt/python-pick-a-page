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


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Pick-a-Page: Create interactive story books',
        prog='pick-a-page'
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile a story to HTML')
    compile_parser.add_argument('input', type=Path, help='Input story file')
    compile_parser.add_argument('-o', '--output', type=Path, help='Output directory (default: output/)')
    compile_parser.add_argument('--no-zip', action='store_true', help='Do not create ZIP file')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a story file')
    validate_parser.add_argument('input', type=Path, help='Input story file')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new story')
    init_parser.add_argument('name', help='Story name')
    init_parser.add_argument('-d', '--directory', type=Path, help='Output directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'compile':
            return compile_story(args)
        elif args.command == 'validate':
            return validate_story_file(args)
        elif args.command == 'init':
            return init_story(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def compile_story(args):
    """Compile a story file to HTML."""
    input_file = args.input
    
    if not input_file.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        return 1
    
    # Read story
    print(f"Reading story from {input_file}...")
    content = input_file.read_text()
    
    # Parse and validate
    print("Parsing story...")
    compiler = StoryCompiler()
    try:
        story = compiler.parse(content)
    except ValidationError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        return 1
    
    print("Validating story...")
    errors = compiler.validate(story)
    if errors:
        print("Validation errors found:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    
    # Generate HTML
    print("Generating HTML...")
    generator = HTMLGenerator()
    html = generator.generate(story, base_path=input_file.parent)
    
    # Determine output directory
    output_dir = args.output if args.output else Path('output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write HTML file
    story_name = input_file.stem
    html_file = output_dir / f"{story_name}.html"
    html_file.write_text(html)
    print(f"Created: {html_file}")
    
    # Create ZIP if requested
    if not args.no_zip:
        zip_file = output_dir / f"{story_name}.zip"
        print(f"Creating ZIP archive: {zip_file}")
        
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
        
        print(f"Created: {zip_file}")
    
    print("\n✓ Story compiled successfully!")
    return 0


def validate_story_file(args):
    """Validate a story file."""
    input_file = args.input
    
    if not input_file.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        return 1
    
    # Read and parse
    content = input_file.read_text()
    compiler = StoryCompiler()
    
    try:
        story = compiler.parse(content)
    except ValidationError as e:
        print(f"✗ Parse error: {e}", file=sys.stderr)
        return 1
    
    # Validate
    errors = compiler.validate(story)
    
    if errors:
        print(f"✗ Found {len(errors)} validation error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    
    print("✓ Story is valid!")
    print(f"  Title: {story.metadata.title}")
    if story.metadata.author:
        print(f"  Author: {story.metadata.author}")
    print(f"  Sections: {len(story.sections)}")
    
    return 0


def init_story(args):
    """Initialize a new story project."""
    story_name = args.name
    directory = args.directory if args.directory else Path(story_name)
    
    if directory.exists():
        print(f"Error: Directory already exists: {directory}", file=sys.stderr)
        return 1
    
    # Create directory structure
    directory.mkdir(parents=True)
    images_dir = directory / 'images'
    images_dir.mkdir()
    
    # Create template story file
    template = f"""---
title: {story_name.replace('-', ' ').replace('_', ' ').title()}
author: Your Name
---

[[start]]

Welcome to your new story!

This is the beginning. What happens next is up to you.

[[Continue]]

---

[[Continue]]

Write your story here. Use **bold** and *italic* for emphasis.

Add images with: ![Description](images/your-image.jpg)

Create choices by writing: [[Choice text]]

The end.
"""
    
    story_file = directory / f"{story_name}.txt"
    story_file.write_text(template)
    
    print(f"✓ Created new story project: {directory}")
    print(f"  Story file: {story_file}")
    print(f"  Images directory: {images_dir}")
    print(f"\nNext steps:")
    print(f"  1. Edit {story_file}")
    print(f"  2. Add images to {images_dir}/")
    print(f"  3. Run: python -m pick_a_page compile {story_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
