# Scaffolds

Read at generation time only, after Step 16 has been answered. This file describes the two shapes a project can take, plus the procedures that run for both shapes.

How to use this file:

- Build exactly one shape — the one chosen at Step 9. Never both, never a mix.
- These instructions are English. Everything the user ends up seeing — file names, on-screen labels, comments in the code, commit messages — is written in the language picked at Step 0.
- Russian text here is reference wording, not literal output. Translate it into the Step 0 language, keeping the meaning and roughly the length. If Step 0 is Русский, use it as written.
- `<angle brackets>` mark a placeholder you replace with the real value. Never write the brackets into a generated file.
- `## Tone rules` from `SKILL.md` applies to every word the user reads, in the register chosen at Step 14: short sentences always, and — unless the user asked for technical terms — no jargon and never a raw error message.
- Nothing in this file re-opens a question the interview already answered. The base and the store came from Steps 11 and 10; everything else below follows from the other answers and from what is already on the computer. `## Generation` promises one pass with no pauses, so this is not the place to start asking — the one thing that does get said out loud is the plain sentence owed to the user when the computer cannot honour an answer they gave, and even that is a statement, not a new question.

Order of operations, fixed:

1. Write `.claude/settings.local.json` from `references/templates.md` — first, so the permissions are in place before anything below runs a command.
2. `## Version control`, steps 1–4: the check for an outer project, `git init`, `.gitignore`, and the first commit — **before the project is built**, on an all-but-empty folder. That commit is the point the user can be brought back to.
3. Write `CLAUDE.md` and the cheat sheet from `references/templates.md`, then commit.
4. Build the shape — `## Single file` or `## Real app` — with the look `## Design reference` prescribes, then commit.
5. Reconcile the three written files with what actually got built — `## Launch and verify`, step 1. Always, not only when something looks off.
6. `## Launch and verify` — the project must actually run, and the list from Step 16 is then walked item by item. Then commit; that commit carries the fixes from step 5 too.
7. Give the final report, per `## Final report` in `SKILL.md`.

Version control used to sit at the end of this list. It does not any more, and the reason is worth keeping in mind while you work: a history that starts only once everything is finished cannot rescue a build that went wrong halfway. Every step above that ends in a commit ends in one for that reason.

The folder to build in was already decided at `## Step 15` in `SKILL.md` and created as the first action after Step 16. Work in it and never move the project afterwards.

## Single file

Chosen at Step 9: «Файл, который открывается двойным кликом».

**Shape.** One self-contained HTML file in the project root. Nothing else is needed to run it.

- Name it in the user's language, after what the project actually does: `Мои расходы.html`, `Калькулятор кредита.html`. Spaces are fine — the user double-clicks the file and never types its name.
- Use that exact name, character for character, in `CLAUDE.md` «Как запустить» and in the cheat sheet. Three different spellings of the file name is the most common way this shape breaks. `CLAUDE.md` and the cheat sheet are written before this file exists, so settle on the name first and then use it unchanged. `## Launch and verify`, step 1, checks all three against each other and is where a drifted name gets fixed.
- No dependency manifest, no build step, no install step, nothing to run in a terminal. This is the «single-file shape» in `references/templates.md` → `## Permissions`: write the base `allow` list and add nothing to it.

**Self-contained means offline.** This is the one shape where that rule holds. Markup, styles and script all live inside that one file, in `<style>` and `<script>` tags.

- No `<link>` or `<script src>` pointing at a CDN, a font service or any other address. No `import` from a URL, no `fetch` to the internet.
- The file must render correctly with the network switched off, and it must still work if it is copied to another computer or emailed to a colleague.
- Always set `<meta charset="utf-8">` and `<html lang="<Step 0 language code>">`, so non-Latin text renders.

**Offline is not an excuse to cut features.** This rule is about where the code comes from, never about what the page can do. A period picker, filters, charts, sortable tables, a summary strip — all of them are perfectly buildable by hand in one file with plain HTML, CSS and inline SVG or `<canvas>`, and if the user asked for one, you build it. Never quietly drop something the person described or showed, and never offer a poorer page than they asked for because a library would have been easier.

