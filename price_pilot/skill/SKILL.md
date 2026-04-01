---
name: cn-shopping-compare
description: Comprehensive China e-commerce comparison skill for JD, Taobao, Pinduoduo, Xianyu, and Zhuanzhuan. Use when Codex, OpenClaw, or another agent needs to find products across major Chinese shopping platforms, compare current prices, evaluate reviews and seller quality, identify risk signals, summarize tradeoffs, or rank options by overall value for money for new or used goods.
---

# CN Shopping Compare

## Overview

Use this skill to turn a shopping request into a structured, cross-platform recommendation. Search live listings, normalize the evidence, score the options, and explain why the top choice wins.

## Workflow

### 1. Clarify the target

Extract the decision constraints before searching:

- product name and generation
- model or configuration
- new or used preference
- budget cap or target price band
- platform preference or exclusions
- risk tolerance
- must-have details such as color, storage, edition, invoice, warranty, shipping origin

Ask a follow-up only when the missing detail would materially change the recommendation. Otherwise proceed with reasonable defaults and state them.

### 2. Search each platform with live data

Use current web data for all time-sensitive facts. Do not rely on stale memory for prices, ratings, or availability.

If direct browsing is blocked, prefer these escalation paths in order:

1. Use a configured marketplace MCP server when available.
2. Use a configured local cookie export for the platform.
3. Ask the user for direct listing links or screenshots instead of stopping at "access denied".

Search these platforms unless the user narrows the scope:

- JD
- Taobao
- Pinduoduo
- Xianyu
- Zhuanzhuan

Read [platform-playbook.md](./references/platform-playbook.md) before searching.

### 3. Normalize candidate listings

Prefer 2 to 5 strong candidates per platform instead of dumping raw search noise.

Capture these fields whenever available:

- platform
- title
- current price
- landed price including shipping or coupons when visible
- condition
- store or seller type
- rating, review count, sales volume, or transaction count
- return policy and warranty
- authenticity or inspection signals
- advantages
- red flags
- listing URL

### 4. Evaluate evidence quality

Treat evidence quality as part of the recommendation:

- prefer complete specs, clear photos, detailed disclosures, and realistic review density
- penalize suspiciously low price, vague descriptions, mismatched specs, or repeated complaints
- for used marketplaces, treat seller credibility and inspection options as first-class inputs

Read [ranking-rubric.md](./references/ranking-rubric.md) before scoring.

### 5. Score and rank

Use `scripts/score_products.py` when the candidate set is large enough to benefit from consistent scoring.

```bash
python3 scripts/score_products.py --input candidates.json
```

Use the result as a structured aid, not as a blind final answer.

### 6. Return a decision-oriented answer

Always answer in a way that helps the user buy or reject:

- lead with the best overall option
- call out the best budget option if it differs
- call out the safest option if it differs
- explain why lower-ranked options lost
- mention the biggest risk to check before checkout

## References

- Use [platform-playbook.md](./references/platform-playbook.md) for platform-specific heuristics.
- Use [ranking-rubric.md](./references/ranking-rubric.md) for default scoring and tie-break rules.
- Use [../../guides/setup-cookies.md](../../guides/setup-cookies.md) for cookie registration.
- Use [../../guides/setup-mcporter.md](../../guides/setup-mcporter.md) for MCP setup.
