#!/usr/bin/env python3
"""Run the prose tools on one chapter file in a single process.

    python3 tools/prose_check.py --json FILE                     rhythm + slop + mannered
    python3 tools/prose_check.py --json --tools rhythm,slop FILE  only the tools you need
    python3 tools/prose_check.py FILE                            short text summary of each

Each block of the JSON report is exactly what that tool prints with --json on its own:

    rhythm    tools/rhythm_scorer/score.py --json --baselines .afternoon/style-guide.json FILE
    slop      tools/slop_checker/check.py --json FILE
    mannered  tools/mannered_checker/check.py --json FILE

so {"file", "tools", "failed", "rhythm", "slop", "mannered"}. The rhythm
baselines default to .afternoon/style-guide.json when it exists. If one tool
fails, its block is {"error", "traceback"}, its name is listed in "failed", the
other blocks are still reported, and the exit status is 3.

Exit status: 0 ok, 1 file not found, 2 bad arguments, 3 a tool failed.
"""

import argparse
import json
import os
import sys
import traceback

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

TOOLS = ("rhythm", "slop", "mannered")
DEFAULT_BASELINES = os.path.join(REPO_ROOT, ".afternoon", "style-guide.json")


def _rhythm(path, opts):
    from tools.rhythm_scorer.analyze import analyze_rhythm
    from tools.rhythm_scorer.formatters import format_summary, report_dict
    from tools.rhythm_scorer.score import load_texture_baselines
    from tools.prose_core.text import drop_headers, read_text

    report = analyze_rhythm(drop_headers(read_text(path)), texture_baselines=load_texture_baselines(opts["baselines"]))
    return report_dict(report, path), format_summary(report, path)


def _slop(path, opts):
    from tools.prose_core.text import read_text
    from tools.slop_checker.check import check_prose, format_summary, report_dict

    report = check_prose(read_text(path))
    return report_dict(report, path), format_summary(report, path)


def _mannered(path, opts):
    from tools.mannered_checker.check import check, summary_text

    report = check(path, recalibrate=opts["recalibrate"], use_cache=opts["use_cache"])
    return report, summary_text(report)


RUNNERS = {"rhythm": _rhythm, "slop": _slop, "mannered": _mannered}


def run(path, tools=TOOLS, baselines=None, recalibrate=True, use_cache=True):
    """({"file", "tools", "failed", <tool>: report or {"error", "traceback"}}, {<tool>: summary text})."""
    if baselines is None and os.path.exists(DEFAULT_BASELINES):
        baselines = DEFAULT_BASELINES
    opts = {"baselines": baselines, "recalibrate": recalibrate, "use_cache": use_cache}
    report = {"file": path, "tools": list(tools), "failed": []}
    summaries = {}
    for name in tools:
        try:
            report[name], summaries[name] = RUNNERS[name](path, opts)
        except Exception as exc:  # one broken tool must not hide the others' results
            report[name] = {"error": f"{type(exc).__name__}: {exc}",
                            "traceback": traceback.format_exc(limit=3)}
            summaries[name] = f"{name}: ERROR {type(exc).__name__}: {exc}"
            report["failed"].append(name)
    return report, summaries


def parse_tools(value: str):
    names = [t.strip() for t in value.split(",") if t.strip()]
    unknown = [t for t in names if t not in RUNNERS]
    if unknown or not names:
        raise argparse.ArgumentTypeError(f"unknown tool(s) {', '.join(unknown) or '(none)'}; choose from {', '.join(TOOLS)}")
    return names


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="prose file, e.g. .afternoon/chapters/chapter5/v2.md")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--json", action="store_true", help="one JSON report with a block per tool")
    mode.add_argument("--summary", action="store_true", help="short text summary per tool (default)")
    ap.add_argument("--tools", type=parse_tools, default=list(TOOLS),
                    help="comma-separated subset of rhythm,slop,mannered (default: all)")
    ap.add_argument("--baselines", help="texture baselines JSON (default: .afternoon/style-guide.json)")
    ap.add_argument("--no-recalibrate", action="store_true", help="mannered: use calibration.json as is")
    ap.add_argument("--no-cache", action="store_true", help="mannered: rebuild the human n-gram set")
    args = ap.parse_args(argv)

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        return 1
    report, summaries = run(args.file, args.tools, args.baselines,
                            recalibrate=not args.no_recalibrate, use_cache=not args.no_cache)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("\n\n".join(f"== {name}\n{summaries[name]}" for name in args.tools))
    return 3 if report["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
