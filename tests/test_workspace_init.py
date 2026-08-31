from __future__ import annotations

import json
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


class WorkspaceInitializationTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
