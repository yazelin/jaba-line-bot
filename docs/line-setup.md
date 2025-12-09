# LINE 設定指南

本文件說明如何在 LINE Developers Console 建立 Messaging API Channel，並取得 Bot 運作所需的憑證。

## 前置需求

- LINE 帳號（個人帳號即可）
- 電子郵件地址（用於 LINE Developers 註冊）

## 步驟 1：登入 LINE Developers Console

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 使用你的 LINE 帳號登入
3. 如果是首次使用，需要同意開發者條款並建立開發者帳號

## 步驟 2：建立 Provider

Provider 是一個開發者或公司的識別單位，用來管理多個 Channel。

1. 在 Console 首頁，點擊 **Create a new provider**
2. 輸入 Provider 名稱（例如：`呷爸系統`）
3. 點擊 **Create**

## 步驟 3：建立 Messaging API Channel

1. 在 Provider 頁面，點擊 **Create a new channel**
2. 選擇 **Messaging API**
3. 填寫 Channel 資訊：

| 欄位 | 說明 | 範例 |
|------|------|------|
| Channel type | 固定為 Messaging API | Messaging API |
| Provider | 選擇剛建立的 Provider | 呷爸系統 |
| Channel icon | Bot 的頭像（可選） | 上傳圖片 |
| Channel name | Bot 的顯示名稱 | 呷爸點餐 |
| Channel description | Bot 的說明 | AI 午餐訂便當助手 |
| Category | 選擇最相關的分類 | Food & Beverage |
| Subcategory | 選擇子分類 | Restaurant |
| Email address | 聯絡信箱 | your@email.com |

4. 同意條款後，點擊 **Create**

## 步驟 4：取得 Channel Secret

Channel Secret 用於驗證 Webhook 請求的簽章。

1. 進入剛建立的 Channel
2. 在 **Basic settings** 頁籤
3. 找到 **Channel secret** 欄位
4. 點擊 **Copy** 複製

**快速連結**（呷爸專案）：
- LINE Official Account Manager: https://manager.line.biz/account/@588voelu/setting/messaging-api

```
記下這個值，稍後設定為 LINE_CHANNEL_SECRET 環境變數
```

## 步驟 5：發行 Channel Access Token

Channel Access Token 用於呼叫 LINE Messaging API。

1. 切換到 **Messaging API** 頁籤
2. 滾動到最下方的 **Channel access token** 區塊
3. 點擊 **Issue** 發行一個新的 Token
4. 複製產生的 Token

**快速連結**（呷爸專案）：
- LINE Developers Console: https://developers.line.biz/console/channel/2008656234/messaging-api

```
記下這個值，稍後設定為 LINE_CHANNEL_ACCESS_TOKEN 環境變數
```

> **注意**：Channel Access Token 很長（約 170 字元），確保完整複製。

## 步驟 6：設定 Webhook URL

Webhook URL 是 LINE Platform 發送訊息到你的伺服器的位址。

1. 在 **Messaging API** 頁籤
2. 找到 **Webhook settings** 區塊
3. 點擊 **Edit** 設定 Webhook URL：

```
https://你的-render-app-名稱.onrender.com/callback
```

例如：
```
https://jaba-line-bot.onrender.com/callback
```

4. 開啟 **Use webhook** 開關
5. 點擊 **Verify** 測試連線（需要先完成 Render 部署）

## 步驟 7：關閉自動回覆訊息

LINE 官方帳號預設會自動回覆訊息，這會與我們的 Bot 衝突。

1. 在 **Messaging API** 頁籤
2. 找到 **LINE Official Account features** 區塊
3. 點擊 **Auto-reply messages** 旁的 **Edit** 連結
4. 會開啟 LINE Official Account Manager
5. 在左側選單找到 **回應設定**
6. 將 **回應模式** 設為 **聊天**
7. 關閉 **自動回應訊息**

或者直接設定：

| 設定項目 | 值 |
|----------|-----|
| 回應模式 | 聊天 |
| 自動回應訊息 | 停用 |
| Webhook | 啟用 |

## 步驟 8：加入 Bot 好友

1. 在 **Messaging API** 頁籤
2. 找到 **Bot information** 區塊
3. 使用 QR Code 或 Bot basic ID 加入好友

## 完成後的設定摘要

確認你已取得以下資訊：

| 項目 | 說明 | 設定位置 |
|------|------|----------|
| Channel Secret | 約 32 字元 | Basic settings |
| Channel Access Token | 約 170 字元 | Messaging API |
| Webhook URL | 你的伺服器位址 | Messaging API |

## 常見問題

### Q: Webhook 驗證失敗？

確認：
1. Render 已部署成功且正在運行
2. Webhook URL 正確（結尾是 `/callback`）
3. 環境變數已正確設定

### Q: Bot 不回覆訊息？

確認：
1. 自動回覆訊息已關閉
2. Webhook 已啟用
3. 查看 Render 的 Logs 檢查錯誤

### Q: 在群組中 Bot 不回應？

確認：
1. Bot 已被加入群組
2. 訊息包含觸發關鍵字（呷爸、點餐、jaba）或 @mention Bot
3. 群組已啟用（輸入啟用密碼）

### Q: Channel Access Token 過期？

Channel Access Token 預設不會過期。如果需要重新發行：
1. 到 Messaging API 頁籤
2. 點擊 **Reissue** 重新發行
3. 更新 Render 的環境變數

## 相關連結

- [LINE Developers Console](https://developers.line.biz/console/)
- [LINE Official Account Manager](https://manager.line.biz/)
- [LINE Messaging API 文件](https://developers.line.biz/en/docs/messaging-api/)

## 下一步

- [部署指南](deployment.md) - 將 Bot 部署到 Render
