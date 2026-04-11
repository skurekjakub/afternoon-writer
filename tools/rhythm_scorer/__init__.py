"""Rhythm & texture scorer — prose rhythm and structural complexity analysis.

Public API:
    from tools.rhythm_scorer import analyze_rhythm, RhythmReport
    from tools.rhythm_scorer import format_json, format_summary, format_comparison
"""

from .analyze import analyze_rhythm, report_from_json_targets
from .constants import DEFAULT_TEXTURE_BASELINES
from .formatters import format_comparison, format_json, format_summary
from .models import RhythmReport

__all__ = [
    "analyze_rhythm",
    "report_from_json_targets",
    "RhythmReport",
    "DEFAULT_TEXTURE_BASELINES",
    "format_json",
    "format_summary",
    "format_comparison",
]
