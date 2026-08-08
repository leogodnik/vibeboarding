# Templates

Read at generation time only, after Step 6 is confirmed. These three templates are filled in and written into the new project in this order: `CLAUDE.md`, the human cheat sheet, `.claude/settings.local.json`.

How to use this file:

- Every heading and every sentence the user will read goes into the language picked at Step 0. File names, paths, commands, config keys and the JSON stay exactly as written here.
- The Russian text in the templates is reference wording, not literal output. Translate it into the Step 0 language, keeping the meaning, the tone and roughly the length. If Step 0 is Русский, use it as written.
- `<angle brackets>` mark a placeholder you replace with the real value for this project. Never leave a placeholder, and never write the angle brackets into the generated file.
- Fill every template from the interview answers. Do not ask the user anything more at this stage.
- These three files are written first, before the project itself is built (`## Generation` step 1 in `SKILL.md`), so the scaffold does not exist on disk yet. Fill them from the plan the user confirmed at Step 6. After the build, check that every file name and every command in them matches what was actually created, and fix them if anything came out different.
- `## Tone rules` from `SKILL.md` still applies to every word here: no jargon, short sentences, no raw error text.

## CLAUDE.md

Written to `CLAUDE.md` in the project root. It is instructions for Claude in later sessions, not a document for the user — but it is written in the user's language, because the user will open it and must be able to read it.

Hard limits:

- Target under 40 lines in total. Shorter is better.
- Never add sections about architecture, testing, ADRs (architecture decision records) or migrations. This project does not have them and inventing them makes the file useless.
- If a section would have nothing real in it, do not create the section at all. An empty heading is worse than a missing one.
- No section beyond the four below. If something genuinely does not fit, it belongs in the cheat sheet.

Template:

```markdown
# <Project name in the user's language>

## О проекте
<One or two sentences, taken from the Step 2 answer: what this is and who it is for. Plain words, no technical terms.>

## Как запустить
<Exactly one way to launch — the one chosen at Step 5. Real-app shape: the command is always `npm start`, in a code block, and nothing else. Single-file shape: the literal instruction «Открыть файл <name>.html двойным кликом».>

## Где что лежит
- `<file or folder>` — <what it is for, one line>
- `<file or folder>` — <what it is for, one line>

## Правила
- Не ломать то, что уже работает, без спроса.
- После изменений проверять, что проект по-прежнему запускается.
- Объяснять сделанное простыми словами, без технического жаргона.
- Если что-то может удалить данные пользователя — сначала спросить.
```

Notes on the sections:

- «О проекте» — reuse the user's own words from Step 2 where you can. Do not upgrade them into technical language.
- «Как запустить» — one line for the single-file shape (double click); for the real-app shape the one documented command is `npm start`, written exactly as it must be typed. `package.json` may also carry a `dev` script, but `dev` is never shown to the user, here or in the cheat sheet.
- «Где что лежит» — one line per file this project will have, in the order the user will care about. The scaffold is built in the next step, so list what the confirmed plan says you are about to create — nothing speculative — and correct the list after the build if a name came out different. Do not list every generated folder.
- «Правила» — three or four items, each one plain sentence. The four above are the default set; keep all four unless one is meaningless for this project. Add a project-specific rule only if the interview produced one (for example: «Файл с выпиской не менять — из него читаются данные»).

## Cheat sheet

The cheat sheet is for the human, not for Claude. It is the file the user opens when they have forgotten how to start the project. Everything in it is literal and concrete: real file names, real commands, real phrases they can copy.

All five sections below always appear, in this order, in every cheat sheet: «Что это за папка», «Как запустить», «Что говорить Клоду дальше», «Если что-то сломалось», «Чего лучше не делать». Never drop one for lack of material — this is the user's only lifeline document, and a missing section is a question they will have no answer to. If a section feels thin, use the default items in the notes below.

File name depends on the Step 0 language, and the file goes in the project root:

- Русский → `ПРОЧТИ-МЕНЯ.md`
- English → `README.md`
- Any other language → the plain local equivalent of "read me", in that language, if it makes a normal file name; otherwise `README.md`. Never leave the file unnamed or hidden in a subfolder.

Template:

