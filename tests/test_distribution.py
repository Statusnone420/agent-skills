from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_adapters

SKILLS = build_adapters.SKILLS
PLUGINS = build_adapters.PLUGINS
ALL_SKILLS = set(SKILLS)
SUITE = "agent-skills"
MANUAL_ONLY = {"english", "orchestrate"}
MAX_SKILL_FILE_BYTES = 16 * 1024
MAX_DESCRIPTION_CHARS = 180


def directory_names(path: Path) -> set[str]:
    return {item.name for item in path.iterdir() if item.is_dir()}


def frontmatter(path: Path) -> dict[str, str]:
    block = path.read_text(encoding="utf-8").split("---", 2)[1]
    fields = (line.split(":", 1) for line in block.splitlines() if ":" in line)
    return {key.strip(): value.strip().strip('"') for key, value in fields}


class DistributionTests(unittest.TestCase):
    def test_generated_files_match_catalog_and_canonical_skills(self) -> None:
        build_adapters.validate_configuration()
        self.assertEqual([], build_adapters.find_drift())

    def test_drift_check_compares_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            expected = Path(temp) / "expected"
            actual = Path(temp) / "actual"
            for root in (expected, actual):
                (root / "skill").mkdir(parents=True)
            (expected / "skill" / "SKILL.md").write_bytes(b"same size\n")
            (actual / "skill" / "SKILL.md").write_bytes(b"same SIZE\n")
            shutil.copystat(expected / "skill" / "SKILL.md", actual / "skill" / "SKILL.md")
            (expected / "skill" / "notes.md").write_bytes(b"kept\n")
            (actual / "skill" / "stale.md").write_bytes(b"left over\n")
            (expected / "marketplace.json").write_bytes(b"{}\n")
            (actual / "marketplace.json").write_bytes(b"[]\n")
            shutil.copystat(expected / "marketplace.json", actual / "marketplace.json")

            tree = build_adapters.compare(expected / "skill", actual / "skill")
            single = build_adapters.compare(expected / "marketplace.json", actual / "marketplace.json")

        kinds = sorted(problem.split(":")[0] + " " + problem.rsplit("/", 1)[-1] for problem in tree)
        self.assertEqual(["changed SKILL.md", "missing notes.md", "unexpected stale.md"], kinds)
        self.assertEqual(1, len(single))
        self.assertTrue(single[0].startswith("changed: "), single)

    def test_skill_files_stay_under_16_kb(self) -> None:
        for root in (ROOT / "skills", ROOT / "adapters"):
            for path in root.rglob("*"):
                if path.is_file() and path.suffix != ".png":
                    self.assertLess(path.stat().st_size, MAX_SKILL_FILE_BYTES, path)

    def test_catalog_ships_one_suite(self) -> None:
        self.assertEqual([SUITE], list(PLUGINS))
        self.assertEqual(ALL_SKILLS, directory_names(ROOT / "skills"))
        self.assertEqual(sorted(ALL_SKILLS), sorted(PLUGINS[SUITE].skills))
        for folder in ("adapters/codex/plugins", "adapters/claude/plugins", "assets/plugins"):
            self.assertEqual({SUITE}, directory_names(ROOT / folder), folder)

    def test_manual_only_skills_are_deliberate(self) -> None:
        self.assertEqual(MANUAL_ONLY, {name for name, skill in SKILLS.items() if not skill.implicit})

    def test_invocation_settings_match_catalog(self) -> None:
        for name, skill in SKILLS.items():
            codex = (
                ROOT / "adapters/codex/plugins" / SUITE / "skills" / name / "agents" / "openai.yaml"
            ).read_text(encoding="utf-8")
            self.assertIn(f"allow_implicit_invocation: {str(skill.implicit).lower()}", codex, name)
            self.assertIn('icon_small: "./assets/icon.png"', codex, name)
            self.assertIn('icon_large: "./assets/icon.png"', codex, name)
            claude = (ROOT / "adapters/claude/plugins" / SUITE / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            manual = "disable-model-invocation: true" in claude.split("---", 2)[1]
            self.assertEqual(not skill.implicit, manual, name)

    def test_descriptions_have_trigger_lines(self) -> None:
        sources = [ROOT / "skills" / name / "SKILL.md" for name in ALL_SKILLS]
        sources += list((ROOT / "skills").glob("*/variants/*.md"))
        for path in sources:
            skill = path.parent.name if path.name == "SKILL.md" else path.parents[1].name
            fields = frontmatter(path)
            description = fields["description"]
            self.assertEqual(skill, fields.get("name"), path)
            self.assertIn("Use when", description, path)
            self.assertLessEqual(len(description), MAX_DESCRIPTION_CHARS, path)
            self.assertNotRegex(description, "[<>]", path)

    def test_frontmatter_check_rejects_values_plain_yaml_cannot_hold(self) -> None:
        for value in ("Designs deep modules: small interfaces.", "Use C # here.", "[draft] skill"):
            text = f"---\nname: sample\ndescription: {value}\n---\n"
            self.assertEqual(1, len(build_adapters.frontmatter_problems(text)), value)
        quoted = '---\nname: sample\ndescription: "Designs deep modules: small interfaces."\n---\n'
        self.assertEqual([], build_adapters.frontmatter_problems(quoted))
        self.assertEqual(
            ["missing closing frontmatter marker"], build_adapters.frontmatter_problems("---\nname: x\n")
        )

    def test_every_canonical_skill_has_a_unique_icon(self) -> None:
        digests = {
            hashlib.sha256((ROOT / "skills" / name / "assets" / "icon.png").read_bytes()).hexdigest()
            for name in ALL_SKILLS
        }
        self.assertEqual(len(ALL_SKILLS), len(digests))

    def test_retired_artwork_is_preserved(self) -> None:
        self.assertEqual(
            {
                "grilling.png",
                "grill-with-docs.png",
                "prompting-opus-5.png",
                "prompting-fable-5.png",
                "luna-subagents.png",
                "ask-pro.png",
                "claude-handoff.png",
                "comment-discipline.png",
                "contract-review.png",
                "domain-modeling.png",
                "grill-me.png",
                "superpowers.png",
                "tdd.png",
            },
            {path.name for path in (ROOT / "assets/retired-skills").glob("*.png")},
        )
        self.assertEqual(
            {"agent-control.png", "communication-tools.png", "frontend-design.png"},
            {path.name for path in (ROOT / "assets/retired-plugins").glob("*.png")},
        )

    def test_marketplace_entries_resolve_to_matching_manifests(self) -> None:
        codex_marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        claude_marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual([SUITE], [entry["name"] for entry in codex_marketplace["plugins"]])
        self.assertEqual([SUITE], [entry["name"] for entry in claude_marketplace["plugins"]])
        for entry in codex_marketplace["plugins"]:
            plugin_root = ROOT / entry["source"]["path"]
            manifest = json.loads((plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(entry["name"], manifest["name"])
            self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
            self.assertTrue((plugin_root / manifest["skills"]).is_dir(), entry["name"])
            for field in ("composerIcon", "logo", "logoDark"):
                self.assertTrue((plugin_root / manifest["interface"][field]).is_file(), field)
        for entry in claude_marketplace["plugins"]:
            plugin_root = ROOT / entry["source"]
            manifest = json.loads((plugin_root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(entry["name"], manifest["name"])
            self.assertEqual(entry["version"], manifest["version"])
            self.assertTrue((plugin_root / "skills").is_dir(), entry["name"])

    def test_only_claude_copies_sit_where_grok_looks(self) -> None:
        # Grok Build loads plugins/<name>/ from Claude Code's copy of this repository and ignores the
        # marketplace source, so another host's copy there would lose the Claude-only settings.
        claude_marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        sources = {entry["name"]: (ROOT / entry["source"]).resolve() for entry in claude_marketplace["plugins"]}
        convention = ROOT / "plugins"
        folders = [path for path in convention.iterdir() if path.is_dir()] if convention.is_dir() else []
        for folder in folders:
            self.assertEqual(sources.get(folder.name), folder.resolve(), folder)

    def test_merged_skills_keep_specialist_behavior(self) -> None:
        review = (ROOT / "skills/conceptual-review/SKILL.md").read_text(encoding="utf-8")
        for marker in ("Reasoning mode", "Spec mode", "Acceptance power", "BLOCKING", "AMEND", "NIT", "**Ready**"):
            self.assertIn(marker, review)
        bugs = (ROOT / "skills/diagnosing-bugs/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("After two failed fix attempts, stop.", bugs)

    def test_subagent_fan_out_needs_an_explicit_ask(self) -> None:
        design = (ROOT / "skills/codebase-design/SKILL.md").read_text(encoding="utf-8")
        twice = (ROOT / "skills/codebase-design/DESIGN-IT-TWICE.md").read_text(encoding="utf-8")
        self.assertIn("use it only when the user asks for it", design)
        self.assertIn("Run this only when the user asks", twice)

    def test_orchestrate_uses_host_native_variants(self) -> None:
        source = ROOT / "skills/orchestrate"
        codex = ROOT / "adapters/codex/plugins" / SUITE / "skills/orchestrate"
        claude = ROOT / "adapters/claude/plugins" / SUITE / "skills/orchestrate"
        self.assertEqual((source / "SKILL.md").read_bytes(), (codex / "SKILL.md").read_bytes())
        native = (source / "variants/claude.SKILL.md").read_text(encoding="utf-8")
        generated = (claude / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(native, generated.replace("disable-model-invocation: true\n", "", 1))
        self.assertNotEqual(native, (source / "SKILL.md").read_text(encoding="utf-8"))
        for token in ("Luna", "Terra", "Sol", "Astra", "gpt-"):
            self.assertNotIn(token, native)
        for folder in (codex, claude):
            self.assertFalse((folder / "variants").exists())
        self.assertEqual({"claude.SKILL.md"}, {p.name for p in (source / "variants").iterdir()})

    def test_no_skill_file_is_named_like_a_host_instruction_file(self) -> None:
        # Hosts auto-load these names, and Windows and macOS ignore case.
        instruction_files = {"agents.md", "agents.local.md", "agents.override.md", "claude.md", "claude.local.md"}
        for root in (ROOT / "skills", ROOT / "adapters"):
            for path in root.rglob("*"):
                self.assertNotIn(path.name.lower(), instruction_files, path)

    def test_retired_hosts_are_absent_from_active_distribution(self) -> None:
        self.assertEqual({"claude", "codex"}, directory_names(ROOT / "adapters"))
        self.assertFalse((ROOT / ".cursor-plugin").exists())
        self.assertFalse((ROOT / "marketplace.json").exists())

    def test_retired_host_artwork_is_preserved(self) -> None:
        archive = ROOT / "assets/retired-hosts"
        manifest = json.loads((archive / "manifest.json").read_text(encoding="utf-8"))
        # The retirement snapshot is fixed even when the active catalog grows.
        self.assertEqual(38, len(manifest))
        actual = {
            p.relative_to(archive).as_posix()
            for host in ("cursor", "zcode")
            for p in (archive / host).rglob("*")
            if p.is_file()
        }
        self.assertEqual(set(manifest), actual)
        for relative, digest in manifest.items():
            path = Path(relative)
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertIn(path.parts[0], {"cursor", "zcode"})
            self.assertEqual(".png", path.suffix)
            self.assertEqual(
                digest, hashlib.sha256((archive / path).read_bytes()).hexdigest(), relative
            )

    def test_skill_references_resolve_and_stale_syntax_is_absent(self) -> None:
        skill_reference = re.compile(r"\$([a-z][a-z0-9-]+)")
        slash_reference = re.compile(r"`/[a-z][a-z0-9-]+`")
        for path in (ROOT / "skills").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertEqual([], slash_reference.findall(text), path)
            self.assertNotIn("fork_context", text, path)
            for name in skill_reference.findall(text):
                self.assertIn(name, ALL_SKILLS, f"{path}: ${name}")

    def test_attribution_and_subdirectory_license_are_present(self) -> None:
        origin = (ROOT / "ORIGIN.md").read_text(encoding="utf-8")
        self.assertIn("anthropics/skills", origin)
        self.assertIn("obra/superpowers", origin)
        self.assertIn("mattpocock/skills", origin)
        apache = (ROOT / "skills" / "frontend-design" / "LICENSE.txt").read_text(encoding="utf-8")
        self.assertIn("Apache License", apache)

    def test_distribution_contains_no_workflow_hooks(self) -> None:
        roots = [ROOT / "skills", ROOT / "adapters"]
        matches = [
            path
            for root in roots
            for path in root.rglob("*")
            if "hook" in path.name.lower() or "pre-commit" in path.name.lower()
        ]
        self.assertEqual([], matches)


if __name__ == "__main__":
    unittest.main()
