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


def run_analysis(prompt: str, model: str, cwd: str | None = None) -> str:
    """Invoke the Copilot CLI with the assembled prompt and return its output.

    The CLI is agentic and may run file/shell tools in its working directory.
    Because the whole app source is already inlined into ``prompt``, the
    analysis needs no access to the real project, so callers should pass an
    isolated ``cwd`` (a throwaway directory) to keep any tool actions away from
    the repository's files.
    """
    cmd = [COPILOT_CMD, "-p", prompt, "--model", model, "--no-color"]
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=True, cwd=cwd
    )
    return result.stdout
