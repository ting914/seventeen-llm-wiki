# SEVENTEEN 韓文專輯 LLM Wiki

用 LLM Wiki 做一份教學 HTML 簡報的課堂作業。主題是 SEVENTEEN 出道以來的韓文專輯，重點放在每張專輯的**概念與故事線**，以及**成績與里程碑**。

- **教學簡報**：`slides/index.html`：https://ting914.github.io/seventeen-llm-wiki/slides/
- 
## 架構

參考 Andrej Karpathy 提出的 LLM Wiki 做法，分成三層：

| 資料夾／檔案 | 內容 |
| --- | --- |
| `raw/` | 原始來源，9 篇，只能新增、不能修改；每篇標明網址、擷取日期、事實型或詮釋型 |
| `wiki/` | LLM 撰寫和維護的 wiki，49 頁；入口是 `wiki/index.md` |
| `AGENTS.md` | schema：範圍、頁面格式、正確性規則、ingest／query／lint／簡報流程、修改紀錄 |
| `slides/` | 教學 HTML 簡報（15 張）、`mapping.md`（投影片 ↔ wiki 對應表，122 列）、`img/` |
| `tools/` | `check_wiki.py`、`check_slides.py`：自動檢查程式 |
| `checks/` | 每次 ingest 和簡報的檢查紀錄 |

## 執行檢查

```bash
python tools/check_wiki.py .
python tools/check_slides.py .
```

## 版權

簡報照片版權屬於 PLEDIS Entertainment，僅供課堂教學使用。`raw/` 內是來源的重點整理與改寫，不是全文；原文請見各檔案標示的網址。
