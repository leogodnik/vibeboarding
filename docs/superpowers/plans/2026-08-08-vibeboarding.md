# VIBEBOARDING — план реализации

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Собрать плагин Claude Code `vibeboarding`, который через короткое интервью на языке пользователя создаёт готовый к работе проект для человека без айти-бэкграунда.

**Architecture:** Плагин-маркетплейс с одним плагином и одним скиллом. Продукт целиком состоит из markdown и JSON — исполняемого кода нет, кроме проверочного скрипта. Скилл разбит на три файла: `SKILL.md` (всегда в контексте: интервью, тон, порядок работы) и два справочника в `references/`, которые скилл читает только на этапе генерации, чтобы не занимать контекст во время разговора.

**Tech Stack:** Markdown, JSON, YAML-фронтматтер, Python 3 (только для проверочного скрипта), git.

## Global Constraints

Эти требования действуют во всех задачах.

- Имена: маркетплейс `leogodnik-plugins`, плагин `vibeboarding`, скилл `start`, команда вызова `/vibeboarding:start` (короткое `/start` работает так же).
- Инструкции внутри `SKILL.md` и `references/*.md` пишутся **на английском**. Всё, что видит пользователь (вопросы, сводки, отчёты, созданные файлы), — на языке, выбранном на шаге 0.
- В генерируемых проектах **не создавать**: git-хуков, docs-gate, структуры `docs/` с ADR, методологического слоя, монорепозитория, многопользовательской изоляции данных (RLS).
- Синтаксис конфигов Claude Code проверен по документации 2026-08-08 и зафиксирован ниже. Значения использовать буквально:
  - Фронтматтер скилла: `name`, `description`, `disable-model-invocation: true`. Все поля опциональны, но эти три обязательны в нашем случае.
  - `marketplace.json` обязательные поля: `name` (kebab-case), `owner` (объект), `plugins` (массив).
  - `plugin.json`: обязателен только `name`; остальное — метаданные.
  - `permissions.defaultMode` допускает: `default`, `acceptEdits`, `plan`, `auto`, `bypassPermissions`, `dontAsk`. Используем `acceptEdits`.
  - `deny` перекрывает `allow` во всех режимах. Формат правила: `Tool(pattern)`, например `Bash(npm run test:*)`, `Read(./.env)`. `deny` — сеть, а не гарантия: правило `Bash()` не ловит составные команды (`cd x && rm -rf y`), а форма `:*` не покрывает голую команду — поэтому в списке есть и голые формы (`Bash(rm)`, `Bash(git reset --hard)`, `Bash(git clean)`).
  - Синтаксис `permissions` в шаблоне зафиксирован, но перед записью файла модель обязана сверить его с актуальной документацией Claude Code и следовать документации, если он изменился (эта часть конфига дрейфует).
  - Файл локальных прав: `.claude/settings.local.json`, в `.gitignore`.
- Имена маркетплейсов, зарезервированные Anthropic, использовать нельзя (`claude-plugins-official`, `anthropic-plugins`, `claude-for-financial-services` и т.п.). `leogodnik-plugins` под запрет не попадает.
- **Телеграм-канал автора `@financialpostpunk`** упоминается ровно в трёх местах, каждый раз одной строкой и по делу, без рекламного тона:
  1. Корневой `README.md` — строка в конце: канал, из которого вырос плагин.
  2. Шпаргалка в сгенерированном проекте — в разделе «Если что-то сломалось»: куда написать, если Клод не справился.
  3. Финальный отчёт скилла после генерации — последняя строка.
  Больше нигде. В `CLAUDE.md` сгенерированного проекта, в `plugin.json` и в коде — не упоминать.
- Каждая задача заканчивается зелёным `python3 scripts/check.py` и коммитом.
- Рабочая директория: `/Users/leogodnik/Starter Skill/vibeboarding` (git-репозиторий уже создан, в нём один коммит со спецификацией).

## Структура файлов

| Файл | Ответственность |
| :--- | :--- |
| `scripts/check.py` | Структурная проверка: наличие файлов, валидность JSON, обязательные поля и разделы |
| `.claude-plugin/marketplace.json` | Каталог маркетплейса: один плагин `vibeboarding` |
| `plugins/vibeboarding/.claude-plugin/plugin.json` | Манифест плагина: метаданные |
| `plugins/vibeboarding/skills/start/SKILL.md` | Ядро: фронтматтер, языковая политика, тон, семь шагов интервью, порядок генерации, финальная проверка |
| `plugins/vibeboarding/skills/start/references/templates.md` | Шаблоны трёх создаваемых файлов: `CLAUDE.md`, шпаргалка для человека, `.claude/settings.local.json` |
| `plugins/vibeboarding/skills/start/references/scaffolds.md` | Два варианта каркаса проекта (один HTML-файл / настоящее приложение) и процедура запуска с проверкой |
| `plugins/vibeboarding/README.md` | Документация плагина |
| `README.md` | Документация репозитория: что это, как поставить |
| `LICENSE` | MIT |
| `.gitignore` | Служебные файлы |

---

### Task 1: Каркас репозитория и проверочный скрипт

**Files:**
- Create: `scripts/check.py`
- Create: `.claude-plugin/marketplace.json`
- Create: `plugins/vibeboarding/.claude-plugin/plugin.json`
- Create: `LICENSE`
- Create: `.gitignore`

**Interfaces:**
- Produces: `python3 scripts/check.py` — команда проверки, возвращает 0 при успехе и 1 при ошибке. Функция `check(cond, msg)` внутри скрипта — точка расширения для следующих задач.

- [ ] **Step 1: Написать падающую проверку**

Создать `scripts/check.py`:

