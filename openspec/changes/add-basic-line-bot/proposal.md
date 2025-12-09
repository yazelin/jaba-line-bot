# Change: 建立基礎 LINE Bot 並部署到 Render

## Why
目前 jaba 系統只能透過 Web 介面使用。為了讓使用者能夠在 LINE 群組中直接進行點餐，需要建立一個 LINE Bot 作為前端介面。第一階段先確保 Bot 能正確部署到 Render 並正常運作。

## What Changes
- 新增 `app.py` - LINE Bot 主程式 (Flask + line-bot-sdk)
- 新增 `requirements.txt` - Python 依賴套件
- 新增 `render.yaml` - Render 部署配置
- 新增 `.env.example` - 環境變數範例檔

## Impact
- Affected specs: `line-bot-core` (新建)
- Affected code: 專案根目錄新增檔案

## Scope
此為 Phase 1，僅實作：
1. 接收 LINE 訊息
2. Echo 回覆（收到什麼回什麼）
3. 部署到 Render

後續 Phase 2 才會整合 jaba 核心系統進行點餐功能。
