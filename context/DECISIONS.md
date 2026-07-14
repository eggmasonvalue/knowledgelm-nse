# DECISIONS

## 2026-07-14 - Reflect credit_rating .pdf/.html mix in skill docs

Context: `screener-scrape` changed `download_credit_ratings_from_screener` to save
HTML-only rating rationale sources (CRISIL static pages, India Ratings
JS-rendered pages) as cleaned `.html` instead of PDF-printing them; native
rating PDFs (ICRA, CARE) are unchanged.
Decision: Update SKILL.md to document that `credit_rating/` mixes `.pdf` and
`.html`, that the `.html` files are already LLM-ready, and that `convert dir`
safely skips them since it only globs `*.pdf`.
Tradeoff: None — this is a documentation change tracking the upstream
behavior change.
Status: active

## 2026-06-29 - Remove xbrl_announcements.json from skill docs

Context: KnowledgeLM removed the JSON table-of-contents file from XBRL
announcements output; only the ixbrl HTML downloads are the deliverable.
Decision: Update SKILL.md to stop referencing ``xbrl_announcements.json``.
Tradeoff: None — the JSON was unnecessary metadata duplication.
Status: active

## 2026-06-28 - Reflect unified XBRL announcements in skill docs

Context: KnowledgeLM unified its three XBRL categories (personnel,
key_announcements, shm) into a single ``xbrl_announcements`` dataset with
ixbrl HTML links instead of parsed XML.
Decision: Update SKILL.md to reference the single ``xbrl_announcements``
dataset and document the ixbrl HTML link as the primary content source.
Tradeoff: None — this is a documentation change tracking the upstream
simplification.
Status: active

## 2026-06-22 - Keep this repo as a thin consumer of shared industry-map client

Context: Multiple sibling repos needed the same NSE industry-map fetch/cache
logic, and local implementations were diverging.
Decision: Use shared `industry_map_client` from `industry-data-in` in
`scripts/fetch_industry_data.py` instead of maintaining a repo-local urllib/ETag
implementation.
Tradeoff: This repo now depends on an external package install step, but avoids
code duplication and keeps fetch/cache behavior consistent across skills.
Status: active

## 2026-06-22 - Degrade gracefully when shared client is missing

Context: Skill users may run the helper before installing the shared client.
Decision: Return machine-readable JSON failure with explicit one-time install
hint instead of raising traceback.
Tradeoff: Adds user setup guidance surface in error strings, but preserves the
skill's structured output contract and avoids brittle failure modes.
Status: active
