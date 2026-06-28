---
name: knowledgelm-nse
description: >
  Batch download Indian company filings (transcripts, investor presentations,
  credit ratings, annual reports, share issuance documents, XBRL announcements
  with ixbrl HTML links) from NSE and valuepickr threads.
  Supports resolving industries to stock lists (e.g., getting all cement stocks).
  Convert downloaded PDFs to LLM-ready Markdown. Optionally add to NotebookLM.
  Use when user asks to: (1) Download investor materials for Indian publicly
  listed companies or entire industries (e.g. "cement stocks", "sugar industry"),
  (2) Research Indian stocks/companies, (3) Create research notebooks with
  company filings, or (4) Analyze NSE-listed company documents.
metadata:
  author: eggmasonvalue
  version: 5.2.0
  homepage: https://github.com/eggmasonvalue/knowledgelm-nse
---

# KnowledgeLM NSE

Batch download Indian company filings from NSE, convert PDFs to Markdown, and optionally integrate with NotebookLM.

Maintenance docs for this repo live in `AGENTS.md` and `context/`.
`SKILL.md` remains the runtime contract for agent behavior.

## Installation

Check if installed: `knowledgelm --version`
If not: `uv tool install knowledgelm`
To upgrade: `uv tool upgrade knowledgelm`

## Skill Upgrade

To keep this skill up-to-date, run:
```bash
npx skills update
```

## Command Discovery

**Use `--help` extensively to discover options and to determine the next steps**

```bash
knowledgelm --help
knowledgelm fetch nse --help
```

## CLI Contract

All commands output **strictly formatted JSON** to stdout. Logs, progress bars, and warnings are routed to `knowledgelm.log` to preserve the context window.

```
Success: {"success": true, ...data...}
Failure: {"success": false, "error": "<reason>"}
```

## Core Workflow

### 1. Gather Required Information

**NSE Symbol:** If not provided, use `web_search` to find it.

