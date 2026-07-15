#!/usr/bin/env python3
"""Convert a JSON array of flat objects to CSV. Missing keys -> empty string."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            data = data["items"]
        else:
            data = [data]
    if not isinstance(data, list):
        raise ValueError("JSON root must be an array of objects (or {items: [...]})")
    rows: list[dict[str, Any]] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Row {i} is not an object")
        rows.append(item)
    return rows


def rows_to_csv(rows: list[dict[str, Any]], out_path: Path) -> None:
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k, "") for k in fieldnames})


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="JSON array -> CSV")
    p.add_argument("input", type=Path, help="Input .json file")
    p.add_argument("-o", "--output", type=Path, required=True, help="Output .csv path")
    args = p.parse_args(argv)
    rows = load_rows(args.input)
    rows_to_csv(rows, args.output)
    print(f"Wrote {len(rows)} rows -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