```python
#!/usr/bin/env python3
"""Структурная проверка плагина VIBEBOARDING. Запуск: python3 scripts/check.py"""
import json
import pathlib
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

print()
if errors:
    print(f"ПРОВАЛЕНО: {len(errors)}")
    sys.exit(1)
print("ВСЁ ХОРОШО")
```

- [ ] **Step 2: Запустить проверку и убедиться, что она падает**

Выполнить: `cd "/Users/leogodnik/Starter Skill/vibeboarding" && python3 scripts/check.py`
Ожидается: строки `✖ есть файл .claude-plugin/marketplace.json` и остальные, в конце `ПРОВАЛЕНО: 4`, код возврата 1.

- [ ] **Step 3: Создать `.claude-plugin/marketplace.json`**

```json
{
  "name": "leogodnik-plugins",
  "owner": { "name": "Leonid Godnik" },
  "version": "1.0.0",
  "description": "Плагины Claude Code для курса «вайб-кодинг для финансистов».",
  "plugins": [
    {
      "name": "vibeboarding",
      "source": "./plugins/vibeboarding",
      "version": "0.1.0",
      "description": "VIBEBOARDING — старт нового проекта для тех, кто не программист: короткое интервью на понятном языке, дальше всё делает Клод.",
      "keywords": ["bootstrap", "beginners", "non-technical", "multilingual"]
    }
  ]
}
```

- [ ] **Step 4: Создать `plugins/vibeboarding/.claude-plugin/plugin.json`**

```json
{
  "name": "vibeboarding",
  "displayName": "VIBEBOARDING",
  "version": "0.1.0",
  "description": "Старт нового проекта для тех, кто не программист. Короткое интервью на языке пользователя — что вы хотите сделать, кто будет пользоваться, откуда данные — и Клод сам создаёт работающий проект, короткий CLAUDE.md, шпаргалку для человека и безопасные настройки прав.",
  "author": { "name": "Leonid Godnik" },
  "license": "MIT",
  "keywords": ["bootstrap", "beginners", "non-technical", "multilingual", "vibe-coding"]
}
```

- [ ] **Step 5: Создать `LICENSE`**

Файл MIT-лицензии с строкой `Copyright (c) 2026 Leonid Godnik`. Полный канонический текст MIT.

- [ ] **Step 6: Создать `.gitignore`**

```gitignore
.DS_Store
__pycache__/
*.pyc
.claude/settings.local.json
```

- [ ] **Step 7: Запустить проверку и убедиться, что она проходит**

Выполнить: `python3 scripts/check.py`
Ожидается: все строки с `✓`, в конце `ВСЁ ХОРОШО`, код возврата 0.

- [ ] **Step 8: Коммит**

```bash
git add scripts/check.py .claude-plugin plugins LICENSE .gitignore
git commit -m "feat: каркас репозитория, манифесты и проверочный скрипт"
```

---

### Task 2: Ядро скилла — интервью

**Files:**
- Create: `plugins/vibeboarding/skills/start/SKILL.md`
- Modify: `scripts/check.py` (добавить блок проверок SKILL.md перед итоговым `print()`)

**Interfaces:**
- Consumes: `check()` и `ROOT` из `scripts/check.py` (Task 1).
- Produces: файл `SKILL.md` с англоязычными заголовками-якорями `## Step 0` … `## Step 7`, `## Tone rules`, `## Generation`, `## Verification`, `## Final report` — следующие задачи ссылаются на эти якоря и добавляют к ним `references/`.

- [ ] **Step 1: Написать падающую проверку**

Добавить в `scripts/check.py` перед финальным блоком `print()`:

```python
import re

skill_path = "plugins/vibeboarding/skills/start/SKILL.md"
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
                   "## Step 4", "## Step 5", "## Step 6", "## Step 7",
                   "## Tone rules", "## Generation", "## Verification",
                   "## Final report"]:
        check(anchor in text, f"SKILL.md: есть раздел «{anchor}»")
    check(text.count("@financialpostpunk") == 1,
          "SKILL.md: телеграм-канал упомянут ровно один раз")
```

- [ ] **Step 2: Запустить проверку и убедиться, что она падает**

Выполнить: `python3 scripts/check.py`
Ожидается: `✖ есть файл plugins/vibeboarding/skills/start/SKILL.md`, `ПРОВАЛЕНО: 1`, код возврата 1.

- [ ] **Step 3: Написать `SKILL.md`**

Фронтматтер — буквально:

```yaml
---
name: vibeboarding
description: "Start a brand-new project for someone who is not a programmer. Asks a short, jargon-free interview in the user's own language — what they want to build, who will use it, where the data comes from, how they want to launch it — then builds a working project plus a short CLAUDE.md, a plain-language cheat sheet, and safe permission settings. Use ONLY when explicitly starting a new project from scratch; invoke manually with /vibeboarding:start (the bare /start also works)."
disable-model-invocation: true
---
```

Тело, разделы строго в этом порядке:

**Вводный абзац.** Одно-два предложения: это интервью-бутстрап для непрограммиста; всё общение и все созданные файлы — на языке пользователя; сами эти инструкции остаются на английском.

**`## Language policy`** — правило: инструкции скилла на английском; все вопросы, сводки, отчёты и содержимое созданных файлов — на языке из шага 0; код, пути к файлам и имена настроек не переводятся.

**`## Interview rules`** — механика разговора:
- One step, one turn. Ask exactly one thing per turn and wait for the answer.
- Never mix free text with a picker widget in one turn: a picker consumes the turn and any free-text question in the same message is lost. A turn is either fully free-text or fully a picker.
- Every picker step **except Step 0** offers an explicit "I don't know — you decide" option; шаг 0 явно выведен из-под правила прямо в его формулировке — все четыре слота заняты языками, и до выбора языка нет осмысленного умолчания. Taking the option is never penalised: pick a sensible option, name it in one short sentence, move on. Never reply with "please clarify".
- Never ask about anything the user would have to look up. Derive technical decisions from the plain-language answers instead.
- Adapt: if an answer makes a later question pointless, skip it.

