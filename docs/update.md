# Update Price Pilot

Use this guide when another agent needs to refresh an existing `cn-shopping-compare` installation.

## Update workflow

1. Locate the current installation directory.
2. Pull the latest repository changes.
3. Replace only the `cn-shopping-compare` skill folder.
4. Preserve any user-local overrides outside the skill folder.
5. Re-run validation by checking the expected files exist.

## Git update example

```bash
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
if [ -d /tmp/price-pilot/.git ]; then
  git -C /tmp/price-pilot pull --ff-only
else
  git clone <your-repo-url> /tmp/price-pilot
fi
rm -rf "$TARGET_DIR/cn-shopping-compare"
cp -R /tmp/price-pilot/skills/cn-shopping-compare "$TARGET_DIR/cn-shopping-compare"
```

