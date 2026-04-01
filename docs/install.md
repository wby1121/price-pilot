# Install Price Pilot

复制这句话给你的 Agent：

```text
帮我安装 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/install.md
```

优先使用真正的安装命令：

```bash
python3 -m pip install "git+https://github.com/wby1121/price-pilot.git"
price-pilot install
```

如果用户指定了 skills 目录：

```bash
price-pilot install --dir /path/to/skills
```

安装成功后，确认这里存在：

```text
${CODEX_HOME:-$HOME/.codex}/skills/cn-shopping-compare/SKILL.md
```

然后告诉用户这样调用：

```text
Use $cn-shopping-compare to compare products across Chinese marketplaces.
```