```markdown
# <Project name in the user's language>

## Что это за папка
<One sentence: what lives here and what it does for the user.>

## Как запустить
<Numbered steps, literal, no assumed knowledge. Single-file shape: «Откройте папку <folder>» / «Дважды кликните по файлу <name>.html» / «Откроется браузер — это и есть ваш проект». Real-app shape: the launch command is `npm start` and only `npm start` — one step, in a code block, plus what the user should see after it.>

## Что говорить Клоду дальше
Скопируйте любую строчку и вставьте в чат с Клодом:

- «<phrase 1>»
- «<phrase 2>»
- «<phrase 3>»

## Если что-то сломалось
1. Скажите Клоду: «Сломалось, вот что я делал: …» — и опишите своими словами последние действия.
2. Не удаляйте файлы сами — почти всё чинится словами, а удалённое вернуть сложнее.
3. Чтобы вернуть предыдущую рабочую версию, скажите Клоду: «Верни, как было до последних изменений».
4. Если Клод не справился — спросите в телеграм-канале `@financialpostpunk`.

## Чего лучше не делать
- <item 1>
- <item 2>
```

Notes on the sections:

- «Что говорить Клоду дальше» — three to five ready phrases, written for this specific project, not generic advice. Each one must be a complete request the user can paste as is. Reference examples of the right shape and length: «Добавь на страницу график расходов по месяцам», «Сделай так, чтобы данные сохранялись после закрытия», «Поменяй цвета на более спокойные». Derive yours from what the user described at Step 2 and from what the project does not do yet.
- «Если что-то сломалось» — keep all four steps and keep them in this order. The last line names the Telegram channel once, in one plain sentence, with no sales tone and no extra praise. Do not repeat the channel anywhere else in the cheat sheet, and do not put it in `CLAUDE.md`.
- «Чего лучше не делать» — two or three items, each a concrete action in this project. Default items that almost always apply: «Не переименовывайте файлы вручную — скажите Клоду, и он переименует», «Не удаляйте папку `.claude` — в ней настройки». Add a project-specific one if there is an obvious way to break this project by hand.

## Permissions

Written to `.claude/settings.local.json` in the project root. Create the `.claude` folder if it is not there. This file is settings, not user-facing text: nothing in it is translated.

Before you write the file, confirm the `permissions` syntax — the key names, the allowed `defaultMode` values, and the `Tool(pattern)` rule form — against the current Claude Code documentation; this part of the configuration drifts between releases. If it has changed, follow the documentation instead of the template below and say so in one plain sentence in the final report. Otherwise the template is the default and is written as is.

Write exactly this, then extend `allow` with the project's real commands:

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

Why it is built this way (this explanation is for you, not for the user — never paste it into the project):

- `deny` overrides `allow` in every mode, so the dangerous commands it names stay blocked even though the rest of the permissions are wide. It is a net, not a guarantee: a `Bash()` rule matches the command as written, so a compound line like `cd x && rm -rf y` is not caught by `Bash(rm:*)`, and a `:*` rule does not reliably cover the bare command — which is why the bare forms `Bash(rm)`, `Bash(git reset --hard)` and `Bash(git clean)` are listed alongside them. The list catches the common shapes and makes a permissive setup reasonable to hand a non-programmer; it is not a sandbox, so never tell the user that nothing can be deleted.
- `"defaultMode": "acceptEdits"` lets Claude edit files and run ordinary file commands without stopping to ask, so the user is not asked to approve things they cannot judge.
- `ask` keeps a confirmation on `git push`: publishing is the one action the user should knowingly agree to.

Rules for adapting it:

- Single-file shape (one self-contained HTML file, no `package.json`): remove the two `npm` lines — `"Bash(npm install:*)"` and `"Bash(npm run:*)"` — from `allow`. Keep everything else in `allow`, including `Bash(open:*)`, `Bash(start:*)` and `Bash(xdg-open:*)`: those are how the file gets opened for the launch check. Keep `deny` and `ask` unchanged.
- Real-app shape (there is a `package.json`): keep the `npm` lines and add the project's own commands. Add only commands this project actually uses.
- Never remove or shorten the `deny` list. Never add keys or modes beyond the template above, unless the documentation check at the top of this section says the syntax has changed — then follow the documentation.
- Add `.claude/settings.local.json` to the project's `.gitignore`. Create `.gitignore` with that single line if the project does not have one — it is a local settings file and does not belong in a shared folder.
