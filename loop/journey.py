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