The only things that genuinely cannot exist here are a font you do not have on the computer, a picture you were not given, and anything that needs live data from the internet or a server. When one of those is what the user wanted, say so in one plain sentence in the final report and offer the «настоящее приложение» version — do not silently approximate it.

**Data that has to survive.** If the user needs their data to still be there next time they open the file, store it in the browser's `localStorage`.

- Handle the first run, when there is nothing stored yet, without an error on screen.
- Warn the human once, in one plain sentence in the cheat sheet: the data lives in this browser on this computer — so it is not on another computer, and clearing the browser's history erases it. One sentence, no lecture, no talk of storage engines.

**A file from Step 7.** If the user has an Excel or CSV file:

- Put a file-choosing button on the page itself, read the file with `FileReader` in the browser, parse it in the page. No server, no upload, the file never leaves the computer.
- CSV is read directly. A `.xlsx` file cannot be parsed without an outside library, and outside libraries cannot exist in a file that has to open offline by itself — so build the page to read CSV, and add one step to the cheat sheet's «Как запустить» telling the user in plain words to save their Excel file as CSV first («Файл → Сохранить как → CSV»). Take this branch without stopping to ask. Mention in the final report, in one sentence, that Excel files need that one save-as step — and that the «настоящее приложение» version reads `.xlsx` directly, if they would rather not have it.

**Interface.** Large readable font. Plain labels in the Step 0 language — never leave English words on screen when the language is not English. Works on a narrow phone screen: a `<meta name="viewport">` tag, no fixed pixel widths, nothing cut off at the edge.

**The look** is governed by `## Design reference` — the Step 12 sample if there was one, otherwise the Step 13 answer.

## Real app

Chosen at Step 9: «Настоящее приложение».

### Choosing the base

**The base is not yours to pick. The user chose it at Step 11**, from two options with one of them recommended, and that answer is what you build on. Nothing here is hardwired and nothing is decided by taste; what is left for this section is one thing only — what to do when the computer does not have what they chose.

1. **Take the answer from Step 11** — Python or Node.js — and check whether it is there: `python3 --version`, or `node --version`. Nobody was asked anything before this moment: `## Interview rules` in `SKILL.md` forbids running a check during the interview, because an approval prompt in the middle of a question is exactly what the user cannot judge.
2. **It is installed** → build on it and say nothing. The choice was already stated out loud at Step 16; repeating it now is narrating work in progress.
3. **It is missing and the other one is there.** Never swap silently — a silent swap is the very thing Steps 10 and 11 were added to stop. Say it in one plain sentence: what they picked is not on this computer, the other one is, it will do this job just as well, and switching costs nothing today. Then build on the one that is there, unless the user says otherwise. Do not hand them an installation manual for the missing one; if they ask for it, one sentence and the direct link (`https://www.python.org/downloads/` for Python, `https://nodejs.org` for Node.js).
4. **If neither is there** — do not paste an installation manual and do not show the raw error. Say in one plain sentence what has to be installed once, give the direct link, and offer to build the `## Single file` version right now so the user sees a working result today. Then do whatever they choose. If they take the single-file version, the shape has changed after `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json` were already written for a real app — `## Launch and verify`, step 1, is mandatory and is where all three get fixed.
5. **Never override the answer for a reason of your own** — not because the other base would suit the task better in your view, not because a library is nicer there. Step 11 already put the recommendation in front of the user and they answered it. If the answer genuinely cannot be built, that is one of the cases above and it is said out loud, not worked around.

**If Step 11 somehow did not run** — a session resuming from a plan file that predates it, an interview that was cut short — fall back to the recommendation logic written at Step 11 in `SKILL.md`: what the project does decides, and when both fit it is Python. Then state the choice in one sentence, never as a question: «Сделаю на Питоне — на нём же вы пишете скрипты к таблицам». In «С объяснениями» mode, one everyday analogy first.

