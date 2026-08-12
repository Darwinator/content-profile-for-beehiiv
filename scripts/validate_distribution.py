#!/usr/bin/env python3
"""Validate that a Content Agent checkout is a clean Hermes distribution."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = {
    "AGENTS.md",
    "README.md",
    "SOUL.md",
    "config.yaml",
    "distribution.yaml",
    "skills/content-agent/SKILL.md",
    "skills/content-agent/scripts/init_workspace.py",
}
PRIVATE_TOP_LEVEL = {
    ".env",
    "auth.json",
    "home",
    "local",
    "logs",
    "memories",
    "sessions",
    "state.db",
    "workspace",
}
IGNORED_PARTS = {".git", ".tmp", "__pycache__"}
TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
HOST_PATH_PATTERNS = (
    re.compile(re.escape("/opt" + "/data/")),
    re.compile(re.escape("/ho" + "me/") + r"[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\]+\\", re.IGNORECASE),
)
CREDENTIAL_PATTERNS = (
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    (
        "GitHub fine-grained token",
        re.compile(r"\bgithub" + r"_pat_[A-Za-z0-9_]{20,}\b"),
    ),
    ("API key", re.compile(r"\bs" + r"k-[A-Za-z0-9_-]{20,}\b")),
    ("bearer credential", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{20,}={0,2}\b")),
    (
        "credential assignment",
        re.compile(
            r"(?im)^\s*(?:access"
            r"_token|refresh"
            r"_token|client"
            r"_secret|api_key|password)\s*[:=]\s*[\"']?"
            r"(?!<|\$\{|not-|fixture|example|none|null)[A-Za-z0-9._~+/-]{16,}"
        ),
    ),
)
EXPECTED_OWNED = {
    "distribution.yaml",
    "SOUL.md",
    "config.yaml",
    "skills/content-agent/",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="distribution checkout to validate",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="run static checks only",
    )
    parser.add_argument(
        "--hermes-bin",
        type=Path,
        help="Hermes executable used by the real install/update test",
    )
    return parser.parse_args()


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            yield path, path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue


def manifest_owned_paths(manifest_text: str) -> set[str]:
    in_owned = False
    owned: set[str] = set()
    for raw_line in manifest_text.splitlines():
        if raw_line.strip() == "distribution_owned:":
            in_owned = True
            continue
        if in_owned:
            match = re.match(r"^\s{2}-\s+([^#]+?)\s*$", raw_line)
            if match:
                owned.add(match.group(1).strip().strip("\"'"))
                continue
            if raw_line and not raw_line.startswith(" "):
                break
    return owned


def static_errors(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"distribution root does not exist: {root}"]

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for name in sorted(PRIVATE_TOP_LEVEL):
        path = root / name
        if path.exists():
            errors.append(f"private runtime state is present: {name}")

    for private_name in ("auth.json", ".env", "state.db"):
        for path in root.rglob(private_name):
            if any(part in IGNORED_PARTS for part in path.parts):
                continue
            if "tests" in path.parts and path.name != private_name:
                continue
            errors.append(f"private runtime file is present: {path.relative_to(root)}")

    manifest = root / "distribution.yaml"
    if manifest.is_file():
        text = manifest.read_text(encoding="utf-8")
        owned = manifest_owned_paths(text)
        if owned != EXPECTED_OWNED:
            errors.append(
                "distribution_owned mismatch: "
                f"expected {sorted(EXPECTED_OWNED)!r}, found {sorted(owned)!r}"
            )
        for required_key in ("name:", "version:", "description:", "hermes_requires:"):
            if not re.search(rf"(?m)^{re.escape(required_key)}\s*\S", text):
                errors.append(f"distribution.yaml is missing a value for {required_key[:-1]}")

    if (root / "mcp.json").exists():
        errors.append("mcp.json is inert for the current runtime; use config.yaml mcp_servers")

    for path, text in iter_text_files(root):
        relative = path.relative_to(root)
        for pattern in HOST_PATH_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(
                    f"host-specific path in {relative}: line {text.count(chr(10), 0, match.start()) + 1}"
                )
        for label, pattern in CREDENTIAL_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(
                    f"possible {label} in {relative}: line {text.count(chr(10), 0, match.start()) + 1}"
                )
        if path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON in {relative}: {exc}")

    skill = root / "skills" / "content-agent" / "SKILL.md"
    if skill.is_file():
        skill_text = skill.read_text(encoding="utf-8")
        references = set(re.findall(r"references/[a-z0-9-]+\.md", skill_text))
        if len(references) < 8:
            errors.append("SKILL.md does not name the complete editorial reference set")
        for relative in sorted(references):
            if not (skill.parent / relative).is_file():
                errors.append(f"SKILL.md references a missing file: {relative}")

    return sorted(set(errors))


def resolve_hermes(explicit: Path | None) -> str | None:
    if explicit:
        return str(explicit)
    configured = os.environ.get("HERMES_BIN")
    if configured:
        return configured
    return shutil.which("hermes")


def run_tests(root: Path, hermes_bin: str | None) -> int:
    if not hermes_bin or not Path(hermes_bin).is_file():
        print(
            "ERROR: Hermes executable not found; pass --hermes-bin or set HERMES_BIN",
            file=sys.stderr,
        )
        return 1
    env = os.environ.copy()
    env["HERMES_BIN"] = hermes_bin
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=root,
        env=env,
        check=False,
    )
    return result.returncode


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = static_errors(root)
    if errors:
        print("distribution validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("static distribution checks passed")
    if args.skip_tests:
        return 0

    return run_tests(root, resolve_hermes(args.hermes_bin))


if __name__ == "__main__":
    raise SystemExit(main())
