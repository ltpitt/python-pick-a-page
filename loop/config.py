"""Model tiers and run settings for the improvement loop.

Model selection precedence (highest wins):
1. ``LOOP_MODEL`` env var — explicit model id.
2. ``LOOP_TIER`` env var — ``cheap`` | ``balanced`` | ``strong``.
3. Default tier (``cheap``).

All tier models below are INCLUDED in the Copilot Pro ($10/mo) plan as of
2026-07. Billing is per-token via GitHub AI Credits (1 credit = $0.01) once
your monthly allowance is used — GitHub retired the old premium-request
multipliers. Prices are per 1M tokens (input / output).

    tier      model              in / out $    notes
    cheap     gpt-5-mini         0.25 / 2.00   cheapest capable Pro model; multimodal
                                               (reads the journey screenshots); GitHub's
                                               recommended general default
    balanced  claude-sonnet-4.5  3.00 / 15.00  stronger reasoning + writing taste
    strong    gpt-5.4            2.50 / 15.00  deep multi-step reasoning / analysis

The default is the cheapest model that still does GOOD work on this analysis
task (largish context in, a reasoned top-3 out) — not the absolute cheapest.

Model ids must match what your Copilot CLI accepts. Finding the exact slug can
be fiddly; verify with ``copilot --help`` (or your CLI's model-list command)
and adjust these values if a run reports an unknown/invalid model.
"""

import os
from pathlib import Path

# Model ids per tier. All included in Copilot Pro. Edit to match your CLI slugs.
TIERS = {
    "cheap": "gpt-5-mini",
    "balanced": "claude-sonnet-4.5",
    "strong": "gpt-5.4",
}

DEFAULT_TIER = "cheap"

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
