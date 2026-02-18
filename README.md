# ⚡️ God Agent (Omniscient Investment Eye)

**God Agent** 是一个基于 AI 的全能投资决策辅助系统，模拟了五位传奇投资大师的智慧，结合实时市场数据（Yahoo Finance）和您私有的研报库（RAG），为您提供上帝视角的交易分析。

## 🌟 核心功能

### 1. 上帝视角 (Omniscience)
每次分析都会召唤六位大师进行“会诊”：
- **巴菲特**: 护城河与现金流。
- **彼得·林奇**: 成长性与生活常识。
- **索罗斯**: 反身性与市场叙事。
- **霍华德·马克斯**: 周期与二阶思维。
- **约翰·邓普顿**: 极度悲观点与全球逆向。
- **纳西姆·塔勒布**: **一票否决权**（毁灭风险）。

### 2. 实时天眼 (Real-Time Eye)
集成 `yfinance`，自动抓取：
- 实时股价、PE、市值
- 波动率 (Volatility) 与动量
- 行业板块信息

### 3. 私有记忆 (Private Memory)
- **Lessons**: 通过 `learn:` 命令教它您的原则（如“不做空热门股”）。
- **Docs (RAG)**: 把 PDF/Markdown 研报丢进 `knowledge/docs/`，它自动查阅引用。
- **Portfolio**: 自动读取 `portfolio/holdings.md`，防止风控超限。

---

## 🚀 快速开始

### 1. 配置环境
```bash
pip install openai httpx yfinance pandas pdfplumber
```
配置 `.env` 文件（填入您的 API Key）。

### 2. 启动上帝模式
```bash
./god.sh
```

### 3. 使用指令
- **分析**: `分析 0700.HK，现价买入`
- **学习**: `learn: 做空英伟达亏损, 教训是不逆势做空`
- **文档转换**: `python3 convert_docs.py` (把 PDF 转为 MD)

---

## 📂 目录结构
- `god.sh`: 启动脚本。
- `investment_committee.py`: 核心大脑。
- `knowledge/`: 记忆库与资料库。
- `portfolio/`: 持仓表。
- `logs/`: 历史分析存档。
