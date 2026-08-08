# Scaffolds

Read at generation time only, after Step 6 is confirmed. This file describes the two shapes a project can take, plus the two procedures that run for both shapes.

How to use this file:

- Build exactly one shape — the one chosen at Step 5. Never both, never a mix.
- These instructions are English. Everything the user ends up seeing — file names, on-screen labels, comments in the code, commit messages — is written in the language picked at Step 0.
- Russian text here is reference wording, not literal output. Translate it into the Step 0 language, keeping the meaning and roughly the length. If Step 0 is Русский, use it as written.
- `<angle brackets>` mark a placeholder you replace with the real value. Never write the brackets into a generated file.
- `## Tone rules` from `SKILL.md` applies to every word the user reads: no jargon, short sentences, never a raw error message.

Order of operations, fixed:

1. Build the shape — `## Single file` or `## Real app`.
2. Write `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json` from `references/templates.md`.
3. `## Launch and verify` — the project must actually run.
4. `## Version control` — only after the launch check has passed.
5. Give the final report, per `SKILL.md`.

## Single file

Chosen at Step 5: «Файл, который открывается двойным кликом».

**Shape.** One self-contained HTML file in the project root. Nothing else is needed to run it.

- Name it in the user's language, after what the project actually does: `Мои расходы.html`, `Калькулятор кредита.html`. Spaces are fine — the user double-clicks the file and never types its name.
- Use that exact name, character for character, in `CLAUDE.md` «Как запустить» and in the cheat sheet. Three different spellings of the file name is the most common way this shape breaks.
- No `package.json`, no build step, no install step, nothing to run in a terminal. This is the «single-file shape» in `references/templates.md` → `## Permissions`: drop the two `npm` lines from `allow` and leave `deny` and `ask` exactly as written there.

**Self-contained means offline.** Markup, styles and script all live inside that one file, in `<style>` and `<script>` tags.

- No `<link>` or `<script src>` pointing at a CDN, a font service or any other address. No `import` from a URL, no `fetch` to the internet.
- The file must render correctly with the network switched off, and it must still work if it is copied to another computer or emailed to a colleague.
- Always set `<meta charset="utf-8">` and `<html lang="<Step 0 language code>">`, so non-Latin text renders.

**Data that has to survive.** If the user needs their data to still be there next time they open the file, store it in the browser's `localStorage`.

- Handle the first run, when there is nothing stored yet, without an error on screen.
- Warn the human once, in one plain sentence in the cheat sheet: the data lives in this browser on this computer — so it is not on another computer, and clearing the browser's history erases it. One sentence, no lecture, no talk of storage engines.

**A file from Step 4.** If the user has an Excel or CSV file:

