# Scaffolds

Read at generation time only, after Step 9 is confirmed. This file describes the two shapes a project can take, plus the two procedures that run for both shapes.

How to use this file:

- Build exactly one shape — the one chosen at Step 6. Never both, never a mix.
- These instructions are English. Everything the user ends up seeing — file names, on-screen labels, comments in the code, commit messages — is written in the language picked at Step 0.
- Russian text here is reference wording, not literal output. Translate it into the Step 0 language, keeping the meaning and roughly the length. If Step 0 is Русский, use it as written.
- `<angle brackets>` mark a placeholder you replace with the real value. Never write the brackets into a generated file.
- `## Tone rules` from `SKILL.md` applies to every word the user reads, in the register chosen at Step 8: short sentences always, and — unless the user asked for technical terms — no jargon and never a raw error message.

Order of operations, fixed:

1. Write `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json` from `references/templates.md` — first, so the permissions are in place before anything below runs a command.
2. Build the shape — `## Single file` or `## Real app`.
3. Reconcile those three files with what actually got built — `## Launch and verify`, step 1. Always, not only when something looks off.
4. `## Launch and verify` — the project must actually run.
5. `## Version control` — only after the launch check has passed.
6. Give the final report, per `## Final report` in `SKILL.md`.

The folder to build in was already decided at `## Step 9` in `SKILL.md`, before the first file was written. Work in it and never move the project afterwards.

## Single file

Chosen at Step 6: «Файл, который открывается двойным кликом».

**Shape.** One self-contained HTML file in the project root. Nothing else is needed to run it.

- Name it in the user's language, after what the project actually does: `Мои расходы.html`, `Калькулятор кредита.html`. Spaces are fine — the user double-clicks the file and never types its name.
- Use that exact name, character for character, in `CLAUDE.md` «Как запустить» and in the cheat sheet. Three different spellings of the file name is the most common way this shape breaks. `CLAUDE.md` and the cheat sheet are written before this file exists, so settle on the name first and then use it unchanged. `## Launch and verify`, step 1, checks all three against each other and is where a drifted name gets fixed.
- No `package.json`, no build step, no install step, nothing to run in a terminal. This is the «single-file shape» in `references/templates.md` → `## Permissions`: drop the two `npm` lines — `"Bash(npm install:*)"` and `"Bash(npm run:*)"` — from `allow`, keep the rest of `allow`, and leave `deny` and `ask` exactly as written there.

**Self-contained means offline.** Markup, styles and script all live inside that one file, in `<style>` and `<script>` tags.

- No `<link>` or `<script src>` pointing at a CDN, a font service or any other address. No `import` from a URL, no `fetch` to the internet.
- The file must render correctly with the network switched off, and it must still work if it is copied to another computer or emailed to a colleague.
- Always set `<meta charset="utf-8">` and `<html lang="<Step 0 language code>">`, so non-Latin text renders.

**Data that has to survive.** If the user needs their data to still be there next time they open the file, store it in the browser's `localStorage`.

- Handle the first run, when there is nothing stored yet, without an error on screen.
- Warn the human once, in one plain sentence in the cheat sheet: the data lives in this browser on this computer — so it is not on another computer, and clearing the browser's history erases it. One sentence, no lecture, no talk of storage engines.

**A file from Step 5.** If the user has an Excel or CSV file:

- Put a file-choosing button on the page itself, read the file with `FileReader` in the browser, parse it in the page. No server, no upload, the file never leaves the computer.
- CSV is read directly. A `.xlsx` file cannot be parsed without an outside library, and outside libraries are banned in this shape — so build the page to read CSV, and add one step to the cheat sheet's «Как запустить» telling the user in plain words to save their Excel file as CSV first («Файл → Сохранить как → CSV»). Take this branch without stopping to ask: `## Generation` promises one pass with no pauses for approval. Mention in the final report, in one sentence, that Excel files need that one save-as step — and if the user would rather not have it, they can ask for the «настоящее приложение» version later.

**Interface.** Large readable font. Plain labels in the Step 0 language — never leave English words on screen when the language is not English. Works on a narrow phone screen: a `<meta name="viewport">` tag, no fixed pixel widths, nothing cut off at the edge.

**The look chosen at Step 7 governs the visual treatment** — colours, spacing, type sizes, how much decoration there is:

- «Строго, по-деловому» — restrained business-report styling: near-white background, dark text, one accent colour, thin dividing lines, aligned columns, numbers right-aligned. No rounded cards, no gradients, no emoji.
- «Мягко и спокойно» — calm everyday styling: soft muted background, generous spacing, gently rounded corners, one warm accent, nothing shouty. It is opened every day, not presented once.
- «На ваш вкус» — your own tasteful default: simple, tidy, well spaced, one accent colour, and nothing competing with the numbers.
- A reference was given at Step 7 (a link, a screenshot in the project folder, or a description in words) — follow it as far as one self-contained file allows: layout, colours, type sizes, overall tone. Whatever cannot be reproduced here — a web font, an image you do not have, something that would need a server — say so in one plain sentence in the final report instead of silently approximating it.

