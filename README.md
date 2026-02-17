# Investment Committee Agent (5-Eyes)

This agent encapsulates the wisdom of 5 legendary investors:
1.  **Warren Buffett** (Value & Moat)
2.  **Peter Lynch** (Growth & PEG)
3.  **George Soros** (Reflexivity & False Narratives)
4.  **Howard Marks** (Cycles & Risk First)
5.  **Nassim Taleb** (Tail Risk & Convexity)

## Usage

1.  **Set your OpenAI API Key**:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```
    Or create a `.env` file in this directory with `OPENAI_API_KEY=sk-...`.

2.  **Run the Agent**:
    ```bash
    ./run_agent.sh
    ```
    Or manually:
    ```bash
    python3 investment_committee.py
    ```

3.  **Interact**:
    -   Enter a trade idea (e.g., "Short Tesla", "Long Bitcoin", "Buy Meta").
    -   The agent will consult all 5 personas and generate a detailed report.
    -   The report is saved as a markdown file (e.g., `report_Short_Tesla.md`).

## Customization

-   You can modify the prompts in `knowledge/*.md`.
-   The prompts are loaded dynamically, so you can tweak the "System Persona" without changing the code.

## Doubao / Volcano Ark (豆包) 支持

本 Agent 支持豆包（火山方舟）OpenAI 兼容接口：
- Base URL: `https://ark.cn-beijing.volces.com/api/v3`
- API Key: 在火山方舟控制台创建（通常称为 ARK API Key）
- Model: 使用控制台“推理接入点 / Model ID”（例如 `doubao-seed-1-6-251015`）

启动时运行 `./run_agent.sh` 并选择 `4) Doubao / Volcano Ark` 即可。
