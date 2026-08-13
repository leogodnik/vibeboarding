# Templates

Read at generation time only, after Step 14 has been answered. There are four templates here, and which of them you fill in depends on how Step 14 was answered:

- **«Делаем прямо сейчас»** — three of them, in the order `## Generation` in `SKILL.md` sets: `.claude/settings.local.json` first, before anything runs a command, then `CLAUDE.md` and the human cheat sheet once `git init` and the first commit are done.
- **«Сохраните план файлом»** — `.claude/settings.local.json`, then `## Plan file`, and that is all. `CLAUDE.md` and the cheat sheet are not written in that branch: both describe a project that does not exist yet.

How to use this file:

- Every heading and every sentence the user will read goes into the language picked at Step 0. File names, paths, commands, config keys and the JSON stay exactly as written here.
- The Russian text in the templates is reference wording, not literal output. Translate it into the Step 0 language, keeping the meaning, the tone and roughly the length. If Step 0 is Русский, use it as written.
- `<angle brackets>` mark a placeholder you replace with the real value for this project. Never leave a placeholder, and never write the angle brackets into the generated file.
- Fill every template from the interview answers. Do not ask the user anything more at this stage.
- `CLAUDE.md` and the cheat sheet are written before the project itself is built (`## Generation` steps 1 and 3 in `SKILL.md`), so the scaffold does not exist on disk yet. Fill them from the plan the user confirmed at Steps 13 and 14. They are then reconciled with reality by a mandatory step that always runs after the build — `## Generation` step 5, spelled out as step 1 of `## Launch and verify` in `references/scaffolds.md`. Write your best version here; that step is what guarantees it ends up true.
- `## Tone rules` from `SKILL.md` still applies to every word here: no jargon, short sentences, no raw error text.

## CLAUDE.md

Written to `CLAUDE.md` in the project root. It is instructions for Claude in later sessions, not a document for the user — but it is written in the user's language, because the user will open it and must be able to read it.

Hard limits:

- Target under 50 lines in total. Shorter is better.
- Never add sections about architecture, testing, ADRs (architecture decision records) or migrations. This project does not have them and inventing them makes the file useless.
- If a section would have nothing real in it, do not create the section at all. An empty heading is worse than a missing one. This is what decides whether the fifth section exists.
- No section beyond the five below. If something genuinely does not fit, it belongs in the cheat sheet.

Template:

```markdown
# <Project name in the user's language>

## О проекте
<One or two sentences, taken from the Step 3 answer: what this is and who it is for. Plain words, no technical terms.>
<One more line, only if a short sample was given at Step 10 — see the notes below.>

## Как запустить
<Exactly one way to launch — the one chosen at Step 9. Real-app shape: the one real command, in a code block, and nothing else. Single-file shape: the literal instruction «Открыть файл <name>.html двойным кликом».>

## Где что лежит
- `<file or folder>` — <what it is for, one line>
- `<file or folder>` — <what it is for, one line>

## Правила
- Не ломать то, что уже работает, без спроса.
- После изменений проверять, что проект по-прежнему запускается.
<Правила про язык общения — из Шага 12. Точный текст в примечаниях к этому разделу ниже.>
- Если что-то может удалить данные пользователя — сначала спросить.

## Что учесть потом
- <plan in the user's own words, one line>
```

Notes on the sections:

