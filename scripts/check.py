#!/usr/bin/env python3
"""Структурная проверка плагина VIBEBOARDING. Запуск: python3 scripts/check.py"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []


def check(cond, msg):
    print(("✓ " if cond else "✖ ") + msg)
    if not cond:
        errors.append(msg)


def load_json(rel):
    path = ROOT / rel
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        check(False, f"валидный JSON {rel} ({exc})")
        return None


REQUIRED_FILES = [
    ".claude-plugin/marketplace.json",
    "plugins/vibeboarding/.claude-plugin/plugin.json",
    "LICENSE",
    ".gitignore",
]
for rel in REQUIRED_FILES:
    check((ROOT / rel).is_file(), f"есть файл {rel}")

marketplace = load_json(".claude-plugin/marketplace.json")
if marketplace is not None:
    check(marketplace.get("name") == "leogodnik",
          "marketplace.json: name = leogodnik")
    check(isinstance(marketplace.get("owner"), dict),
          "marketplace.json: owner — объект")
    plugins = marketplace.get("plugins")
    check(isinstance(plugins, list) and len(plugins) == 1,
          "marketplace.json: ровно один плагин")
    if isinstance(plugins, list) and plugins:
        check(plugins[0].get("name") == "vibeboarding",
              "marketplace.json: плагин называется vibeboarding")
        check(plugins[0].get("source") == "./plugins/vibeboarding",
              "marketplace.json: source = ./plugins/vibeboarding")

manifest = load_json("plugins/vibeboarding/.claude-plugin/plugin.json")
if manifest is not None:
    check(manifest.get("name") == "vibeboarding", "plugin.json: name = vibeboarding")
    check(bool(manifest.get("description")), "plugin.json: есть description")

skill_path = "plugins/vibeboarding/skills/start/SKILL.md"
check((ROOT / skill_path).is_file(), f"есть файл {skill_path}")
if (ROOT / skill_path).is_file():
    text = (ROOT / skill_path).read_text(encoding="utf-8")
    matched = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    check(bool(matched), "SKILL.md: есть YAML-фронтматтер")
    front = matched.group(1) if matched else ""
    check(re.search(r"^name:\s*start\s*$", front, re.M) is not None,
          "SKILL.md: name = start")
    check(re.search(r"^description:\s*\S", front, re.M) is not None,
          "SKILL.md: есть description")
    check(re.search(r"^disable-model-invocation:\s*true\s*$", front, re.M) is not None,
          "SKILL.md: disable-model-invocation: true")
    for anchor in ["## Step 0", "## Step 1", "## Step 2", "## Step 3",
                   "## Step 4", "## Step 5", "## Step 6", "## Step 7",
                   "## Step 8", "## Step 9", "## Tone rules", "## Generation",
                   "## Verification", "## Final report"]:
        check(anchor in text, f"SKILL.md: есть раздел «{anchor}»")
    check(text.count("financialpostpunk") == 1,
          "SKILL.md: телеграм-канал упомянут ровно один раз")

templates_path = "plugins/vibeboarding/skills/start/references/templates.md"
check((ROOT / templates_path).is_file(), f"есть файл {templates_path}")
if (ROOT / templates_path).is_file():
    templates = (ROOT / templates_path).read_text(encoding="utf-8")
    for anchor in ["## CLAUDE.md", "## Cheat sheet", "## Permissions"]:
        check(anchor in templates, f"templates.md: есть раздел «{anchor}»")
    check("acceptEdits" in templates, "templates.md: режим прав acceptEdits")
    check('"deny"' in templates, "templates.md: есть список deny")
    check("@financialpostpunk" in templates,
          "templates.md: шпаргалка упоминает телеграм-канал")

scaffolds_path = "plugins/vibeboarding/skills/start/references/scaffolds.md"
check((ROOT / scaffolds_path).is_file(), f"есть файл {scaffolds_path}")
if (ROOT / scaffolds_path).is_file():
    scaffolds = (ROOT / scaffolds_path).read_text(encoding="utf-8")
    for anchor in ["## Single file", "## Real app", "## Version control",
                   "## Launch and verify"]:
        check(anchor in scaffolds, f"scaffolds.md: есть раздел «{anchor}»")
    check("git init" in scaffolds, "scaffolds.md: каркас создаёт git-репозиторий")

templates_text = (ROOT / templates_path).read_text(encoding="utf-8") \
    if (ROOT / templates_path).is_file() else ""
check(templates_text.count("@financialpostpunk") == 1,
      "templates.md: телеграм-канал упомянут ровно один раз")

for rel in ["README.md", "plugins/vibeboarding/README.md"]:
    check((ROOT / rel).is_file(), f"есть файл {rel}")
root_readme = ROOT / "README.md"
if root_readme.is_file():
    readme = root_readme.read_text(encoding="utf-8")
    check("/plugin marketplace add" in readme,
          "README.md: есть команда установки маркетплейса")
    check("vibeboarding@leogodnik" in readme,
          "README.md: есть команда установки плагина")
    check("/vibeboarding:start" in readme, "README.md: есть команда запуска")
    check("@financialpostpunk" in readme,
          "README.md: есть упоминание телеграм-канала")

print()
if errors:
    print(f"ПРОВАЛЕНО: {len(errors)}")
    sys.exit(1)
print("ВСЁ ХОРОШО")
