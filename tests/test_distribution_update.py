from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = next(line.split(": ", 1)[1] for line in (ROOT / "distribution.yaml").read_text().splitlines() if line.startswith("version: "))
HERMES = Path(os.environ.get("HERMES_BIN") or shutil.which("hermes") or "hermes")
PROFILE_NAME = "content-profile-update-test"
BASE_RELEASE_SHA = "5aa34cc274322170d6075120d8ddafcc769644a0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_hermes(home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HERMES_HOME"] = str(home)
    env["HERMES_PROFILE"] = "default"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(
        [str(HERMES), *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


def export_git_revision(revision: str, destination: Path) -> None:
    archive = destination.parent / f"{revision[:8]}.tar"
    exported = subprocess.run(
        ["git", "archive", "--format=tar", "--output", str(archive), revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if exported.returncode != 0:
        raise AssertionError(exported.stderr or exported.stdout)
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as bundle:
        bundle.extractall(destination)


class DistributionUpdateTests(unittest.TestCase):
    def test_historical_update_archives_legacy_and_preserves_workspace(self) -> None:
        if not HERMES.is_file():
            self.fail("Set HERMES_BIN to the Hermes executable before running this test")
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            source = temp / "source"
            profile_root = temp / "hermes-home"
            export_git_revision(BASE_RELEASE_SHA, source)

            install = run_hermes(
                profile_root,
                "profile",
                "install",
                str(source),
                "--name",
                PROFILE_NAME,
                "--yes",
            )
            self.assertEqual(install.returncode, 0, install.stderr or install.stdout)

            installed = profile_root / "profiles" / PROFILE_NAME
            # BASE_RELEASE_SHA predates the content-agent -> content-profile
            # rename, so the freshly installed old profile uses the old path.
            init = subprocess.run(
                [
                    sys.executable,
                    str(installed / "skills/content-agent/scripts/init_workspace.py"),
                    "--hermes-home",
                    str(installed),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            self.assertEqual(init.returncode, 0, init.stderr or init.stdout)

            legacy_root = installed / "skills/content-agent"
            (legacy_root / "user-note.bin").write_bytes(b"\x00\xffCustomized legacy fixture\r\n")
            legacy_before = {
                str(path.relative_to(legacy_root)): sha256(path)
                for path in legacy_root.rglob("*") if path.is_file()
            }
            private_root = installed / "workspace" / "editorial-memory"
            publication_brief = private_root / "publication-brief.md"
            publication_brief.write_bytes(
                publication_brief.read_bytes()
                + b"\n## Founder-owned legacy note\nPreserve this byte-for-byte.\n"
            )
            before = {
                str(path.relative_to(private_root)): sha256(path)
                for path in private_root.rglob("*")
                if path.is_file()
            }

            shutil.rmtree(source)
            shutil.copytree(
                ROOT,
                source,
                ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "*.pyc"),
            )
            update = run_hermes(
                profile_root,
                "profile",
                "update",
                PROFILE_NAME,
                "--yes",
            )
            self.assertEqual(update.returncode, 0, update.stderr or update.stdout)

            after = {
                str(path.relative_to(private_root)): sha256(path)
                for path in private_root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(after, before)
            self.assertIn(
                f"Version: {CURRENT_VERSION}",
                (
                    installed
                    / "skills/content-profile/references/release-marker.md"
                ).read_text(encoding="utf-8"),
            )
            installed_skill = (
                installed / "skills/content-profile/SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Preserve existing file paths and user-authored values", installed_skill)
            self.assertIn("additive diff and approval", installed_skill)
            for license_path in ("LICENSE", "skills/content-profile/LICENSE"):
                self.assertEqual((installed / license_path).read_bytes(), (ROOT / "LICENSE").read_bytes())
            # The rename must not leave a stale duplicate skill behind. The
            # update itself preserves paths the new manifest no longer owns,
            # so the startup initializer recognizes the legacy identity and
            # archives all its bytes outside skills on the next run.
            post_update_init = subprocess.run(
                [
                    sys.executable,
                    str(installed / "skills/content-profile/scripts/init_workspace.py"),
                    "--hermes-home",
                    str(installed),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            self.assertEqual(
                post_update_init.returncode,
                0,
                post_update_init.stderr or post_update_init.stdout,
            )
            report = json.loads(post_update_init.stdout)
            self.assertEqual(report["archived_legacy"], ["local/legacy-skills/content-agent/"])
            self.assertFalse(
                (installed / "skills" / "content-agent").exists(),
                "stale skills/content-agent/ left behind after rename update",
            )
            archive = installed / "local/legacy-skills/content-agent"
            self.assertEqual({
                str(path.relative_to(archive)): sha256(path)
                for path in archive.rglob("*") if path.is_file()
            }, legacy_before)
            final_workspace = {
                str(path.relative_to(private_root)): sha256(path)
                for path in private_root.rglob("*") if path.is_file()
            }
            self.assertEqual(final_workspace, before)

    def test_real_profile_update_replaces_shared_intelligence_and_preserves_user_state(self) -> None:
        if not HERMES.is_file():
            self.fail("Set HERMES_BIN to the Hermes executable before running this test")
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            source = temp / "source"
            profile_root = temp / "hermes-home"
            shutil.copytree(
                ROOT,
                source,
                ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "*.pyc"),
            )

            install = run_hermes(
                profile_root,
                "profile",
                "install",
                str(source),
                "--name",
                PROFILE_NAME,
                "--yes",
            )
            self.assertEqual(install.returncode, 0, install.stderr or install.stdout)

            installed = profile_root / "profiles" / PROFILE_NAME
            shared_marker = (
                installed
                / "skills"
                / "content-profile"
                / "references"
                / "release-marker.md"
            )
            self.assertIn(CURRENT_VERSION, shared_marker.read_text(encoding="utf-8"))

            sentinels = {
                "memory": installed / "memories" / "MEMORY.md",
                "workspace": installed / "workspace" / "editorial-memory" / "private.md",
                "session": installed / "sessions" / "private.jsonl",
                "auth": installed / "auth.json",
                "env": installed / ".env",
                "config": installed / "config.yaml",
                "local": installed / "local" / "overrides.yaml",
                "state": installed / "state.db",
                "unrelated_skill": installed / "skills" / "founder-private" / "SKILL.md",
            }
            sentinel_payloads = {
                "memory": b"private-memory-v1\n",
                "workspace": b"private-editorial-history-v1\n",
                "session": b'{"private":"session-v1"}\n',
                "auth": b'{"fixture":"not-a-real-credential"}\n',
                "env": b"FIXTURE_ONLY=not-a-secret\n",
                "config": b"local_fixture: preserve-me\n",
                "local": b"private_override: true\n",
                "state": b"fixture-state-not-a-real-database\n",
                "unrelated_skill": b"---\nname: founder-private\ndescription: Private fixture.\n---\nPrivate.\n",
            }
            for key, path in sentinels.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(sentinel_payloads[key])
            before = {key: sha256(path) for key, path in sentinels.items()}

            marker_source = (
                source
                / "skills"
                / "content-profile"
                / "references"
                / "release-marker.md"
            )
            marker_source.write_text(
                "# Shared intelligence release marker\n\nVersion: 0.1.7\n",
                encoding="utf-8",
            )
            manifest = source / "distribution.yaml"
            manifest_text = manifest.read_text(encoding="utf-8")
            self.assertIn(f"version: {CURRENT_VERSION}", manifest_text)
            manifest.write_text(
                manifest_text.replace(f"version: {CURRENT_VERSION}", "version: 0.1.7", 1),
                encoding="utf-8",
            )

            update = run_hermes(
                profile_root,
                "profile",
                "update",
                PROFILE_NAME,
                "--yes",
            )
            self.assertEqual(update.returncode, 0, update.stderr or update.stdout)

            after = {key: sha256(path) for key, path in sentinels.items()}
            self.assertEqual(after, before)
            self.assertIn("0.1.7", shared_marker.read_text(encoding="utf-8"))

            installed_manifest = (installed / "distribution.yaml").read_text(
                encoding="utf-8"
            )
            self.assertIn("version: 0.1.7", installed_manifest)
            info = run_hermes(profile_root, "profile", "info", PROFILE_NAME)
            self.assertEqual(info.returncode, 0, info.stderr or info.stdout)
            self.assertIn("0.1.7", info.stdout)


if __name__ == "__main__":
    unittest.main()