- Put a file-choosing button on the page itself, read the file with `FileReader` in the browser, parse it in the page. No server, no upload, the file never leaves the computer.
- CSV is read directly. A `.xlsx` file cannot be parsed without an outside library, and outside libraries are banned in this shape — so either tell the user in one plain sentence to save the file as CSV first (and put that as a step in the cheat sheet's «Как запустить»), or, if it has to stay `.xlsx`, say in one sentence that this is a reason to build `## Real app` instead and let the user decide.

**Interface.** Large readable font. Plain labels in the Step 0 language — never leave English words on screen when the language is not English. Works on a narrow phone screen: a `<meta name="viewport">` tag, no fixed pixel widths, nothing cut off at the edge.

## Real app

Chosen at Step 5: «Настоящее приложение».

**Check Node.js before you build anything.** Run `node --version`.

- If it is there, continue.
- If it is not, do not paste an installation manual and do not show the raw error. Say in one plain sentence what has to be installed once, give the direct link `https://nodejs.org`, and offer to build the `## Single file` version right now so the user sees a working result today. Then do whatever they choose.

**Shape.** The smallest project that does the job.

- One `package.json` in the project root. Not a monorepo: no workspaces, no `packages/` folder, no second `package.json` anywhere.
- `package.json` has the scripts `dev` and `start`.
- The script names in `package.json`, in `CLAUDE.md` «Как запустить» and in the cheat sheet must match literally, character for character. If the cheat sheet says `npm run dev`, then `dev` is the key in `package.json`.
- Exactly one way to launch. Pick it, document only it, and never write «или так, или так» — a second option is a second thing that can go wrong.
- As few outside libraries as possible. Prefer what Node already has built in. Every added library is something the user will one day have to reinstall.
- Pick one fixed port and write the address literally — `http://localhost:3000`. Never let the port float between runs.

**Data.** The simplest storage that closes the task, and no more.

- A JSON file on disk or a single local SQLite file covers almost everything this audience asks for.
- Stand up a real database server only if the task genuinely cannot work without one. In that case you start it and verify it works yourself — the user never gets install steps to run by hand, and never sees a connection error.
- If Step 3 was «Внешние люди», give each person their own login, but keep one application and one data store. No tenant isolation layer, no separate schema or database per customer.

## Launch and verify

Mandatory for both shapes. The project is not finished until it has been launched and seen to work.

1. Launch the result yourself. Never write "готово" without having run it.
2. **Single file:** open it in the default browser — `open "<name>.html"` on macOS, `start "" "<name>.html"` on Windows, `xdg-open "<name>.html"` on Linux. Confirm the page renders and that the main action actually works: the number is calculated, the file loads, the entry is saved and is still there after a reload.
3. **Real app:** install the dependencies, start the app with the one documented command, open the browser at its address, and confirm the page renders and the main action works.
4. **If it fails:** fix it and launch again — up to three attempts. Do not report the failure to the user unless it needs a decision only they can make, and then in plain language, never as a raw error message, stack trace or exit code.
5. **After three failed attempts, stop.** Tell the user in plain language: what does not work, what already does work, and what you will try next. Never claim success, and never keep looping past three attempts.
6. Only after a launch that worked: run `## Version control`, then report success and describe exactly what the user should see on screen.

## Version control

Mandatory for both shapes, and invisible to the user. It exists so the cheat sheet is telling the truth: it promises that «Верни, как было до последних изменений» works, and that promise is empty if nothing was ever saved.

Run this after the project files exist and after the launch check in `## Launch and verify` has passed — a snapshot is only useful if it is a snapshot of something that works.

1. **Create the local history.** In the project root, unless that folder already contains a `.git` folder, run:

   ```bash
   git init
   ```

   Only ever in the project root — never in a parent folder, never in the user's home folder.

2. **Write `.gitignore`** in the project root. It must contain at least these two lines:

   ```
   .claude/settings.local.json
   .DS_Store
   ```

   For `## Real app`, add `node_modules/` as well. If the permissions step from `references/templates.md` already created `.gitignore` with the single `.claude/settings.local.json` line, add the missing lines to that same file — do not create a second one.

3. **Make one initial commit** containing everything:

   ```bash
   git add -A
   git commit -m "<message in the user's language, e.g. «Первая рабочая версия»>"
   ```

   If the commit fails only because a name and an email are not configured, set them locally for this project folder with a neutral value and commit again. Do not ask the user for them.

4. **Say nothing about any of this.** Do not narrate it, do not list it in the final report, and never use the word «репозиторий» with the user — `## Tone rules` bans it. In the cheat sheet this shows up only as the fact that «Верни, как было до последних изменений» works.

5. **Local only.** Never run `git push`, never add a remote, never mention GitHub, never ask whether the user wants to publish. This is a safety net on their own computer and nothing else. The `ask` rule on `Bash(git push:*)` in the permissions template is a guard rail, not an invitation to use it.

## Never add

Not in either shape, no matter how tempting or how standard it looks elsewhere:

- Git hooks of any kind.
- A documentation gate, or any rule that blocks work until a document is updated.
- A `docs/` tree, architecture decision records, or design documents. The project has `CLAUDE.md` and one cheat sheet, and that is all.
- A methodology or process layer on top of the project.
- A monorepo, workspaces, or more than one `package.json`.
- Multi-tenant data isolation.

Anything the interview did not actually ask for is out of scope. When in doubt, build less: the user has to be able to hold the whole project in their head.
