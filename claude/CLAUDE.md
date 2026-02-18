## 📢 Communication

- 使用中文時**以繁體中文為優先**
- 永遠用中文跟我對話
- 電腦領域相關的術語，都使用英文表達
- 對我的提問或要求如果有任何不清楚的地方，請先詢問我以釐清細節，再進行回答，不要直接假設我的需求
- 不要一味地附和我，對我提出的任何問題，都要進行仔細的思考，再進行回答，不要直接回答，要進行思考，再進行回答

## 💻 Code Style & Standards

- Source code 及 comments 一律使用英文

## 🔍 Code Navigation & Understanding

優先使用 LSP 功能進行代碼導航、理解和診斷。只有在 LSP 無法滿足時，才退而使用文字搜尋工具。

### LSP 功能應用場景

Claude Code 支援以下 LSP 功能（需要安裝對應語言的 LSP plugin）：

| 功能 | 使用時機 |
|------|--------|
| **Go to Definition** | 需要查看某個 function、class、variable 的定義位置 |
| **Find References** | 需要了解某個 symbol 在哪些地方被使用 |
| **Find Implementations** | 需要找到 interface 或 abstract class 的所有實現 |
| **Hover** | 需要查看變數、參數的型別資訊或 function 的文件 |
| **List Symbols** | 需要查看檔案或 workspace 中的所有 symbol 列表 |
| **Trace Call Hierarchies** | 需要追蹤 function 的呼叫鏈或被呼叫關係 |
| **Automatic Diagnostics** | 每次編輯後自動檢查語法錯誤、型別錯誤或 linter 警告 |


## 📚 Documentation & Research

- LLM 內建的知識可能已過時，查詢 API 或 library 文件時，優先使用 context7 MCP 取得最新文件, 若 context7 找不到相關資料，再使用 web search 作為備案

## 🔄 Git Workflow

- 不要自動執行 `git add` 或 `git commit`，除非我有明確要求