- «О проекте» — reuse the user's own words from Step 3 where you can. Do not upgrade them into technical language. If Step 10 produced a short sample (a link, a picture, a phrase), add the one line `## Design reference` in `references/scaffolds.md` prescribes: «Оформление — по образцу, который дал пользователь: <ссылка / имя файла / в двух словах>». A long sample goes into `design.md` instead and is listed in «Где что лежит».
- «Как запустить» — one line for the single-file shape (double click). For the real-app shape it is the one command that actually launches this project, written exactly as it must be typed — `npm start`, `.venv/bin/python app.py`, `.venv/bin/streamlit run app.py`, whatever the build really produced. Never a command you have not run, never two options, never a step before it like activating an environment. `package.json` may also carry a `dev` script, but `dev` is never shown to the user, here or in the cheat sheet.
- «Где что лежит» — one line per file this project will have, in the order the user will care about. Include `design.md` and any picture the user put in the folder, and — when the build produces them — `.env.example` and the seeding script from `### Data`. The scaffold is built in the next step, so list what the confirmed plan says you are about to create — nothing speculative. The mandatory reconciliation step after the build (`## Launch and verify`, step 1) corrects this list against the files that really exist. Do not list every generated folder.
- «Правила» — each item one plain sentence. The first, the second and the last item of the template are fixed and go into every project; keep all three unless one is genuinely meaningless here. Between the second and the last go the language items from Step 12, and which ones they are is not a judgement call.

  «Совсем простыми словами», and the default when the user did not choose → these three, as three separate items:

  ```markdown
  - Объяснять сделанное простыми словами, без технического жаргона.
  - Вместо технических слов говорить по-человечески: «деплой» → «выложить в интернет», «репозиторий» → «папка с проектом», «зависимости» → «дополнительные программы», «фронтенд» → «то, что видно на экране», «бэкенд» → «то, что считает внутри», «авторизация» → «вход по паролю».
  - Не показывать текст ошибок — объяснять словами, что случилось и что вы с этим делаете.
  ```

  «Как обычно, можно с терминами» → exactly this one item instead of those three, and never alongside them:

  ```markdown
  - Можно пользоваться техническими терминами, упрощать не нужно.
  ```

  Leaving the simple-language items in after the user asked for terms is the one mistake this step exists to prevent: the file would then order the opposite of what they chose.

  The word pairs are Russian reference wording like everything else in this file. In another Step 0 language, write that language's own jargon-and-plain-word pairs — not a translation of the Russian ones — and drop any pair that has no everyday equivalent there rather than inventing one.

  Six items is the most «Правила» ever runs to. Add a project-specific rule on top only if the interview produced one (for example: «Файл с выпиской не менять — из него читаются данные»).

- «Что учесть потом» — the fifth section, and the only conditional one. It exists so the plans from Step 4 survive this session; `## Now and later` in `SKILL.md` is the rule it serves.

  - Write it only when there is something real in it: the user answered Step 4 with plans, or named one as an aside somewhere else in the interview. Nothing to write → no heading at all.
  - One line per plan, in the user's own words. Do not upgrade them into technical language and do not turn one plan into three.
  - Add one line for any decision that was made because of those plans, so a later session does not quietly undo it. For example: «Работа с данными сделана через общий слой запросов — переезд на настоящую базу это одна строка настроек, а не переписывание».
  - Five lines is the ceiling. If the user named more plans than that, keep the ones they said first.
  - **This is not a to-do list.** No stages, no priorities, no dates, no checkboxes. It is the note that lets the next conversation start informed. Never build anything from this section on your own initiative — only when the user asks for it.

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
<Numbered steps, literal, no assumed knowledge. Single-file shape: «Откройте папку <folder>» / «Дважды кликните по файлу <name>.html» / «Откроется браузер — это и есть ваш проект». Real-app shape: the one documented launch command, in a code block, as a single step — the same command, character for character, as in `CLAUDE.md` — plus the address to open and what the user should see.>

## Что говорить Клоду дальше
Скопируйте любую строчку и вставьте в чат с Клодом:

- «<phrase 1>»
- «<phrase 2>»
- «<phrase 3>»

## Если что-то сломалось
1. Скажите Клоду: «Сломалось, вот что я делал: …» — и опишите своими словами последние действия.
2. Не удаляйте файлы сами — почти всё чинится словами, а удалённое вернуть сложнее.
3. <If this project keeps its own history: «Чтобы вернуть предыдущую рабочую версию, скажите Клоду: „Верни, как было до последних изменений“». If it does not: «Этот проект лежит внутри вашего большого проекта, поэтому свои старые версии он отдельно не хранит».>
4. <Only when the store is PostgreSQL — see the notes below. Otherwise this step does not exist.>

