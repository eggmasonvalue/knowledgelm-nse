# AGENTS

This repo is a **skill repo** (`SKILL.md` + `scripts/`), not a Python package.
`SKILL.md` is the runtime contract for assistant behavior.

## Hard guardrails

- Never commit directly to `main`.
- Always work on a branch and open a PR into `main`.
- Keep this repo as a thin skill wrapper; do not re-implement shared L3 client
  behavior in local scripts.
- Do not edit migration control docs outside this repo's scope unless explicitly
  asked.

## Read routing (read only what you need)

- Read `context/MAP.md` before changing structure, file layout, or data flow.
- Read `context/DECISIONS.md` before changing any established tradeoff.
- Read `context/CONVENTIONS.md` while writing or editing files.
- Read `SKILL.md` before changing user-facing workflow or command guidance.
- At task start, run `todo list`; before doing work, `todo claim <id>` when a
  matching todo exists.

## Write triggers (event-based)

- Module/script added, moved, removed, or data flow changed -> update
  `context/MAP.md`.
- Intentional tradeoff made -> append an entry to `context/DECISIONS.md`.
- New repeatable rule/pattern adopted -> update `context/CONVENTIONS.md`.
- User-facing behavior, setup, or usage changed -> update `README.md` and/or
  `SKILL.md`.

## Do not document

- Changelog/worklog content (use git history).
- Feature/status trackers that duplicate code or issues.
- Obvious code behavior that can be recovered quickly from source.
- "Decisions" with no real tradeoff.

## CONVENTIONS vs DECISIONS

- `CONVENTIONS.md`: imperative rules only, no rationale.
- `DECISIONS.md`: context, choice, and tradeoff.
- If a rule needs "because", move rationale to `DECISIONS.md`.

## Todos and decisions

- Todos are durable task state in `.pi/todos`, not scratch notes.
- Keep live implementation notes in todo bodies while work is active.
- Before closing a todo that contains a real tradeoff, copy the durable decision
  into `context/DECISIONS.md`.
- Closed/done todos are not long-term archives.

## Definition of done

A change is done only when code and matching durable docs are both updated:

- Structure/data-flow changes reflected in `MAP.md`.
- Tradeoffs reflected in `DECISIONS.md`.
- Repeatable rules reflected in `CONVENTIONS.md`.
- User-facing usage reflected in `README.md`/`SKILL.md`.
