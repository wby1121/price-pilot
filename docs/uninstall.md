# Uninstall Price Pilot

复制这句话给你的 Agent：

```text
帮我卸载 Price Pilot：https://raw.githubusercontent.com/wby1121/price-pilot/main/docs/uninstall.md
```

执行：

```bash
price-pilot uninstall
```

如果用户指定了 skills 目录：

```bash
price-pilot uninstall --dir /path/to/skills
```

如果还需要移除命令行工具本身，再执行：

```bash
python3 -m pip uninstall price-pilot
```

卸载完成后，确认 `cn-shopping-compare` 目录已经不存在。

