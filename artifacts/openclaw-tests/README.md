# OpenClaw Test Notes

Date: 2026-04-08

Artifacts in this folder:

- `manual_candidates.json`: manual link/screenshot input used for discovery + workflow testing
- `discover-output.json`: `price-pilot discover` output
- `workflow-output.json`: `price-pilot workflow` output
- `inquiry-send-output.json`: `price-pilot inquiry send` shell-transport output
- `sent-messages.txt`: dispatched inquiry messages captured by shell transport
- `openclaw-agent-output.json`: first OpenClaw agent run before discovery title fix
- `openclaw-agent-output-fixed.json`: OpenClaw agent run after discovery title fix
- `openclaw-skill-trigger-output.json`: explicit `$cn-shopping-compare` trigger check
- `20260408.jsonl`: inquiry transport trace log

Findings:

1. Discovery title extraction initially misread screenshot text and promoted `发布时间：2026-04-08 10:00` as the title.
   Fixed in `price_pilot/discovery.py` by filtering metadata-like lines when selecting title text.

2. End-to-end workflow now succeeds for manual evidence without requiring live browsing.
   Verified by `workflow-output.json`.

3. Confirmed inquiry dispatch works through shell transport and leaves replayable traces.
   Verified by `inquiry-send-output.json`, `sent-messages.txt`, and `20260408.jsonl`.

4. OpenClaw can produce a recommendation from the provided candidates, but one-shot `openclaw agent` runs still do not show `cn-shopping-compare` in `systemPromptReport.skills.entries`.
   Even explicit `$cn-shopping-compare` did not make it appear there.
   This looks like an OpenClaw skill-selection/indexing behavior issue rather than a Price Pilot runtime failure.

Follow-up:

- Keep improving trigger metadata, but assume OpenClaw one-shot agent runs may not always inject the custom skill automatically.
- For deterministic testing, continue using `price-pilot discover`, `price-pilot workflow`, and `price-pilot inquiry send` as the canonical runtime checks.
