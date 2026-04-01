# Update Price Pilot

复制这句话给你的 Agent：

```text
帮我更新 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/update.md
```

优先执行：

```bash
python3 -m pip install --upgrade "git+https://github.com/wby1121/price-pilot.git"
price-pilot update
```

如果用户指定了 skills 目录：

```bash
price-pilot update --dir /path/to/skills
```

更新成功后，确认：

```text
${CODEX_HOME:-$HOME/.codex}/skills/cn-shopping-compare/SKILL.md
```

