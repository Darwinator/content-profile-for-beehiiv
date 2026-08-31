#!/usr/bin/env python3
"""Initialize Content Profile private Editorial Memory without overwriting user data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


FILE_NAMES = (
    "launch-checklist.md",
    "publication-brief.md",
    "voice-and-boundaries.md",
    "source-ledger.md",
    "idea-ledger.md",
    "decision-log.md",
    "learning-proposals.md",
)
DIRECTORY_NAMES = ("issue-history", "drafts")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create missing Content Profile Editorial Memory files."
    )
    parser.add_argument(
        "--hermes-home",
        type=Path,
        default=None,
        help="Profile home. Defaults to $HERMES_HOME.",
    )
    return parser.parse_args()


def resolve_hermes_home(requested: Path | None) -> Path:
    if requested is not None:
        return requested.expanduser().resolve()
    raw = os.environ.get("HERMES_HOME", "").strip()
    if not raw:
        raise SystemExit("HERMES_HOME is not set; pass --hermes-home explicitly.")
    return Path(raw).expanduser().resolve()


def initialize_workspace(hermes_home: Path) -> dict[str, list[str]]:
    template_dir = Path(__file__).resolve().parents[1] / "templates" / "editorial-memory"
    missing_templates = [name for name in FILE_NAMES if not (template_dir / name).is_file()]
    if missing_templates:
        raise RuntimeError(
            "Missing bundled Editorial Memory templates: " + ", ".join(missing_templates)
        )

    removed_stale = migrate_renamed_skill(hermes_home)

    target_dir = hermes_home / "workspace" / "editorial-memory"
    target_dir.mkdir(parents=True, exist_ok=True)

    created_directories: list[str] = []
    preserved_directories: list[str] = []
    for name in DIRECTORY_NAMES:
        destination = target_dir / name
        if destination.exists():
            if not destination.is_dir():
                raise RuntimeError(f"Expected a directory but found a file: {destination}")
            preserved_directories.append(name)
            continue
        destination.mkdir()
        created_directories.append(name)

    created_files: list[str] = []
    preserved_files: list[str] = []
    for name in FILE_NAMES:
        destination = target_dir / name
        if destination.exists():
            if not destination.is_file():
                raise RuntimeError(f"Expected a file but found another type: {destination}")
            preserved_files.append(name)
            continue
        template_bytes = (template_dir / name).read_bytes()
        try:
            with destination.open("xb") as handle:
                handle.write(template_bytes)
        except FileExistsError:
            preserved_files.append(name)
        else:
            created_files.append(name)

    return {
        "created_files": created_files,
        "preserved_files": preserved_files,
        "created_directories": created_directories,
        "preserved_directories": preserved_directories,
        "removed_stale": removed_stale,
    }


def migrate_renamed_skill(hermes_home: Path) -> list[str]:
    """Remove the pre-0.1.0 distribution-owned skill left behind by the rename.

    Hermes profile updates replace paths the new manifest owns but preserve
    paths it no longer names, so the 0.1.x `skills/content-agent/` directory
    survives an update to 0.1.0 as a stale duplicate. Delete it only when
    provenance proves it is the old shipped skill and the renamed skill is
    already installed; anything else is preserved untouched.
    """
    old_dir = hermes_home / "skills" / "content-agent"
    new_skill = hermes_home / "skills" / "content-profile" / "SKILL.md"
    if not old_dir.is_dir() or not new_skill.is_file():
        return []
    old_skill = old_dir / "SKILL.md"
    if not old_skill.is_file():
        return []
    try:
        frontmatter = old_skill.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    if "name: content-agent" not in frontmatter:
        return []
    shutil.rmtree(old_dir)
    return ["skills/content-agent/"]


def main() -> int:
    args = parse_args()
    report = initialize_workspace(resolve_hermes_home(args.hermes_home))
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