**Frameworks: one, well known, boring.** Python → Flask or FastAPI with server-rendered templates; Streamlit is fine when the project really is a dashboard and nothing else. Node.js → Express with a plain front end, or Vite with React when the interface genuinely has many moving parts. Never a second framework on top of the first.

### Shape

The smallest project that does the job.

- One dependency manifest in the project root: `package.json` for Node.js, `requirements.txt` (or `pyproject.toml`) for Python. Not a monorepo: no workspaces, no `packages/` folder, no second manifest anywhere.
- Pick one fixed port and write the address literally — `http://localhost:3000` for Node.js, `http://localhost:8000` for Python. Never let the port float between runs.

### The launch command

- **Exactly one command, and it is the real one.** Never document a command you have not run yourself. Whatever `## Launch and verify` actually used is what goes into the files.
- It must work from the project folder as a **single line, with nothing to activate or set up first**. A Python project with its own extra programs means a virtual environment in `.venv`, and the documented command uses that interpreter directly: `.venv/bin/python app.py`, or `.venv/bin/streamlit run app.py` (on Windows `.venv\Scripts\python app.py`). Never document «сначала активируйте окружение» — that is a second command and a second thing to get wrong.
- Node.js: `package.json` gets a `start` script that really launches the finished project — not a placeholder, not an alias for a build step — and the documented command is `npm start`. A `dev` script may exist for your own use; it is never shown to the user and never named in a generated file.
- **Write that one command, character for character, into `CLAUDE.md` «Как запустить» and into the cheat sheet**, and use exactly it in `## Launch and verify`. Three different spellings of the launch command is how this shape breaks.
- Exactly one way to launch. Never write «или так, или так» — a second option is a second thing that can go wrong.

### Data

**The store is not yours to pick either. The user chose it at Step 10** — «файл рядом с проектом» or «настоящая база данных» — after seeing what each one gives and costs, with the recommendation marked. Answers 5, 7 and 8 have already done their work there: they decided which option carried the «рекомендую» label. What is left here is honouring the answer and handling the one way the computer can contradict it.

**The store.**

- **«Файл рядом с проектом» → SQLite.** One file next to the project, nothing to install, nothing to start, nothing that can fail to connect. Build it and say nothing — the user already knows, they picked it.
- **«Настоящая база данных» → PostgreSQL, but only if it is already running on this computer.** Check it: `pg_isready`, or one connection attempt on the default port. Running → use it and create the project's own database inside it.
- **Chosen but not running** — never fall back in silence. Step 10 promised the user that nothing would be installed and that this option needs a database that is already there, so say the outcome in one plain sentence: it was not found running on this computer, so the data goes into a file next to the project for now, and moving it over later is a settings change rather than a rebuild. One sentence, no port numbers, no error text. Then build on SQLite and carry on — this does not stop the build and is not a question.
- **Never install a database.** Not by yourself, and never by handing the user steps to run. There is no case in this plugin where a database gets installed — a project that works today beats an installation the person cannot finish.
- **If Step 10 did not run** — the double-click shape, a project that keeps nothing, or a plan file older than this step — SQLite is the default and nothing is asked or announced beyond the one everyday sentence about where the data lives. In «С объяснениями» mode, one analogy before it: «база данных — это как Excel-файл, только несколько человек могут писать в него одновременно и он не ломается».

**With PostgreSQL, the data also has to survive a rollback.**

A SQLite file sits inside the project folder and is committed along with everything else, which is why `## Version control` deliberately keeps it out of `.gitignore`: «верни, как было» brings the numbers back together with the code. PostgreSQL lives outside the folder and does not roll back with it. The user goes back to an earlier version and gets a working project with an empty screen — which, to them, is simply a project that broke.

So when PostgreSQL was the store:

- **Write a seeding script into the project and commit it** — `seed.py` for Python, `seed.js` for Node.js. It creates the tables through the query layer and puts in a little demo data: enough for every screen to have something on it, and no more. Write it so that running it on a database that already has rows adds nothing and removes nothing — a script that wipes the user's data is a worse problem than the one it was written to solve.
- **Run it once yourself** during `## Launch and verify`, before the launch check, so the check has something to show on screen and so the script is known to work. Never document a script you have not run.
- **Add one plain line to the cheat sheet** saying what to run to fill an empty database, per `## Cheat sheet` in `references/templates.md`. One line. Do not explain why it happens and do not describe how the database works.

**Always through a query layer. This is the part that matters.**

- Every table, every read and every write goes through a query layer that is not tied to one engine: **SQLAlchemy** for Python, **Knex** for Node.js.
- No SQL written for one engine's dialect: no `SERIAL`, no Postgres-only types, no SQLite-only tricks, no hand-built strings for one and not the other.
- The connection address lives in **exactly one place** — one line in one file. Moving from SQLite to a real database is then that one line plus copying the data across, not a rewrite.
- Because of this, the answers that point at a real database — several sources at Step 7, several people at Step 5, «из интернета» at Step 8 — cost nothing when the user chose the file at Step 10 anyway, or when no database is running. Build on SQLite and write one line into `CLAUDE.md` «Что учесть потом»: the data work is written so the base can be swapped, and moving to a real database is a settings change, not a rebuild. It is a note, not a debt. Never show a connection error, never mention a port, never present this as a compromise.
- That silence has exactly one exception, and it is the one above: when the user **chose** «настоящая база данных» at Step 10 and it turned out not to be running, they are told in one plain sentence what happened instead. Everything they were not promised stays unsaid; the thing they picked and did not get is said.

**Logins and rights.**

- Step 5 «Я и ещё несколько человек» → one simple shared login.
- Step 5 «Много людей» → a separate login per person, but one application and one data store. No isolation layer, no separate schema or database per customer.
- Step 6 «Кто-то только смотрит, кто-то вносит» → exactly two kinds of user: one who can look at everything, one who can also enter and change. Nothing more elaborate, and never a permission system the interview did not ask for.

### Interface

**Ready-made parts are allowed here, and expected.** This shape has an install step, so the reason the single file has none of them does not apply.

- Everything the person asked for gets built: a period picker, filters, charts, sortable tables, forms, an export. Never drop one of these to keep the project small — the interview asked for it, and a smaller project that does not do the job is not the simpler option.
- Use ordinary, well-known, boring libraries for those parts. One charting library, one set of interface parts — not three of each, and never a second one doing the same job as the first.
- The bar that stays: nothing added for what plain HTML already does; no design system dragged in for one button; no state library for one screen; nothing at all that the interview did not ask for. Fewer moving parts, but never fewer features than the person described.
- Libraries are installed into the project the ordinary way — `npm install`, or `pip install` into `.venv` — and never pulled from a CDN when the page opens. The finished app has to keep working when the network is flaky. Same for fonts: ship the file inside the project or use what is already on the computer.
- An `.xlsx` file from Step 7 is read directly here, with a library. No save-as-CSV step in this shape.
- Large readable font. Plain labels in the Step 0 language — never leave English words on screen when the language is not English. Works on a narrow phone screen: no fixed pixel widths, nothing cut off at the edge.

**The look** is governed by `## Design reference`.

## Design reference

Applies to both shapes. Two jobs: apply what the person actually gave, and make sure it survives past this session.

**If a sample was given at Step 12**, it is one of four kinds, and all four carry the same weight. None of them is a weaker form of another.

- **A link** to a site or a program. Do not open it and do not fetch it. What you use is what the user said about it, plus the genre the name suggests. Do not ask them to explain it further.
- **A picture in the project folder.** Open it and look at it before you write a single line of the interface — not after. Take the layout, the colours, the type sizes, the density, how much decoration there is.
- **A ready-made design description from another tool.** Treat it as instructions and follow them point by point. Never compress it into «в спокойных тонах» and then build your own thing — that is the same as losing it. Ignore only the parts that genuinely cannot exist in the chosen shape (a web font in a file that must open offline), and say which part that was, in one plain sentence, in the final report.
- **Their own words.** Exactly the same weight as everything above. Follow them literally: if they said «как в банковском приложении, только без рекламы», that is a brief.

