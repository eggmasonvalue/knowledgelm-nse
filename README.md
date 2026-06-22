# knowledgelm-nse (skill repo)

Agent skill for downloading NSE company filings in batch, resolving industry to
symbol sets, and optionally integrating outputs with NotebookLM.

## What this repository is

- A skill repository (`SKILL.md` + `scripts/`), not a Python package.
- The behavior contract lives in `SKILL.md`.
- `scripts/fetch_industry_data.py` is a helper that refreshes/returns the local
  industry cache path using shared `industry_map_client`.

## Core usage

From an agent session that has this skill installed, follow `SKILL.md`.

Manual helper invocation example:

```bash
python scripts/fetch_industry_data.py
```

Success output:

```json
{"success": true, "cache_path": "<absolute_path_to_cache_json>"}
```

If the shared industry client is missing, install once:

```bash
pip install "industry-data-in @ git+https://github.com/eggmasonvalue/stock-industry-map-in.git@v0.1.0"
```

## Maintenance docs

- `AGENTS.md`
- `context/MAP.md`
- `context/DECISIONS.md`
- `context/CONVENTIONS.md`
