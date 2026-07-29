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