None of this bends the rules above: no external links, no web fonts, no CDN. The file must still render with the network switched off, so use a plain system font stack and write the colours into the file.

## Real app

Chosen at Step 6: «Настоящее приложение».

**Check Node.js before you build anything.** Run `node --version`.

- If it is there, continue.
- If it is not, do not paste an installation manual and do not show the raw error. Say in one plain sentence what has to be installed once, give the direct link `https://nodejs.org`, and offer to build the `## Single file` version right now so the user sees a working result today. Then do whatever they choose.
- If they take the single-file version, the shape has changed after `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json` were already written for a real app. Build the single-file shape, then correct all three in `## Launch and verify`, step 1 — that step is mandatory and is where this gets fixed.

**Shape.** The smallest project that does the job.

- One `package.json` in the project root. Not a monorepo: no workspaces, no `packages/` folder, no second `package.json` anywhere.
- `package.json` has the scripts `dev` and `start`.
- **The documented launch command is always `npm start`.** That is the one command written into `CLAUDE.md` «Как запустить» and into the cheat sheet, in every real-app project, with no exceptions. `dev` may exist in `package.json` for your own use, but it is never shown to the user and never named in a generated file.
- So `start` in `package.json` must be the script that actually launches the finished project — not a placeholder, not an alias for a build step.
- Exactly one way to launch. Document only `npm start` and never write «или так, или так» — a second option is a second thing that can go wrong.
- As few outside libraries as possible. Prefer what Node already has built in. Every added library is something the user will one day have to reinstall.
- Pick one fixed port and write the address literally — `http://localhost:3000`. Never let the port float between runs.

**Data.** The simplest storage that closes the task, and no more.

- A JSON file on disk or a single local SQLite file covers almost everything this audience asks for.
- Stand up a real database server only if the task genuinely cannot work without one. In that case you start it and verify it works yourself — the user never gets install steps to run by hand, and never sees a connection error.
- If Step 4 was «Внешние люди», give each person their own login, but keep one application and one data store. No tenant isolation layer, no separate schema or database per customer.

**Interface.** Large readable font. Plain labels in the Step 0 language — never leave English words on screen when the language is not English. Works on a narrow phone screen: no fixed pixel widths, nothing cut off at the edge.

**The look chosen at Step 7 governs the visual treatment** here exactly as in `## Single file`:

- «Строго, по-деловому» — restrained business-report styling: near-white background, dark text, one accent colour, thin dividing lines, aligned columns, numbers right-aligned. No rounded cards, no gradients, no emoji.
- «Мягко и спокойно» — calm everyday styling: soft muted background, generous spacing, gently rounded corners, one warm accent, nothing shouty.
- «На ваш вкус» — your own tasteful default: simple, tidy, well spaced, one accent colour, and nothing competing with the numbers.
- A reference was given at Step 7 — follow it as far as this project allows, and say in one plain sentence in the final report whatever could not be reproduced, instead of silently approximating it.

The offline rules hold here too: no CDN, no web font service, no external links. Ship the styles inside the project and use fonts already on the computer — the app has to work with no internet.

## Launch and verify

Mandatory for both shapes. The project is not finished until it has been launched and seen to work.

