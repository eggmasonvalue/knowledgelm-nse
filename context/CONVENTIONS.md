# CONVENTIONS

- Treat `SKILL.md` as the primary runtime contract for agent behavior.
- Keep `scripts/fetch_industry_data.py` as a thin wrapper around
  `industry_map_client`; do not duplicate shared L3 fetch logic locally.
- Preserve structured JSON stdout contracts for helper scripts.
- Keep install/setup hints pinned to released tags, not floating HEAD.
- Run Markdown lint before submitting docs changes:
  `npx --yes markdownlint-cli2`.
- Keep lines and sections concise; prefer lists over narrative in maintenance
  docs.
