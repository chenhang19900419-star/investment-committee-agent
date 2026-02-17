# 🏛️ 投资委员会 Agent (Investment Committee Agent)

这是一个基于 AI 的投资决策辅助系统，模拟了五位传奇投资大师的智慧，为您提供全方位的交易分析和风控建议。

## 🌟 核心功能

### 1. 五位大师 (The 5 Personas)
每次分析都会召唤以下五位虚拟委员进行“会诊”：
- **巴菲特 (Warren Buffett)**: 关注护城河、现金流和安全边际。
- **彼得·林奇 (Peter Lynch)**: 关注成长性 (PEG)、PEG<1 的机会和生活常识。
- **索罗斯 (George Soros)**: 关注反身性、市场叙事偏差和不对称机会。
- **霍华德·马克斯 (Howard Marks)**: 关注市场周期、二阶思维和风险溢价。
- **纳西姆·塔勒布 (Nassim Taleb)**: **拥有否决权**。关注尾部风险、凸性回报和反脆弱性。

### 2. 结构化评分 (Structured Scoring)
Agent 会综合五位大师的意见，生成一份标准评分卡：
- **综合评分**: 0-10 分。
- **决策建议**: 强力推荐 (STRONG BUY) / 买入 / 观察 / 卖出。
- **一票否决**: 如果塔勒布判定存在“毁灭风险 (Risk of Ruin)”，无论其他大师给分多高，项目直接被否决。

### 3. 自我进化系统 (Self-Learning Principles)
Agent 拥有长期记忆库 `knowledge/lessons.md`。
- **读取**: 每次分析前，它会强制复习您过去的交易教训。
- **写入**: 您可以通过 `learn:` 命令教它新原则。
- **示例**: 如果您告诉它“做空亏了”，它下次遇到类似情况会警告您。

### 4. 多模型支持 (Multi-Provider)
原生支持多种 API，免费付费皆可：
- **GitHub Models** (推荐，免费，GPT-4o)
- **Groq** (极速，Llama 3)
- **Google Gemini**
- **Ollama** (本地运行)
- **OpenAI** (官方)
- **豆包 (Volcano Ark)**

---

## 🚀 快速开始

### 1. 配置环境
在项目根目录创建 `.env` 文件（可参考 `.env.example`）：

```bash
# 推荐：使用 GitHub Models (免费)
OPENAI_API_KEY=ghp_xxxxxx
OPENAI_BASE_URL=https://models.inference.ai.azure.com
OPENAI_MODEL_NAME=gpt-4o
```

### 2. 运行 Agent
```bash
./run_agent.sh
```

### 3. 使用指令

#### 分析交易
直接输入您的交易想法，支持中文：
```text
> 【标的】: 做多腾讯
> 【逻辑】: 游戏版号恢复，回购力度大
> 【止损】: 跌破280
```

#### 教授新原则 (自我进化)
```text
> learn: 追高英伟达, 亏损15%, 不要在RSI>80时追涨
```
Agent 会自动将这条教训转化为通用原则写入 `knowledge/lessons.md`。

---

## 📂 目录结构
- `investment_committee.py`: 核心逻辑。
- `knowledge/`: 大师的 System Prompt 和 `lessons.md` (记忆库)。
- `run_agent.sh`: 启动脚本。
- `report_*.md`: 自动保存的分析报告。

## 🤝 贡献
欢迎提交 PR 增加新的大师人格或优化 Prompt！
