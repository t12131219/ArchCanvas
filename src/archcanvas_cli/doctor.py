"""Identify the actual runtime and assets without running a user model."""
import hashlib
import json
import re
import shutil
import stat
import sys
from pathlib import Path, PurePosixPath
from archcanvas_authoring import module_catalog
from .canvas import canvas_operation


def verify_inventory(root: Path, manifest: dict) -> None:
    """Verify the exact frozen inventory, without executing release code."""
    if (not isinstance(manifest, dict) or manifest.get("schemaVersion") != 1
            or manifest.get("product") != "archcanvas" or manifest.get("kind") != "local-beta-preview"
            or not isinstance(manifest.get("version"), str)
            or not re.fullmatch(r"\d+\.\d+\.\d+-beta\.\d+", manifest["version"])):
        raise ValueError("Invalid bundle identity")
    rows = manifest.get("files")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Bundle inventory is required")
    expected = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "bytes"}:
            raise ValueError("Invalid bundle inventory row")
        name = row["path"]
        if (not isinstance(name, str) or not name or "\\" in name or "\x00" in name
                or PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
                or str(PurePosixPath(name)) != name or name == "BUNDLE-MANIFEST.json" or name in expected
                or not isinstance(row["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])
                or type(row["bytes"]) is not int or row["bytes"] < 0):
            raise ValueError("Invalid bundle inventory path, digest or size")
        expected[name] = row
    observed = set()
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise ValueError("Bundle contains a link or special file")
        name = path.relative_to(root).as_posix()
        if name == "BUNDLE-MANIFEST.json":
            continue
        observed.add(name)
        row = expected.get(name)
        if row is None or path.stat().st_size != row["bytes"]:
            raise ValueError(f"Bundle inventory mismatch: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise ValueError(f"Bundle digest mismatch: {name}")
    if observed != set(expected):
        raise ValueError("Bundle inventory is incomplete")


def diagnose(*, summary=False) -> dict:
    from .server import project_root
    from . import __version__
    root = project_root()
    assets = []
    if root:
        for file in sorted((root / "studio/dist").rglob("*")):
            if file.is_file() and not file.is_symlink():
                assets.append({"path": file.relative_to(root).as_posix(), "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
    inventory = hashlib.sha256(json.dumps(assets, sort_keys=True).encode()).hexdigest()
    bundle = root / "BUNDLE-MANIFEST.json" if root else None
    frozen = bool(bundle and (bundle.exists() or bundle.is_symlink()))
    version = None
    integrity = "development-bytes"
    integrity_error = None
    if frozen:
        try:
            if bundle.is_symlink():
                raise ValueError("Bundle manifest may not be a symlink")
            manifest = json.loads(bundle.read_text(encoding="utf-8"))
            version = manifest.get("version") if isinstance(manifest, dict) else None
            verify_inventory(root, manifest)
            integrity = "verified"
        except (ValueError, OSError, UnicodeError) as exc:
            integrity, integrity_error = "mismatch", str(exc)
    try: presets = canvas_operation(root, {"action": "catalog"})["presets"]
    except ValueError: presets = None
    ready = bool(root and (root / "studio/dist/index.html").is_file() and presets is not None and integrity != "mismatch")
    return {"schemaVersion": 1, "status": "ready-local" if ready else "incomplete", "runtimeVersion": __version__,
            "releaseVersion": version, "releaseIntegrity": integrity, "distribution": "frozen-local-preview" if frozen else "development-checkout",
            **({"integrityError": integrity_error} if integrity_error else {}),
            "runtimeRoot": str(root) if root else None, "interpreter": str(Path(sys.executable).resolve()),
            "node": shutil.which("node"), "studio": {"available": bool(assets), "assetCount": len(assets),
                **({} if summary else {"assets": assets}), "digest": inventory},
            "catalog": {"atomicModules": len(module_catalog()["modules"]), "presets": presets},
            "modelExecution": False, "hostE2E": "not-tested", "publicationReview": "not-certified",
            "next": "Start serve --data-dir /absolute/independent-state-root, then open --root MODEL_ROOT --entry module:Class --server http://127.0.0.1:8765" if ready else "Install the complete verified release and Node.js 24+, then run doctor again."}
