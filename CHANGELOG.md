# Changelog

## 0.3.0

- Added `price_pilot/sources.py` and a new `price-pilot sources` command to expose deterministic platform source routing.
- Reframed the architecture around data ingestion, normalization, decision, and inquiry instead of treating the agent as the primary crawler.
- Updated the skill and README so platform coverage, fallback order, and recommendation boundaries are explained more honestly.

## 0.2.0

- Split discovery into platform capability routing instead of assuming every marketplace has a stable public search page.
- Added direct-link-first normalization for Xianyu and Pinduoduo.
- Added `top_recommendations` to workflow and decision outputs so higher value listing URLs are returned explicitly.
- Improved inquiry and skill guidance so platform failures are explained in plain language.

## 0.1.0

- Initialize `price_pilot` package layout inspired by Agent Reach.
- Add platform registry, doctor command, and ranking CLI.
- Bundle installable skill for China shopping comparison.
- Add GitHub review automation and validation workflow.
