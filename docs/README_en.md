# Price Pilot

Price Pilot gives your AI agent a repeatable workflow for comparing products across major Chinese marketplaces.

It is designed for prompts like:

- "Compare iPhone 15 Pro offers on JD, Taobao, and Pinduoduo."
- "Find the safest used Switch OLED listing across Xianyu and Zhuanzhuan."
- "Rank these listings by value for money, not just sticker price."

## What it does

- Search JD, Taobao, Pinduoduo, Xianyu, and Zhuanzhuan
- Normalize listing fields into one comparison table
- Score options by price, reviews, completeness, protection, and risk
- Return buying advice, not just raw links
- Discover local cookie exports and mcporter marketplace aliases

## Install

```bash
python3 -m pip install "git+https://github.com/wby1121/price-pilot.git"
price-pilot install
```

## Update

```bash
python3 -m pip install --upgrade "git+https://github.com/wby1121/price-pilot.git"
price-pilot update
```

## Uninstall

```bash
price-pilot uninstall
python3 -m pip uninstall price-pilot
```

## Use with an agent

After installation, the bundled skill is placed in your skills directory as `cn-shopping-compare`.

Prompt example:

```text
Use $cn-shopping-compare to compare current listings on JD, Taobao, Pinduoduo, Xianyu, and Zhuanzhuan, then rank the best options by value for money.
```

## Cookie and MCP layer

Price Pilot now includes a lightweight access layer:

```bash
price-pilot config cookie taobao --file ~/Downloads/taobao-cookies.json
price-pilot config show
price-pilot doctor
```

It also auto-detects `mcporter.json`, especially in OpenClaw workspaces.
