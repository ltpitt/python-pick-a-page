# Repository Instructions for AI Agents

> **Instructions for AI**: This file contains critical context for working on this codebase. Read it completely before making changes. All design decisions here are intentional and battle-tested.

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
2. **Zero external dependencies**: Use Python 3.10+ standard library only (NON-NEGOTIABLE)
3. **TDD-first**: All features driven by tests (Red → Green → Refactor) - NO CODE WITHOUT TESTS
4. **Modern IF UX**: Scrolling text, prominent buttons, clean typography (inspired by Squiffy/Twine)

### Critical Constraints (DO NOT VIOLATE)
- ⛔ **NO external runtime dependencies** - Only Python stdlib (pytest is dev-only)
- ⛔ **NO package managers** for story format (no YAML, TOML libraries)
- ⛔ **NO markdown libraries** - Use simple regex parsing only
- ⛔ **NO HTML parsers** - Use string templates only
- ✅ **DO maintain >85% test coverage** on all new code
- ✅ **DO write tests before implementation** (TDD cycle)
- ✅ **DO keep backward compatibility** with existing story format

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

[[beginning]]

You wake up in a mysterious forest. The sun is shining through the tall trees.

What do you want to do?

[[Explore the forest]]
[[Follow the path]]

---

[[Explore the forest]]

You venture deeper into the forest and discover a sparkling stream.

[[Follow the stream]]
[[Go back|beginning]]

---

[[Follow the path]]

The path leads you to a small cottage with smoke coming from the chimney.

You found a safe place!

---

[[Follow the stream]]

You follow the stream and find a treasure chest filled with gold!

You won!
```

**Key Points:**
- `[[section-name]]` defines a section (simple format, no colon - easy for kids!)
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

## Decision Trees for Common Scenarios

### When Asked to Add a Feature

```
1. Does it require external dependencies?
   NO  → Proceed to step 2
   YES → Refuse or find stdlib alternative

2. Is there a test for this behavior?
   YES → Proceed to step 3
   NO  → Write test first (RED), then implement

3. Does it change story format syntax?
   NO  → Implement and maintain backward compatibility
   YES → Discuss with user first (breaking change)

4. Does it affect navigation/UI?
   NO  → Implement with standard patterns
   YES → Test in browser, verify chronological order
```

### When Asked to Fix a Bug

```
1. Is there a failing test that reproduces it?
   YES → Fix code until test passes
   NO  → Write failing test first, then fix

2. Does it affect existing tests?
   NO  → Verify all tests still pass
   YES → Update tests if behavior change is intentional

3. Is it a navigation/rendering issue?
   YES → Check: event delegation, appendChild, section order
   NO  → Check: parser regex, validation logic
