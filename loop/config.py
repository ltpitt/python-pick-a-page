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
