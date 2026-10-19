from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
PLUGIN_ASSETS = ROOT / "assets" / "plugins"
CODEX_PLUGINS = ROOT / "plugins"
CLAUDE_PLUGINS = ROOT / "adapters" / "claude" / "plugins"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

AUTHOR = "Statusnone"
AUTHOR_URL = "https://github.com/Statusnone420"
REPOSITORY = "https://github.com/Statusnone420/agent-skills"
PLUGIN_ICON = "./assets/plugin-icon.png"
MARKETPLACE_NAME = "statusnone-agent-skills"
MARKETPLACE_DISPLAY_NAME = "Statusnone Agent Skills"
MARKETPLACE_DESCRIPTION = "Explicit-only personal workflows maintained by Statusnone."


def write_text_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_lf(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


@dataclass(frozen=True)
class SkillMetadata:
    display_name: str
    short_description: str
    default_prompt: str | None = None


@dataclass(frozen=True)
class PluginDefinition:
    skills: tuple[str, ...]
    version: str
    description: str
    display_name: str
    short_description: str
    long_description: str
    category: str
    capabilities: tuple[str, ...]
    keywords: tuple[str, ...]
    brand_color: str
    default_prompts: tuple[str, ...]
    license: str = "MIT"


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
        skills=(
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
        version="0.5.1",
        description=(
            "Explicit-only engineering, debugging, comment discipline, design, planning, "
            "contract review, and documentation workflows."
        ),
        display_name="Engineering Workflows",
        short_description="Manual engineering and planning workflows",
        long_description=(
            "Ten explicit-only workflows for planning, domain modeling, debugging, comment "
            "discipline, TDD, codebase design, conceptual and contract review, and repository "
            "documentation."
        ),
        category="Developer Tools",
        capabilities=("Interactive", "Read", "Write"),
        keywords=(
            "engineering",
            "debugging",
            "comments",
            "tdd",
            "planning",
            "domain-modeling",
            "reasoning",
        ),
        brand_color="#6D4AFF",
        default_prompts=(
            "Use $grill-me to stress-test this plan.",
            "Use $diagnosing-bugs to diagnose this issue.",
            "Use $comment-discipline to prevent comment-backed shortcuts and clean up comment debt in this scope.",
        ),
    ),
    "communication-tools": PluginDefinition(
        skills=("english", "concise"),
        version="0.4.1",
        description="Explicit-only tools for clearer, denser technical communication.",
        display_name="Communication Tools",
        short_description="Manual clear communication",
        long_description="Two explicit-only tools for plain-English rescue and compression without loss.",
        category="Productivity",
        capabilities=("Interactive", "Read"),
        keywords=("communication", "plain-english", "concise", "explanation"),
        brand_color="#7C4DFF",
        default_prompts=(
            "Use $english to explain this in plain language.",
            "Use $concise to compress this answer without losing important information.",
        ),
    ),
    "agent-control": PluginDefinition(
        skills=("orchestrate", "superpowers"),
        version="0.3.1",
        description=(
            "Explicit-only workflows for proportional development discipline and bounded agent "
            "coordination."
        ),
        display_name="Agent Control",
        short_description="Manual coordination and development control",
        long_description=(
            "Two explicit-only workflows for proportional development discipline and bounded agent "
            "coordination."
        ),
        category="Developer Tools",
        capabilities=("Interactive", "Read", "Write"),
        keywords=("agents", "orchestration", "delegation", "workflow", "superpowers"),
        brand_color="#7C3AED",
        default_prompts=(
            "Use $superpowers for a compact build-and-verify workflow.",
            "Use $orchestrate to coordinate this large-scope task.",
        ),
    ),
    "frontend-design": PluginDefinition(
        skills=("frontend-design",),
        version="0.1.1",
        description="Statusnone-maintained guidance for distinctive, intentional interface design.",
        display_name="Frontend Design",
        short_description="Distinctive intentional interface design",
        long_description=(
            "An explicit-only Statusnone-maintained Codex and Claude adaptation for opinionated, "
            "subject-specific interface design."
        ),
        category="Design",
        capabilities=("Read", "Write"),
        keywords=("frontend", "design", "ui", "ux", "visual-direction"),
        brand_color="#8B5CF6",
        default_prompts=(
            "Use $frontend-design to give this interface a distinctive visual direction.",
        ),
        license="Apache-2.0",
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


def repository_path(path: Path) -> str:
    return "./" + path.relative_to(ROOT).as_posix()


def codex_manifest(name: str, plugin: PluginDefinition) -> dict:
    return {
        "name": name,
        "version": plugin.version,
        "description": plugin.description,
        "author": {"name": AUTHOR, "url": AUTHOR_URL},
        "repository": REPOSITORY,
        "license": plugin.license,
        "keywords": list(plugin.keywords),
        "skills": "./skills/",
        "interface": {
            "displayName": plugin.display_name,
            "shortDescription": plugin.short_description,
            "longDescription": plugin.long_description,
            "composerIcon": PLUGIN_ICON,
            "logo": PLUGIN_ICON,
            "logoDark": PLUGIN_ICON,
            "brandColor": plugin.brand_color,
            "developerName": AUTHOR,
            "category": plugin.category,
            "capabilities": list(plugin.capabilities),
            "websiteURL": REPOSITORY,
            "defaultPrompt": list(plugin.default_prompts),
        },
    }


def claude_manifest(name: str, plugin: PluginDefinition) -> dict:
    return {
        "name": name,
        "version": plugin.version,
        "description": plugin.description,
        "author": {"name": AUTHOR},
        "homepage": REPOSITORY,
        "repository": REPOSITORY,
        "license": plugin.license,
        "keywords": list(plugin.keywords),
    }


def codex_marketplace() -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": MARKETPLACE_DISPLAY_NAME},
        "plugins": [
            {
                "name": name,
                "source": {"source": "local", "path": repository_path(CODEX_PLUGINS / name)},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": plugin.category,
            }
            for name, plugin in PLUGINS.items()
        ],
    }


def claude_marketplace() -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "owner": {"name": AUTHOR},
        "description": MARKETPLACE_DESCRIPTION,
        "plugins": [
            {
                "name": name,
                "source": repository_path(CLAUDE_PLUGINS / name),
                "description": plugin.description,
                "version": plugin.version,
                "author": {"name": AUTHOR},
            }
            for name, plugin in PLUGINS.items()
        ],
    }


