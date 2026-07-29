# Pick-a-Page Improvement Loop — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local, Copilot-CLI-powered improvement loop that drives Pick-a-Page through a child's full user experience, grades it against a deterministic rubric, and asks a configurable model for the top 3 child-UX improvements.

**Architecture:** A standalone `loop/` harness that observes the app in `backend/` without modifying it. `run.py` orchestrates three phases — capture (Playwright journey), verify (deterministic rubric), analyze (Copilot CLI hill-climb) — writing timestamped artifacts. Model choice is tiered (cheap/balanced/strong) and env-overridable.

**Tech Stack:** Python 3.10+, Flask (existing app), Playwright (browser automation), pytest, Copilot CLI, Make.

**Design spec:** `docs/superpowers/specs/2026-07-29-improvement-loop-design.md`

---

## File Structure

- Create: `loop/__init__.py` — marks the harness a package.
- Create: `loop/NORTH_STAR.md` — north star + rubric weighting (the vision).
- Create: `loop/config.py` — model tiers, selection precedence, run settings.
- Create: `loop/prompt.md` — analysis instructions ("top 3 improvements").
- Create: `loop/rubric.py` — deterministic grader over a captured trace.
- Create: `loop/journey.py` — Playwright child-user journey + trace capture.
- Create: `loop/analyze.py` — assembles the prompt, calls Copilot CLI.
- Create: `loop/run.py` — orchestrator: capture → verify → analyze.
- Create: `tests/loop/__init__.py` — test package marker.
- Create: `tests/loop/test_config.py` — model-selection precedence tests.
- Create: `tests/loop/test_rubric.py` — grader tests with synthetic traces.
- Create: `tests/loop/test_analyze.py` — prompt assembly + CLI invocation tests.
- Modify: `.gitignore` — ignore `loop/artifacts/`.
- Modify: `Makefile` — add a `loop` target.
- Modify: `requirements.txt` — add `playwright`.

Each file has one responsibility. `config.py`, `rubric.py`, and `analyze.py` hold the testable pure logic; `journey.py` and `run.py` are thin I/O wrappers exercised by a smoke run.

---

## Task 1: Package scaffolding and North Star

**Files:**
- Create: `loop/__init__.py`
- Create: `loop/NORTH_STAR.md`
- Create: `tests/loop/__init__.py`

- [ ] **Step 1: Create the loop package marker**

Create `loop/__init__.py`:

```python
"""Pick-a-Page improvement loop harness.

Observes the app in ``backend/`` and proposes child-UX improvements.
Never modifies application code.
"""
```

- [ ] **Step 2: Create the test package marker**

Create `tests/loop/__init__.py`:

```python
```

(An empty file — just marks the directory as a package.)

- [ ] **Step 3: Write the North Star**

Create `loop/NORTH_STAR.md`:

```markdown
# Pick-a-Page — North Star

**Pick-a-Page helps children (8+) learn to write Markdown by making it fun.**

Every improvement is judged first on the child's experience: is it delightful,
obvious, and rewarding to use? Education is the vehicle; fun and ease-of-use are
the goal.

## Rubric (highest weight first)

1. **Fun & delight** — does it feel playful and rewarding for a child?
2. **Ease of use / low friction** — can an 8-year-old proceed without adult help?
3. **Clarity of the Markdown-learning journey** — does the child learn Markdown naturally?
4. **Correctness & quality** — compiles cleanly, no broken choices, accessible,
   mobile-first, tests pass.

When ranking improvements, an item that raises fun or lowers friction for a
child outranks a purely technical correctness fix of similar effort.
```

- [ ] **Step 4: Verify files exist**

Run: `ls loop/__init__.py loop/NORTH_STAR.md tests/loop/__init__.py`
Expected: all three paths listed, no error.

- [ ] **Step 5: Commit**

```bash
git add loop/__init__.py loop/NORTH_STAR.md tests/loop/__init__.py
git commit -m "feat(loop): scaffold harness package and north star"
```

---

## Task 2: Model configuration with tiered selection

**Files:**
- Create: `loop/config.py`
- Test: `tests/loop/test_config.py`

- [ ] **Step 1: Write the failing test**

Create `tests/loop/test_config.py`:

