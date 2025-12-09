# Tasks: 建立基礎 LINE Bot

## 1. 專案設定
- [x] 1.1 建立 `requirements.txt` 包含 Flask, line-bot-sdk, gunicorn
- [x] 1.2 建立 `.env.example` 列出所需環境變數
- [x] 1.3 建立 `.gitignore` 排除 .env, __pycache__, .venv 等

## 2. LINE Bot 核心程式
- [x] 2.1 建立 `app.py` 實作 Flask 應用
- [x] 2.2 實作 `/callback` Webhook endpoint
- [x] 2.3 實作簽名驗證 (LINE Channel Secret)
- [x] 2.4 實作文字訊息處理器 (Echo 回覆)

## 3. Render 部署配置
- [x] 3.1 建立 `render.yaml` Blueprint 配置
- [x] 3.2 設定啟動指令 (gunicorn)
- [x] 3.3 設定環境變數

## 4. Git 與部署
- [x] 4.1 初始化 Git repository
- [ ] 4.2 建立 GitHub repository
- [ ] 4.3 部署到 Render
- [ ] 4.4 在 LINE Developers Console 設定 Webhook URL
- [ ] 4.5 測試 Bot 回應

## 5. 驗收
- [ ] 5.1 發送訊息給 Bot，確認收到相同回覆
- [ ] 5.2 在群組中 @ Bot，確認回應正常
