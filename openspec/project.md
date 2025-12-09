# Project Context

## Purpose
Jaba LINE Bot 是 jaba (呷爸) AI 午餐訂便當系統的 LINE 前端介面。使用者可以透過 LINE 群組與 Bot 互動進行點餐，Bot 會將請求轉發到自建伺服器上的 jaba 核心系統處理。

### 專案目標
1. **Phase 1**: 建立基礎 LINE Bot 部署到 Render，確認基本功能運作正常
2. **Phase 2**: 整合 jaba 核心系統，實現點餐功能（將請求轉發到自建伺服器）
3. **Phase 3**: 完善群組點餐體驗與管理功能

## Tech Stack
- **Language**: Python 3.12+
- **Web Framework**: Flask (LINE Bot SDK 官方範例使用)
- **LINE SDK**: line-bot-sdk
- **Deployment**: Render (Web Service)
- **Future Integration**: 連接到 jaba 核心系統 (FastAPI + Socket.IO)

## Project Conventions

### Code Style
- 使用繁體中文撰寫註解和文件
- 遵循 PEP 8 Python 程式碼風格
- 函數和變數命名使用 snake_case
- 類別命名使用 PascalCase

### Architecture Patterns
- 單一進入點 (app.py)
- 環境變數管理敏感資訊 (LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN)
- Webhook endpoint 路徑: `/callback`

### Testing Strategy
- 使用 LINE Developers Console 測試 Bot 回應
- 本地開發時可使用 ngrok 進行測試

### Git Workflow
- 主分支: `main`
- 功能開發: `feature/*` 分支
- 提交訊息使用繁體中文描述

## Domain Context
- **jaba (呷爸)**: 原有的 AI 午餐訂便當系統，運行在使用者自建伺服器
- **LINE Messaging API**: 用於接收和發送 LINE 訊息
- **Render**: 雲端平台，提供免費的 Web Service 部署

### 使用流程 (Phase 2 目標)
1. 使用者在 LINE 群組發送訊息
2. LINE Platform 將訊息透過 Webhook 發送到 Render
3. Render 上的 Bot 將請求轉發到 jaba 核心系統
4. jaba 處理點餐邏輯並回傳結果
5. Bot 將結果回覆到 LINE 群組

## Important Constraints
- LINE Channel Secret 和 Access Token 必須透過環境變數設定
- Render 免費方案有冷啟動延遲
- Bot 需要在 3 秒內回應 LINE Platform (否則會重試)

## External Dependencies
- **LINE Messaging API**: https://developers.line.biz/
- **Render**: https://render.com/
- **jaba 核心系統**: 運行在使用者自建伺服器 (192.168.x.x 或透過公開 URL)
