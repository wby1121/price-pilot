---
name: cn-shopping-compare
description: Comprehensive China e-commerce comparison skill for JD, Taobao, Pinduoduo, Xianyu, and Zhuanzhuan. Use when Codex, OpenClaw, or another agent needs to find products across major Chinese shopping platforms, compare current prices, evaluate reviews and seller quality, identify risk signals, summarize tradeoffs, or rank options by overall value for money for new or used goods.
---

# CN Shopping Compare

## Overview

Use this skill to turn a vague shopping request into a structured, cross-platform comparison with an explicit recommendation. Gather live listings, normalize them into comparable fields, score them consistently, and explain why the top option wins.

## Workflow

### 1. Clarify the shopping target

Extract the decision constraints before searching:

- product name and generation
- model or configuration
- new or used preference
- budget cap or target price band
- platform preference or exclusions
- risk tolerance
- must-have details such as color, storage, edition, invoice, warranty, shipping origin

Ask a follow-up only when a missing detail would materially change the recommendation. Otherwise proceed with reasonable defaults and state them.

### 2. Search each platform with current data

Use live browsing or search for current listings. Do not rely on stale memory for prices, ratings, or availability.

Search these platforms unless the user narrows the scope:

- JD
- Taobao
- Pinduoduo
- Xianyu
- Zhuanzhuan

Read [platform-playbook.md](./references/platform-playbook.md) when choosing search terms and platform-specific heuristics.

### 3. Normalize candidate listings

Collect the strongest candidates and normalize them into one comparison table. Prefer 2 to 5 strong candidates per platform instead of dumping search noise.

Capture these fields whenever available:

- platform
- title
- current price
- estimated landed price including shipping or coupons when visible
- condition
- store or seller type
- rating, review count, sales volume, or transaction count
- return policy and warranty
- authenticity or inspection signals
- advantages
- red flags
- listing URL

If a field is missing, say so explicitly instead of inferring it.

### 4. Evaluate evidence quality

Treat evidence quality as part of the recommendation:

- Prefer listings with complete specs, clear photos, detailed seller disclosures, warranty terms, and realistic review density.
- Penalize listings with suspiciously low price, vague descriptions, obvious keyword stuffing, mismatched specs, or repeated complaint patterns.
- For used marketplaces, treat seller credibility, inspection options, and defect disclosure as first-class ranking inputs.

Read [ranking-rubric.md](./references/ranking-rubric.md) before scoring.

### 5. Score and rank

Use `scripts/score_products.py` whenever the candidate set is large enough to benefit from consistent scoring or when the user wants a ranked list.

Prepare a JSON array of normalized listings and run:

```bash
python3 scripts/score_products.py --input candidates.json
```

Use the script output as a structured aid, not as a blind final answer. Adjust narrative emphasis when the user's priorities differ from the default rubric.

### 6. Return a decision-oriented answer

Always answer in a way that helps the user buy or reject:

- lead with the best overall option
- call out the best budget option if it differs
- call out the safest option if it differs
- explain why lower-ranked options lost
- mention the biggest risk to watch before checkout

## Output format

When the user asks for direct buying advice, prefer this structure:

1. One-paragraph verdict with the best choice.
2. Compact comparison table.
3. Ranked list with 1 to 2 sentences per option.
4. Caveats, especially for used or unusually cheap listings.

## References

- Use [platform-playbook.md](./references/platform-playbook.md) for search patterns, platform quirks, and risk cues.
- Use [ranking-rubric.md](./references/ranking-rubric.md) for default weighting and tie-break rules.

## Scripts

- Use [score_products.py](./scripts/score_products.py) to compute a consistent value-for-money ranking from normalized listing data.

