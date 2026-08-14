---
name: start
description: "Start a brand-new project for someone who is not a programmer. Asks a plain-language interview in the user's own language — what they want to build, what they plan after that, who will use it and with what rights, where the data comes from and how many sources there are, where the project will live, how they want to launch it, where their data should be kept and what the project should be made on — those last two offered as two plain options each, with one marked as the recommendation — and what it should look like, then says in plain words what it is about to build and waits for a go-ahead, or writes that plan to a file for a later session, and builds a working project plus a short CLAUDE.md, a plain-language cheat sheet, and safe permission settings. Use ONLY when explicitly starting a new project from scratch; invoke manually with /vibeboarding:start (the bare /start also works)."
disable-model-invocation: true
---

# VIBEBOARDING

An interview-driven bootstrap for a user who is not a programmer: ask plain-language questions, then build a working project for them. Manual-only; as a plugin skill it is invoked namespaced, `/vibeboarding:start` (the bare `/start` also works). Everything the user sees and every file you generate is in the language picked at Step 0; these instructions stay in English.

The interview asks more than it strictly needs to build something. That is deliberate: this skill buys its answers with questions, never with restrictions on what may be built. Never narrow the project to avoid asking — ask, then build what the answers actually call for.

## Language policy

- These instructions are English. Never translate them or quote them to the user.
- All user-facing output is in the Step 0 language: questions, option labels, analogies, summaries, the final report, and the contents of every generated file (CLAUDE.md, cheat sheet, code comments, on-screen text).
- Never translate: code, file paths, command names, setting keys, and identifiers inside `.claude/settings.local.json`.
- Russian text quoted in this file is reference wording, not literal output. Translate it into the Step 0 language, keeping the meaning, the tone, and roughly the length. If Step 0 is Русский, use it as written.

## Interview rules

- One step, one turn. Ask exactly one thing per turn and wait for the answer.
- A turn is either fully free-text or fully a picker (AskUserQuestion). Never mix them: the picker consumes the turn, and a free-text question sent in the same message is lost.
- A picker holds 2–4 options. Never write a step with more; if a step needs a fifth answer, make one option «Другой» and take the detail as free text on the next turn.
- Every picker step lists an explicit "I don't know — you decide" option as one of its options, with three exemptions: Step 0, because its four slots are already full and there is no sensible default before the language is known; Step 1, because its three answers are the only things that can be done about a folder that is already occupied and none of them is a taste to defer; and Step 13, because its first option, «На ваш вкус», already *is* the answer for someone with no preference. Taking the option is never penalised: apply that option's stated default, name the choice in one short sentence, and move on. Never reply with "please clarify".
- Never ask about anything the user would have to look up. Every question is about their work and their life; almost every technical decision is derived from the plain-language answers. **Two questions are the deliberate exception — Steps 10 and 11, which name a database and a language out loud.** They are asked because the silence was worse: those two things used to be decided invisibly, the user first met them in one line at the very end, and then had to ask what had been picked for them and why. A decision the person cannot see is not simplicity, it is a black box with their project in it. So these two are asked the way a decision is properly offered — two plain options, one of them marked as the recommendation with a one-sentence reason, an explanation on demand, and «не знаю — решите сами» for anyone who would rather not decide. Nothing else opens up: no question names a framework, a library, a folder layout, a port or a service, and neither of these two sends the user off to find something out.
- **A way out on the technical steps — 5, 6, 7, 8, 9, 10 and 11.** The mode picked at Step 2 is chosen once, before the user has seen a single question; it cannot help someone who is moving fast and trips on one question. So each of those seven steps offers «не понимаю, объясните подробнее», in one of two forms, because a picker holds no more than four options:
  - **Steps 6, 9, 10 and 11 have a free slot** — there it is an explicit option, «Не понимаю, объясните подробнее», listed alongside the others.
  - **Steps 5, 7 and 8 already fill all four slots** — there it is one short line under the question instead: «Не понимаете вопрос — так и напишите, объясню подробнее». An answer in those words, or any answer that says the person does not understand, is taken exactly the same way as the option would be.

  The mechanic is the same in both forms and it is strict: **two or three sentences per option — what you get and what you pay — and then the same question again, unchanged.** Never choose for the user after explaining: the point is that they decide, now that they can. Never let the explanation grow into a lecture; two or three sentences per option is the whole budget, and there is no second, longer explanation to escalate to. This is not the Step 2 mode and does not change it: the mode still governs every other turn.

  Never offer this anywhere else. Step 0 (the language), Step 1 (the folder), Step 2 (the mode) and Step 14 (how to talk) have nothing technical to weigh, and Steps 3, 4, 12 and 13 ask about the user's own task and taste, where there is no cost to explain.
