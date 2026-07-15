import json
from pathlib import Path
from json_to_csv import load_rows, rows_to_csv


def test_missing_keys(tmp_path: Path):
    src = tmp_path / "in.json"
    out = tmp_path / "out.csv"
    src.write_text(json.dumps([{"a": 1, "b": 2}, {"a": 3, "c": 4}]), encoding="utf-8")
    rows = load_rows(src)
    rows_to_csv(rows, out)
    text = out.read_text(encoding="utf-8")
    assert "a,b,c" in text.splitlines()[0]
    assert "1,2," in text
    assert "3,,4" in text
