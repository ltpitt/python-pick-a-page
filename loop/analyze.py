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
