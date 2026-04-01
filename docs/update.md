# Update Price Pilot

复制这句话给你的 Agent：

```text
帮我更新 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/update.md
```

Agent 应该执行以下步骤：

1. 找到当前安装目录。
2. 拉取 `https://github.com/wby1121/price-pilot` 最新代码。
3. 仅替换 `cn-shopping-compare` skill 目录。
4. 检查 `SKILL.md` 仍然存在。

## Shell example

```bash
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
if [ -d /tmp/price-pilot/.git ]; then
  git -C /tmp/price-pilot pull --ff-only
else
  git clone https://github.com/wby1121/price-pilot.git /tmp/price-pilot
fi
rm -rf "$TARGET_DIR/cn-shopping-compare"
cp -R /tmp/price-pilot/price_pilot/skill "$TARGET_DIR/cn-shopping-compare"
```

