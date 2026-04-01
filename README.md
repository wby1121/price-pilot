# Price Pilot

`Price Pilot` 是一个面向 OpenClaw、Codex 和其他支持 skills 的模型的国内商品比价 skill 仓库。

它的目标很直接: 当你问“想买什么”“值不值得买”“哪个平台更划算”时，agent 能同时查拼多多、闲鱼、转转、京东和淘宝，提取可比商品，结合价格、评论、商品信息完整度和风险信号给出综合评价，并按性价比排序。

## 能力概览

- 跨平台搜索: 拼多多、闲鱼、转转、京东、淘宝
- 统一字段: 标题、价格、到手价、成色、销量、评分、评论摘要、售后信息、风险提示
- 综合评价: 按价格竞争力、评论质量、信息完整度、平台可信度、风险项进行评分
- 场景适配: 支持全新商品、二手商品、准新品、收藏品与高风险闲置交易
- 结果输出: 返回候选列表、排序理由、购买建议和避坑点

## 仓库结构

```text
.
├── skills/
│   └── cn-shopping-compare/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/
├── docs/
│   ├── install.md
│   └── update.md
├── tools/
│   └── validate_skill.py
└── .github/
    ├── workflows/
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

## 安装

把仓库中的 `skills/cn-shopping-compare` 放到你的 skills 目录即可使用。

- Codex 默认目录: `${CODEX_HOME:-$HOME/.codex}/skills`
- OpenClaw: 放到对应 skills 目录，或让 agent 读取 [docs/install.md](docs/install.md) 执行安装

## 使用示例

- “帮我找 iPhone 15 Pro 256G 国行，京东、淘宝、拼多多都看一下，按性价比排一下。”
- “我想买二手 Switch OLED，优先闲鱼和转转，避开高风险卖家。”
- “帮我比较 RTX 5070 显卡，重点看评论里翻车点和售后。”

## 开源协作

仓库已经预留了适合公开协作的基础设施:

- PR 模板和 Issue 模板
- Skill 校验工作流
- 自动请求仓库 owner 审核的 GitHub Action

要让“有人提交代码后你能收到审核通知”真正生效，只需要在 GitHub 仓库里配置一个仓库变量:

- 变量名: `REVIEW_OWNER`
- 值: `wby1121`

当外部贡献者打开或转为 Ready for review 的 PR 时，工作流会自动向该用户发起 review request，GitHub 就会给你推送通知。

## 开发

```bash
python3 tools/validate_skill.py skills/cn-shopping-compare
python3 skills/cn-shopping-compare/scripts/score_products.py --input sample.json
```

## License

[MIT](LICENSE)