```python
import importlib

import loop.config as config


def reload_config(monkeypatch, env):
    for key in ("LOOP_MODEL", "LOOP_TIER"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(config)


def test_default_is_balanced_tier(monkeypatch):
    cfg = reload_config(monkeypatch, {})
    assert cfg.resolve_model() == cfg.TIERS["balanced"]


def test_tier_env_selects_tier(monkeypatch):
    cfg = reload_config(monkeypatch, {"LOOP_TIER": "strong"})
    assert cfg.resolve_model() == cfg.TIERS["strong"]


def test_explicit_model_overrides_tier(monkeypatch):
    cfg = reload_config(monkeypatch, {"LOOP_TIER": "strong", "LOOP_MODEL": "custom-x"})
    assert cfg.resolve_model() == "custom-x"


def test_unknown_tier_falls_back_to_default(monkeypatch):
    cfg = reload_config(monkeypatch, {"LOOP_TIER": "nonsense"})
    assert cfg.resolve_model() == cfg.TIERS["balanced"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/loop/test_config.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'loop.config'` (or `AttributeError` on `resolve_model`).

- [ ] **Step 3: Write minimal implementation**

Create `loop/config.py`:

```python
"""Model tiers and run settings for the improvement loop.

Model selection precedence (highest wins):
1. ``LOOP_MODEL`` env var — explicit model id.
2. ``LOOP_TIER`` env var — ``cheap`` | ``balanced`` | ``strong``.
3. Default tier (``balanced``).

Adjust the model ids below to match the models your Copilot CLI exposes
(run ``copilot --help`` or your CLI's model-list command to check).
"""

import os
from pathlib import Path

# Model ids per tier. Edit to match your available Copilot CLI models.
TIERS = {
    "cheap": "gpt-5.4-mini",
    "balanced": "claude-sonnet-4.5",
    "strong": "claude-opus-4.5",
}

DEFAULT_TIER = "balanced"

# Run settings.
SERVER_HOST = os.environ.get("LOOP_HOST", "127.0.0.1")
SERVER_PORT = int(os.environ.get("LOOP_PORT", "8011"))
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
COVERAGE_THRESHOLD = float(os.environ.get("LOOP_COVERAGE_MIN", "85"))
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"


def resolve_model() -> str:
    """Return the model id to use for this run, honoring env overrides."""
    explicit = os.environ.get("LOOP_MODEL")
    if explicit:
        return explicit
    tier = os.environ.get("LOOP_TIER", DEFAULT_TIER)
    return TIERS.get(tier, TIERS[DEFAULT_TIER])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/loop/test_config.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add loop/config.py tests/loop/test_config.py
git commit -m "feat(loop): add tiered model configuration"
```

---

## Task 3: Deterministic rubric grader

**Files:**
- Create: `loop/rubric.py`
- Test: `tests/loop/test_rubric.py`

The grader operates on a `trace` dict (produced later by `journey.py`) plus a
`test_result` dict, so it is pure and testable without a browser.

- [ ] **Step 1: Write the failing test**

Create `tests/loop/test_rubric.py`:

```python
from loop.rubric import grade

PASSING_TRACE = {
    "server_booted": True,
    "console_errors": [],
    "network_errors": [],
    "steps_completed": ["land", "template", "edit", "compile", "play", "i18n"],
    "steps_expected": ["land", "template", "edit", "compile", "play", "i18n"],
    "compile_ok": True,
    "broken_choices": [],
}
PASSING_TESTS = {"passed": True, "coverage": 91.0}


def test_all_checks_pass():
    report = grade(PASSING_TRACE, PASSING_TESTS, coverage_threshold=85.0)
    assert report["passed"] is True
    assert all(c["passed"] for c in report["checks"])


def test_console_error_fails_grade():
    trace = {**PASSING_TRACE, "console_errors": ["TypeError: x is undefined"]}
    report = grade(trace, PASSING_TESTS, coverage_threshold=85.0)
    assert report["passed"] is False
    assert any(c["name"] == "no_console_errors" and not c["passed"] for c in report["checks"])


def test_low_coverage_fails_grade():
    report = grade(PASSING_TRACE, {"passed": True, "coverage": 70.0}, coverage_threshold=85.0)
    assert report["passed"] is False
    assert any(c["name"] == "coverage_threshold" and not c["passed"] for c in report["checks"])


def test_incomplete_journey_fails_grade():
    trace = {**PASSING_TRACE, "steps_completed": ["land", "template"]}
    report = grade(trace, PASSING_TESTS, coverage_threshold=85.0)
    assert report["passed"] is False
    assert any(c["name"] == "journey_complete" and not c["passed"] for c in report["checks"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/loop/test_rubric.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'loop.rubric'`.

