from __future__ import annotations

import argparse
import filecmp
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
PLUGIN_ASSETS = ROOT / "assets" / "plugins"
CODEX_PLUGINS = ROOT / "plugins"
CLAUDE_PLUGINS = ROOT / "adapters" / "claude" / "plugins"


def write_text_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


@dataclass(frozen=True)
class SkillMetadata:
    display_name: str
    short_description: str
    default_prompt: str | None = None


@dataclass(frozen=True)
class PluginDefinition:
    codex_skills: tuple[str, ...]
    claude_skills: tuple[str, ...]


SKILLS = {
    "grill-me": SkillMetadata("Grill Me", "Sharpen a plan through structured interview"),
    "domain-modeling": SkillMetadata(
        "Domain Modeling", "Build and sharpen a project's domain language"
    ),
    "diagnosing-bugs": SkillMetadata("Diagnosing Bugs", "Diagnose difficult bugs and regressions"),
    "comment-discipline": SkillMetadata(
        "Comment Discipline",
        "Stop comments from replacing durable engineering",
        "Use $comment-discipline to prevent comment-backed shortcuts and clean up comment debt in this scope.",
    ),
    "tdd": SkillMetadata("TDD", "Develop through a red-green feedback loop"),
    "codebase-design": SkillMetadata("Codebase Design", "Design deeper modules and cleaner seams"),
    "conceptual-review": SkillMetadata(
        "Conceptual Review",
        "Challenge technical reasoning before implementation",
        "Use $conceptual-review to check whether this technical conclusion follows from its evidence and assumptions.",
    ),
    "contract-review": SkillMetadata(
        "Contract Review",
        "Test an implementation contract against evidence",
        "Use $contract-review to determine whether this implementation contract is ready.",
    ),
    "repository-docs": SkillMetadata(
        "Repository Docs",
        "Map and retrieve trustworthy repository guidance",
        "Use $repository-docs to map this repository's documentation and load the guidance needed for my task.",
    ),
    "maintaining-docs": SkillMetadata(
        "Maintaining Docs",
        "Create and update evidence-backed repository docs",
        "Use $maintaining-docs to update this repository's documentation from the verified change.",
    ),
    "english": SkillMetadata(
        "English",
        "Plain-English rescue for technical explanations",
        "Use $english to explain the selected text or current situation in plain language without taking action.",
    ),
    "concise": SkillMetadata(
        "Concise",
        "Compression without loss for clear answers",
        "Use $concise to give the shortest complete answer without losing evidence, caveats, or next actions.",
    ),
    "orchestrate": SkillMetadata(
        "Orchestrate",
        "Coordinate focused subagents",
        "Use $orchestrate to delegate bounded supporting work while keeping decisions and integration in the parent.",
    ),
    "superpowers": SkillMetadata(
        "Superpowers",
        "Adaptive build, TDD, and verification workflow",
        "Use $superpowers for a compact, adaptive build-and-verify workflow.",
    ),
    "frontend-design": SkillMetadata(
        "Frontend Design",
        "Create distinctive intentional interfaces",
        "Use $frontend-design to give this interface a distinctive, intentional visual direction.",
    ),
}

HOST_VARIANTS = {
    "orchestrate": frozenset({"claude"}),
}


PLUGINS = {
    "engineering-workflows": PluginDefinition(
        codex_skills=(
            "grill-me",
            "domain-modeling",
            "diagnosing-bugs",
            "comment-discipline",
            "tdd",
            "codebase-design",
            "conceptual-review",
            "contract-review",
            "repository-docs",
            "maintaining-docs",
        ),
        claude_skills=(
            "grill-me",
            "domain-modeling",
            "diagnosing-bugs",
            "comment-discipline",
            "tdd",
            "codebase-design",
            "conceptual-review",
            "contract-review",
            "repository-docs",
            "maintaining-docs",
        ),
    ),
    "communication-tools": PluginDefinition(
        codex_skills=("english", "concise"),
        claude_skills=("english", "concise"),
    ),
    "agent-control": PluginDefinition(
        codex_skills=("orchestrate", "superpowers"),
        claude_skills=("orchestrate", "superpowers"),
    ),
    "frontend-design": PluginDefinition(
        codex_skills=("frontend-design",),
        claude_skills=("frontend-design",),
    ),
}


def add_claude_manual_only(skill_md: Path) -> None:
    text = skill_md.read_text(encoding="utf-8")
    if "disable-model-invocation:" in text:
        raise ValueError(f"Claude-only frontmatter leaked into canonical source: {skill_md}")
    closing = text.find("\n---", 4)
    if closing == -1:
        raise ValueError(f"Missing closing frontmatter marker: {skill_md}")
    text = text[:closing] + "\ndisable-model-invocation: true" + text[closing:]
    write_text_lf(skill_md, text)


def add_codex_metadata(skill_dir: Path, name: str) -> None:
    metadata = SKILLS[name]
    agents = skill_dir / "agents"
    agents.mkdir(exist_ok=True)
    lines = [
        "interface:",
        f'  display_name: "{metadata.display_name}"',
        f'  short_description: "{metadata.short_description}"',
    ]
    if metadata.default_prompt:
        lines.append(f'  default_prompt: "{metadata.default_prompt}"')
    lines.extend(
        [
            '  icon_small: "./assets/icon.png"',
            '  icon_large: "./assets/icon.png"',
            "policy:",
            "  allow_implicit_invocation: false",
        ]
    )
    write_text_lf(agents / "openai.yaml", "\n".join(lines) + "\n")


