#!/usr/bin/env python3
"""TDD tests for dual-vessel flight recorder (Grok + AGY)."""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
HOME_ABS_RE = re.compile(r"/home/[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class TestSkillFrontmatterAndPortability(unittest.TestCase):
    def test_skill_md_valid(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        self.assertIsNotNone(m, "SKILL.md needs YAML frontmatter")
        body = m.group(1)
        name_m = re.search(r"^name:\s*(.+)$", body, re.M)
        self.assertTrue(name_m)
        name = name_m.group(1).strip().strip("\"'")
        self.assertEqual(name, "aim-flight-recorder")
        self.assertRegex(name, NAME_RE)
        self.assertIn("description:", body)
        # Dual vessels in description or body
        self.assertTrue(
            "Grok" in text or "grok" in text,
            "SKILL.md must document Grok sessions",
        )
        self.assertTrue(
            "gemini" in text.lower() or "AGY" in text or "Antigravity" in text,
            "SKILL.md must retain AGY/Antigravity docs",
        )

    def test_no_machine_absolute_home_paths_in_docs(self):
        offenders = []
        for rel in ("SKILL.md", "README.md"):
            path = ROOT / rel
            if not path.is_file():
                continue
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"/home/user\b|/home/YOU\b|/Users/you\b", line, re.I):
                    continue
                if HOME_ABS_RE.search(line):
                    offenders.append(f"{rel}:{i}: {line.strip()}")
        self.assertEqual(offenders, [], "portable paths only:\n" + "\n".join(offenders))

    def test_skill_documents_both_skill_install_roots(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".grok/skills", text)
        self.assertTrue(
            ".gemini" in text or "antigravity-cli/skills" in text,
            "SKILL.md should keep AGY install/skill path",
        )

    def test_readme_documents_both_installs(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(".grok/skills", text)
        self.assertTrue(
            "antigravity-cli/skills" in text or ".gemini" in text,
            "README must keep AGY install",
        )


class TestParseAgyAndGrok(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fr = load_module("flight_recorder", SCRIPTS / "flight_recorder.py")

    def test_parse_agy_cleaned(self):
        path = FIXTURES / "agy_transcript.jsonl"
        self.assertTrue(path.is_file())
        md = self.fr.parse_transcript(str(path), mode="cleaned")
        self.assertIn("Operator", md)
        self.assertIn("Agent", md)
        self.assertIn("Check the status of the repo", md)
        self.assertIn("run_command", md)
        self.assertNotIn("On branch master", md)  # tool output dropped in cleaned

    def test_parse_agy_full_includes_tool_output(self):
        md = self.fr.parse_transcript(
            str(FIXTURES / "agy_transcript.jsonl"), mode="full"
        )
        self.assertIn("On branch master", md)

    def test_parse_grok_cleaned(self):
        path = FIXTURES / "grok_updates.jsonl"
        self.assertTrue(path.is_file())
        md = self.fr.parse_transcript(str(path), mode="cleaned")
        self.assertIn("Grok", md)
        self.assertIn("Operator", md)
        self.assertIn("flight record", md.lower())
        self.assertIn("Agent", md)
        self.assertIn("run_terminal_command", md)

    def test_looks_like_grok_updates(self):
        self.assertTrue(
            self.fr._looks_like_grok_updates(str(FIXTURES / "grok_updates.jsonl"))
        )
        self.assertFalse(
            self.fr._looks_like_grok_updates(str(FIXTURES / "agy_transcript.jsonl"))
        )

    def test_cli_input_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "flight_recorder.py"),
                    "--input",
                    str(FIXTURES / "grok_updates.jsonl"),
                    "--mode",
                    "chat_only",
                    "--output",
                    str(out),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            text = out.read_text(encoding="utf-8")
            self.assertIn("Operator", text)
            self.assertNotIn("run_terminal_command", text)


class TestListSessionsDual(unittest.TestCase):
    def test_list_sessions_module_has_grok_support(self):
        src = (SCRIPTS / "list_sessions.py").read_text(encoding="utf-8")
        self.assertIn(".grok", src)
        self.assertIn("antigravity-cli", src)
        self.assertIn("updates.jsonl", src)

    def test_list_sessions_runs(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "list_sessions.py")],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        # Should not hard-fail if only one vessel present
        self.assertNotIn("[FATAL]", proc.stdout + proc.stderr)


class TestDualPolicyDoc(unittest.TestCase):
    def test_policy_exists(self):
        path = ROOT / "docs" / "VESSEL_DUAL_COMPAT.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("Grok", text)
        self.assertIn("AGY", text)


if __name__ == "__main__":
    unittest.main()