1. **Reconcile the three written files with what is actually on disk. This step is mandatory and runs every time — never treat it as a check to skip when nothing seems to have changed.** `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json` were written before the build, from the plan, so nothing guarantees they describe the project that now exists. Re-open all three and compare against reality:

   - Every file name, character for character — the HTML file the user double-clicks, and every file listed in «Где что лежит». The launch check below opens the file that exists, so a wrong name in the cheat sheet passes verification silently and leaves the user with a lifeline document that points at nothing.
   - Every command, character for character — the documented launch command against the `start` script that is really in `package.json`, and any extra step the build added (for example the xlsx→CSV save-as step from `## Single file`, which has to be written into the cheat sheet's «Как запустить» now, not assumed to be there).
   - Every line of `allow` in `.claude/settings.local.json` against the shape that was actually built.

   **The shape itself can change mid-run.** The real-app build runs `node --version` after these three files are already written; if Node.js is missing and the user takes the offered `## Single file` version, all three describe a project that was never built. Then this step rewrites them: «Как запустить» becomes the double-click instruction instead of `npm start`, «Где что лежит» lists the HTML file, and the two `npm` lines — `"Bash(npm install:*)"` and `"Bash(npm run:*)"` — come out of `allow`. Fix the written files; never bend the project to match a stale document.

   Say nothing to the user about any of this, with one exception. It is bookkeeping, and `## Tone rules` bans narrating work in progress. The exception is a file that ended up with a name other than the one promised in the Step 9 summary: say so in one plain sentence naming both the promised name and the real one — «Файл, который я обещал назвать "<обещанное>", назвал "<фактическое>" — так понятнее». One sentence per renamed file, not a list of changes and not an apology. A better name is welcome; a silent one leaves the user holding a summary that no longer matches their folder.

2. Launch the result yourself. Never write "готово" without having run it.
3. **Single file:** open it in the default browser — `open "<name>.html"` on macOS, `start "" "<name>.html"` on Windows, `xdg-open "<name>.html"` on Linux. Confirm the page renders and that the main action actually works: the number is calculated, the file loads, the entry is saved and is still there after a reload.
4. **Real app:** install the dependencies with `npm install`, start the app with `npm start` — the one documented command — open the browser at its address, and confirm the page renders and the main action works.
5. **If it fails:** fix it and launch again — up to three attempts. Do not report the failure to the user unless it needs a decision only they can make, and then in plain language, never as a raw error message, stack trace or exit code.
6. **After three failed attempts, stop.** Tell the user in plain language: what does not work, what already does work, and what you will try next. Never claim success, and never keep looping past three attempts.
7. Only after a launch that worked: run `## Version control`, then report success and describe exactly what the user should see on screen.

## Version control

Mandatory for both shapes, and invisible to the user. It exists so the cheat sheet is telling the truth: it promises that «Верни, как было до последних изменений» works, and that promise is empty if nothing was ever saved. There is exactly one case where no history is created — step 1 below — and there the cheat sheet drops the promise instead.

Run this after the project files exist and after the launch check in `## Launch and verify` has passed — a snapshot is only useful if it is a snapshot of something that works.

1. **First find out whether this project already sits inside one of the user's own projects.** From the project folder, before initialising anything:

   ```bash
   git rev-parse --is-inside-work-tree
   ```

   If that says the folder is already inside a repository, this project lives inside a bigger project of theirs — which is what happens when Step 1 was answered «Сделать новый проект рядом» in a folder that was already under version control. Then this project gets **no separate history**: skip `git init` in step 2, skip the commit in step 4, and touch the outer project in no way at all — nothing written to its `.gitignore`, nothing written under its `.git/`. A history inside a history is worse than none: the outer project records this folder as a broken reference, and a copy of the outer project comes out with the new work missing entirely, which is not something this user can repair. Skipping here is a deliberate choice, not a failure, so say nothing about it — but the cheat sheet must not promise what is not there, so its «Если что-то сломалось» step three is written per the note in `references/templates.md` for a project without its own history.

2. **Create the local history** — only when step 1 found this folder is not already inside another project, and unless the project root already contains a `.git` folder. In the project root, run:

   ```bash
   git init
   ```

   Only ever in the project folder chosen at `## Step 9` — never in a parent folder, and never in the user's home folder. `## Step 9` already guaranteed that folder is neither the home folder nor a folder full of the user's other things, so there is nothing to move and no path to rewrite here. Apart from the one case in step 1, never skip version control: skipping it hollows out the «верни, как было» promise the cheat sheet makes.

3. **Write `.gitignore`** in the project root — in both cases, whether or not this project got a history of its own; it is a file inside the project folder, and the outer project's own `.gitignore` is still never touched. It must contain at least these two lines:

   ```gitignore
   .claude/settings.local.json
   .DS_Store
   ```

   For `## Real app`, add `node_modules/` as well. If the permissions step from `references/templates.md` already created `.gitignore` with the single `.claude/settings.local.json` line, add the missing lines to that same file — do not create a second one.

4. **Make one initial commit** containing everything — skipped entirely when step 1 found this folder inside another project:

   ```bash
   git add -A
   git commit -m "<message in the user's language, e.g. «Первая рабочая версия»>"
   ```

   If the commit fails only because a name and an email are not configured, set them locally for this project folder with a neutral value and commit again. Do not ask the user for them.

5. **Say nothing about any of this — unless it was blocked.** Do not narrate it, do not list it in the final report, and never use the word «репозиторий» with the user — `## Tone rules` bans it. In the cheat sheet this shows up only as the fact that «Верни, как было до последних изменений» works — or, in the step-1 case, does not appear at all. The one exception is the blocked-action rule in `## Tone rules` of `SKILL.md`: if `git init`, `git add` or the commit is denied or refused, never quietly skip the step and carry on. Say in plain words that the history of changes was not saved and that «вернуть предыдущую версию не получится» — the cheat sheet promises it, and silence would leave that promise empty. That rule is about a denial only; the skip in step 1 is not one, and is never announced.

6. **Local only.** Never run `git push`, never add a remote, never mention GitHub, never ask whether the user wants to publish. This is a safety net on their own computer and nothing else. The `ask` rule on `Bash(git push:*)` in the permissions template is a guard rail, not an invitation to use it.

## Never add

Not in either shape, no matter how tempting or how standard it looks elsewhere:

- Git hooks of any kind.
- A documentation gate, or any rule that blocks work until a document is updated.
- A `docs/` tree, architecture decision records, or design documents. The project has `CLAUDE.md` and one cheat sheet, and that is all.
- A methodology or process layer on top of the project.
- A monorepo, workspaces, or more than one `package.json`.
- Multi-tenant data isolation.

Anything the interview did not actually ask for is out of scope. When in doubt, build less: the user has to be able to hold the whole project in their head.
