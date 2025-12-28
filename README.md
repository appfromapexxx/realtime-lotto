# Realtime Lotto (Taiwan)

即時查詢台灣威力彩開獎結果的 Python 工具。

## ✨ 優化特點
- **導入 `uv`**: 使用現代化的 Python 套件管理器，執行更快速且環境更穩定。
- **錯誤處理**: 增強網路請求異常與 HTML 解析失敗的檢查。
- **程式結構**: 採用函式化編寫，並加入型別提示 (Type Hints)。
- **安全性**: 預設使用 HTTPS 連線。
- **穩定性**: 改用官方 API 取得開獎資料，避免前端改版影響。
- **備援**: API 失敗時自動改用 Playwright。

## 🚀 快速開始

這支程式使用 [uv](https://docs.astral.sh/uv/) 進行套件管理。

### 1. 安裝 uv
如果你還沒有安裝 `uv`：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 執行程式
在專案目錄下執行：
```bash
uv run taiwan_lotto_realtime.py
```

### 3. (可選) 啟用 Playwright 備援
如需在 API 失敗時啟用瀏覽器備援，請先安裝瀏覽器：
```bash
uv run playwright install chromium
```

## 🔒 隱私
- 程式只會請求官方 API/網站資料，不會收集或上傳個人資訊。
- Playwright 備援會自動封鎖非台灣彩券域名的第三方請求，以降低追蹤風險。

---

![image](https://github.com/appfromapexxx/realtime-lotto/blob/main/terminal.png)
![image](https://github.com/appfromapexxx/realtime-lotto/blob/main/lotto_website.png)