- [ ] **Step 3: Write minimal implementation**

Create `loop/rubric.py`:

```python
"""Deterministic grader for a captured loop run.

Runs before any model call so the analysis model can focus on judgment and
taste rather than mechanical bugs. Pure function of the captured trace and the
test result — no browser or server needed.
"""


def grade(trace: dict, test_result: dict, coverage_threshold: float) -> dict:
    """Grade a run trace against deterministic checks.

    Args:
        trace: Captured journey signals (server, console, network, steps, compile).
        test_result: ``{"passed": bool, "coverage": float}`` from the test suite.
        coverage_threshold: Minimum acceptable coverage percentage.

    Returns:
        ``{"passed": bool, "checks": [{"name", "passed", "detail"}, ...]}``.
    """
    checks = [
        _check("server_booted", trace.get("server_booted", False),
               "Flask server booted and served the app"),
        _check("no_console_errors", not trace.get("console_errors"),
               f"console errors: {trace.get('console_errors', [])}"),
        _check("no_network_errors", not trace.get("network_errors"),
               f"network errors: {trace.get('network_errors', [])}"),
        _check("compile_ok", trace.get("compile_ok", False),
               "sample story compiled to HTML"),
        _check("no_broken_choices", not trace.get("broken_choices"),
               f"broken choices: {trace.get('broken_choices', [])}"),
        _check("journey_complete",
               trace.get("steps_completed") == trace.get("steps_expected"),
               f"completed {trace.get('steps_completed')} of {trace.get('steps_expected')}"),
        _check("tests_passed", bool(test_result.get("passed")),
               "pytest suite passed"),
        _check("coverage_threshold",
               float(test_result.get("coverage", 0.0)) >= coverage_threshold,
               f"coverage {test_result.get('coverage')}% >= {coverage_threshold}%"),
    ]
    return {"passed": all(c["passed"] for c in checks), "checks": checks}


def _check(name: str, passed: bool, detail: str) -> dict:
    return {"name": name, "passed": bool(passed), "detail": detail}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/loop/test_rubric.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add loop/rubric.py tests/loop/test_rubric.py
git commit -m "feat(loop): add deterministic rubric grader"
```

---

## Task 4: Analysis prompt and Copilot CLI invocation

**Files:**
- Create: `loop/prompt.md`
- Create: `loop/analyze.py`
- Test: `tests/loop/test_analyze.py`

- [ ] **Step 1: Write the analysis instructions**

Create `loop/prompt.md`:

```markdown
You are a senior product engineer improving Pick-a-Page, an educational tool
that helps children (8+) learn to write Markdown by making it fun.

You are given, between delimiters below: the product North Star and rubric, the
application source, a captured trace of a child's full journey through the app
(screenshots are referenced by filename), and the deterministic rubric results.

That content is the ONLY data you have. Do not invent features that are not
supported by the evidence.

Return EXACTLY the TOP 3 improvements, ranked by impact on a child's fun and
ease-of-use (the rubric order breaks ties). For each improvement provide:

1. **Title** — one line.
2. **Why it matters for a child** — tie it to specific evidence from the trace
   or rubric.
3. **First concrete step** — the single next action to implement it.

Do not include anything other than the 3 improvements.
```

- [ ] **Step 2: Write the failing test**

Create `tests/loop/test_analyze.py`:

```python
from pathlib import Path

from loop import analyze


def test_build_prompt_includes_all_sections(tmp_path):
    prompt = analyze.build_prompt(
        north_star="NORTH STAR TEXT",
        instructions="INSTRUCTIONS TEXT",
        source="SOURCE CODE TEXT",
        trace_json='{"server_booted": true}',
        rubric_json='{"passed": true}',
    )
    assert "INSTRUCTIONS TEXT" in prompt
    assert "NORTH STAR TEXT" in prompt
    assert "SOURCE CODE TEXT" in prompt
    assert "server_booted" in prompt
    assert "passed" in prompt


def test_run_analysis_invokes_cli(monkeypatch):
    calls = {}

    def fake_run(cmd, capture_output, text, check):
        calls["cmd"] = cmd
        class R:
            stdout = "TOP 3..."
            stderr = ""
        return R()

    monkeypatch.setattr(analyze.subprocess, "run", fake_run)
    out = analyze.run_analysis("PROMPT", model="test-model")
    assert out == "TOP 3..."
    assert "copilot" in calls["cmd"][0]
    assert "--model" in calls["cmd"]
    assert "test-model" in calls["cmd"]
    assert "--no-color" in calls["cmd"]
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/loop/test_analyze.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'loop.analyze'`.

