"""Package self-containment, frontmatter, link integrity, and evaluation-suite checks."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
EVALUATIONS = ROOT / "evaluations"
REGISTRY = json.loads((SKILLS / "bootstrap-repo/references/registry.json").read_text(encoding="utf-8"))
FENCED_BLOCK = re.compile(r"(^|\n)(`{3,}|~{3,})[^\n]*\n.*?\n\2[ \t]*(?=\n|\Z)", re.S)
INLINE_CODE = re.compile(r"(`+)([^`]|(?!\1)`)+?\1")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s#]+)(?:#[^)]+)?\)")


def strip_code(markdown):
    without_fences = FENCED_BLOCK.sub("\n", markdown)
    return INLINE_CODE.sub("", without_fences)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{path}: missing opening frontmatter delimiter")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise AssertionError(f"{path}: missing closing frontmatter delimiter")
    fields = {}
    for line in parts[0].splitlines()[1:]:
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise AssertionError(f"{path}: malformed frontmatter line: {line!r}")
        fields[key.strip()] = value.strip().strip("'\"")
    return fields, parts[1]


class PackageIntegrityTests(unittest.TestCase):
    def test_frontmatter_and_upstream_licenses(self):
        for name, entry in sorted(REGISTRY["skills"].items()):
            with self.subTest(skill=name):
                skill_dir = SKILLS / name
                fields, body = parse_frontmatter(skill_dir / "SKILL.md")
                self.assertEqual(fields.get("name"), name)
                self.assertTrue(fields.get("description"))
                self.assertNotIn("disable-model-invocation", fields)
                self.assertNotIn("argument-hint", fields)
                self.assertTrue(body.strip())
                if entry.get("source") == "mattpocock":
                    self.assertTrue((skill_dir / "LICENSE").is_file())

    def test_skill_links_resolve_and_stay_within_declared_closure(self):
        for name, entry in sorted(REGISTRY["skills"].items()):
            pkg_root = (SKILLS / name).resolve()
            allowed_roots = [pkg_root] + [
                (SKILLS / dep).resolve() for dep in entry.get("dependencies", [])
            ]
            for md_file in sorted((SKILLS / name).rglob("*.md")):
                text = strip_code(md_file.read_text(encoding="utf-8"))
                for match in MARKDOWN_LINK.finditer(text):
                    target = match.group(1)
                    if target.startswith(("http://", "https://", "mailto:")):
                        continue
                    with self.subTest(file=str(md_file.relative_to(ROOT)), target=target):
                        resolved = (md_file.parent / target).resolve()
                        self.assertTrue(resolved.exists(), f"Broken link: {md_file} -> {target}")
                        self.assertTrue(
                            any(resolved.is_relative_to(root) for root in allowed_roots),
                            f"Link escapes package closure: {md_file} -> {target}",
                        )

    def test_top_level_documentation_links_resolve(self):
        docs = [
            ROOT / "README.md",
            ROOT / "UPSTREAM.md",
            EVALUATIONS / "README.md",
            EVALUATIONS / "validation.md",
        ]
        for doc in docs:
            text = strip_code(doc.read_text(encoding="utf-8"))
            for match in MARKDOWN_LINK.finditer(text):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                with self.subTest(doc=str(doc.relative_to(ROOT)), target=target):
                    resolved = (doc.parent / target).resolve()
                    self.assertTrue(resolved.exists(), f"Broken doc link: {doc} -> {target}")

    def test_readme_catalog_covers_every_registered_skill(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in sorted(REGISTRY["skills"]):
            with self.subTest(skill=name):
                self.assertIn(f"(skills/{name}/SKILL.md)", readme)

    def test_github_pr_entrypoint_stays_command_free(self):
        raw = (SKILLS / "github-pr/SKILL.md").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"^```", raw, re.M))
        self.assertIsNone(re.search(r"\b(git|gh)\s+(commit|push|pr|issue|add|rebase|merge|cherry-pick|revert)\b", raw))

    def test_every_skill_has_valid_evaluation_cases(self):
        for name in sorted(REGISTRY["skills"]):
            with self.subTest(skill=name):
                suite_dir = EVALUATIONS / name
                cases_path = suite_dir / "cases.json"
                self.assertTrue(cases_path.is_file(), f"Missing {cases_path}")
                payload = json.loads(cases_path.read_text(encoding="utf-8"))
                cases = payload.get("cases")
                self.assertIsInstance(cases, list)
                self.assertTrue(cases)
                ids = [case["id"] for case in cases]
                self.assertEqual(len(ids), len(set(ids)), f"Duplicate case IDs in {cases_path}")
                for case in cases:
                    self.assertIsInstance(case.get("activate"), bool)
                    self.assertTrue(case.get("request", "").strip())
                    for rel_input in case.get("inputs", []):
                        self.assertTrue(
                            (suite_dir / rel_input).exists(),
                            f"Missing fixture {rel_input} in {cases_path}",
                        )


if __name__ == "__main__":
    unittest.main()
