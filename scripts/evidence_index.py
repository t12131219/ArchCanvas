#!/usr/bin/env python3
"""Index tracked evidence by Git blob identity; never copy or modify evidence."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess


def inventory(root: Path) -> dict:
    raw = subprocess.check_output(["git", "-C", str(root), "ls-files", "-s", "-z", "--", "docs/evidence"])
    groups = defaultdict(lambda: {"files": 0, "workingTreeBytes": 0, "nestedEvidencePaths": 0, "entries": []})
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        path = encoded_path.decode("utf-8")
        parts = Path(path).parts
        group = groups["/".join(parts[:3])]
        group["files"] += 1
        group["workingTreeBytes"] += (root / path).stat().st_size
        group["nestedEvidencePaths"] += path.count("docs/evidence") > 1
        group["entries"].append(record)
    result = []
    for path, group in sorted(groups.items()):
        entries = group.pop("entries")
        result.append({"path": path, **group, "gitIndexDigest": hashlib.sha256(b"\0".join(sorted(entries))).hexdigest()})
    return {
        "schema": "archcanvas-evidence-index/1",
        "commit": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
        "identityScope": "Git index mode/blob/path; sizes describe current working files, not publication certification",
        "changedTrackedEvidence": subprocess.check_output(
            ["git", "-C", str(root), "diff", "HEAD", "--name-only", "--", "docs/evidence"], text=True).splitlines(),
        "files": sum(row["files"] for row in result),
        "workingTreeBytes": sum(row["workingTreeBytes"] for row in result),
        "groups": result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    if output.is_relative_to(root / "docs/evidence"):
        parser.error("Write the index outside docs/evidence to avoid recursive snapshots")
    result = inventory(root)
    if output.exists():
        parser.error("Refusing to overwrite an existing index; choose a new output")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({key: result[key] for key in ("commit", "files", "workingTreeBytes")}))


if __name__ == "__main__":
    main()
