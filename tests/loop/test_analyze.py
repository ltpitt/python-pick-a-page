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