def build_plugin(destination: Path, name: str, plugin: PluginDefinition, host: str) -> None:
    copy_skills(plugin.skills, destination / "skills", host)
    shutil.copytree(PLUGIN_ASSETS / name, destination / "assets")
    if host == "codex":
        write_json(destination / ".codex-plugin" / "plugin.json", codex_manifest(name, plugin))
    else:
        write_json(destination / ".claude-plugin" / "plugin.json", claude_manifest(name, plugin))


def build_expected(root: Path) -> dict[Path, Path]:
    codex_root = root / "codex"
    claude_root = root / "claude"
    for name, plugin in PLUGINS.items():
        build_plugin(codex_root / name, name, plugin, "codex")
        build_plugin(claude_root / name, name, plugin, "claude")
    write_json(root / "codex-marketplace.json", codex_marketplace())
    write_json(root / "claude-marketplace.json", claude_marketplace())
    return {
        codex_root: CODEX_PLUGINS,
        claude_root: CLAUDE_PLUGINS,
        root / "codex-marketplace.json": CODEX_MARKETPLACE,
        root / "claude-marketplace.json": CLAUDE_MARKETPLACE,
    }


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def files_under(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def compare(expected: Path, actual: Path) -> list[str]:
    if expected.is_file():
        if not actual.is_file():
            return [f"missing: {display(actual)}"]
        if expected.read_bytes() != actual.read_bytes():
            return [f"changed: {display(actual)}"]
        return []
    if not actual.is_dir():
        return [f"missing: {display(actual)}"]
    expected_files = files_under(expected)
    actual_files = files_under(actual)
    problems = [f"missing: {display(actual / path)}" for path in sorted(expected_files - actual_files)]
    problems += [
        f"unexpected: {display(actual / path)}" for path in sorted(actual_files - expected_files)
    ]
    problems += [
        f"changed: {display(actual / path)}"
        for path in sorted(expected_files & actual_files)
        if (expected / path).read_bytes() != (actual / path).read_bytes()
    ]
    return problems


def find_drift() -> list[str]:
    with tempfile.TemporaryDirectory(prefix="agent-skills-build-") as temp:
        expected = build_expected(Path(temp))
        return [
            problem
            for expected_path, actual_path in expected.items()
            for problem in compare(expected_path, actual_path)
        ]


def replace(source: Path, destination: Path) -> None:
    if destination.is_dir():
        shutil.rmtree(destination)
    elif destination.exists():
        destination.unlink()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copyfile(source, destination)


def validate_configuration() -> None:
    names = {path.name for path in SOURCE.iterdir() if path.is_dir()}
    if names != set(SKILLS):
        raise SystemExit(f"Canonical skill set mismatch: {sorted(names)}")

    memberships = [name for plugin in PLUGINS.values() for name in plugin.skills]
    if len(memberships) != len(set(memberships)) or set(memberships) != set(SKILLS):
        raise SystemExit("Every canonical skill must belong to exactly one plugin.")

    artwork = {path.name for path in PLUGIN_ASSETS.iterdir() if path.is_dir()}
    if artwork != set(PLUGINS):
        raise SystemExit(f"Plugin artwork mismatch: {sorted(artwork)}")
    for plugin_name in PLUGINS:
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
        description="Build Codex and Claude Code adapters and marketplaces from skills/ and the catalog."
    )
    parser.add_argument("--check", action="store_true", help="Verify generated files without writing.")
    args = parser.parse_args()
    validate_configuration()

    if args.check:
        problems = find_drift()
        if problems:
            print("Adapter drift detected:")
            for problem in problems:
                print(f"- {problem}")
            return 1
        print("Codex and Claude Code adapters and marketplaces match the catalog and canonical skills.")
        return 0

    with tempfile.TemporaryDirectory(prefix="agent-skills-build-") as temp:
        for expected_path, actual_path in build_expected(Path(temp)).items():
            replace(expected_path, actual_path)

    print("Built Codex and Claude Code adapters and marketplaces from the catalog and canonical skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
