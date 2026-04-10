#!/usr/bin/env python3
"""Download and cache the Brysbaert concreteness norms."""

import csv
import os
import sys
import urllib.request

NORMS_URL = (
    "https://huggingface.co/datasets/StephanAkkerman/"
    "concreteness-ratings/resolve/main/concreteness_ratings.csv"
)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
NORMS_PATH = os.path.join(DATA_DIR, "concreteness_norms.csv")
MIN_ROWS = 39000


def download():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(NORMS_PATH):
        # Verify existing file
        with open(NORMS_PATH, newline="", encoding="utf-8") as f:
            row_count = sum(1 for _ in csv.reader(f)) - 1  # minus header
        if row_count >= MIN_ROWS:
            print(f"Already downloaded: {NORMS_PATH} ({row_count} rows)")
            return
        print(f"Existing file has only {row_count} rows — re-downloading")

    print(f"Downloading Brysbaert norms from HuggingFace...")
    tmp_path = NORMS_PATH + ".tmp"
    try:
        urllib.request.urlretrieve(NORMS_URL, tmp_path)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"Download failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Verify download
    with open(tmp_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        if "Word" not in fields or "Conc.M" not in fields:
            os.remove(tmp_path)
            print(f"Bad CSV: expected 'Word' and 'Conc.M' columns, got {fields}", file=sys.stderr)
            sys.exit(1)
        row_count = sum(1 for _ in reader)

    if row_count < MIN_ROWS:
        os.remove(tmp_path)
        print(f"Partial download: only {row_count} rows (need {MIN_ROWS}+)", file=sys.stderr)
        sys.exit(1)

    os.rename(tmp_path, NORMS_PATH)

    # Sample a few entries
    norms = {}
    with open(NORMS_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            norms[row["Word"].lower()] = float(row["Conc.M"])

    samples = ["coffee", "hand", "floor", "deliberation", "feeling", "expression"]
    print(f"Downloaded: {row_count} rows to {NORMS_PATH}")
    print(f"Mean concreteness: {sum(norms.values()) / len(norms):.2f}")
    for w in samples:
        score = norms.get(w, "NOT FOUND")
        if isinstance(score, float):
            score = f"{score:.2f}"
        print(f"  {w}: {score}")


if __name__ == "__main__":
    download()