**`## Step 0. Language`** — отдельный ход, виджет выбора, без свободного текста. Ровно четыре варианта, потому что виджет принимает от двух до четырёх: `Русский · English · 中文 (简体) · Другой / Other`. Язык ещё не известен, поэтому текст вопроса на шаге 0 показывается **двуязычно** — по-русски и по-английски, — а подпись четвёртого варианта буквально `Другой / Other`. Варианта «не знаю» на шаге 0 нет (см. исключение в `## Interview rules`). Если выбран «Другой / Other» — следующим ходом принять название языка свободным текстом. Весь дальнейший разговор и все созданные файлы — на выбранном языке.

**`## Step 1. Mode`** — виджет выбора из трёх вариантов. Формулировки для пользователя (перевести на язык шага 0):
- «Быстро» — «Я сам подберу технику и просто скажу одной фразой, что сделаю. Меньше вопросов, быстрее результат.»
- «С объяснениями» — «Каждый технический выбор объясню бытовой аналогией, чтобы вы понимали, что происходит. Дольше, но вы научитесь.»
- «Не знаю — решите сами» — взять «С объяснениями», назвать этот выбор одной фразой и идти дальше.

В режиме «С объяснениями» перед каждым техническим решением давать одну короткую аналогию. Образец, на который нужно равняться: «база данных — это как Excel-файл, только несколько человек могут писать в него одновременно и он не ломается». В режиме «Быстро» аналогии не давать, решение сообщать одной фразой.

**`## Step 2. What do you want to build`** — свободный текст, отдельным ходом, **без виджета в этом же ходе**. Вопрос: «Расскажите своими словами, что вы хотите сделать. Не думайте о технике — просто опишите задачу.» К вопросу приложить три примера-подсказки из финансовой области, чтобы человек понял ожидаемый объём ответа:
- «Хочу видеть на одной странице, сколько у меня денег на всех счетах и куда они уходят по месяцам.»
- «Хочу загружать банковскую выписку и получать готовый отчёт по статьям расходов.»
- «Хочу калькулятор, который считает график платежей по кредиту и показывает переплату.»

**`## Step 3. Who will use it`** — виджет выбора: «Только я» / «Я и коллеги» / «Внешние люди — клиенты, партнёры» / «Пока не знаю».
Из ответа модель сама делает выводы про вход по паролю, хранение и размещение — **не произнося** слов «авторизация» и «деплой». Соответствия:
- Только я → без входа по паролю, данные лежат локально.
- Я и коллеги → простой общий вход, данные в одном общем месте.
- Внешние люди → отдельный вход для каждого, данные хранятся на сервере; предупредить одной фразой, что это заметно больше работы, и предложить начать с версии «только я», чтобы сначала увидеть результат.
- Пока не знаю → взять «только я».

**`## Step 4. Where the data comes from`** — виджет выбора: «Ввожу руками» / «У меня есть файл Excel или CSV» / «Надо забирать из другой системы» / «Пока не знаю».
Если выбран файл — попросить (следующим, отдельным ходом) положить пример файла в папку проекта или описать словами, какие в нём столбцы. Если «из другой системы» — спросить одним свободным вопросом, из какой именно, и предупредить, что для этого может понадобиться доступ, которого сейчас нет; предложить на первом шаге работать с файлом-выгрузкой.

**`## Step 5. How do you want to launch it`** — виджет выбора из трёх вариантов, с честным объяснением:
- «Файл, который открывается двойным кликом» — «Ничего устанавливать не надо. Открывается в браузере как обычная страница. Подходит для калькуляторов, дашбордов и таблиц.»
- «Настоящее приложение» — «Возможностей больше: данные сохраняются между запусками, могут работать несколько человек. Но понадобится установить дополнительные программы, и запускать его нужно будет командой — я покажу как.»
- «Не знаю — решите сами» — взять «файл двойным кликом», кроме случая, когда срабатывает правило конфликта ниже: тогда взять «настоящее приложение». Назвать выбор одной фразой и идти дальше.

Если ответ шага 3 «внешние люди» или ответ шага 4 «из другой системы», а здесь выбран «файл двойным кликом» — назвать конфликт одной фразой и предложить «настоящее приложение», но решить так, как хочет пользователь.

**`## Step 6. How it should look`** — виджет выбора ровно из четырёх вариантов: «На ваш вкус — сделайте просто и аккуратно» / «Строго, по-деловому — как отчёт для руководства» / «Мягко и спокойно — для себя, каждый день» / «Есть пример — покажу». В самом вопросе — одна короткая фраза о том, что вид можно переделать потом обычными словами, поэтому человек ничем себя не связывает и отдельного упоминания в финальном отчёте не нужно. «На ваш вкус» служит ответом и для тех, кому всё равно, — отдельного «не знаю» здесь нет, исключение отмечено в `## Interview rules`. Если выбран «есть пример» — следующим, отдельным свободным ходом попросить ссылку, скриншот в папке проекта или описание словами и взять то, что дали; названный сайт не открывать и не догружать. Ответ доходит до сборки: `## Single file` и `## Real app` в `references/scaffolds.md` говорят, что каждый вариант значит на экране.

**`## Step 7. Summary and confirmation`** — показать сводку простым человеческим языком, без технических терминов, по схеме: что вы хотите → как я это сделаю → какие файлы появятся и зачем каждый → что вам нужно будет сделать руками (если нужно). Дождаться подтверждения. **До подтверждения не создавать ни одного файла.**

