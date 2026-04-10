"""Auto-collect all pattern modules from this directory.

Each module exports:
    PATTERNS: list[dict]      — pattern definitions for one category
    COMBINED_CAP: int | None  — optional combined cap for the category

This __init__ merges them into two flat exports:
    ALL_PATTERNS: list[dict]         — every pattern across all categories
    COMBINED_CAPS: dict[str, int]    — category → combined cap (only categories that have one)
"""

import importlib
import os
import pkgutil

ALL_PATTERNS: list[dict] = []
COMBINED_CAPS: dict[str, int] = {}

_pkg_dir = os.path.dirname(__file__)

for _finder, _name, _ispkg in pkgutil.iter_modules([_pkg_dir]):
    _mod = importlib.import_module(f"{__name__}.{_name}")
    ALL_PATTERNS.extend(_mod.PATTERNS)
    if _mod.COMBINED_CAP is not None:
        COMBINED_CAPS[_name] = _mod.COMBINED_CAP