**Industry-based / Sector-based Queries:**
If the user asks for filings, research, or notebooks for stocks belonging to an industry or sector (e.g., "all cement stocks", "sugar industry", "consumer discretionary stocks"):
- Do NOT search for individual symbols one-by-one online.
- Do NOT assume a simple keyword query is always sufficient. For broad or hierarchical queries (e.g. "Consumer Discretionary"), the user might want a specific subcategory or sector.
- Ensure the local cache is updated and obtain its path by running the bundled helper script `scripts/fetch_industry_data.py` (located in this skill's folder, find the path from the system prompt):
  ```bash
  python <path_to_skill>/scripts/fetch_industry_data.py
  ```
  This returns a JSON with the cached path, e.g., `{"success": true, "cache_path": "<absolute_path_to_cache_json>"}`.
  > One-time setup: the helper uses the shared industry-map client. If it reports `industry_map_client not installed`, run:
  > `pip install "industry-data-in @ git+https://github.com/eggmasonvalue/stock-industry-map-in.git"`
- The JSON schema is optimized as a fields-values matrix for efficient filtering and aggregation. Example structure:
  ```json
  {
    "metadata": ["Macro", "Sector", "Industry", "Basic Industry"],
    "data": {
      "ABB": ["Industrials", "Capital Goods", "Electrical Equipment", "Heavy Electrical Equipment"],
      "BAJAJHIND": ["Fast Moving Consumer Goods", "Fast Moving Consumer Goods", "Agricultural Food & other Products", "Sugar"]
    }
  }
  ```
- Write a custom script on the fly to load, filter, or aggregate the JSON:
  - For precise targets (e.g., "cement"), filter symbols where any of the 4 levels match the term case-insensitively.
  - For broad categories (e.g., "Consumer Discretionary" macro), write a script to extract and list the sub-sectors, industries, or stock counts. Present the hierarchy to the user to clarify their intent (e.g., "Consumer Discretionary has subcategories like Textiles (50 stocks) and Auto Components (40 stocks). Do you want all of them, or a specific subcategory?").
- Once the list of symbols is finalized/resolved, batch download their filings using `knowledgelm fetch nse <SYMBOL>`.

**Date Range:** If not provided, ask for clarification. Accept various formats:
- Explicit: `"2023-01-01 to 2025-01-26"`, `"2023 to 2025"`, `"from 2023"`
- Relative: `"last 2 years"`
- Milestones: `"Since IPO"`, `"since <event>"` (use `web_search` to resolve dates)

Convert to `YYYY-MM-DD` for CLI.

**Datasets:** Default to all datasets if not specified. Uses `--annual-reports-all` by default.

Run `knowledgelm list-datasets` to get the full list of valid dataset keys. 

**Share Issuance Documents note:** Use `issue_documents` when the user asks about docs related to events involving issuance of shares: IPO prospectus, rights issues, QIP placements, information memoranda, or scheme of arrangement documents.

**XBRL Announcements note:** Output goes to ``xbrl_announcements/``:
- ``html/`` — downloaded ixbrl HTML files (one per filing, named by date + type + appId)
- ``xbrl_announcements.json`` — table of contents with metadata and ``local_ixbrl_path``
  pointing to each downloaded HTML. No XML parsing; the ixbrl HTML is the primary
  content source — stable, always available, and LLM-friendly.

### 2. Fetch Filings

Use `knowledgelm fetch nse` with appropriate flags. 

```bash
# Fetch all standard categories
knowledgelm fetch nse HDFCBANK --start 2024-01-01 --end 2025-01-26

# Fetch specific datasets
knowledgelm fetch nse HDFCBANK --start 2024-01-01 --end 2025-01-26 --datasets transcripts,annual_reports
```
The CLI's return .json provides useful metadata about the results.

## NotebookLM Integration

**The below is a comprehensive CLI for Google NotebookLM - offers full programmatic access to NotebookLM's features from the command line**

Follow this if the user wants to create a notebook

### 1. Ensure Latest Package Version

Check if installed and upgrade to latest:

```bash
notebooklm --version
```

If not installed:
```bash
uv tool install notebooklm-py
```

If installed, upgrade to latest:
```bash
uv tool upgrade notebooklm-py
```

**Browser extras (for first-time setup):** 
Do not use this unless you run into issues running any of the `notebooklm` commands.
If user hasn't authenticated with NotebookLM before, they need browser login support:

```bash
uv tool install "notebooklm-py[browser]"
playwright install chromium
```

### 2. Create Notebook

**Use `--help` extensively to discover options and to determine the next steps**

```bash
notebooklm --help
notebooklm source add --help
```

Use the notebooklm CLI to create a **new** notebook and add all downloaded files(.pdf, .md, .json) to that notebook (exclude `.pkl` files).


## Follow-up/CTA
Contextually come up with a call-to-action to help the user benefit from the below add-on features/unused core features.

### Highly likely add-on — ValuePickr forum as a source

- Use `web_search` to find the company's thread URL on `forum.valuepickr.com`.
- Run `knowledgelm fetch vp <URL> --symbol <SYMBOL>`. Files saved to `./{SYMBOL}_sources/forum_valuepickr/`.
- **Artifacts:** 1. thread PDF  2. popular links in the thread in a `.md`
- **Note**:
  - This is a forum thread and may not fit as an upload to NotebookLM as a source of truth.
  - The output is well-formatted to be vastly more distraction-free and print-friendly compared to the site.

  Make the user understand both and offer it as just a download for the user to read manually or as a potential source.

```bash
knowledgelm fetch vp "https://forum.valuepickr.com/t/nrb-bearings-ev-and-exports-to-drive-growth/106674" --symbol NRBBEARING
```

### Optional add-on — Audio Overview Generation

The [notebooklm_audio_prompt](.\references\notebooklm_audio_prompt.md) can be used to generate a fundamental deep-dive of the company in audio format by passing it as an argument to the corresponding `notebooklm` command. 

### On-demand add-on — Markdown conversion of .pdfs

The `convert` command converts downloaded PDFs to LLM-ready Markdown using `markitdown`.

**Important:** Conversion is deliberately separate from `fetch` because it can take **over 2 minutes per file** for large documents (e.g., annual reports). 

Use when a user wants to analyze an individual source/small subset without using notebookLM/as a fallback for when notebooklm faces persistent issues. Explicitly warn the user regarding the tradeoff beforehand.


```bash
# Convert a single PDF
knowledgelm convert file "./HDFCBANK_sources/transcripts/2024-10-19_Transcript.pdf"

# Bulk convert all PDFs in a directory
knowledgelm convert dir "./HDFCBANK_sources/transcripts/"
```

## Exception Handling

- **Invalid symbol:** CLI returns `"success": false` in JSON
- **Network issues:** Retry once after 5 seconds
- **Incomplete data:** May indicate newly listed company on the NSE mainboard or corporate action. Use `web_search` to verify.