**Выбор папки проекта — здесь же, до первой записи на диск.** На шаге 7 (при подготовке сводки или сразу после подтверждения, но всегда до создания первого файла) проверить рабочую директорию. Если это домашняя папка пользователя или папка непустая — создать подпапку с названием проекта на языке шага 0 и делать всё внутри неё. Сказать об этом пользователю одной простой фразой («Сделаю проект в отдельной папке "<имя>", чтобы ничего не перепутать») — это один из немногих технических фактов, который стоит произнести, потому что человек должен знать, где лежат его файлы. Причина жёсткая: `.claude/settings.local.json`, записанный в `~`, попадает в **глобальные** настройки Claude Code пользователя и действует на все его проекты. Никаких перемещений файлов постфактум — папка выбирается до записи, поэтому переписывать пути потом не нужно.

**`## Tone rules`** — действуют на каждом ходу:
- No jargon. If a technical word is unavoidable, explain it in the same sentence.
- Banned words, in every turn and in the final report, not just at Step 3: «авторизация», «деплой», «фронтенд», «бэкенд», «репозиторий», «зависимости». Say what they mean instead: «вход по паролю», «выложить в интернет», «то, что видно на экране», «то, что считает внутри», «папка с проектом», «дополнительные программы».
- Never show a raw error message, stack trace, or exit code to the user. Say what happened in plain language, say you are fixing it, then fix it.
- Never blame the user for an unclear answer.
- Short messages. No walls of text.
- Do not narrate the technical work in progress. Report the result.

**`## Generation`** — что делать после подтверждения. Порядок жёсткий, выполняется в один заход, без пауз на согласование:
1. Read `references/templates.md` and write `CLAUDE.md`, the human cheat sheet, and `.claude/settings.local.json`. Права записываются **первыми** — иначе команды сборки (`node --version`, `npm install`) выполняются без разрешающих правил и пользователь видит сырые запросы подтверждения посреди работы, что запрещено `## Tone rules`.
2. Read `references/scaffolds.md` and build the project itself in the shape chosen at Step 5.
3. Reconcile the three written files with what was actually built — **обязательный шаг, выполняется всегда**, а не «если что-то изменилось». Перечитать `CLAUDE.md`, шпаргалку и `.claude/settings.local.json` и сверить с тем, что реально на диске и с реально собранным каркасом: каждое имя файла, каждую команду, каждый путь, каждую строку `allow`. Расхождения править в записанных файлах, а не в проекте. Каркас может смениться посреди прогона (нет Node.js → пользователь берёт «один файл»), и тогда неверны все три файла.
4. Launch the result and verify it, per `## Verification`.
5. Put the project under version control, per `## Version control` in `references/scaffolds.md`. Never skip this: the cheat sheet's «верни, как было» promise depends on it.
6. Give the final report, per `## Final report`.

Явно отметить: `references/*.md` читаются **только на этом этапе**, не во время интервью.

**`## Verification`** — обязательная часть, не опциональная:
- Actually launch the result. Do not write "done" without launching.
- Single-file shape: open the HTML file in the browser and confirm the page renders and the main action works.
- Real-app shape: install dependencies, start it, open the browser, confirm the page renders.
- If it fails, fix it and launch again — up to three attempts, without showing the user the raw error.
- If three attempts fail, stop and tell the user in plain language: what does not work, what already does work, what you will try next, and what they can do (usually: nothing, keep talking to Claude). Never claim success, and never loop silently past three attempts.

**`## Final report`** — отдельный раздел, вынесенный из `## Verification`, потому что отчёт даётся последним, уже после `## Version control`, а `## Verification` вызывается в середине последовательности:

- In the user's language: what was built, where the files are, exactly how to launch it next time, exactly what to type to Claude to continue, and what to do if something breaks. Point at the cheat sheet file for the details.
- Если проект ушёл в подпапку по правилу шага 7 — назвать эту папку в отчёте.
- Last line, exactly once, in the user's language and without a salesy tone — эталонная формулировка: «Этот плагин от Леонида, подписывайтесь на его канал https://t.me/financialpostpunk, там ещё много про вайб-кодинг для финансистов.» Ничего сверх этой фразы; никогда не повторять канал где-либо ещё за сессию.

- [ ] **Step 4: Запустить проверку и убедиться, что она проходит**

Выполнить: `python3 scripts/check.py`
Ожидается: все строки с `✓`, в конце `ВСЁ ХОРОШО`, код возврата 0.

- [ ] **Step 5: Коммит**

```bash
git add scripts/check.py plugins/vibeboarding/skills/start/SKILL.md
git commit -m "feat: ядро скилла — интервью, тон и порядок генерации"
```

---

### Task 3: Справочник шаблонов

**Files:**
- Create: `plugins/vibeboarding/skills/start/references/templates.md`
- Modify: `scripts/check.py` (добавить блок проверок перед финальным `print()`)

**Interfaces:**
- Consumes: `check()`, `ROOT` из `scripts/check.py`; якорь `## Generation` из `SKILL.md` (Task 2), который ссылается на этот файл.
- Produces: три шаблона с якорями `## CLAUDE.md`, `## Cheat sheet`, `## Permissions`.

- [ ] **Step 1: Написать падающую проверку**

Добавить в `scripts/check.py` перед финальным блоком `print()`:

```python
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
```

- [ ] **Step 2: Запустить проверку и убедиться, что она падает**

Выполнить: `python3 scripts/check.py`
Ожидается: `✖ есть файл plugins/vibeboarding/skills/start/references/templates.md`, `ПРОВАЛЕНО: 1`, код возврата 1.

- [ ] **Step 3: Написать `references/templates.md`**

Вводная строка: these templates are filled in and written during the Generation step; all headings and prose go into the user's language, file paths and config keys stay as-is.

