"""Tests for the prose tools. Run from the repo root:

    python3 -m unittest discover -s tools/tests -t .

The last test in the run checks that no test touched the real calibration,
gram cache, config or style guide.
"""

import os


def load_tests(loader, standard_tests, pattern):
    # unittest calls this for the package, and the nested discover below would call it
    # again; only the outer call runs discovery and appends the guard, so it runs once, last.
    global _loading
    if _loading:
        return standard_tests
    _loading = True
    try:
        here = os.path.dirname(__file__)
        standard_tests.addTests(loader.discover(start_dir=here, pattern=pattern or "test*.py",
                                                top_level_dir=os.path.dirname(os.path.dirname(here))))
    finally:
        _loading = False
    from tools.tests.support import ProtectedFilesUntouched

    standard_tests.addTest(ProtectedFilesUntouched("test_protected_files_unchanged"))
    return standard_tests


_loading = False
