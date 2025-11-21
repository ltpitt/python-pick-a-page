# Repository Instructions for AI Agents

## Project Overview

**python-pick-a-page** is an interactive story book tool designed for teaching programming to children. It converts Markdown-style stories with choice-based navigation into:
1. A playable web application (single HTML file with embedded JavaScript)
2. A printable book (PDF-ready with proper page breaks)

### Target Audience
- Primary: 8-year-old learning programming
- Platform: Mac OS X 10.5 with Python 3.10+ (via Tigerbrew)
- Goal: Simple, fun, educational tool for creating "Choose Your Own Adventure" style stories

### Key Design Principles
1. **Simplicity**: Easy syntax for children to understand
2. **Zero external dependencies**: Use Python 3.10+ standard library only
3. **TDD-first**: All features driven by tests (Red → Green → Refactor)
4. **Modern IF UX**: Scrolling text, prominent buttons, clean typography (inspired by Squiffy/Twine)

## Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Verify Python version (should be 3.10+)
python --version
```

### 2. Install Dependencies

```bash
# Install development dependencies
pip install -r requirements.txt

# Or use Makefile
make install
```

### 3. Run Tests

```bash
# Run all tests with coverage
make test

# Run tests in watch mode (continuous)
make test-watch

# Generate detailed coverage report
make coverage

# Run linting
make lint
```

## Project Structure

```
python-pick-a-page/
├── pick_a_page/           # Main package
│   ├── __init__.py
│   ├── __main__.py        # CLI entry point
│   ├── compiler.py        # Story parser and validator
│   ├── generator.py       # HTML/CSS/JS generator
│   └── templates.py       # HTML/CSS/JS templates
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_compiler.py   # 21 tests for parser
│   ├── test_generator.py  # 18 tests for HTML generator
│   ├── test_integration.py # 24 end-to-end tests
│   └── fixtures/          # Sample story files for testing
│       ├── valid_story.txt      # Complete working story
│       ├── broken_links.txt     # Story with invalid links
│       ├── with_images.txt      # Story with image references
│       ├── no_choices.txt       # Story ending test
│       └── images/              # Test images
├── output/                # Generated stories (gitignored)
├── examples/              # Example stories
│   ├── first_adventure.txt
│   ├── treasure_hunt.txt
│   └── template.txt
├── Makefile              # Development automation
├── requirements.txt      # Python dependencies
├── README.md            # User documentation
├── AGENTS.md           # This file (for AI agents)
└── LICENSE
```

## Story Format

### Basic Syntax

```markdown
---
title: My First Adventure
author: Your Name
---

[[beginning]]:
You wake up in a mysterious forest. The sun is shining through the tall trees.

What do you want to do?

[[Explore the forest]]
[[Follow the path]]

---

[[Explore the forest]]:
You venture deeper into the forest and discover a sparkling stream.

[[Follow the stream]]
[[Go back|beginning]]

---

[[Follow the path]]:
The path leads you to a small cottage with smoke coming from the chimney.

You found a safe place!

---

[[Follow the stream]]:
You follow the stream and find a treasure chest filled with gold!

You won!
```

**Key Points:**
- `[[section-name]]:` defines a section (colon is required)
- `[[Choice text]]` creates a button linking to section "choice-text" (normalized)
- `[[Display|target]]` creates button with custom text
- `---` separates sections
- First section in file is the starting point
- Sections without choices are endings

### Image Support

```markdown
![A mysterious door](images/door.jpg)

The door looks ancient and mysterious.

[[Open the door]]
[[Walk away]]
```

### Metadata (Required)

```markdown
---
title: The Great Adventure
author: My Name
---

[[beginning]]:
The story begins here...
```

**Required fields:** `title`, `author`

## Test-Driven Development Workflow

### TDD Cycle

1. **RED**: Write a failing test that describes the desired behavior
2. **GREEN**: Write the minimal code to make the test pass
3. **REFACTOR**: Clean up code while keeping tests green

### Example TDD Session

```python
# tests/test_compiler.py

def test_parse_basic_section():
    """Parser should extract section name and content from valid story."""
    story = """
[[Start]]:
Welcome to the adventure!
[[Next]]
"""
    result = parse_story(story)
    
    assert len(result.sections) == 1
    assert result.sections[0].name == "Start"
    assert "Welcome to the adventure!" in result.sections[0].content
    assert "Next" in result.sections[0].choices
```

### Running Tests

```bash
# Run specific test file
pytest tests/test_compiler.py -v

# Run specific test
pytest tests/test_compiler.py::test_parse_basic_section -v

# Run with coverage
make test