**`## CLAUDE.md`** — шаблон, целевой объём до 40 строк. Разделы (заголовки переводятся на язык пользователя):
- «О проекте» — что это, для кого, одна-две фразы из ответа на шаге 2.
- «Как запустить» — ровно один способ. Для «настоящего приложения» команда **всегда `npm start`** и только она; `dev` может быть в `package.json`, но пользователю не показывается никогда. Для «одного файла» — «открыть файл X двойным кликом».
- «Где что лежит» — по одной строке на каждый созданный файл.
- «Правила» — три-четыре пункта, каждый простой фразой: не ломать то, что уже работает, без спроса; после изменений проверять, что проект по-прежнему запускается; объяснять сделанное простыми словами, без технического жаргона; если что-то может удалить данные пользователя — сначала спросить.

Явно запретить: разделы про архитектуру, тестирование, ADR, миграции. Если нечего написать в раздел — раздел не создавать.

**`## Cheat sheet`** — шпаргалка для человека. Имя файла — на языке пользователя (для русского `ПРОЧТИ-МЕНЯ.md`, для английского `README.md`). **Все пять разделов присутствуют всегда и в этом порядке** — ни один нельзя выкинуть из-за нехватки материала: шпаргалка — единственный спасательный документ пользователя. Разделы:
- «Что это за папка» — одна фраза.
- «Как запустить» — пошагово, буквально, с точными командами или «двойной клик по файлу X».
- «Что говорить Клоду дальше» — три-пять готовых фраз, которые можно скопировать и вставить. Формулировки под конкретный проект, например: «Добавь на страницу график расходов по месяцам», «Сделай так, чтобы данные сохранялись после закрытия», «Поменяй цвета на более спокойные».
- «Если что-то сломалось» — по шагам: 1) сказать Клоду «сломалось, вот что я делал: …»; 2) не удалять файлы самому; 3) как вернуть предыдущую рабочую версию через Клода; 4) последней строкой раздела — одна фраза без рекламного тона: если Клод не справился, спросить в телеграм-канале `@financialpostpunk`.
- «Чего лучше не делать» — два-три пункта, например: не переименовывать файлы вручную, не удалять папку `.claude`.

**`## Permissions`** — шаблон `.claude/settings.local.json`. Перед записью файла сверить синтаксис `permissions` (ключи, значения `defaultMode`, форма правил) с актуальной документацией Claude Code; если он изменился — следовать документации и сказать об этом одной фразой в финальном отчёте. Иначе записывать в проект буквально следующее, дополнив `allow` реальными командами проекта:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Bash(npm install:*)",
      "Bash(npm run:*)",
      "Bash(node:*)",
      "Bash(open:*)",
      "Bash(start:*)",
      "Bash(xdg-open:*)",
      "Bash(git init)",
      "Bash(git config:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)"
    ],
    "deny": [
      "Bash(rm)",
      "Bash(rm:*)",
      "Bash(git reset --hard)",
      "Bash(git reset --hard:*)",
      "Bash(git clean)",
      "Bash(git clean:*)",
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Edit(./.env*)",
      "Write(./.env*)"
    ],
    "ask": [
      "Bash(git push:*)"
    ]
  }
}
```

Пояснение в справочнике (для модели, не для пользователя): `deny` перекрывает `allow` в любом режиме, поэтому названные в нём команды остаются заблокированными даже при широких правах — но это сеть, а не гарантия: составная строка `cd x && rm -rf y` под `Bash(rm:*)` не попадает, а форма `:*` не покрывает голую команду, поэтому рядом стоят голые формы. Формулировка в шаблоне честная: «ловит типовые случаи», а не «ничего нельзя удалить». `defaultMode: acceptEdits` разрешает правку файлов и обычные файловые команды без вопросов. Если выбран каркас «один HTML-файл», из `allow` убрать две строки с `npm` (`"Bash(npm install:*)"` и `"Bash(npm run:*)"`), остальное в `allow` оставить — `open`/`start`/`xdg-open` нужны для проверки запуска. Файл добавить в `.gitignore` проекта.

- [ ] **Step 4: Запустить проверку и убедиться, что она проходит**

Выполнить: `python3 scripts/check.py`
Ожидается: все строки с `✓`, `ВСЁ ХОРОШО`, код возврата 0.

- [ ] **Step 5: Коммит**

```bash
git add scripts/check.py plugins/vibeboarding/skills/start/references/templates.md
git commit -m "feat: справочник шаблонов CLAUDE.md, шпаргалки и прав доступа"
```

---

### Task 4: Справочник каркасов

**Files:**
- Create: `plugins/vibeboarding/skills/start/references/scaffolds.md`
- Modify: `scripts/check.py` (добавить блок проверок перед финальным `print()`)

**Interfaces:**
- Consumes: `check()`, `ROOT` из `scripts/check.py`; выбор пользователя на шаге 5 интервью (Task 2).
- Produces: два каркаса с якорями `## Single file` и `## Real app`, плюс `## Version control` и `## Launch and verify`.

- [ ] **Step 1: Написать падающую проверку**

Добавить в `scripts/check.py` перед финальным блоком `print()`:

```python
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
```

- [ ] **Step 2: Запустить проверку и убедиться, что она падает**

Выполнить: `python3 scripts/check.py`
Ожидается: `✖ есть файл plugins/vibeboarding/skills/start/references/scaffolds.md`, `ПРОВАЛЕНО: 1`, код возврата 1.

- [ ] **Step 3: Написать `references/scaffolds.md`**

Жёсткий порядок операций в начале файла, совпадающий с `## Generation`: 1) шаблоны (`CLAUDE.md`, шпаргалка, права) — первыми; 2) каркас; 3) `## Launch and verify`; 4) `## Version control`; 5) финальный отчёт. Плюс напоминание: папка проекта выбрана на шаге 7, работать в ней и потом никуда не переносить.