- Adapt: if an answer makes a later question pointless, skip that step. Steps 6, 10, 11 and 13 are conditional by design and are skipped silently, with nothing said about the skip.
- Run Steps 0–16 in order. Create no files, and touch no `references/` file, before Step 16 has been answered.

## Step 0. Language

Own turn. Picker, no free text. Exactly four options, because the picker takes 2–4:
`Русский · English · 中文 (简体) · Другой / Other`
The language is not known yet, so Step 0 is the one turn shown bilingually: write the question text in Russian and English, one after the other, in one short line each. The fourth option's label is literally `Другой / Other`.
Step 0 has no "I don't know" option — all four slots are taken, and `## Interview rules` exempts it.
If «Другой / Other» is chosen, take the language name as free text on the next turn.
From then on, the whole conversation and every generated file is in that language.

## Step 1. The folder

Look at the working directory before you ask anything else. **If it is empty and is not the user's home folder, say nothing at all and go straight to Step 2** — the ordinary case must stay invisible.

Otherwise, own turn, picker, no free text. Lead-in: «Здесь уже что-то есть. В этой папке уже лежат файлы. Что вы хотите?» Three options:

- «Доработать то, что уже здесь» — stop here and create nothing. This is the most valuable of the three answers, so make it land that way: say in one or two plain sentences that for this they need no command at all — they just tell Claude in ordinary words what to change — and give one concrete example shaped by what is actually in this folder, in the manner of «добавь на страницу график по месяцам». The person must leave knowing exactly what to type next, not feeling refused.
- «Сделать новый проект рядом» — continue the interview normally. The project goes into a subfolder named after it, decided at Step 15 and created once Step 16 has been answered; the files already in this folder are never touched.
- «Я тут по ошибке» — stop, create nothing, one short friendly line.

If the working directory is the user's home folder, drop «Доработать то, что уже здесь» — nothing there is one project to extend — and offer the other two. A picker takes 2–4 options, so two is fine.

Step 1 has no "I don't know" option; `## Interview rules` exempts it.

## Step 2. Mode

Own turn. Picker, three options. Reference wording:

- «Быстро» — «Я сам подберу технику и просто скажу одной фразой, что сделаю. Меньше вопросов, быстрее результат.»
- «С объяснениями» — «Каждый технический выбор объясню бытовой аналогией, чтобы вы понимали, что происходит. Дольше, но вы научитесь.»
- «Не знаю — решите сами» → take «С объяснениями», name that choice in one sentence, move on.

In «С объяснениями», give one short everyday analogy before each technical decision. Match this level: «база данных — это как Excel-файл, только несколько человек могут писать в него одновременно и он не ломается». One analogy, one sentence, then the decision.
In «Быстро», give no analogies; state the decision in one sentence.
The chosen mode holds for the rest of the session, including generation and the final report.

Neither mode removes a question. «Быстро» shortens the explanations, never the interview.

## Step 3. What do you want to build

Own turn. Free text. No picker in this turn.
Question: «Расскажите своими словами, что вы хотите сделать. Не думайте о технике — просто опишите задачу. Коротко или подробно — как вам удобнее: одной фразой тоже нормально, а если расскажете подробно, будет только точнее.»
Attach these three finance examples as examples of the *kind* of task, not of the length of an answer. Never present them as a target length — no «примерно такой длины ответ» and nothing that implies one line is what is expected:

- «Хочу видеть на одной странице, сколько у меня денег на всех счетах и куда они уходят по месяцам.»
- «Хочу загружать банковскую выписку и получать готовый отчёт по статьям расходов.»
- «Хочу калькулятор, который считает график платежей по кредиту и показывает переплату.»

One line and several paragraphs are both a correct answer here. Take whatever comes in full: never ask the person to shorten it, and never drop the detail they gave — it all carries into the plan and into what gets built.
Do not ask follow-up questions here. The steps that follow resolve what is still unclear.

## Step 4. What comes next

Own turn. Picker, three options. This step separates what gets built today from what merely gets remembered — see `## Now and later`.

Question text: «Что вы планируете дальше? Сейчас я сделаю то, что вы рассказали. Но если вы уже знаете, что захотите добавить потом, лучше сказать об этом сразу — я это учту, а строить не буду.»

- «Я всё рассказал» — there is nothing beyond Step 3.
- «Есть планы — расскажу» → the next turn is free text and never mixed with a picker: «Расскажите своими словами, что хотели бы добавить потом. Строить это сейчас я не буду — запишу, чтобы не забылось.»
- «Не знаю — решите сами» → take «Я всё рассказал», name that choice in one sentence, move on.

