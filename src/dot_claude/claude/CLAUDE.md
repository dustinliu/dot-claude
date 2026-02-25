## 📢 Communication

- 使用中文時**以繁體中文為優先**
- 永遠用中文跟我對話
- 電腦領域相關的術語，都使用英文表達
- 對我的提問或要求如果有任何不清楚的地方，請先詢問我以釐清細節，再進行回答，不要直接假設我的需求
- **區分提問與指令**：當我詢問「某操作會做什麼？」、「這樣做會發生什麼事？」等問題時，這是在求知、想理解，**不是要你執行那個操作**。請先解釋，不要採取行動
- 不要一味地附和我，對我提出的任何問題，都要進行仔細的思考，我很期待你提出不同的意見。
- 我不熟悉 Web Frontend 及 Mobile App 技術，涉及這兩個領域時請提供更詳細的解釋與背景說明
- 當對話變長、context 可能接近上限時，主動提醒我，建議開新 session 或做階段性總結，避免系統自動 compact 導致遺失重要上下文

## 💻 Code Style & Standards

- Source code 及 comments 一律使用英文

## 🔍 Code Navigation & Understanding

優先使用 LSP 功能（Go to Definition、Find References、Hover 等）進行代碼導航與理解。只有在 LSP 無法滿足時，才退而使用文字搜尋工具。

需要深入理解 codebase 時，盡量使用 code-explorer subagent，避免污染主 context。

## 📚 Documentation & Research

- LLM 內建的知識可能已過時，查詢 API 或 library 文件時，優先使用 context7 MCP 取得最新文件, 若 context7 找不到相關資料，再使用 web search 作為備案

## 📋 Task Processing

Process tasks **strictly one at a time** in sequential order:

1. Pick the first pending task
2. Focus exclusively on that single task — do NOT read or analyze other tasks
3. Complete the task fully, then mark it `completed` immediately
4. Only then move to the next pending task

**Never** batch-analyze or pre-plan multiple tasks at once.

## 🔄 Git Workflow

- 不要自動執行 `git add` 或 `git commit`，除非我有明確要求