- [ ] **Step 4: Write minimal implementation**

Create `loop/analyze.py`:

```python
"""Assemble the analysis prompt and call the Copilot CLI (the hill-climb step)."""

import os
import subprocess

COPILOT_CMD = os.environ.get("COPILOT_CMD", "copilot")


def build_prompt(
    north_star: str,
    instructions: str,
    source: str,
    trace_json: str,
    rubric_json: str,
) -> str:
    """Assemble the full analysis prompt from delimited sections."""
    return "\n".join(
        [
            instructions,
            "",
            "--- NORTH STAR START ---",
            north_star,
            "--- NORTH STAR END ---",
            "",
            "--- SOURCE CODE START ---",
            source,
            "--- SOURCE CODE END ---",
            "",
            "--- RUN TRACE START ---",
            trace_json,
            "--- RUN TRACE END ---",
            "",
            "--- RUBRIC RESULTS START ---",
            rubric_json,
            "--- RUBRIC RESULTS END ---",
            "",
            "Now provide your TOP 3 improvements exactly as specified.",
        ]
    )


def run_analysis(prompt: str, model: str) -> str:
    """Invoke the Copilot CLI with the assembled prompt and return its output."""
    cmd = [COPILOT_CMD, "-p", prompt, "--model", model, "--no-color"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/loop/test_analyze.py -v`
Expected: PASS (2 passed).

- [ ] **Step 6: Commit**

```bash
git add loop/prompt.md loop/analyze.py tests/loop/test_analyze.py
git commit -m "feat(loop): add analysis prompt assembly and Copilot CLI call"
```

---

## Task 5: Playwright child journey with trace capture

**Files:**
- Create: `loop/journey.py`
- Modify: `requirements.txt`

This task adds the browser dependency and the journey. It is thin I/O code
exercised by the smoke run in Task 6, not unit-tested with a mocked browser.

- [ ] **Step 1: Add Playwright to requirements**

Modify `requirements.txt` — add this line at the end:

```
playwright>=1.40.0
```

- [ ] **Step 2: Install Playwright and its browser**

Run: `pip install -r requirements.txt && python -m playwright install chromium`
Expected: install completes; Chromium downloaded.

- [ ] **Step 3: Implement the journey**

Create `loop/journey.py`:

```python
"""Drive Pick-a-Page through a child's full user experience and capture a trace.

Thin wrapper over Playwright. Each step is resilient: a failure is recorded in
the trace (with a screenshot) rather than aborting the whole run, so the
analysis still receives signal.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

STEPS = ["land", "template", "edit", "compile", "play", "i18n"]


def run_journey(base_url: str, shots_dir: Path) -> dict:
    """Run the child journey and return a trace dict.

    Args:
        base_url: URL where the app is served.
        shots_dir: Directory to write per-step screenshots into.

    Returns:
        A trace dict consumed by ``loop.rubric.grade`` and the analysis prompt.
    """
    shots_dir.mkdir(parents=True, exist_ok=True)
    console_errors: list[str] = []
    network_errors: list[str] = []
    steps_completed: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda m: console_errors.append(m.text)
                if m.type == "error" else None)
        page.on("response", lambda r: network_errors.append(f"{r.status} {r.url}")
                if r.status >= 400 else None)

        _step(page, base_url, shots_dir, steps_completed)
        browser.close()

    return {
        "server_booted": bool(steps_completed),
        "console_errors": console_errors,
        "network_errors": network_errors,
        "steps_completed": steps_completed,
        "steps_expected": STEPS,
        # compile_ok / broken_choices are filled by run.py via the compile API.
        "compile_ok": None,
        "broken_choices": [],
    }


def _step(page, base_url: str, shots_dir: Path, done: list[str]) -> None:
    """Execute each journey step, screenshotting and recording completion."""
    def shot(name: str) -> None:
        page.screenshot(path=str(shots_dir / f"{name}.png"))
        done.append(name)

    page.goto(base_url, wait_until="networkidle")
    shot("land")

    # The remaining steps use best-effort selectors; adjust to the real DOM.
    # Each is guarded so one failure does not abort the journey.
    for name, action in [
        ("template", lambda: page.get_by_role("button", name="Template").click()),
        ("edit", lambda: page.locator("textarea").first.fill("# Hello\n\nOnce upon a time.")),
        ("compile", lambda: page.get_by_role("button", name="Compile").click()),
        ("play", lambda: page.get_by_role("button", name="Play").click()),
        ("i18n", lambda: page.locator("select").first.select_option(index=1)),
    ]:
        try:
            action()
            page.wait_for_timeout(300)
            shot(name)
        except Exception:  # noqa: BLE001 — record failure, keep going
            page.screenshot(path=str(shots_dir / f"{name}-FAILED.png"))
```