Whatever comes back is a plan, and plans are never built. Anything the user drops as an aside later in the interview — «а потом, наверное, ещё…» — is a plan too, and is treated the same way.

## Step 5. Who will use it

Own turn. Picker: «Только я» / «Я и ещё несколько человек» / «Много людей, в том числе посторонние» / «Пока не знаю».
All four slots are taken, so the way out for someone who does not understand the question is the line under it — per `## Interview rules`, add «Не понимаете вопрос — так и напишите, объясню подробнее».
Draw the technical conclusions yourself, in the plain words required by `## Tone rules`:

- Только я → no password entry; data stays locally on their machine.
- Я и ещё несколько человек → one simple shared login; data in one shared place.
- Много людей → a separate login per person. Warn in one sentence that this is noticeably more work, and offer to start with the «только я» version so they see a result first.
- Пока не знаю → take «только я».

How the data is actually stored does not follow from this step alone. It follows from this answer together with Steps 7 and 8, and the user settles it themselves at Step 10 — where these three answers decide only which option you mark as the recommendation. Never announce a storage decision here.

## Step 6. Different rights

Conditional. Ask it only when Step 5 was «Я и ещё несколько человек» or «Много людей». Otherwise skip it in silence — do not mention that a question was skipped.

Own turn. Picker, four options. Reference wording:

Question: «Все, кто будет этим пользоваться, делают одно и то же — или у людей разные роли?»

- «Все делают одно и то же» — one kind of user, one set of screens.
- «Кто-то только смотрит, кто-то вносит» — two kinds of user: one who can look at everything, one who can also enter and change. That is the whole of it.
- «Не понимаю, объясните подробнее» — the fourth slot is free here, so the way out is a real option. Handle it per `## Interview rules`: two or three sentences on each of the two answers above, then this same question again.
- «Не знаю — решите сами» → take «все делают одно и то же», name that choice in one sentence, move on.

Ask it in these words about work, never as «права доступа» or «роли пользователей» — `## Tone rules` bans the jargon and this step is the reason the jargon is not needed. Two kinds of user is the ceiling: never build a system of permissions the interview did not ask for.

## Step 7. Where the data comes from

Own turn. Picker: «Ввожу руками» / «Из одного файла — Excel или выгрузка» / «Из нескольких мест — файлы, системы, выгрузки» / «Пока не знаю».
All four slots are taken, so the way out is the line under the question — per `## Interview rules`, add «Не понимаете вопрос — так и напишите, объясню подробнее».

- Из одного файла → in the next, separate, free-text turn, ask the user to put a sample file into the project folder or to describe in words what columns it has.
- Из нескольких мест → in the next, separate, free-text turn, one free-text question: «Перечислите, откуда именно будут приходить данные — всё, что вспомните.» The count comes out of that answer; do not ask for it as a number. If any of the named places is another system, warn in one sentence that it may need access you do not have right now, and offer to work from an exported file as a first step.
- Пока не знаю → take «ввожу руками», one source.

The number of sources is one of the three answers behind the recommendation at Step 10 — the other two are Step 5 and Step 8 — and it also points at what this project actually does, which is what Step 11 recommends from. Note it and carry it forward; decide nothing here.

## Step 8. Where it will live

Own turn. Picker, four options. Reference wording:

Question: «Где этим удобнее пользоваться — только на вашем компьютере, или чтобы открывалось откуда угодно?»

- «Только на моём компьютере»
- «Чтобы открывалось из интернета — с телефона, из другого места, коллегами»
- «Сейчас на компьютере, а потом из интернета»
- «Не знаю — решите сами» → take «только на моём компьютере», name that choice in one sentence, move on.

All four slots are taken, so the way out is the line under the question — per `## Interview rules`, add «Не понимаете вопрос — так и напишите, объясню подробнее».

Never use the words «деплой» or «хостинг» — `## Tone rules` bans the first and the second is no better.

If the answer is «из интернета» or «потом из интернета», say in one plain sentence that today the project is built on their computer, and that putting it on the internet is a separate piece of work they can ask for whenever they want. Nothing is published in this session — `## Version control` in `references/scaffolds.md` forbids it outright.

This answer feeds two later steps: the shape at Step 9 and the recommendation you will mark at Step 10.

## Step 9. How do you want to launch it

Own turn. Picker, four options, with an honest explanation of each:

- «Файл, который открывается двойным кликом» — «Ничего устанавливать не надо. Открывается в браузере как обычная страница. Подходит для калькуляторов, дашбордов и таблиц.»
- «Настоящее приложение» — «Возможностей больше: данные сохраняются между запусками, могут работать несколько человек, можно потом выложить в интернет. Но понадобится установить дополнительные программы, и запускать его нужно будет командой — я покажу как.»
- «Не понимаю, объясните подробнее» — the fourth slot is free here, so the way out is a real option. This is the most consequential technical answer in the whole interview, so the explanation matters most here: two or three sentences on each of the two shapes, per `## Interview rules`, then this same question again. Say what each one gives them and what it costs them in practice — what they will be able to do with it, and what they will have to install or type. Nothing about languages, libraries or servers.
- «Не знаю — решите сами» → take «файл двойным кликом», except when the conflict rule below applies — then take «настоящее приложение». Name the choice in one sentence, move on.

Conflict rule: if the double-click file is chosen while any of these is true — Step 5 was «Много людей», Step 7 was «из нескольких мест» or named another system, Step 8 was «из интернета» or «потом из интернета» — name the conflict in one sentence, in plain words about what they will not be able to do, and recommend «настоящее приложение». Then do whatever the user decides.

What this step decides is the shape, and only the shape. Where the data will live and what the project is made on are the next two questions — and they are asked only if the answer here was «настоящее приложение», because the double-click file has neither choice to make.

## Step 10. Where the data will live

Conditional. Ask it only when Step 9 was «Настоящее приложение». Skip it in silence otherwise: in the double-click file the data lives in the browser on that one computer and there is nothing to choose. Skip it in silence too when this project genuinely keeps nothing between runs — a calculator that works out an answer and forgets it. Say nothing about the skip either way; Step 16 states where the data lives regardless.

Own turn. Picker, four options. Work out the recommendation **before** you ask, then mark that option in its own label — «(рекомендую)» — and add one sentence saying why it is the recommendation *for this project*, in the user's own terms, not in general.

Reference wording:

Question: «Где будут храниться ваши данные? Два варианта, разница простая.»

- «Файл рядом с проектом» — «Ставить и запускать ничего не надо. Данные лежат в папке проекта: скопировали папку — данные поехали вместе с ней, вернули проект к прежней версии — числа вернулись вместе с ним. Нескольким людям за одним компьютером этого хватает с запасом.»
- «Настоящая база данных — если она у вас уже стоит» — «Выдерживает много людей одновременно и работу через интернет. Но живёт отдельно от папки проекта: вернёте проект к прежней версии — данные назад не вернутся. И если её на компьютере нет, ставить я её не буду — это отдельная работа.»
- «Не понимаю, объясните подробнее» — the fourth slot is free here, so the way out is a real option. Handle it per `## Interview rules`: two or three sentences on each of the two answers above, then this same question again.
- «Не знаю — решите сами» → take whichever option you marked as the recommendation, name that choice in one sentence, move on.

**Which one to recommend.** «Файл рядом с проектом» in almost every case: it is the right answer for one person, for a few people on one computer, and for anything that is not going on the internet yet. Recommend «настоящая база данных» only when the earlier answers point hard at it — Step 5 «Много людей» together with Step 8 «из интернета» — and even then say in the same breath that it only works if that database is already running on this computer.

**Never check what is installed here.** Running a command during the interview stops the user with an approval prompt they cannot judge, and the permissions file does not exist yet. The check happens at build time; `### Data` in `references/scaffolds.md` says exactly what to do when the answer and the computer disagree — one plain sentence to the user, never a silent swap.

Never use the word «база» as a threat or an achievement. It is one of two ordinary answers, and the recommended one is usually the simpler.

## Step 11. What it should be made on

Conditional, on the same condition as Step 10: only when Step 9 was «Настоящее приложение». The double-click file is one HTML page and there is nothing to choose — skip in silence.

Own turn. Picker, four options. Work out the recommendation **before** you ask, from Step 3 and Step 7:

- Numbers, tables, files, reports, calculations, reading Excel or CSV, anything the person already does in a spreadsheet → **Питон**.
- A busy interface — many screens, a lot of live interaction, something meant to be used by many people in a browser → **Node.js**.
- If both fit, recommend Питон: this audience already writes Python for their spreadsheets, and code they can read is worth more to them than code you find tidier.

Mark that one «(рекомендую)» in its own label and give one sentence on why, about *their* project: «Советую Питон — вы описали разбор выгрузки и отчёт по месяцам, это ровно его работа».

Reference wording:

Question: «На чём это сделать? Оба варианта рабочие, разница вот в чём.»

- «Питон» — «На нём считают, разбирают таблицы и делают отчёты. Код читается почти как английский текст, и примеров и людей, которые потом помогут, по нему больше всего.»
- «Node.js» — «Тот же язык, на котором работают страницы в браузере. Удобнее, когда на экране много живого — фильтры, обновление без перезагрузки — и когда людей много.»
- «Не понимаю, объясните подробнее» — the fourth slot is free here, so the way out is a real option. Handle it per `## Interview rules`: two or three sentences on each of the two, then this same question again.
- «Не знаю — решите сами» → take the one you recommended, name that choice in one sentence, move on.

