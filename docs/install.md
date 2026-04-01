# Install Price Pilot

复制这句话给你的 Agent：

```text
帮我安装 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/install.md
```

严格按下面执行，不要自己改步骤。

## 规则

- 不要使用 `git clone`
- 不要使用 `/tmp` 临时目录
- 不要先下载仓库再复制文件
- 不要自己发明安装流程
- 只允许执行下面这两条命令

## 安装命令

先执行：

```bash
python3 -m pip install --upgrade "git+https://github.com/wby1121/price-pilot.git"
```

再执行：

```bash
price-pilot install
```

如果用户指定了 skills 目录：

```bash
price-pilot install --dir /path/to/skills
```

如果 `price-pilot` 命令尚不可用，只允许使用这个等价命令：

```bash
python3 -m price_pilot install
```

安装成功后，确认这里存在：

```text
${CODEX_HOME:-$HOME/.codex}/skills/cn-shopping-compare/SKILL.md
```

然后告诉用户这样调用：

```text
Use $cn-shopping-compare to compare products across Chinese marketplaces.
```