**`## Single file`** — выбран на шаге 5 вариант «файл двойным кликом».
- Один самодостаточный HTML-файл в корне проекта. Имя — на языке пользователя и по сути проекта, например `Мои расходы.html`.
- Всё внутри одного файла: разметка, стили, скрипт. Никаких внешних ссылок на библиотеки и шрифты — файл должен работать без интернета.
- Данные, если их надо сохранять между открытиями, хранить в `localStorage` браузера. В шпаргалке предупредить человека одной фразой: данные лежат в этом браузере на этом компьютере.
- Если пользователь на шаге 4 дал файл Excel или CSV — предусмотреть кнопку загрузки файла прямо на странице, чтение через `FileReader`, без сервера.
- Интерфейс: крупный шрифт, понятные подписи на языке пользователя, работает и на узком экране.

**`## Real app`** — выбран вариант «настоящее приложение».
- Минимально возможный проект, не монорепозиторий. Один `package.json` в корне, скрипты `dev` и `start`.
- Ровно один способ запуска, и он зафиксирован: **`npm start`**. Именно эта команда попадает в `CLAUDE.md` «Как запустить» и в шпаргалку, всегда. `dev` пользователю не показывается. Никаких вариантов «или так, или так».
- Хранение данных — самое простое, что закрывает задачу; полноценную базу поднимать, только если без неё никак, и в этом случае Клод поднимает её сам и проверяет, что она работает.
- Перед началом проверить, установлен ли Node.js (`node --version`). Если нет — не вываливать инструкцию по установке, а объяснить одной фразой, что нужно установить, дать прямую ссылку и предложить пока сделать вариант «один файл», чтобы человек сразу увидел результат.
- Имена скриптов в `package.json` и в разделе «Как запустить» шпаргалки должны совпадать буквально; `start` обязан реально запускать готовый проект.

**`## Version control`** — обязательный раздел, общий для обоих вариантов. Без него шпаргалка врёт: она советует «верни, как было до последних изменений», а права доступа разрешают `git add`/`git commit` — но откатывать будет нечего, если репозитория нет.
- After the project files exist and the launch check has passed, run `git init` in the project root if the directory is not already a repository.
- Never `git init` the user's home folder and never a parent folder. Случай «корень проекта = домашняя папка» здесь уже не обрабатывается: папка выбрана на шаге 7 **до первой записи**, перемещать нечего и пути переписывать не нужно. Do not skip version control — skipping it re-hollows the «верни, как было» promise.
- Write a `.gitignore` that at minimum contains `.claude/settings.local.json` and `.DS_Store`.
- Make one initial commit containing everything, with a message in the user's language, e.g. «Первая рабочая версия».
- Do not narrate any of this to the user and do not use the word «репозиторий» with them. In the cheat sheet, this is simply why «верни, как было» works.
- Never run `git push`, never ask about GitHub, never set up a remote. This is purely a local safety net.

**`## Launch and verify`** — общая процедура, обязательная в обоих вариантах:
1. **Сверить три записанных файла с тем, что реально на диске** — обязательный шаг, выполняется всегда. Имена файлов, команды, строки `allow` — всё символ в символ против реального каркаса. Отдельно оговорено, что каркас может смениться посреди прогона (нет Node.js → «один файл»), и тогда из `allow` убираются `npm`-строки, а команда запуска меняется на двойной клик. Пользователю об этом не говорить.
2. Launch the result.
3. Single file: open it in the default browser (`open` on macOS, `start` on Windows, `xdg-open` on Linux) and confirm the page renders and the main action works.
3. Real app: `npm install`, затем `npm start`, открыть браузер по адресу проекта, убедиться, что страница отрисовалась.
4. On failure: fix it and launch again, up to three attempts. Do not report the failure to the user unless it needs their decision — and then in plain language, never as a raw error.
5. After three failed attempts, stop: say in plain language what does not work, what already works, and what you will try next. Never claim success and never loop past three attempts.
6. Only after a successful launch, report success and show what the user should see.

- [ ] **Step 4: Запустить проверку и убедиться, что она проходит**

Выполнить: `python3 scripts/check.py`
Ожидается: все строки с `✓`, `ВСЁ ХОРОШО`, код возврата 0.

- [ ] **Step 5: Коммит**

```bash
git add scripts/check.py plugins/vibeboarding/skills/start/references/scaffolds.md
git commit -m "feat: справочник каркасов проекта и процедура запуска"
```

---

### Task 5: Документация репозитория и плагина

**Files:**
- Create: `README.md`
- Create: `plugins/vibeboarding/README.md`
- Modify: `scripts/check.py` (добавить блок проверок перед финальным `print()`)

**Interfaces:**
- Consumes: `check()`, `ROOT` из `scripts/check.py`; имена из `marketplace.json` (Task 1).
- Produces: пользовательская документация. Дальше от неё ничего не зависит.

- [ ] **Step 1: Написать падающую проверку**

Добавить в `scripts/check.py` перед финальным блоком `print()`:

```python
for rel in ["README.md", "plugins/vibeboarding/README.md"]:
    check((ROOT / rel).is_file(), f"есть файл {rel}")
root_readme = ROOT / "README.md"
if root_readme.is_file():
    readme = root_readme.read_text(encoding="utf-8")
    check("/plugin marketplace add" in readme,
          "README.md: есть команда установки маркетплейса")
    check("vibeboarding@leogodnik-plugins" in readme,
          "README.md: есть команда установки плагина")
    check("/vibeboarding:start" in readme, "README.md: есть команда запуска")
    check("@financialpostpunk" in readme,
          "README.md: есть упоминание телеграм-канала")
```

- [ ] **Step 2: Запустить проверку и убедиться, что она падает**