# Watch mode for continuous testing
make test-watch
```

## Code Quality Standards

### Coverage Goals
- **Current**: 92% overall coverage (63 tests passing)
  - `compiler.py`: 97% coverage (21 tests)
  - `generator.py`: 90% coverage (18 tests)
  - `test_integration.py`: 24 end-to-end tests
- **Target**: Maintain >85% code coverage
- Focus on behavior testing, not implementation details

### Testing Guidelines
1. **Test behavior, not implementation**: Tests should describe what the code does, not how
2. **Clear test names**: Use `test_<action>_<expected_result>` pattern
3. **One assertion per test**: Prefer focused tests over large ones
4. **Use fixtures**: Share test data via fixtures in `tests/fixtures/`
5. **Mock external dependencies**: Use `unittest.mock` or `pytest` fixtures

### Code Style
- Follow PEP 8
- Use type hints where helpful (Python 3.10+ syntax)
- Keep functions small and focused
- Document public APIs with docstrings
- Use meaningful variable names (child-friendly context)

## Makefile Targets

```bash
make help          # Show all available targets
make install       # Install dependencies
make test          # Run tests with coverage
make test-watch    # Continuous testing
make coverage      # Detailed coverage report
make lint          # Run linting (flake8/pylint)
make clean         # Remove build artifacts
make example       # Build example stories
```

## Common Tasks

### Adding a New Feature

1. **Write the test first** (RED)
   ```bash
   # Edit tests/test_compiler.py or appropriate test file
   # Run: make test (should fail)
   ```

2. **Implement the feature** (GREEN)
   ```bash
   # Edit pick_a_page/compiler.py or appropriate module
   # Run: make test (should pass)
   ```

3. **Refactor if needed** (REFACTOR)
   ```bash
   # Clean up code
   # Run: make test (should still pass)
   ```

### Creating a Test Fixture

```bash
# Add new story file to tests/fixtures/
echo "[[Start]]:
Hello world!
[[End]]

---

[[End]]:
The end." > tests/fixtures/my_test_story.txt
```

### Running Examples

```bash
# Compile an example story
python -m pick_a_page examples/first_adventure.txt

# Initialize a new story
python -m pick_a_page init my_new_story

# Validate a story
python -m pick_a_page validate examples/treasure_hunt.txt
```

## Dependencies Rationale

### Required (pytest ecosystem)
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `pytest-watch`: Continuous testing

### Optional (code quality)
- `flake8` or `pylint`: Linting
- `black`: Auto-formatting (if desired)
- `mypy`: Type checking (if using type hints)

### NOT Required
- No external libraries for HTML generation (use stdlib only)
- No external libraries for image processing (use `base64` stdlib)
- No external libraries for Markdown (simple regex parsing sufficient)

## Troubleshooting

### Virtual Environment Issues

```bash
# Deactivate current venv
deactivate

# Remove old venv
rm -rf .venv

# Create fresh venv
python3 -m venv .venv
source .venv/bin/activate
make install
```

### Test Failures

```bash
# Run tests with verbose output
pytest -vv

# Run specific failing test
pytest tests/test_compiler.py::test_parse_basic_section -vv

# See print statements in tests
pytest -s
```

### Coverage Issues

```bash
# Generate HTML coverage report
make coverage
open htmlcov/index.html  # View in browser

# Find untested code
coverage report --show-missing
```

## Contributing Guidelines

1. **Always start with a test**: No code without a test
2. **Keep the build green**: Don't commit failing tests
3. **Write clear commit messages**: Describe the behavior added/fixed
4. **Update tests when refactoring**: Tests are documentation
5. **Ask before adding dependencies**: Prefer stdlib solutions

## Technical Constraints

### Python Version
- **Minimum**: Python 3.10
- **Target Platform**: Mac OS X 10.5 with Python 3.10+ via Tigerbrew
- Use f-strings, type hints, match statements (Python 3.10+ features)

### Standard Library Only
- HTML generation: `string.Template`, `html` module
- Image embedding: `base64` module
- File operations: `pathlib`, `zipfile`
- Argument parsing: `argparse`
- Regular expressions: `re`
- Testing: `unittest` (or pytest as dev dependency)

### Output Requirements
1. **Web App**: Single `index.html` with embedded CSS/JS, Base64 images
2. **ZIP Package**: `story_name.zip` containing HTML + original images + source
3. **Print-Ready**: CSS `@media print` rules for A4 paper with page breaks

## Design Patterns

### Compiler (Parser)
- Input: Story text file
- Output: Internal data structure (dataclasses: Story, Section, Choice, Image)
- Responsibilities: Parse, validate links, extract metadata, normalize section names
- **Implementation**: Uses regex for parsing, validates all links, detects orphaned sections
- **Current State**: 97% coverage, 130 statements, 4 lines uncovered

### Generator
- Input: Parsed story data structure
- Output: HTML string with embedded CSS/JS
- Responsibilities: Template rendering, Base64 encoding, Markdown conversion, print styles
- **Implementation**: Uses string templates, embeds images as Base64, converts bold/italic
- **Current State**: 90% coverage, 70 statements, 7 lines uncovered

### Templates (templates.py)
- **CSS**: Squiffy-inspired clean design, responsive layout, print styles
- **JavaScript**: Event delegation for dynamic content, section cloning for backtracking
- **Navigation Model**: 
  - First-time sections: `appendChild()` moves section to end for chronological order
  - Revisited sections: `cloneNode(true)` creates fresh copy with enabled buttons
  - Buttons in current section disabled after click to show reading history

### CLI
- Input: Command-line arguments via argparse
- Output: ZIP file with compiled HTML, images, and source
- Commands: `compile`, `validate`, `init`
- **Current State**: Implemented but not yet tested (0% coverage)

## Learning Resources

For understanding the project inspiration:
- Squiffy: https://github.com/textadventures/squiffy
- Twine: https://twinery.org/
- Interactive Fiction: https://en.wikipedia.org/wiki/Interactive_fiction
- Choose Your Own Adventure books

## Questions?

When implementing features, always consider:
1. **Is there a test for this?** (TDD)
2. **Can this use stdlib only?** (No external deps)
3. **Is this simple enough for an 8-year-old to understand?** (Child-friendly)
4. **Does this follow the Squiffy/Twine UX patterns?** (Modern IF UX)