**If no sample was given**, the Step 13 answer governs the visual treatment — colours, spacing, type sizes, how much decoration there is:

- «Строго, по-деловому» — restrained business-report styling: near-white background, dark text, one accent colour, thin dividing lines, aligned columns, numbers right-aligned. No rounded cards, no gradients, no emoji.
- «Мягко и спокойно» — calm everyday styling: soft muted background, generous spacing, gently rounded corners, one warm accent, nothing shouty. It is opened every day, not presented once.
- «На ваш вкус» — your own tasteful default: simple, tidy, well spaced, one accent colour, and nothing competing with the numbers.

**The sample has to outlive the conversation.** Write it down before you build — a sample that only ever existed in the chat is gone the moment the session ends, and the next conversation will restyle the project against it.

- **Short — up to about three lines:** one line at the end of `CLAUDE.md` «О проекте»: «Оформление — по образцу, который дал пользователь: <ссылка / имя файла / в двух словах>».
- **Longer — a ready-made design description usually is:** save it word for word as `design.md` in the project root, and add one line for it to `CLAUDE.md` «Где что лежит»: «`design.md` — образец оформления, по которому сделан внешний вид». Never rewrite, summarise or tidy the text on the way in.
- **A picture** stays exactly where the user put it — never moved, never renamed — and gets the same one line in «Где что лежит».
- `design.md` keeps that name in every language: it is a file name, and `## Language policy` in `SKILL.md` never translates those. Its contents are the user's, unchanged.

## Launch and verify

Mandatory for both shapes. The project is not finished until it has been launched and seen to work.