## Чего лучше не делать
- <item 1>
- <item 2>
```

Notes on the sections:

- «Как запустить» — the launch command here and in `CLAUDE.md` must be the same string, and both must be the command that was actually run at `## Launch and verify`. This is checked again in step 1 of that section and is the most common way a real-app project breaks for its owner.
- «Что говорить Клоду дальше» — three to five ready phrases, written for this specific project, not generic advice. Each one must be a complete request the user can paste as is. Reference examples of the right shape and length: «Добавь на страницу график расходов по месяцам», «Сделай так, чтобы данные сохранялись после закрытия», «Поменяй цвета на более спокойные». Derive yours from what the user described at Step 3 and from what the project does not do yet. If there were plans at Step 4, one of these phrases is the first of those plans, written as a request — that is the only place a plan may appear in this file, and it is written as something to ask for, never as something the project already does.
- «Если что-то сломалось» — keep all three steps and keep them in this order. The first two are the same in every project. The third depends on whether this project keeps a history of its own: `## Version control` in `references/scaffolds.md` creates one, except when the project folder sits inside a bigger project of the user's — then there is no earlier version to come back to, and the step must say so plainly instead of promising a return: «Этот проект лежит внутри вашего большого проекта, поэтому свои старые версии он отдельно не хранит». Never the word «репозиторий» — `## Tone rules` bans it. You already know which case you are in when you write this file: the project folder was fixed at Step 13, so run `git rev-parse --is-inside-work-tree` in it and write the matching sentence.

  The section ends after the third step — with one exception. **When the store is PostgreSQL, and only then, add a fourth step: one plain line about refilling an empty database.** `### Data` in `references/scaffolds.md` says why it is needed — that store lives outside the project folder and does not come back with «верни, как было», so a person who rolls back finds a working project with nothing on the screen. Reference wording, with the real command in it: «Если после возврата предыдущей версии в приложении стало пусто — запустите: `<команда>`». One line. Do not explain what a database is, do not say why it happened, and do not let it grow into a second line.
- «Чего лучше не делать» — two or three items, each a concrete action in this project. Default items that almost always apply: «Не переименовывайте файлы вручную — скажите Клоду, и он переименует», «Не удаляйте папку `.claude` — в ней настройки». Add a project-specific one if there is an obvious way to break this project by hand — for the single-file shape, «Не чистите историю браузера на этой странице — в ней лежат ваши данные».
- **The file ends with «Чего лучше не делать».** Nothing comes after it: no sign-off, no thanks, no mention of who wrote this plugin, no telegram channel, nothing to subscribe to. This is the user's working document — the file they open when they have forgotten how to start their project — and the place for who made the plugin is the plugin's own README, where somebody choosing a plugin will actually see it.

## Permissions

Written to `.claude/settings.local.json` in the project root. Create the `.claude` folder if it is not there. This file is settings, not user-facing text: nothing in it is translated.

Before you write the file, confirm the `permissions` syntax — the key names, the allowed `defaultMode` values, and the `Tool(pattern)` rule form — against the current Claude Code documentation; this part of the configuration drifts between releases. If it has changed, follow the documentation instead of the template below and say so in one plain sentence in the final report. Otherwise the template is the default and is written as is.

**The base**, written in every project whatever was built:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
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

**Then add to `allow` what this project actually runs, and nothing else:**

| What was built | Added to `allow` |
| :--- | :--- |
| Single-file shape | nothing — the base is the whole list |
| Real app on Node.js | `"Bash(npm install:*)"`, `"Bash(npm run:*)"`, `"Bash(node:*)"` |
| Real app on Python | `"Bash(python3:*)"`, `"Bash(pip install:*)"`, `"Bash(.venv/bin/python:*)"`, `"Bash(.venv/bin/pip:*)"` |

Why it is built this way (this explanation is for you, not for the user — never paste it into the project):

- `deny` overrides `allow` in every mode, so the dangerous commands it names stay blocked even though the rest of the permissions are wide. It is a net, not a guarantee: a `Bash()` rule matches the command as written, so a compound line like `cd x && rm -rf y` is not caught by `Bash(rm:*)`, and a `:*` rule does not reliably cover the bare command — which is why the bare forms `Bash(rm)`, `Bash(git reset --hard)` and `Bash(git clean)` are listed alongside them. The list catches the common shapes and makes a permissive setup reasonable to hand a non-programmer; it is not a sandbox, so never tell the user that nothing can be deleted.
- `"defaultMode": "acceptEdits"` lets Claude edit files and run ordinary file commands without stopping to ask, so the user is not asked to approve things they cannot judge.
- `ask` keeps a confirmation on `git push`: publishing is the one action the user should knowingly agree to.
- `Bash(open:*)`, `Bash(start:*)` and `Bash(xdg-open:*)` stay in the base for every shape: that is how the finished project gets opened for the launch check.

Rules for adapting it:

