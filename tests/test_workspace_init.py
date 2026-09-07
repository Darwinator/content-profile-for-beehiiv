from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "content-profile" / "scripts" / "init_workspace.py"
EXPECTED_FILES = {
    "launch-checklist.md",
    "publication-brief.md",
    "voice-and-boundaries.md",
    "source-ledger.md",
    "idea-ledger.md",
    "decision-log.md",
    "learning-proposals.md",
}
EXPECTED_DIRECTORIES = {"issue-history", "drafts"}


def run_initializer(home: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--hermes-home", str(home)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def seed_legacy(home: Path) -> tuple[Path, Path]:
    old = home / "skills/content-agent"
    old.mkdir(parents=True)
    (old / "SKILL.md").write_bytes(b"---\nname: content-agent\n---\n# Customized legacy\n")
    (old / "user-note.bin").write_bytes(b"\x00\xffprivate fixture\r\n")
    replacement = home / "skills/content-profile/SKILL.md"
    replacement.parent.mkdir(parents=True)
    replacement.write_bytes(b"---\nname: content-profile\n---\n# Replacement\n")
    return old, replacement


class WorkspaceInitializationTests(unittest.TestCase):
    def test_unknown_legacy_identity_is_preserved_in_place(self) -> None:
        for payload in (
            b"---\nname: content-agent-personal\n---\n# Prefix is not identity\n",
            b"---\nname: content-agent\nname: another\n---\n# Ambiguous\n",
            b"---\nname: content-agent\n# Unclosed header\n",
            b"# No frontmatter\nname: content-agent\n", b"\xff",
        ):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "profile"
                old, _ = seed_legacy(home)
                (old / "SKILL.md").write_bytes(payload)

                result = run_initializer(home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(old.is_dir())
                self.assertEqual((old / "SKILL.md").read_bytes(), payload)
                self.assertEqual((old / "user-note.bin").read_bytes(), b"\x00\xffprivate fixture\r\n")
                self.assertEqual(json.loads(result.stdout)["archived_legacy"], [])

    def test_archived_migration_is_idempotent_and_keeps_workspace_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            old, _ = seed_legacy(home)
            first = run_initializer(home)
            self.assertEqual(first.returncode, 0, first.stderr)
            archive = home / "local/legacy-skills/content-agent"
            self.assertTrue(archive.is_dir())
            archive_before = {p.name: p.read_bytes() for p in archive.iterdir()}
            private = home / "workspace/editorial-memory"
            (private / "publication-brief.md").write_bytes(b"Approved private fixture\r\n")
            private_before = {p.name: p.read_bytes() for p in private.iterdir() if p.is_file()}

            second = run_initializer(home)

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(second.stdout)["archived_legacy"], [])
            self.assertFalse(old.exists())
            self.assertEqual({p.name: p.read_bytes() for p in archive.iterdir()}, archive_before)
            self.assertEqual({p.name: p.read_bytes() for p in private.iterdir() if p.is_file()}, private_before)

    @unittest.skipIf(sys.platform == "win32", "Symlinks may require elevated privileges")
    def test_nested_legacy_symlink_is_moved_without_touching_its_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            old, _ = seed_legacy(home)
            outside = Path(tmp) / "outside.bin"
            outside.write_bytes(b"untouched external fixture")
            (old / "linked-note").symlink_to(outside)

            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            link = home / "local/legacy-skills/content-agent/linked-note"
            self.assertTrue(link.is_symlink())
            self.assertEqual(os.readlink(link), str(outside))
            self.assertEqual(outside.read_bytes(), b"untouched external fixture")

    @unittest.skipIf(sys.platform == "win32" or (hasattr(os, "geteuid") and os.geteuid() == 0),
                     "Requires non-root POSIX permission checks")
    def test_unreadable_skill_marker_does_not_block_workspace_startup(self) -> None:
        for marker in ("skills/content-agent/SKILL.md", "skills/content-profile/SKILL.md"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "profile"
                old, _ = seed_legacy(home)
                unreadable = home / marker
                unreadable.chmod(0)
                try:
                    result = run_initializer(home)
                finally:
                    unreadable.chmod(0o600)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(old.is_dir())
                self.assertEqual(json.loads(result.stdout)["archived_legacy"], [])
                self.assertTrue((home / "workspace/editorial-memory/publication-brief.md").is_file())

    @unittest.skipIf(sys.platform == "win32", "Symlinks may require elevated privileges")
    def test_symlinked_migration_paths_leave_legacy_and_targets_untouched(self) -> None:
        for relative in (
            "skills", "skills/content-agent", "skills/content-agent/SKILL.md",
            "skills/content-profile", "skills/content-profile/SKILL.md",
            "local", "local/legacy-skills",
        ):
            with self.subTest(path=relative), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "profile"
                old, _ = seed_legacy(home)
                before = {p.name: p.read_bytes() for p in old.iterdir()}
                link = home / relative
                if not link.exists():
                    link.mkdir(parents=True)
                outside = Path(tmp) / "outside-target"
                link.rename(outside)
                link.symlink_to(outside, target_is_directory=outside.is_dir())
                sentinel = Path(tmp) / "outside-sentinel.bin"
                sentinel.write_bytes(b"external fixture must survive")

                result = run_initializer(home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(link.is_symlink(), "migration must leave symlinked paths alone")
                self.assertTrue(old.is_dir(), "symlinked migration path must not deactivate legacy")
                self.assertEqual({p.name: p.read_bytes() for p in old.iterdir()}, before)
                self.assertEqual(sentinel.read_bytes(), b"external fixture must survive")
                self.assertEqual(json.loads(result.stdout)["archived_legacy"], [])
                self.assertFalse((home / "local/legacy-skills/content-agent").exists())

    def test_archive_collision_never_overwrites_or_deactivates_legacy(self) -> None:
        for kind in ("empty-directory", "nonempty-directory", "file", "dangling-symlink"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "profile"
                old, _ = seed_legacy(home)
                archive = home / "local/legacy-skills/content-agent"
                archive.parent.mkdir(parents=True)
                if kind.endswith("directory"):
                    archive.mkdir()
                    if kind == "nonempty-directory":
                        (archive / "saved.bin").write_bytes(b"earlier archive")
                elif kind == "file":
                    archive.write_bytes(b"existing local file")
                else:
                    if sys.platform == "win32":
                        continue  # Symlinks can require elevated privileges.
                    archive.symlink_to(Path(tmp) / "missing")
                archive_inode = archive.lstat().st_ino
                before = {p.name: p.read_bytes() for p in old.iterdir()}

                result = run_initializer(home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(old.is_dir(), "archive collision must preserve active legacy")
                self.assertEqual({p.name: p.read_bytes() for p in old.iterdir()}, before)
                self.assertEqual(archive.lstat().st_ino, archive_inode)
                self.assertEqual(json.loads(result.stdout)["archived_legacy"], [])
                if kind == "nonempty-directory":
                    self.assertEqual((archive / "saved.bin").read_bytes(), b"earlier archive")
                elif kind == "file":
                    self.assertEqual(archive.read_bytes(), b"existing local file")

    def test_unusable_replacement_preserves_active_legacy_skill(self) -> None:
        for payload in (
            b"", b"# No identity\n", b"---\nname: another-skill\n---\n# Wrong\n",
            b"---\nname: content-profile\n---\n \n",
            b"---\nname: content-profile-personal\n---\n# Wrong\n",
            b"---\nname: content-profile\n# Unclosed header\n", b"\xff",
        ):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "profile"
                old, replacement = seed_legacy(home)
                replacement.write_bytes(payload)
                before = {p.name: p.read_bytes() for p in old.iterdir()}

                result = run_initializer(home)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(old.is_dir(), "unusable replacement must not deactivate legacy")
                self.assertEqual({p.name: p.read_bytes() for p in old.iterdir()}, before)
                self.assertEqual(json.loads(result.stdout)["archived_legacy"], [])
                self.assertEqual(replacement.read_bytes(), payload)

    def test_first_run_creates_the_editorial_memory_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            editorial_memory = home / "workspace" / "editorial-memory"
            self.assertEqual(
                {path.name for path in editorial_memory.iterdir() if path.is_file()},
                EXPECTED_FILES,
            )
            self.assertTrue(
                EXPECTED_DIRECTORIES.issubset(
                    {path.name for path in editorial_memory.iterdir() if path.is_dir()}
                )
            )
            self.assertEqual(set(report["created_files"]), EXPECTED_FILES)
            self.assertEqual(set(report["created_directories"]), EXPECTED_DIRECTORIES)
            self.assertEqual(report["preserved_files"], [])

    def test_second_run_preserves_existing_user_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            first = run_initializer(home)
            self.assertEqual(first.returncode, 0, first.stderr)

            publication_brief = (
                home / "workspace" / "editorial-memory" / "publication-brief.md"
            )
            user_bytes = b"# Darwin's confirmed publication brief\n\nKeep this exactly.\n"
            publication_brief.write_bytes(user_bytes)

            second = run_initializer(home)

            self.assertEqual(second.returncode, 0, second.stderr)
            report = json.loads(second.stdout)
            self.assertEqual(publication_brief.read_bytes(), user_bytes)
            self.assertIn("publication-brief.md", report["preserved_files"])
            self.assertEqual(report["created_files"], [])

    def test_partial_workspace_only_fills_missing_contract_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            editorial_memory = home / "workspace" / "editorial-memory"
            editorial_memory.mkdir(parents=True)
            existing = editorial_memory / "decision-log.md"
            existing_bytes = b"# Existing decisions\n\n- Keep this.\n"
            existing.write_bytes(existing_bytes)

            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(existing.read_bytes(), existing_bytes)
            self.assertIn("decision-log.md", report["preserved_files"])
            self.assertNotIn("decision-log.md", report["created_files"])
            self.assertEqual(set(report["created_files"]), EXPECTED_FILES - {"decision-log.md"})

    def test_rename_migration_archives_customized_matching_skill_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            old_skill = home / "skills" / "content-agent"
            old_skill.mkdir(parents=True)
            (old_skill / "SKILL.md").write_text(
                "---\nname: content-agent\ndescription: Customized legacy skill.\n---\nUser edits.\n",
                encoding="utf-8",
            )
            new_skill = home / "skills" / "content-profile"
            new_skill.mkdir(parents=True)
            (new_skill / "SKILL.md").write_text(
                "---\nname: content-profile\n---\n# Replacement\n", encoding="utf-8"
            )
            (old_skill / "notes").mkdir()
            (old_skill / "notes/private.bin").write_bytes(b"\x00\xffKeep every byte\r\n")
            before = {
                str(path.relative_to(old_skill)): path.read_bytes()
                for path in old_skill.rglob("*") if path.is_file()
            }

            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            archive = home / "local/legacy-skills/content-agent"
            self.assertTrue(archive.is_dir(), "customized legacy bytes must be archived, not deleted")
            self.assertEqual(report["archived_legacy"], ["local/legacy-skills/content-agent/"])
            self.assertEqual({
                str(path.relative_to(archive)): path.read_bytes()
                for path in archive.rglob("*") if path.is_file()
            }, before)
            self.assertFalse(old_skill.exists())
            self.assertTrue((new_skill / "SKILL.md").is_file())

    def test_rename_migration_preserves_unrelated_or_user_authored_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            # User-authored skill that happens to reuse the old directory name:
            # frontmatter does not match the shipped skill, so it must survive.
            user_skill = home / "skills" / "content-agent"
            user_skill.mkdir(parents=True)
            user_bytes = "---\nname: my-own-thing\n---\nUser-authored.\n"
            (user_skill / "SKILL.md").write_text(user_bytes, encoding="utf-8")
            new_skill = home / "skills" / "content-profile"
            new_skill.mkdir(parents=True)
            (new_skill / "SKILL.md").write_text(
                "---\nname: content-profile\n---\n", encoding="utf-8"
            )

            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["archived_legacy"], [])
            self.assertEqual(
                (user_skill / "SKILL.md").read_text(encoding="utf-8"), user_bytes
            )

    def test_body_only_legacy_phrase_does_not_delete_user_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            old = home / "skills/content-agent"
            old.mkdir(parents=True)
            payload = b"---\nname: my-own-thing\n---\nExample only: name: content-agent\n"
            (old / "SKILL.md").write_bytes(payload)
            replacement = home / "skills/content-profile/SKILL.md"
            replacement.parent.mkdir(parents=True)
            replacement.write_bytes(b"---\nname: content-profile\n---\n# Replacement\n")

            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(old.is_dir(), "body-only legacy phrase deleted a user skill")
            self.assertEqual((old / "SKILL.md").read_bytes(), payload)

    def test_rename_migration_is_inert_when_new_skill_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "profile"
            old_skill = home / "skills" / "content-agent"
            old_skill.mkdir(parents=True)
            (old_skill / "SKILL.md").write_text(
                "---\nname: content-agent\n---\n", encoding="utf-8"
            )

            result = run_initializer(home)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["archived_legacy"], [])
            self.assertTrue((old_skill / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
