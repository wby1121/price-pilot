# Install Price Pilot

复制这句话给你的 Agent：

```text
帮我安装 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/install.md
```

Agent 应该执行以下步骤：

1. 确认 skills 目录。
   默认使用 `${CODEX_HOME:-$HOME/.codex}/skills`。
2. 克隆仓库到临时目录。
3. 把 `price_pilot/skill` 复制到目标目录，目录名保持为 `cn-shopping-compare`。
4. 确认 `<skills-dir>/cn-shopping-compare/SKILL.md` 存在。
5. 告诉用户可以这样调用：
   `Use $cn-shopping-compare to compare products across Chinese marketplaces.`

## Shell example

```bash
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$TARGET_DIR"
git clone https://github.com/wby1121/price-pilot.git /tmp/price-pilot
rm -rf "$TARGET_DIR/cn-shopping-compare"
cp -R /tmp/price-pilot/price_pilot/skill "$TARGET_DIR/cn-shopping-compare"
```

