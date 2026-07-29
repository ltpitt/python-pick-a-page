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

    # A known-valid story so the compile + play steps succeed deterministically.
    sample = (
        "---\n"
        "title: My Adventure\n"
        "author: Kid\n"
        "---\n\n"
        "[[beginning]]\n\n"
        "You wake up in a mysterious place.\n\n"
        "[[Explore]]\n\n"
        "---\n\n"
        "[[Explore]]\n\n"
        "You found treasure! The end.\n"
    )

    # Each step maps to the real DOM in backend/templates/index.html and is
    # guarded so one failure does not abort the whole journey.
    for name, action in [
        ("template", lambda: page.locator("#newStoryBtn").click()),
        ("edit", lambda: page.locator("#storyEditor").fill(sample)),
        ("compile", lambda: page.locator("#compileBtn").click()),
        ("play", lambda: page.locator("#storyPlayer").wait_for(state="visible")),
        ("i18n", lambda: page.locator("#languageSelector").select_option(index=1)),
    ]:
        try:
            action()
            page.wait_for_timeout(300)
            shot(name)
        except Exception:  # noqa: BLE001 — record failure, keep going
            page.screenshot(path=str(shots_dir / f"{name}-FAILED.png"))
