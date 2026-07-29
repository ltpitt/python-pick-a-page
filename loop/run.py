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
    from backend.core.compiler import StoryCompiler

    sample = (REPO / "tests" / "fixtures" / "valid_story.txt").read_text()
    try:
        StoryCompiler().parse(sample)
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