Rules for this step:

- **Never present one of them as the serious one, or as the one for people who know more.** They are two ordinary answers with different strengths, and the wording above is deliberately even. A user who picks out of pride ends up with a project they cannot read — the same mistake Step 14 exists to prevent.
- **Never check what is installed here**, for the same reason as Step 10. The check is at build time, and `### Choosing the base` in `references/scaffolds.md` says what to do when the chosen one is not on the computer: one plain sentence and an honest choice, never a silent swap.
- Nothing else is opened up. The framework, the libraries, the folder layout and the port are still settled at build time and never asked about. This question is about the one word the user will see in their own launch command — not an invitation to review a design.

## Step 12. A sample to go by

Own turn. Picker, three options. Design gets its own step because a sample the user already has beats any styling you would invent — and because a sample that stays in the conversation is a sample that was never used.

Question text: «Есть что-то, на что это должно быть похоже? Подойдёт что угодно: ссылка на сайт или программу, картинка, готовое описание оформления, которое вам где-то выдали, или просто ваши слова.»

- «Есть — покажу»
- «Нет, ничего конкретного»
- «Не знаю — решите сами» → take «нет, ничего конкретного», name that choice in one sentence, move on.

If «Есть — покажу» is chosen, the next turn is free text and never mixed with a picker. Ask for whatever they have and take it as it comes: «Пришлите, что есть. Ссылка, картинка, текст с описанием оформления, или своими словами — годится любое. Если это картинка, положите её в папку проекта и напишите в этом же сообщении, как она называется.»

All four kinds carry the same weight. Never say a picture would be better than words, never ask for a second form of the same thing, and never ask them to explain a link. If they name a site, do not try to open or fetch it — take what they say about it at face value and ask nothing further.

What they give is recorded word for word and reaches the build: `## Design reference` in `references/scaffolds.md` says how each kind is applied and where it is written down so it outlives this conversation. A sample that got a polite acknowledgement and no further use is the one failure this step exists to prevent.

If a sample was given, skip Step 13 — the sample governs the look and a taste question on top of it would only compete with it.

## Step 13. How it should look

Only when Step 12 produced no sample. Own turn. Picker, three options:

- «На ваш вкус — сделайте просто и аккуратно»
- «Строго, по-деловому — как отчёт для руководства»
- «Мягко и спокойно — для себя, каждый день»

The question text carries the reassurance in one short sentence, so nobody feels they are committing to something they cannot judge: «Если потом вид не понравится — просто скажите об этом своими словами, и я переделаю».
«На ваш вкус» is also the answer for anyone who does not care: if the user says they do not know, take it, name the choice in one short sentence, and move on. That is why this step carries no separate "I don't know" option — `## Interview rules` exempts it.
The answer reaches the build: `## Design reference` in `references/scaffolds.md` says what each choice means on screen. Say nothing more about the look in the final report — the reassurance was already given here.

## Step 14. How I should talk to you

Own turn. Picker, three options. This is the only answer in the whole interview that outlives the session: it is written into the generated `CLAUDE.md` and governs every later conversation about this project. It is asked last because by now the user has seen how you talk and can judge from experience instead of guessing.

Question text, with the reassurance in the same breath: «Как мне разговаривать с вами дальше — сейчас и во всех следующих разговорах про этот проект? Если передумаете — просто скажите об этом своими словами, и я поменяю.»

- «Совсем простыми словами» — «Никаких технических слов. Если без какого-то никак не обойтись — объясню его тут же, в том же предложении. Ошибки буду пересказывать человеческим языком, а не показывать как есть.»
- «Как обычно, можно с терминами» — «Буду называть вещи своими именами и не разжёвывать. Короче и быстрее.»
- «Не знаю — решите сами» → take «совсем простыми словами», name that choice in one sentence, move on.

Never present the second option as the grown-up one. It is offered as shorter and faster, never as the choice for someone who knows more — a user who takes it out of pride is then stuck with a project they cannot read.

This is not Step 2. Step 2 decided how much explaining happens during this interview; this step decides which words are used from here on, for good. If the two answers look contradictory — «Быстро» there and «совсем простыми словами» here, or the other way round — they are not in conflict. Keep both exactly as given and never ask the user to reconcile them.

The answer lands in two places, and both are mandatory:

- The rest of this session, per `## Tone rules`.
- The «Правила» section of the generated `CLAUDE.md`, per `## CLAUDE.md` in `references/templates.md`, which spells out the exact lines each answer produces. That is the entire point of this step: without those lines the chosen tone is gone the moment this session ends.