- Add only the lines for the base that was really built. A Python project does not get the Node.js lines, and the other way round. The base can change during the build — `## Launch and verify`, step 1, in `references/scaffolds.md` is where a stale list gets corrected.
- Add a command the project itself needs beyond the table, only if it really uses it.
- Never remove or shorten the `deny` list. Never add keys or modes beyond the template above, unless the documentation check at the top of this section says the syntax has changed — then follow the documentation.
- **Do not write `.gitignore` here.** `## Version control` in `references/scaffolds.md` writes it in the very next step, and it already puts `.claude/settings.local.json` in — a local settings file has no business in a shared folder — alongside the lines that keep keys and passwords out of the history of changes. One file written from two places is one file quietly overwritten by the second of them.

## Plan file

Written only when Step 14 was answered «Сохраните план файлом»; `## Saving the plan instead of building` in `SKILL.md` is the procedure this template serves. It goes in the project root.

The file name follows the Step 0 language, the same way the cheat sheet's does:

- Русский → `ПЛАН.md`
- English → `PLAN.md`
- Any other language → the plain local word for "plan" in that language, if it makes a normal file name; otherwise `PLAN.md`.

**This is a working document, not notes.** The session that opens it will know nothing at all about this conversation — not the answers, not the reasons, not what was considered and dropped. Everything needed to build the project has to be inside the file.

- **Never write a pointer back into this conversation.** No «как обсуждали выше», no «как договорились», no «см. предыдущее сообщение», no «тот образец, который вы прислали». Every phrase like that is a hole in the document. Where the sample was long it is already saved as `design.md` — name that file instead of alluding to it.
- **Never leave a decision out because it felt obvious while you were making it.** The base, the store, the shape: each written down with its one-line reason. Without the reason the next session will decide it differently and be certain it is right.
- The user opens this file too, so it is in the Step 0 language and follows `## Tone rules`. It is longer than the cheat sheet, and it may name the base and the store plainly — it is instructions for work, not reassurance.
- Nothing gets built in this branch, so nothing reconciles this file afterwards. There is no later step that fixes it. Write it right the first time.

Template:

```markdown
# План: <название проекта на языке пользователя>

## Что это за приложение и для кого
<Two or three sentences from the Step 3 answer, in the user's own words. Then who will use it, from Steps 5 and 6: how many people, and whether their rights differ.>

## Ответы на вопросы
- Язык общения: <Step 0>
- Что нужно сделать: <the Step 3 answer in full, in the user's own words>
- Что планируется дальше: <Step 4, or «ничего не назвали»>
- Кто будет пользоваться: <Step 5>
- Разные роли: <Step 6, or «вопрос не задавался»>
- Откуда данные: <Step 7, with every source listed if there were several>
- Где будет жить: <Step 8>
- Как запускать: <Step 9>
- Образец оформления: <Step 10 — what was given and where it is now: the link, `design.md`, the name of the picture file>
- Как разговаривать с пользователем: <Step 12>

## На чём делаем
<The shape from Step 9 and the base that `### Choosing the base` in `references/scaffolds.md` selects, with the one-line reason for that base. If the base could not be settled because nothing suitable is installed, write that down plainly instead, and say what has to be installed once.>

## Где хранятся данные
<The store per `### Data`, one or two lines, with the reason. Plus the rule that every read and write goes through the query layer — that is a decision a later session must not quietly undo.>

## Из чего состоит оформление
- <one line per screen and per part of the interface, named>
- <...>

## Как это будет запускаться
<The double click, or the one command. If the command cannot be known yet because nothing is built, say what shape it will take.>

## Что учесть потом
- <plans from Step 4, one line each, in the user's own words>
- <any decision that was made because of them>
```

Notes on the sections:

- «Ответы на вопросы» is what makes the document self-sufficient. Keep every line, including the ones that look redundant next to the prose above them — a later session reads answers, not atmosphere. Where a step was skipped, say it was skipped rather than dropping the line.
- «Из чего состоит оформление» is neither optional nor a summary. **If Step 10 brought a ready-made design description, every component it names gets its own line here** — eleven components, eleven lines. This is the same list Step 14 said out loud and the same list `## Verification` walks after a build, and it is the one part of the plan that cannot be reconstructed from anything else in the folder.
- «Что учесть потом» follows the same rule as the section of that name in `CLAUDE.md`: plans are written down and never built, and five lines is the ceiling.
- Add no sections beyond these six. No stages, no estimates, no dates, no checkboxes, no acceptance criteria. This is a plan for one session of work, not a project management document.
