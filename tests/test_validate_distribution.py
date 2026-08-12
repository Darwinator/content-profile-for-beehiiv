from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_distribution.py"


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root), "--skip-tests"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class DistributionValidatorTests(unittest.TestCase):
    def copy_source(self, destination: Path) -> None:
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", ".tmp", "__pycache__", "*.pyc"),
        )

    def test_clean_distribution_passes_static_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "distribution"
            self.copy_source(copied)

            result = run_validator(copied)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("static distribution checks passed", result.stdout)

    def test_private_runtime_file_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "distribution"
            self.copy_source(copied)
            (copied / "auth.json").write_text('{"fixture":"not-a-secret"}\n', encoding="utf-8")

            result = run_validator(copied)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("auth.json", result.stdout + result.stderr)

    def test_host_specific_path_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / "distribution"
            self.copy_source(copied)
            private_prefix = "/opt" + "/data/"
            (copied / "README-private.md").write_text(
                f"Private path: {private_prefix}profiles/example\n", encoding="utf-8"
            )

            result = run_validator(copied)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("host-specific path", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