Выполнить: `python3 scripts/check.py`
Ожидается: `✖ есть файл README.md`, `✖ есть файл plugins/vibeboarding/README.md`, `ПРОВАЛЕНО: 2`, код возврата 1.

- [ ] **Step 3: Написать корневой `README.md`**

На русском, для слушателя курса. Разделы:
- Заголовок и одна фраза о том, что это.
- «Что это» — два-три предложения: помогает начать новый проект тому, кто не программист; задаёт несколько понятных вопросов и дальше делает всё сам.
- «Установка» — блок с тремя командами:

```
/plugin marketplace add leogodnik/vibeboarding
/plugin install vibeboarding@leogodnik-plugins
/vibeboarding:start
```

  Первая строка предполагает, что репозиторий опубликован на GitHub как `leogodnik/vibeboarding`. Пока публикации нет — оставить эту строку как есть (README пишется для будущих пользователей), а локальную установку описать в Task 6.

  Под блоком — предупреждение: запускать `/vibeboarding:start` в **пустой папке**, потому что он делает проект с нуля.
- «Как это работает» — нумерованный список из шести шагов интервью, каждый одной строкой на человеческом языке. В строках про режим (шаг 1 интервью) и про способ запуска (шаг 5 интервью) обязательно упомянуть вариант «не знаю, решите сами» — это то, что реально предлагает `SKILL.md`, и это успокаивает читателя-новичка.
- «Что получится» — четыре пункта: работающий проект; `CLAUDE.md`; шпаргалка; безопасные настройки прав.
- «Автор» — предпоследний раздел, две строки: плагин вырос из телеграм-канала `@financialpostpunk` про вайб-кодинг для финансистов; ссылка `https://t.me/financialpostpunk`. Без восклицательных знаков и без слова «подписывайтесь!» в рекламном тоне — просто указание, откуда это.
- «Лицензия» — MIT.

- [ ] **Step 4: Написать `plugins/vibeboarding/README.md`**

Короче корневого, без раздела установки маркетплейса. Что делает плагин, два режима интервью, что создаёт, ссылка на `../../LICENSE`.

- [ ] **Step 5: Запустить проверку и убедиться, что она проходит**

Выполнить: `python3 scripts/check.py`
Ожидается: все строки с `✓`, `ВСЁ ХОРОШО`, код возврата 0.

- [ ] **Step 6: Коммит**

```bash
git add scripts/check.py README.md plugins/vibeboarding/README.md
git commit -m "docs: README репозитория и плагина"
```

---

### Task 6: Живой прогон и правки

**Files:**
- Modify: `plugins/vibeboarding/skills/start/SKILL.md` (по результатам прогона)
- Modify: `plugins/vibeboarding/skills/start/references/templates.md` (по результатам прогона)
- Modify: `plugins/vibeboarding/skills/start/references/scaffolds.md` (по результатам прогона)

**Interfaces:**
- Consumes: весь плагин из задач 1–5.
- Produces: проверенный на реальном прогоне плагин. Финальное состояние.

- [ ] **Step 1: Подготовить чистую площадку**

```bash
rm -rf /tmp/vibeboarding-test && mkdir -p /tmp/vibeboarding-test && cd /tmp/vibeboarding-test && git status
```

Ожидается: `fatal: not a git repository` — папка чистая и пустая.

- [ ] **Step 2: Поставить маркетплейс из локальной папки**

В новой сессии Claude Code, запущенной в `/tmp/vibeboarding-test`, выполнить:

```
/plugin marketplace add "/Users/leogodnik/Starter Skill/vibeboarding"
/plugin install vibeboarding@leogodnik-plugins
```

Путь в кавычках обязателен — в нём есть пробел.

Ожидается: установка прошла; если в отчёте есть `Run /reload-plugins to activate.` — выполнить `/reload-plugins`.

- [ ] **Step 3: Проверить, что команда появилась**

Ввести `/vibe` и посмотреть автодополнение.
Ожидается: в списке есть `/vibeboarding:start` (скиллы плагина именуются с префиксом плагина).

- [ ] **Step 4: Пройти интервью в режиме «Быстро»**

Запустить, ответить: язык — Русский; режим — Быстро; задача — «Хочу видеть на одной странице, сколько я трачу по категориям за месяц»; пользователи — Только я; данные — Ввожу руками; запуск — Файл двойным кликом.

Контрольный список наблюдений, каждый пункт отметить «да/нет»:
- Первым вопросом был именно язык, отдельным ходом.
- Ни один ход не смешивал свободный текст с виджетом выбора.
- Ни в одном вопросе не встретилось непонятного термина без объяснения.
- В каждом вопросе был вариант «не знаю, реши сам».
- Перед созданием файлов показана сводка и запрошено подтверждение.
- Созданы: HTML-файл, `CLAUDE.md`, шпаргалка, `.claude/settings.local.json` — и больше ничего лишнего.
- Клод сам открыл результат в браузере и показал, что он работает.
- В финальном отчёте есть готовые фразы, что говорить Клоду дальше.

- [ ] **Step 5: Пройти интервью в режиме «С объяснениями»**

В новой чистой папке `/tmp/vibeboarding-test-2` повторить с режимом «С объяснениями», пользователи — «Я и коллеги», запуск — «Настоящее приложение».

Контрольный список:
- Технические решения сопровождались бытовыми аналогиями.
- Проверено наличие Node.js до начала работы.
- Приложение реально запустилось и открылось в браузере.
- Имена скриптов в `package.json` совпадают с тем, что написано в шпаргалке.

- [ ] **Step 6: Исправить найденное**

Каждое «нет» из шагов 4 и 5 — правка в соответствующий файл скилла. После правок повторить прогон, на котором наблюдение провалилось, и убедиться, что теперь «да».

- [ ] **Step 7: Прогнать структурную проверку**