def apply_host_variant(skill_dir: Path, name: str, host: str) -> None:
    variants = skill_dir / "variants"
    expected_hosts = HOST_VARIANTS.get(name)
    if expected_hosts is None:
        if variants.exists():
            raise ValueError(f"Unexpected host variants: {variants}")
        return

    if not variants.is_dir():
        raise ValueError(f"Missing host variants: {variants}")
    actual_hosts = {path.stem for path in variants.glob("*.md")}
    if actual_hosts != expected_hosts:
        raise ValueError(
            f"Host variant mismatch for {name}: expected {sorted(expected_hosts)}, "
            f"found {sorted(actual_hosts)}"
        )
    if host != "codex":
        shutil.copyfile(variants / f"{host}.md", skill_dir / "SKILL.md")
    shutil.rmtree(variants)


def copy_skills(names: tuple[str, ...], destination: Path, host: str) -> None:
    destination.mkdir(parents=True)
    for name in names:
        skill_dir = destination / name
        shutil.copytree(SOURCE / name, skill_dir)
        apply_host_variant(skill_dir, name, host)
        if host == "codex":
            add_codex_metadata(skill_dir, name)
        elif host == "claude":
            add_claude_manual_only(skill_dir / "SKILL.md")
        else:
            raise ValueError(f"Unsupported host: {host}")


def build_expected(root: Path) -> dict[Path, Path]:
    expected: dict[Path, Path] = {}
    for plugin_name, definition in PLUGINS.items():
        codex_root = root / "codex" / plugin_name
        claude_root = root / "claude" / plugin_name
        copy_skills(definition.codex_skills, codex_root / "skills", "codex")
        copy_skills(definition.claude_skills, claude_root / "skills", "claude")
        shutil.copytree(PLUGIN_ASSETS / plugin_name, codex_root / "assets")
        shutil.copytree(PLUGIN_ASSETS / plugin_name, claude_root / "assets")
        expected[codex_root / "skills"] = CODEX_PLUGINS / plugin_name / "skills"
        expected[codex_root / "assets"] = CODEX_PLUGINS / plugin_name / "assets"
        expected[claude_root / "skills"] = CLAUDE_PLUGINS / plugin_name / "skills"
        expected[claude_root / "assets"] = CLAUDE_PLUGINS / plugin_name / "assets"
    return expected


def compare_dirs(expected: Path, actual: Path) -> list[str]:
    if not actual.is_dir():
        return [f"missing directory: {actual}"]
    comparison = filecmp.dircmp(expected, actual)
    problems: list[str] = []

    def walk(node: filecmp.dircmp, prefix: Path) -> None:
        for name in node.left_only:
            problems.append(f"missing: {prefix / name}")
        for name in node.right_only:
            problems.append(f"unexpected: {prefix / name}")
        for name in node.diff_files:
            problems.append(f"changed: {prefix / name}")
        for name in node.funny_files:
            problems.append(f"unreadable: {prefix / name}")
        for name, child in node.subdirs.items():
            walk(child, prefix / name)

    walk(comparison, Path("."))
    return problems


def replace_tree(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def validate_configuration() -> None:
    names = {path.name for path in SOURCE.iterdir() if path.is_dir()}
    if names != set(SKILLS):
        raise SystemExit(f"Canonical skill set mismatch: {sorted(names)}")

    codex_names = [name for plugin in PLUGINS.values() for name in plugin.codex_skills]
    if len(codex_names) != len(set(codex_names)) or set(codex_names) != set(SKILLS):
        raise SystemExit("Every canonical skill must belong to exactly one Codex plugin.")

    for plugin_name, definition in PLUGINS.items():
        if not set(definition.claude_skills).issubset(definition.codex_skills):
            raise SystemExit(f"Claude skills must be a subset of Codex skills: {plugin_name}")
        if not (PLUGIN_ASSETS / plugin_name / "plugin-icon.png").is_file():
            raise SystemExit(f"Missing canonical plugin icon: {plugin_name}")

    for name in SKILLS:
        if not (SOURCE / name / "assets" / "icon.png").is_file():
            raise SystemExit(f"Missing canonical skill icon: {name}")

    variant_names = {
        path.parent.name for path in SOURCE.glob("*/variants") if path.is_dir()
    }
    if variant_names != set(HOST_VARIANTS):
        raise SystemExit(
            f"Host variant skill mismatch: expected {sorted(HOST_VARIANTS)}, "
            f"found {sorted(variant_names)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Codex and Claude Code skill adapters."
    )
    parser.add_argument("--check", action="store_true", help="Verify generated adapters without writing.")
    args = parser.parse_args()
    validate_configuration()

    with tempfile.TemporaryDirectory(prefix="agent-skills-build-") as temp:
        expected = build_expected(Path(temp))
        if args.check:
            problems = [
                problem
                for expected_path, actual_path in expected.items()
                for problem in compare_dirs(expected_path, actual_path)
            ]
            if problems:
                print("Adapter drift detected:")
                for problem in problems:
                    print(f"- {problem}")
                return 1
            print("Codex and Claude Code adapters match canonical skills.")
            return 0
        for expected_path, actual_path in expected.items():
            replace_tree(expected_path, actual_path)

    print("Built Codex and Claude Code adapters from canonical skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