1. **Reconcile the three written files with what is actually on disk. This step is mandatory and runs every time — never treat it as a check to skip when nothing seems to have changed.** `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json` were written before the build, from the plan, so nothing guarantees they describe the project that now exists. Re-open all three and compare against reality:

   - Every file name, character for character — the HTML file the user double-clicks, `design.md` if there is one, and every file listed in «Где что лежит». The launch check below opens the file that exists, so a wrong name in the cheat sheet passes verification silently and leaves the user with a lifeline document that points at nothing.
   - The launch command, character for character — what is written in `CLAUDE.md` and in the cheat sheet against the command you actually ran, and any extra step the build added (for example the xlsx→CSV save-as step from `## Single file`, which has to be written into the cheat sheet's «Как запустить» now, not assumed to be there).
   - Every line of `allow` in `.claude/settings.local.json` against the shape and the base that were actually built — the Node.js lines have no business in a Python project and the other way round.

   **The shape and the base can both change mid-run.** The real-app build looks for Python and Node.js after these three files are already written; if neither is there and the user takes the offered `## Single file` version, all three describe a project that was never built. Then this step rewrites them: «Как запустить» becomes the double-click instruction instead of a command, «Где что лежит» lists the HTML file, and the base's lines come out of `allow`. Fix the written files; never bend the project to match a stale document.

   Say nothing to the user about any of this, with one exception. It is bookkeeping, and `## Tone rules` bans narrating work in progress. The exception is a file that ended up with a name other than the one promised in the Step 15 summary: say so in one plain sentence naming both the promised name and the real one — «Файл, который я обещал назвать "<обещанное>", назвал "<фактическое>" — так понятнее». One sentence per renamed file, not a list of changes and not an apology. A better name is welcome; a silent one leaves the user holding a summary that no longer matches their folder.

2. Launch the result yourself. Never write "готово" without having run it.
3. **Single file:** open it in the default browser — `open "<name>.html"` on macOS, `start "" "<name>.html"` on Windows, `xdg-open "<name>.html"` on Linux. Confirm the page renders and that the main action actually works: the number is calculated, the file loads, the entry is saved and is still there after a reload.
4. **Real app:** install the extra programs the ordinary way for the chosen base — `npm install`, or a `.venv` and `pip install`. If the store is PostgreSQL, run the seeding script from `### Data` now, so the screens have something on them. Then start the app with the one documented launch command, open the browser at the documented address, and confirm the page renders and the main action works.
5. **If it fails:** fix it and launch again — up to three attempts. Do not report the failure to the user unless it needs a decision only they can make, and then in plain language, never as a raw error message, stack trace or exit code.
6. **After three failed attempts, stop.** Tell the user in plain language: what does not work, what already does work, and what you will try next. Never claim success, and never keep looping past three attempts.
7. **Then walk the list from Step 16** — every screen and every part you named there, one at a time, per `## Verification` in `SKILL.md`. A launch that worked only proves the project starts. Something missing from that list is built now and checked again; it does not count against the three attempts above.
8. Only after a launch that worked and a list with nothing left unchecked: make the commit from step 5 of `## Version control`, then report success and describe exactly what the user should see on screen.

## Version control

Mandatory for both shapes, and invisible to the user. It exists so the cheat sheet is telling the truth: it promises that «Верни, как было до последних изменений» works, and that promise is empty if nothing was ever saved. There is exactly one case where no history is created — step 1 below — and there the cheat sheet drops the promise instead.

**This runs before the project is built, not after it.** Steps 1–4 — the check, `git init`, `.gitignore`, the first commit — come first, while the folder is still all but empty, and that first commit is the point the user can be brought back to. Then step 5 adds a commit after each state that works. The old order, one commit at the very end, left a hole: if the build went somewhere wrong there was nothing to return to, because no clean-folder point had ever existed.

1. **First find out whether this project already sits inside one of the user's own projects.** From the project folder, before initialising anything:

   ```bash
   git rev-parse --is-inside-work-tree
   ```

   If that says the folder is already inside a repository, this project lives inside a bigger project of theirs — which is what happens when Step 1 was answered «Сделать новый проект рядом» in a folder that was already under version control. Then this project gets **no separate history**: skip `git init` in step 2, skip the first commit in step 4 and every commit in step 5, and touch the outer project in no way at all — nothing written to its `.gitignore`, nothing written under its `.git/`. A history inside a history is worse than none: the outer project records this folder as a broken reference, and a copy of the outer project comes out with the new work missing entirely, which is not something this user can repair. Skipping here is a deliberate choice, not a failure, so say nothing about it — but the cheat sheet must not promise what is not there, so its «Если что-то сломалось» step three is written per the note in `references/templates.md` for a project without its own history.

2. **Create the local history** — only when step 1 found this folder is not already inside another project, and unless the project root already contains a `.git` folder. In the project root, run:

   ```bash
   git init
   ```

   Only ever in the project folder chosen at `## Step 15` — never in a parent folder, and never in the user's home folder. `## Step 15` already guaranteed that folder is neither the home folder nor a folder full of the user's other things, so there is nothing to move and no path to rewrite here. Apart from the one case in step 1, never skip version control: skipping it hollows out the «верни, как было» promise the cheat sheet makes.

3. **Write `.gitignore`** in the project root — in both cases, whether or not this project got a history of its own; it is a file inside the project folder, and the outer project's own `.gitignore` is still never touched. This is the only place `.gitignore` is written. It must contain at least these lines, all of them, before the first commit:

   ```gitignore
   .claude/settings.local.json
   .DS_Store
   .env
   .env.*
   !.env.example
   *-service-account.json
   credentials.json
   ```

   **Why the secret lines are not optional, and why they go in before the first commit.** A secret that gets into the history of changes stays there for good: deleting the file in a later commit does not take it out of the earlier ones, and from that moment on the key has to be treated as given away. There is no tidying up afterwards. And this audience's projects do reach for keys — a project that goes to another system for its data needs a token to get in, and that token lives in `.env`. The lines cost nothing today and cannot be added late, so they go in now, before there is a single commit to be sorry about.

   **`.env.example`.** If the project uses `.env`, write an `.env.example` next to it with the same keys and empty values. That file is committed — the `!.env.example` line above is what lets it through — and it is the sample: it shows a later session, or the same person on another computer, exactly which values have to be filled in. Never put a real value in it.

   Add what the built base needs on top: `node_modules/` for Node.js; `.venv/` and `__pycache__/` for Python.

   **A local SQLite file is the user's data — never put it in `.gitignore`.** That is deliberate: the data then rolls back together with the code, and «верни, как было» gives the user back a working project with their numbers in it. When the store is PostgreSQL instead, the data lives outside the folder and this no longer holds — `### Data` says what is done about that.

4. **Make the first commit — the point of return.** Skipped entirely when step 1 found this folder inside another project.

   ```bash
   git add -A
   git commit -m "<message in the user's language, e.g. «Начало работы над проектом»>"
   ```

   The folder holds almost nothing at this moment — `.gitignore`, and the plan file if `## Saving the plan instead of building` in `SKILL.md` sent us here. That is the whole point: it is a clean state that is guaranteed to be intact, and everything after it can be undone back to here. `.gitignore` always exists by now, so this commit never has nothing to record.

   If the commit fails only because a name and an email are not configured, set them locally for this project folder with a neutral value and commit again. Do not ask the user for them.

5. **Then a commit after every state that works** — not one commit at the end. Each of these is skipped along with the rest when step 1 found this folder inside another project:

   - after `CLAUDE.md` and the cheat sheet have been written;
   - after the project itself has been built;
   - after the launch check in `## Launch and verify` has passed and the Step 16 list has been walked — this one also carries the fixes the reconciliation step made to the three written files.

   ```bash
   git add -A
   git commit -m "<one short line in the user's language, saying what now exists>"
   ```

   Each message is one plain line about what the project has now, in the user's language: «Памятка и шпаргалка», «Страница расходов работает». Never `git commit --amend`, never `git rebase`, never anything that rewrites what is already committed — an earlier point the user can return to is worth more than a tidy history.

6. **Say nothing about any of this — unless it was blocked.** Do not narrate it, do not list it in the final report, and never use the word «репозиторий» with the user — `## Tone rules` bans it. In the cheat sheet this shows up only as the fact that «Верни, как было до последних изменений» works — or, in the step-1 case, does not appear at all. The one exception is the blocked-action rule in `## Tone rules` of `SKILL.md`: if `git init`, `git add` or any of the commits is denied or refused, never quietly skip the step and carry on. Say in plain words that the history of changes was not saved and that «вернуть предыдущую версию не получится» — the cheat sheet promises it, and silence would leave that promise empty. That rule is about a denial only; the skip in step 1 is not one, and is never announced.

7. **Local only.** Never run `git push`, never add a remote, never mention GitHub, never ask whether the user wants to publish — including when Step 8 said the project will one day live on the internet. That is a separate piece of work for a later conversation, and Step 8 already told the user so. The `ask` rule on `Bash(git push:*)` in the permissions template is a guard rail, not an invitation to use it.

## Never add

Not in either shape, no matter how tempting or how standard it looks elsewhere:

- Git hooks of any kind.
- A documentation gate, or any rule that blocks work until a document is updated.
- A `docs/` tree, architecture decision records, or design documents. The project has `CLAUDE.md`, one cheat sheet, and nothing beyond what the interview actually produced: `design.md` when the user gave a long sample at Step 12, the plan file when Step 16 was answered «сохраните план файлом», `.env.example` when the project uses `.env`, and the seeding script when the store is PostgreSQL. Never a document written for its own sake.
- A methodology or process layer on top of the project.
- A monorepo, workspaces, or more than one dependency manifest.
- Separate data isolation per customer.
- Anything from the plans at Step 4. Those are written into `CLAUDE.md` and built in a later conversation, never today — see `## Now and later` in `SKILL.md`.

Anything the interview did not actually ask for is out of scope. When in doubt, build less — but never less than the person asked for. Something they described at Step 3 or showed at Step 12 is in scope, and dropping it is not simplicity, it is a project that does not do the job.