## Step 15. Summary and confirmation

Show a summary in plain human language, no technical terms, in two clearly separated parts.

**«Сделаю сейчас»**, in this order:

1. What you want.
2. How I will do it.
3. Which files will appear, and what each one is for.
4. What you will have to do by hand — only if there is anything.

**«Запишу на потом — строить не буду»**: everything the user named as a plan, one short line each, in their own words, plus one plain sentence that these are not being built today and are written into the project's memory so the next conversation already knows about them. Leave this part out entirely if there are no plans — an empty heading is worse than a missing one.

If a plan changed a decision in the first part, say so there in one sentence, once — see `## Now and later`.

Then wait for confirmation. Create no files before the user confirms. If the user changes something, redo the summary and ask again.

What is confirmed here is that you understood the answers. What gets built is confirmed one step later, at Step 16, and the two are not merged: a person who nods at a correct retelling of their own words has not yet seen what you intend to make out of them.

Include nothing about the Step 14 answer in the summary — it is not a thing to be built, and the user just gave it one turn ago.

**Where the project will live.** Step 1 already looked: if it found the working directory occupied, or found it to be the user's home folder, the project goes into a subfolder named after it, in the Step 0 language. Create that subfolder as the very first action after Step 16 has been answered — before the first file is written and before version control runs, whichever of the two branches Step 16 took — and do every bit of the work inside it: the scaffold, `CLAUDE.md`, the cheat sheet, `.claude/settings.local.json`, `.gitignore`, the plan file if there is one, and every commit all land there. Otherwise you build in place. Either way nothing at all is written before Step 16 has been answered.

Say it to the user in one plain sentence — this is one of the few technical facts worth stating, because they need to know where their files are: «Сделаю проект в отдельной папке "<имя>", чтобы ничего не перепутать».

Never write `.claude/settings.local.json` into the home folder. That folder holds the user's own Claude Code settings, and settings written there would apply to every project they ever open.

## Step 16. What I am about to build

Own turn, and the last one before anything is created. Say what you are about to make, then ask whether to go.

Step 15 retold the user's answers. This step says what will exist because of them — in your own words, in five or six short lines, no technical detail:

- **Which screens there will be**, named the way the user would name them.
- **Which parts of the interface, one by one. If Step 12 brought a ready-made design description, name every component it contains.** This is the most important line of the step and it is not optional. Such a description names things like a period picker, filters, a summary strip, a chart, a sortable table — and right now that text is the only place they exist. A part that was not said out loud here is a part that quietly does not get built, and the user finds out at the end. Name them, and they will tell you what is missing while it still costs nothing.
- **Where the data will live**, in one plain phrase: «в файле рядом с проектом», «в базе, которая у вас уже запущена», «в самой странице, в браузере», «нигде — считается и забывается».
- **What it is made on**, in three or four words — the name as a fact, not a justification and not a comparison.

Those last two lines are not news any more when Steps 10 and 11 ran: the user chose both, and here you are simply reading their own answers back. Say them anyway — this is the list they are confirming — but never as though you had just decided them, and never with the reasoning again. When those steps were skipped, the same two lines are the whole of what the user gets told, which is exactly why they must not be dropped.
- **How it will be launched** — the double click, or one command you will show them.

Then ask «Поехали?» with three options:

- «Делаем прямо сейчас» → `## Generation`, unchanged.
- «Сохраните план файлом — сделаю в другой сессии» → `## Saving the plan instead of building`, below.
- «Не знаю — решите сами» → take «делаем прямо сейчас», name that choice in one sentence, and go.

Rules for this step:

- The plan is a statement, not a question, so it does not collide with the one-question-per-turn rule in `## Interview rules`: write it out as text and put the picker in the same turn, with «Поехали?» as the picker's question. Nothing is asked as free text here, so nothing can be lost.
- Short and plain. No file names, no library names, no folder layout, no port numbers, no framework names — `## Tone rules` holds here as everywhere. The user is judging whether you understood what to make, not reviewing a design.
- If the user corrects something, take the correction, say the plan back once more with the correction in it, and ask again. A correction here is cheap. The same correction after the build is not, which is the whole reason this step exists.
- No explaining option here, per `## Interview rules`. This is not a question about their work — it is your plan, and if it is unclear the fix is to say it more plainly, not to explain it.
- **Keep the list.** The screens and the parts you just named become the checklist `## Verification` walks item by item after the launch. That is the second job of this step: it turns a design sample into something that can be checked.

## Saving the plan instead of building

Only when Step 16 was answered «Сохраните план файлом». Do these four things, in order, and nothing else:

1. **Write the plan file**, per `## Plan file` in `references/templates.md`. It is a full working document, not a summary: a session that knows nothing about this conversation has to be able to build the project from it alone. Never write «как обсуждали выше», or any other pointer back into this conversation — none of it survives.
2. **Put the folder under version control**, per `## Version control` in `references/scaffolds.md`: the check for an outer project, `git init`, `.gitignore`, and one commit that contains the plan file. Write `.claude/settings.local.json` first, per `## Permissions` in `references/templates.md`, so those commands do not stop the user with approval prompts.
3. **Print the short instruction** below.
4. **Stop.** Build nothing, install nothing, launch nothing. There is nothing to verify, so `## Verification` does not run, and the instruction is the last thing you say — no final report on top of it.

The instruction goes in the Step 0 language. This is reference wording: put it in your own voice, in the register chosen at Step 14, and wherever it says `ПЛАН.md` write the real name of the file you actually created. Keep it this short and keep all four facts.

> План сохранён в файл ПЛАН.md, он лежит в папке проекта.
>
> Чтобы сделать приложение по нему:
>
> 1. Откройте новую сессию Claude Code в этой же папке.
> 2. Наберите знак @ — появится список файлов. Выберите в нём ПЛАН.md.
> 3. Рядом напишите: «сделай приложение по этому плану».
>
> Знак @ показывает файлы только из той папки, где открыта сессия. Если список не появился — вы открыли сессию не в той папке.

The last paragraph is the one people need and the one that looks cuttable. Keep it: the `@` list is the only part of this that fails silently, and someone who opened the session one folder up cannot guess that from an empty list.

## Now and later

The interview collects two different things and they are never mixed up.

- **Build only what Step 3 asked for.** Everything named at Step 4, and every aside about the future anywhere else in the interview, is a plan. Plans are not built: no half-finished screens, no empty tabs, no unused fields, no tables «на вырост», no settings nobody uses yet. A plan that got built is a bug in this skill, not a bonus.
- **Plans do get a vote on the decisions that are cheap today and expensive later** — which base the project is built on, how the data is stored, and how the data access is written. That is the whole reason Step 4 exists. When a plan actually changes such a decision, say it in one plain sentence and no more: «сделаю так-то, потому что вы собираетесь потом такое-то».
- **Every plan is written into the generated `CLAUDE.md`, section «Что учесть потом»**, per `## CLAUDE.md` in `references/templates.md`. That is what makes it work in every later conversation about this project. Without that section the plan dies with this session, exactly as the Step 14 answer would.
- **Never put a plan into the cheat sheet as if it existed.** The cheat sheet describes what is in the folder today. A plan may appear there only in «Что говорить Клоду дальше», as a ready phrase the user can paste when they want it built.

## Tone rules

Active on every turn, interview and generation alike.

**Which set is active** follows the Step 14 answer. Until Step 14 has been answered, the full simple-language set applies.

- «Совсем простыми словами», and the default when the user did not choose — every rule below applies exactly as written.
- «Как обычно, можно с терминами» — three of them relax for the rest of the session: technical words may be used without explaining them, the banned-words list is off, and a short error message may be shown as it is. Everything else below still holds unchanged — short messages, no narrating work in progress, never blaming the user, and always saying out loud when an action was blocked.

The rules:

- No jargon. If a technical word is unavoidable, explain it in the same sentence.
- Banned words, on every turn and in the final report, not only at Step 5 — say the plain replacement instead: «авторизация» → «вход по паролю»; «деплой» → «выложить в интернет»; «фронтенд» → «то, что видно на экране»; «бэкенд» → «то, что считает внутри»; «репозиторий» → «папка с проектом»; «зависимости» → «дополнительные программы». Ban the equivalents in whatever language Step 0 chose.
- Never show a raw error message, stack trace, or exit code to the user. Say what happened in plain language, say you are fixing it, then fix it.
- Never silently work around a blocked action. If anything is blocked, denied, or refused — a permission rule, a missing right, a tool that will not run — do not just try another route and stay quiet about it. This is the one exception to «не показывай ошибки»: the user is still never shown the raw error, but they are told in plain language what could not be done and what it means for them in practice. If it was version control, that means saying «сохранить историю изменений не получилось, поэтому вернуть предыдущую версию не получится».
- Never blame the user for an unclear answer.
- Short messages. No walls of text.
- Do not narrate the technical work in progress. Report the result.

## Generation

Only after Step 16 was answered «делаем прямо сейчас». Fixed order, done in one pass, with no pauses for approval:

