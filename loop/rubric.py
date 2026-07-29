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
