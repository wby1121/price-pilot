# Update Price Pilot

复制这句话给你的 Agent：

```text
帮我更新 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/update.md
```

严格按下面执行，不要自己改步骤。

## 规则

- 不要使用 `git clone`
- 不要使用 `/tmp` 临时目录
- 不要自己复制 skill 目录
- 只允许执行下面的更新命令

## 更新命令

先执行：

```bash
python3 -m pip install --upgrade "git+https://github.com/wby1121/price-pilot.git"
```

再执行：

```bash
price-pilot update
```

如果用户指定了 skills 目录：

```bash
price-pilot update --dir /path/to/skills
```

如果 `price-pilot` 命令尚不可用，只允许使用这个等价命令：

```bash
python3 -m price_pilot update
```

更新成功后，确认：

```text
${CODEX_HOME:-$HOME/.codex}/skills/cn-shopping-compare/SKILL.md
```
