# Jaba LINE Bot

呷爸 AI 午餐訂便當系統的 LINE 介面。讓使用者可以透過 LINE 與呷爸系統互動，進行點餐、查詢等操作。

## 系統概覽

```
┌─────────────────┐     HTTPS      ┌─────────────────┐     HTTP      ┌─────────────────┐
│   LINE 使用者    │ ────────────> │  LINE Platform  │ ────────────> │   Render        │
│  (手機/電腦)     │ <──────────── │   (webhook)     │ <──────────── │  (jaba-line-bot)│
└─────────────────┘                └─────────────────┘               └────────┬────────┘
                                                                              │
                                                                              │ HTTPS
                                                                              │ (API Key)
                                                                              ▼
                                   ┌─────────────────┐               ┌─────────────────┐
                                   │   jaba 系統      │ <──────────── │   nginx         │
                                   │  (AI 點餐核心)   │               │  (API Gateway)  │
                                   │  192.168.11.9   │               │  ching-tech.ddns│
                                   └─────────────────┘               └─────────────────┘
```

### 核心元件

| 元件 | 說明 | 位置 |
|------|------|------|
| **LINE Bot** | 接收/回覆 LINE 訊息 | Render (雲端) |
| **jaba 系統** | AI 點餐核心邏輯 | 本地伺服器 |
| **nginx** | API Gateway、流量分流 | 本地伺服器 |

## 快速開始

1. 設定 LINE 開發者帳號 → [LINE 設定指南](docs/line-setup.md)
2. 部署到 Render → [部署指南](docs/deployment.md)
3. 設定 jaba 整合 → [jaba 整合說明](docs/jaba-integration.md)

## 文件目錄

- [系統架構](docs/architecture.md) - 完整架構說明與資料流程
- [LINE 設定指南](docs/line-setup.md) - LINE Developers Console 設定步驟
- [部署指南](docs/deployment.md) - Render 部署完整流程
- [jaba 整合說明](docs/jaba-integration.md) - 與 jaba 系統的整合方式
- [環境變數說明](docs/configuration.md) - 所有環境變數的說明

## 功能特色

- **1對1 聊天**：直接與 Bot 對話即可點餐
- **群組支援**：在群組中使用 `@呷爸` 或關鍵字觸發
- **白名單機制**：僅啟用的使用者/群組可使用
- **密碼啟用**：透過密碼啟用點餐功能
- **自動清理**：Bot 被踢出群組或使用者封鎖時，自動從白名單移除

## 觸發方式

| 情境 | 觸發方式 |
|------|----------|
| 1對1 聊天 | 任何訊息都會處理 |
| 群組聊天 | `@mention` 或包含關鍵字（呷爸、點餐、jaba） |

## 本地開發

```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 填入實際值
vim .env

# 安裝依賴
pip install -r requirements.txt

# 啟動開發伺服器
python app.py
```

## 專案結構

```
jaba-line-bot/
├── app.py                      # 主程式
├── requirements.txt            # Python 依賴
├── render.yaml                 # Render 部署設定
├── .env.example                # 環境變數範本
├── nginx-config-for-server.conf # nginx 設定參考
└── docs/                       # 詳細文件
    ├── architecture.md         # 系統架構
    ├── line-setup.md           # LINE 設定
    ├── deployment.md           # 部署指南
    ├── jaba-integration.md     # jaba 整合
    └── configuration.md        # 環境變數
```

## 授權

內部使用
