# Render 部署指南

本文件說明如何將 jaba-line-bot 部署到 Render 雲端平台。

## 為什麼選擇 Render？

- **免費方案**：提供免費的 Web Service
- **自動 HTTPS**：LINE Webhook 需要 HTTPS
- **GitHub 整合**：推送到 GitHub 自動部署
- **簡單設定**：無需複雜的伺服器管理

## 免費方案限制

Render 免費方案有以下限制：

| 限制項目 | 說明 |
|----------|------|
| 冷啟動 | 15 分鐘無流量後服務會休眠，下次請求需等待 30-60 秒啟動 |
| 運行時間 | 每月 750 小時（足夠 24/7 運行一個服務） |
| 頻寬 | 100 GB/月 |
| 自動部署 | 支援，從 GitHub 自動部署 |

> **注意**：冷啟動可能導致第一則訊息回應較慢，但之後會正常。

## 前置需求

1. [GitHub 帳號](https://github.com)
2. [Render 帳號](https://render.com)（可用 GitHub 登入）
3. 已完成 [LINE 設定](line-setup.md)，取得 Channel Secret 和 Access Token

## 步驟 1：準備 GitHub Repository

### 方法 A：從現有專案建立

如果你已有本地專案：

```bash
# 進入專案目錄
cd jaba-line-bot

# 初始化 Git（如果還沒有）
git init

# 加入所有檔案
git add .

# 建立第一個 commit
git commit -m "Initial commit"

# 在 GitHub 建立新的 repository，然後：
git remote add origin https://github.com/你的帳號/jaba-line-bot.git
git branch -M main
git push -u origin main
```

### 方法 B：Fork 現有專案

如果有現成的專案可以 fork：

1. 到專案的 GitHub 頁面
2. 點擊 **Fork**
3. 選擇你的帳號

## 步驟 2：連接 Render 與 GitHub

1. 前往 [Render Dashboard](https://dashboard.render.com)
2. 如果還沒登入，點擊 **Get Started** 並選擇 **GitHub** 登入
3. 授權 Render 存取你的 GitHub repositories

## 步驟 3：建立 Web Service

### 方法 A：使用 render.yaml（推薦）

專案已包含 `render.yaml` 設定檔，可以自動建立服務。

1. 在 Render Dashboard，點擊 **New** → **Blueprint**
2. 選擇你的 GitHub repository
3. Render 會讀取 `render.yaml` 並顯示將建立的服務
4. 點擊 **Apply** 開始部署

### 方法 B：手動建立

1. 在 Render Dashboard，點擊 **New** → **Web Service**
2. 選擇 **Build and deploy from a Git repository**
3. 連接你的 GitHub repository
4. 填寫設定：

| 設定項目 | 值 |
|----------|-----|
| Name | `jaba-line-bot` |
| Region | Singapore (離台灣最近) |
| Branch | `main` |
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Plan | Free |

5. 點擊 **Create Web Service**

## 步驟 4：設定環境變數

部署前需要設定環境變數：

**快速連結**（呷爸專案）：
- Render 環境變數設定頁: https://dashboard.render.com/web/srv-d4ro3a75r7bs73eu63kg/env

1. 在 Render Dashboard，進入你的 Web Service
2. 點擊左側的 **Environment**
3. 點擊 **Add Environment Variable**
4. 加入以下變數：

| Key | Value | 說明 |
|-----|-------|------|
| `LINE_CHANNEL_SECRET` | 你的 Channel Secret | 從 LINE Console 取得 |
| `LINE_CHANNEL_ACCESS_TOKEN` | 你的 Access Token | 從 LINE Console 取得 |
| `JABA_API_URL` | `http://ching-tech.ddns.net/jaba-api` | jaba API 位址 |
| `JABA_API_KEY` | 你的 API Key | 與 nginx 設定一致 |
| `REGISTER_SECRET` | 你的啟用密碼 | 使用者啟用時需輸入 |

5. 點擊 **Save Changes**

> **重要**：環境變數設定後會觸發重新部署。

## 步驟 5：確認部署成功

1. 等待部署完成（約 2-5 分鐘）
2. 查看 **Logs** 確認沒有錯誤
3. 訪問你的服務 URL：
   ```
   https://jaba-line-bot.onrender.com
   ```
   應該看到：`Jaba LINE Bot is running! (jaba 模式)`

## 步驟 6：設定 LINE Webhook

1. 回到 [LINE Developers Console](https://developers.line.biz/console/)
2. 進入你的 Channel → **Messaging API** 頁籤
3. 設定 **Webhook URL**：
   ```
   https://jaba-line-bot.onrender.com/callback
   ```
4. 開啟 **Use webhook**
5. 點擊 **Verify** 測試連線

如果看到 **Success**，表示設定完成！

## 步驟 7：測試 Bot

1. 在 LINE 加入你的 Bot 好友
2. 發送訊息測試（第一則可能較慢，因為冷啟動）
3. 發送啟用密碼來啟用功能
4. 開始使用點餐功能

## 更新部署

當你推送新的 commit 到 GitHub，Render 會自動重新部署：

```bash
# 修改程式碼後
git add .
git commit -m "更新說明"
git push origin main
```

## 手動重新部署

如果需要手動觸發部署：

1. 到 Render Dashboard → 你的 Web Service
2. 點擊右上角的 **Manual Deploy** → **Deploy latest commit**

## 查看 Logs

排查問題時，查看 Logs 很有幫助：

1. 到 Render Dashboard → 你的 Web Service
2. 點擊左側的 **Logs**
3. 可以看到即時的應用程式輸出

## 常見問題

### Q: 部署失敗？

檢查：
1. `requirements.txt` 格式是否正確
2. Python 版本是否支援（建議 3.10+）
3. 查看 Render Logs 找出錯誤訊息

### Q: Webhook 驗證失敗？

確認：
1. 部署已完成且服務正在運行
2. URL 結尾是 `/callback`（不是 `/`）
3. 環境變數 `LINE_CHANNEL_SECRET` 設定正確

### Q: 訊息回應很慢？

原因：
- 免費方案有冷啟動延遲
- 第一則訊息需要等待服務啟動

解決方案：
- 升級到付費方案（無冷啟動）
- 使用外部服務定期 ping 保持服務活躍

### Q: 如何保持服務不休眠？

可以使用免費的 cron 服務（如 [cron-job.org](https://cron-job.org)）每 10 分鐘 ping 一次你的服務 URL。

## render.yaml 說明

```yaml
services:
  - type: web
    name: jaba-line-bot
    runtime: python
    plan: free                              # 免費方案
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app          # 使用 gunicorn 運行
    envVars:
      - key: LINE_CHANNEL_SECRET
        sync: false                         # 不同步，手動設定
      - key: LINE_CHANNEL_ACCESS_TOKEN
        sync: false
      - key: PYTHON_VERSION
        value: 3.12.0                       # 指定 Python 版本
```

## 相關連結

- [Render 文件](https://render.com/docs)
- [Render 免費方案說明](https://render.com/docs/free)
- [Gunicorn 文件](https://gunicorn.org/)

## 下一步

- [jaba 整合說明](jaba-integration.md) - 設定與 jaba 系統的連接
