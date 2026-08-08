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
    check(marketplace.get("name") == "leogodnik-plugins",
          "marketplace.json: name = leogodnik-plugins")
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

skill_path = "plugins/vibeboarding/skills/vibeboarding/SKILL.md"
check((ROOT / skill_path).is_file(), f"есть файл {skill_path}")
if (ROOT / skill_path).is_file():
    text = (ROOT / skill_path).read_text(encoding="utf-8")
    matched = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    check(bool(matched), "SKILL.md: есть YAML-фронтматтер")
    front = matched.group(1) if matched else ""
    check(re.search(r"^name:\s*vibeboarding\s*$", front, re.M) is not None,
          "SKILL.md: name = vibeboarding")
    check(re.search(r"^description:\s*\S", front, re.M) is not None,
          "SKILL.md: есть description")
    check(re.search(r"^disable-model-invocation:\s*true\s*$", front, re.M) is not None,
          "SKILL.md: disable-model-invocation: true")
    for anchor in ["## Step 0", "## Step 1", "## Step 2", "## Step 3",
                   "## Step 4", "## Step 5", "## Step 6",
                   "## Tone rules", "## Generation", "## Verification"]:
        check(anchor in text, f"SKILL.md: есть раздел «{anchor}»")
    check(text.count("@financialpostpunk") == 1,
          "SKILL.md: телеграм-канал упомянут ровно один раз")

print()
if errors:
    print(f"ПРОВАЛЕНО: {len(errors)}")
    sys.exit(1)
print("ВСЁ ХОРОШО")