```

### When Asked to Refactor

```
1. Are all tests passing before refactoring?
   YES → Proceed
   NO  → Fix tests first (don't refactor on red)

2. Does refactoring maintain coverage?
   YES → Proceed
   NO  → Add missing tests

3. Does it simplify without over-engineering?
   YES → Commit
   NO  → Discuss trade-offs with user
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

## Critical Implementation Notes

### Known Issues and Solutions

**SOLVED: Navigation Bug (DO NOT REINTRODUCE)**
- ❌ **Wrong**: Setting `display: block` on template sections leaves them in original DOM position
- ✅ **Correct**: Use `appendChild()` to MOVE sections to end for chronological order
- **Why**: Users navigate non-linearly, sections must append in reading order not generation order
- **Test**: `test_integration.py` covers backtracking paths

**SOLVED: Event Handler Bug**
- ❌ **Wrong**: Adding click handlers directly to buttons (fails on cloned sections)
- ✅ **Correct**: Event delegation on parent `#story` container
- **Why**: Cloned sections need handlers without re-attaching events

**Parser Edge Cases**
- Section names are normalized: `"Explore the Forest"` → `"explore-the-forest"`
- Empty lines between choices are preserved in content (not stripped)
- Images MUST be embedded as Base64 (no external references in HTML)

## Architecture Decision Records

### Why Event Delegation?
- **Problem**: Dynamically cloned sections lose event handlers
- **Solution**: Single listener on parent container catches all button clicks
- **Trade-off**: Slight complexity in event handling logic vs reliable dynamic content
- **Status**: Working perfectly, DO NOT change to individual handlers

### Why Section Cloning?
- **Problem**: Users want to see full reading history including backtracking
- **Solution**: Clone sections with `cloneNode(true)` when revisiting
- **Trade-off**: Duplicated DOM nodes vs clean scrolling history
- **Status**: Matches Squiffy UX, keep as-is

### Why No Markdown Library?
- **Problem**: Need bold/italic support but no dependencies allowed
- **Solution**: Simple regex for `**bold**` and `*italic*`
- **Trade-off**: Limited markdown vs zero dependencies
- **Status**: Sufficient for target audience, don't over-engineer

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

## Workflow Examples

### Example 1: Adding Image Alt Text Support

**User Request**: "Add support for image alt text in the parser"

**Correct Workflow**:
```bash
# Step 1: Write failing test (RED)
# Edit tests/test_compiler.py
def test_parse_image_with_alt_text():
    story = "![A door](door.jpg)"
    result = parse_story(story)
    assert result.images[0].alt_text == "A door"

# Step 2: Run test (should fail)
make test

# Step 3: Implement feature (GREEN)
# Edit pick_a_page/compiler.py
# Add regex group for alt text in _parse_images()

# Step 4: Run test (should pass)
make test

# Step 5: Verify coverage maintained
make coverage
```

### Example 2: Investigating Navigation Issue

**User Report**: "Sections appear in wrong order"

**Correct Investigation**:
```bash
# Step 1: Reproduce with test
# Check test_integration.py for path coverage

# Step 2: Check known issues section above
# → Navigation Bug: appendChild() vs display:block

# Step 3: Verify JavaScript in templates.py
# → Ensure navigateToSection() uses appendChild()

# Step 4: Test in browser if needed
python -m pick_a_page compile tests/fixtures/valid_story.txt
open output/valid_story.html

# Step 5: Add regression test if missing
```

### Example 3: Optimizing Parser Performance

**User Request**: "Parser is slow on large files"

**Correct Approach**:
```bash
# Step 1: Profile first
python -m cProfile -s cumtime -m pick_a_page compile large_story.txt

# Step 2: Identify bottleneck (regex, validation, etc)

# Step 3: Write performance test
def test_parse_large_story_performance():
    # Generate 1000-section story
    assert parse_time < 1.0  # seconds

# Step 4: Optimize with test coverage maintained
# Example: Cache normalized names, batch validations

# Step 5: Verify optimization doesn't break existing tests
make test
```

## Questions to Ask Yourself Before Committing

When implementing features, always verify:
1. ✅ **Is there a test for this?** (TDD) - If NO, write test first
2. ✅ **Does it use stdlib only?** (No external deps) - If NO, find alternative
3. ✅ **Is it simple enough for an 8-year-old to understand?** (Child-friendly) - If NO, simplify
4. ✅ **Does it follow Squiffy/Twine UX patterns?** (Modern IF UX) - If NO, reconsider
5. ✅ **Do all 63 tests still pass?** (Regression) - If NO, fix before committing
6. ✅ **Is coverage >85%?** (Quality) - If NO, add tests
7. ✅ **Is the commit message descriptive?** (Documentation) - If NO, rewrite

## Getting Help

If you're unsure about a design decision:
1. Check "Critical Implementation Notes" section above
2. Check "Architecture Decision Records" for why things are the way they are
3. Run tests to see expected behavior: `make test`
4. Check git history for context: `git log --oneline --grep="keyword"`
5. Ask the user rather than guessing and breaking things