Выполнить: `cd "/Users/leogodnik/Starter Skill/vibeboarding" && python3 scripts/check.py`
Ожидается: все строки с `✓`, `ВСЁ ХОРОШО`, код возврата 0.

- [ ] **Step 8: Убрать площадки и закоммитить**

```bash
rm -rf /tmp/vibeboarding-test /tmp/vibeboarding-test-2
git add plugins/vibeboarding/skills/start
git commit -m "fix: правки скилла по результатам живого прогона"
```

---

### Task 7: Финальная волна правок по итогам ревью всей ветки

**Files:**
- Modify: `plugins/vibeboarding/skills/start/SKILL.md`
- Modify: `plugins/vibeboarding/skills/start/references/templates.md`
- Modify: `plugins/vibeboarding/skills/start/references/scaffolds.md`
- Modify: `README.md`
- Modify: `scripts/check.py`

**Interfaces:**
- Consumes: весь плагин из задач 1–6.
- Produces: состояние, с которым плагин выходит наружу. Решения ниже — окончательные, тексты задач 2–5 выше уже приведены к ним.

- [x] **F2 (критично): выбор папки проекта перенесён в `## Step 7`, до первой записи на диск**

Раньше случай «корень проекта = домашняя папка» разбирался в `## Version control` (шаг 4 генерации) — уже после того, как `CLAUDE.md`, шпаргалка и `.claude/settings.local.json` записаны. Это означало запись `acceptEdits` и широкого `allow` в **глобальный** `~/.claude/` пользователя и приглашение «переместить файлы проекта», под которое мог попасть сам `~/.claude`. Теперь: на шаге 7, до первого файла, проверяется рабочая директория; если это домашняя папка или папка непустая — создаётся подпапка с названием проекта, и вся работа идёт в ней. Пользователю говорится одна фраза о том, где будет проект. Из `## Version control` убраны и перенос файлов, и оговорка про переписывание путей; там осталось простое правило: никогда не `git init` в домашней или родительской папке.

- [x] **F3 (важно): права записываются до команд, которые они разрешают**

В `## Generation` шаги 1 и 2 поменяны местами: сначала шаблоны (`CLAUDE.md`, шпаргалка, `.claude/settings.local.json`), потом каркас. Иначе `node --version` и `npm install` выполнялись без разрешающих правил и пользователь видел сырые запросы подтверждения. Порядок в `references/scaffolds.md` приведён в соответствие. В `allow` добавлены команды, которые скилл запускает сам для проверки своей работы: `Bash(node:*)`, `Bash(open:*)`, `Bash(start:*)`, `Bash(xdg-open:*)`. `Bash(npm install)` заменено на `Bash(npm install:*)` — точная форма не покрывает `npm install <пакет>`. Инструкция для каркаса «один файл» теперь называет обе убираемые строки поимённо.

- [x] **F4 (важно): у зашитого блока прав появилась инструкция на пересверку**

В `## Permissions` добавлено: перед записью файла сверить синтаксис `permissions` (ключи, значения `defaultMode`, форма правил) с актуальной документацией Claude Code; если изменился — следовать документации и сказать об этом в финальном отчёте. Шаблон остаётся значением по умолчанию.

- [x] **F5 (важно): обещание про `deny` приведено к правде**

`Bash()`-правило не ловит составные команды (`cd x && rm -rf y`), а форма `:*` не покрывает голую команду. Добавлены голые формы `Bash(rm)`, `Bash(git reset --hard)`, `Bash(git clean)`; формулировка смягчена — список ловит типовые случаи, но не является гарантией и не песочница.

- [x] **F6 (важно): команда запуска зафиксирована**

Для каркаса «настоящее приложение» в `CLAUDE.md` «Как запустить» и в шпаргалку всегда пишется `npm start` и только он. `dev` может быть в `package.json`, но пользователю не показывается. `references/templates.md` приведён в соответствие.

- [x] **F10 (мелкое): финальный отчёт вынесен из `## Verification` в отдельный `## Final report`**

`## Verification` вызывается в середине последовательности, а отчёт даётся последним — из-за этого файлы противоречили друг другу. Строка про `@financialpostpunk` переехала вместе с отчётом и по-прежнему встречается в `SKILL.md` ровно один раз. `## Final report` добавлен в список якорей в `scripts/check.py`.

- [x] **F8 (мелкое): шаг 0 выведен из-под правила про «не знаю»**

Исключение записано в самой формулировке правила в `## Interview rules`.

- [x] **F9 (мелкое): подпись варианта на шаге 0 стала двуязычной**

`Другой / Other`; текст вопроса шага 0 показывается по-русски и по-английски, потому что язык ещё не выбран.

- [x] **Долги из журнала прогресса**

Шпаргалка: в `references/templates.md` явно сказано, что все пять разделов присутствуют всегда — «Чего лучше не делать» нельзя молча выкинуть. Корневой `README.md`: в строках про шаг 1 (режим) и шаг 5 (способ запуска) добавлен вариант «не знаю, решите сами».

- [x] **Ложное срабатывание ревью — не исправлять**

Ревью требовало заменить голое имя команды на полную форму с префиксом плагина в обоих README. Это неверно: по актуальной документации Claude Code голое имя скилла плагина тоже вызывает скилл, если оно не занято другой командой. Оба README, строка 9 `SKILL.md` и проверка в `scripts/check.py` были оставлены как есть. Позже скилл переименован в `start`: команда — `/vibeboarding:start`, короткая форма — `/start`.

- [x] **Проверка**

`python3 scripts/check.py` — код возврата 0. JSON прав извлечён из `references/templates.md` и разобран программно: валиден, `defaultMode: acceptEdits`, все правила в форме `Tool(pattern)`. `@financialpostpunk`: `SKILL.md` — 1, `references/templates.md` — 1, `references/scaffolds.md` — 0.
