# Install Price Pilot

Use this guide when another agent needs to install the `cn-shopping-compare` skill from this repository.

## Install workflow

1. Confirm the user's skill directory.
   Default to `${CODEX_HOME:-$HOME/.codex}/skills` when the user does not specify one.
2. Clone or download this repository.
3. Copy `skills/cn-shopping-compare` into the target skills directory.
4. Confirm that `SKILL.md` exists at `<skills-dir>/cn-shopping-compare/SKILL.md`.
5. Tell the user how to invoke the skill: `Use $cn-shopping-compare to ...`

## Git install example

```bash
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$TARGET_DIR"
git clone <your-repo-url> /tmp/price-pilot
rm -rf "$TARGET_DIR/cn-shopping-compare"
cp -R /tmp/price-pilot/skills/cn-shopping-compare "$TARGET_DIR/cn-shopping-compare"
```

## Validation

Check:

- `SKILL.md` exists
- `agents/openai.yaml` exists
- `references/` and `scripts/` are copied

