# DECISIONS

This is a curated ADR file for durable, non-obvious project-level choices. It is not a changelog or implementation worklog.

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