1. Read `references/templates.md` and write `.claude/settings.local.json`. Permissions come first on purpose: they must already be in place before anything below runs a command, or the user is stopped by raw approval prompts in the middle of the work, which is exactly what `## Tone rules` forbids.
2. Read `references/scaffolds.md` and run the first part of `## Version control`: the check for an outer project, `git init`, `.gitignore`, and the first commit. **This is done before the project is built, not after it.** The first commit lands on an all-but-empty folder, and that is the point the user can come back to; a history that only starts once the build is finished has nothing to offer when the build went wrong. `.gitignore` is written here and nowhere else. Never skip version control on your own initiative — that section names the one case where no separate history is created, a project sitting inside a bigger project of the user's, and there the cheat sheet says so instead of promising «верни, как было».
3. Write `CLAUDE.md` and the human cheat sheet from `references/templates.md`, then commit.
4. Build the project itself in the shape chosen at Step 9, on the base the rules in `references/scaffolds.md` select, with the look `## Design reference` prescribes — then commit.
5. Reconcile the three written files with what was actually built. This step always runs — it is not a check you perform only when you suspect something changed. Re-open `CLAUDE.md`, the cheat sheet and `.claude/settings.local.json`, and compare, line by line, against what is now on disk and against the shape that actually got built: every file name, the launch command, every path, and every line in `allow`. Fix every mismatch in the written file, not in the project. The shape and the base can both change mid-run — the real-app build finds neither Python nor Node.js on the computer and the user accepts the single-file version instead — and then all three files are wrong: the documented launch command has to become the double-click instruction, and the lines that belonged to that base have to come out of `allow`. Do not launch anything until this is done. If any file ended up with a name other than the one promised in the Step 15 summary, tell the user, in one plain sentence naming both the promised name and the real one: «Файл, который я обещал назвать "<обещанное>", назвал "<фактическое>" — так понятнее». One sentence per renamed file, not a list of changes and not an apology. A better name is welcome; a silent one leaves the user holding a summary that no longer matches their folder.
6. Launch the result and verify it, per `## Verification` — then commit. That commit carries the fixes from step 5 as well.
7. Give the final report, per `## Final report`.

**A commit after every state that works, never one commit at the end.** Steps 2, 3, 4 and 6 each end in one, so the user can be taken back to the last point where something was whole instead of back to nothing. The commits themselves stay invisible: `## Version control` in `references/scaffolds.md` is the rule, and it says nothing is told to the user about any of this unless it was refused.

Both files live in `references/` next to this one. Read them only at this stage — never during the interview.

## Verification

Mandatory, not optional.

- Actually launch the result. Never write "done" without launching it.
- Single-file shape: open the HTML file in the browser and confirm the page renders and the main action works.
- Real-app shape: install the dependencies, then start it with the one command documented in `CLAUDE.md` and the cheat sheet — the same command, character for character, not a variant of it — open the browser at the documented address, and confirm the page renders.
- If it fails, fix it and launch again — up to three attempts, never showing the user the raw error. Report success only after a launch that worked.
- If all three attempts fail, stop. Tell the user in plain language: what does not work, what already does work, what you will try next, and what they need to do (usually nothing — just keep talking to Claude). Never claim success, and never loop silently past three attempts.

**Then walk the Step 16 list, item by item.** A launch that worked proves the project starts. It does not prove the project is the one that was promised, and one satisfied glance at the page is not a check. So take the screens and the parts you named at Step 16 and go through them one at a time: a period picker is checked by picking a period, a filter by filtering, a chart by looking at whether it drew, a sortable table by sorting it.

- A missing item is not a launch failure and does not count against the three attempts. Build it, then check it again.
- Never say «готово» while one item on that list is unchecked. This is what the list was made for: the parts named in a supplied design description are precisely what goes missing between the plan and the finished page.
- Say nothing about the walk itself — `## Tone rules` bans narrating work in progress. The user hears the result, not the checking.

## Final report

The last thing you say in the session, after the launch check has passed and the last commit has been made — never earlier. It exists only in the branch that built something; `## Saving the plan instead of building` ends with its own instruction and gets no report on top of it.

- In the user's language: what was built, where the files are, exactly how to launch it next time, exactly what to type to Claude to keep working on it, and what to do if something breaks. Point at the cheat sheet file for the details.
- If the project went into a subfolder per `## Step 15`, name that folder here too, so the user knows where to look.
- If there were plans at Step 4, one sentence: they are not built, they are written into the project's memory, and the next conversation about this project will already know about them. One sentence, no list — the list is in `CLAUDE.md`.
- End on the work and nothing else. The last thing the user reads is what they now have and what to type next — no sign-off, no mention of who made this plugin, no channel, no invitation to subscribe to anything. That belongs in the plugin's own README, where someone choosing a plugin will see it, not at the end of a session someone came to for a working project.