- [ ] **Step 4: Verify import works**

Run: `python -c "from loop.journey import run_journey, STEPS; print(STEPS)"`
Expected: prints the six step names, no error.

- [ ] **Step 5: Commit**

```bash
git add loop/journey.py requirements.txt
git commit -m "feat(loop): add Playwright child journey with trace capture"
```

> **Note for implementer:** the selectors in `_step` are best-effort. During the
> first smoke run (Task 6) inspect `backend/templates/index.html` and the JS in
> `backend/static/js/` and adjust the selectors to the real DOM. Steps are
> guarded, so wrong selectors degrade to recorded failures rather than crashes.

---

## Task 6: Orchestrator and Make target

**Files:**
- Create: `loop/run.py`
- Modify: `Makefile`
- Modify: `.gitignore`

- [ ] **Step 1: Ignore artifacts**

Modify `.gitignore` — add at the end:

```
# Improvement loop run artifacts
loop/artifacts/
```

- [ ] **Step 2: Implement the orchestrator**

Create `loop/run.py`:

```python
"""Improvement loop orchestrator: capture -> verify -> analyze.

Boots the Flask app in a background thread, runs the child journey, grades the
trace, compiles a sample story to fill compile signals, calls the analysis
model, and writes timestamped artifacts.
"""

import json
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen

from loop import analyze, config, journey, rubric

HERE = Path(__file__).parent
REPO = HERE.parent


def _serve() -> threading.Thread:
    """Start the Flask app in a background daemon thread."""
    from backend.main import app

    thread = threading.Thread(
        target=lambda: app.run(host=config.SERVER_HOST, port=config.SERVER_PORT),
        daemon=True,
    )
    thread.start()
    return thread


def _wait_for_server(url: str, timeout: float = 15.0) -> bool:
    """Poll the server until it responds or the timeout elapses."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urlopen(url)
            return True
        except Exception:  # noqa: BLE001
            time.sleep(0.3)
    return False


def _run_tests() -> dict:
    """Run pytest with coverage and parse pass/fail and coverage percent."""
    proc = subprocess.run(
        ["pytest", "--cov=backend", "--cov-report=term-missing", "-q"],
        cwd=REPO, capture_output=True, text=True,
    )
    coverage = 0.0
    for line in proc.stdout.splitlines():
        if line.strip().startswith("TOTAL"):
            for tok in line.split():
                if tok.endswith("%"):
                    coverage = float(tok.rstrip("%"))
    return {"passed": proc.returncode == 0, "coverage": coverage}


def _compile_sample() -> dict:
    """Compile a known-good sample story to fill compile signals in the trace."""
    from backend.core.compiler import compile_story

    sample = (REPO / "tests" / "fixtures" / "valid_story.txt").read_text()
    try:
        compile_story(sample)
        return {"compile_ok": True, "broken_choices": []}
    except Exception as exc:  # noqa: BLE001
        return {"compile_ok": False, "broken_choices": [str(exc)]}


def _gather_source() -> str:
    """Concatenate the app source so the model can reason over it."""
    parts = []
    for path in sorted(REPO.glob("backend/**/*.py")):
        parts.append(f"--- FILE: {path.relative_to(REPO)} ---")
        parts.append(path.read_text())
    return "\n".join(parts)


def main() -> int:
    run_dir = config.ARTIFACTS_DIR / datetime.now().strftime("%Y-%m-%d-%H%M%S")
    shots = run_dir / "screenshots"
    run_dir.mkdir(parents=True, exist_ok=True)

    print("[loop] 1/3 Capture — booting server and running child journey")
    _serve()
    if not _wait_for_server(config.BASE_URL):
        print("[loop] ERROR: server did not start", file=sys.stderr)
        return 1

    trace = journey.run_journey(config.BASE_URL, shots)
    trace.update(_compile_sample())
    (run_dir / "trace.json").write_text(json.dumps(trace, indent=2))

    print("[loop] 2/3 Verify — running rubric grader")
    tests = _run_tests()
    report = rubric.grade(trace, tests, config.COVERAGE_THRESHOLD)
    (run_dir / "rubric.json").write_text(json.dumps(report, indent=2))
    print(f"[loop] rubric passed={report['passed']}")

    print("[loop] 3/3 Analyze — asking the model for the top 3 improvements")
    model = config.resolve_model()
    prompt = analyze.build_prompt(
        north_star=(HERE / "NORTH_STAR.md").read_text(),
        instructions=(HERE / "prompt.md").read_text(),
        source=_gather_source(),
        trace_json=json.dumps(trace, indent=2),
        rubric_json=json.dumps(report, indent=2),
    )
    improvements = analyze.run_analysis(prompt, model=model)
    (run_dir / "improvements.md").write_text(improvements)

    print("=" * 48)
    print(f"[loop] TOP 3 IMPROVEMENTS (model: {model})")
    print("=" * 48)
    print(improvements)
    print("=" * 48)
    print(f"[loop] artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: Add the Make target**

Modify `Makefile` — update the `.PHONY` line and add the target. Change:

```make
.PHONY: help test test-watch coverage clean install lint serve all
```

to:

```make
.PHONY: help test test-watch coverage clean install lint serve all loop
```

Then add before the `# Clean build artifacts` section:

```make
# Run one improvement-loop iteration (capture -> verify -> analyze)
loop:
	python -m loop.run
```

And add a help line under the existing echoes in the `help` target:

```make
	@echo "  make loop         - Run one improvement-loop iteration"
```

- [ ] **Step 4: Verify the orchestrator imports**

Run: `python -c "import loop.run"`
Expected: no error.

- [ ] **Step 5: Smoke-run the loop (adjust journey selectors as needed)**

Run: `make loop`
Expected: three phases print; a new `loop/artifacts/<timestamp>/` appears containing `trace.json`, `rubric.json`, `improvements.md`, and screenshots. If a journey step failed, inspect `backend/templates/index.html` and adjust selectors in `loop/journey.py`, then re-run.

- [ ] **Step 6: Commit**

```bash
git add loop/run.py Makefile .gitignore
git commit -m "feat(loop): add orchestrator and make loop target"
```

---

## Task 7: Documentation

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Document the loop**

Modify `README.md` — add a section near the development/workflow area:

```markdown
## Improvement Loop

Continuously improve the child experience with a local, model-powered loop:

```bash
make loop                    # default: balanced model (cheapest that works well)
LOOP_TIER=cheap make loop    # smallest/cheapest model
LOOP_TIER=strong make loop   # highest-capability model
LOOP_MODEL=<id> make loop    # pin an explicit model id
```

Each run drives the real app through a child's full journey (Playwright),
grades it against the North Star rubric in `loop/NORTH_STAR.md`, and writes the
top 3 improvements to `loop/artifacts/<timestamp>/improvements.md`.
```

- [ ] **Step 2: Verify markdown renders**

Run: `grep -n "Improvement Loop" README.md`
Expected: the new heading is found.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: document the improvement loop"
```

---

## Self-Review

- **Spec coverage:** North Star (Task 1), model tiers with precedence (Task 2),
  deterministic rubric/verification loop (Task 3), analysis/hill-climb via
  Copilot CLI (Task 4), full-UX Playwright journey (Task 5), orchestrator +
  artifacts + `make loop` (Task 6), `.gitignore` for artifacts (Task 6), docs
  (Task 7). All spec sections map to a task.
- **Type consistency:** the `trace` dict keys written in `journey.py` /
  `_compile_sample` (`server_booted`, `console_errors`, `network_errors`,
  `steps_completed`, `steps_expected`, `compile_ok`, `broken_choices`) match the
  keys read in `rubric.grade`. `test_result` keys (`passed`, `coverage`) match
  `_run_tests` output. `analyze.build_prompt` / `run_analysis` signatures match
  their call sites in `run.py`.
- **Placeholder scan:** model ids in `config.py` are real defaults with a note
  to adjust to the user's available models; journey selectors are flagged as
  best-effort with an explicit adjustment step. No TODO/TBD left.
```