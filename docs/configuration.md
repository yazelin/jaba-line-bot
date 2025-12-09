# 環境變數說明

本文件說明 jaba-line-bot 的所有環境變數設定。

## 環境變數總覽

| 變數名稱 | 必填 | 說明 | 預設值 |
|----------|------|------|--------|
| `LINE_CHANNEL_SECRET` | **必填** | LINE Channel Secret | - |
| `LINE_CHANNEL_ACCESS_TOKEN` | **必填** | LINE Channel Access Token | - |
| `JABA_API_URL` | 可選 | jaba API 位址 | - (Echo 模式) |
| `JABA_API_KEY` | 可選 | jaba API 驗證金鑰 | - |
| `REGISTER_SECRET` | 可選 | 啟用功能的密碼 | - |
| `PORT` | 可選 | 服務監聽埠號 | 5000 |

## 詳細說明

### LINE_CHANNEL_SECRET

**必填** - LINE Messaging API 的 Channel Secret

- **用途**：驗證 LINE Platform 發送的 Webhook 請求簽章
- **取得方式**：[LINE Developers Console](https://developers.line.biz/console/) → 你的 Channel → Basic settings
- **格式**：32 字元的十六進位字串
- **範例**：`a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

```bash
LINE_CHANNEL_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### LINE_CHANNEL_ACCESS_TOKEN

**必填** - LINE Messaging API 的 Channel Access Token

- **用途**：呼叫 LINE Messaging API（發送訊息、取得用戶資料等）
- **取得方式**：[LINE Developers Console](https://developers.line.biz/console/) → 你的 Channel → Messaging API → Issue
- **格式**：約 170 字元的 Base64 字串
- **範例**：`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

```bash
LINE_CHANNEL_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> **注意**：Token 很長，確保完整複製。

### JABA_API_URL

**可選** - jaba 系統的 API 位址

- **用途**：指定 jaba API 的完整 URL
- **格式**：`http(s)://domain/path`
- **預設**：未設定時進入 Echo 模式（不連接 jaba）
- **範例**：`http://ching-tech.ddns.net/jaba-api`

```bash
JABA_API_URL=http://ching-tech.ddns.net/jaba-api
```

**Echo 模式**：
- 如果未設定 `JABA_API_URL`，Bot 會直接回傳使用者發送的訊息
- 適合測試 LINE Bot 基本功能是否正常

### JABA_API_KEY

**可選** - jaba API 的驗證金鑰

- **用途**：呼叫 jaba API 時的身份驗證
- **格式**：自訂字串
- **設定位置**：需與 nginx 設定的 API Key 一致
- **範例**：`my_secret_api_key_12345`

```bash
JABA_API_KEY=my_secret_api_key_12345
```

**注意**：
- 必須與 nginx 設定中的 `$http_x_api_key` 驗證值一致
- 建議使用足夠複雜的字串

### REGISTER_SECRET

**可選** - 啟用點餐功能的密碼

- **用途**：使用者輸入此密碼後，其帳號/群組會被加入白名單
- **格式**：自訂字串
- **預設**：未設定時，無法透過密碼啟用
- **範例**：`secret123`

```bash
REGISTER_SECRET=secret123
```

**使用方式**：
1. 使用者在 LINE 發送此密碼
2. Bot 識別後呼叫 jaba 註冊 API
3. 使用者被加入白名單，可以開始使用點餐功能

**安全建議**：
- 使用不易猜測的密碼
- 定期更換密碼
- 不要在程式碼中寫死密碼

### PORT

**可選** - 服務監聽的埠號

- **用途**：指定 Flask 應用程式監聽的埠號
- **預設**：5000
- **範例**：`8080`

```bash
PORT=8080
```

> **注意**：在 Render 上不需要設定，Render 會自動設定 `PORT`。

## 設定方式

### 本地開發

建立 `.env` 檔案（不要提交到 Git）：

```bash
# 從範本複製
cp .env.example .env

# 編輯設定
vim .env
```

`.env` 內容：

```bash
# LINE 設定（必填）
LINE_CHANNEL_SECRET=your_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here

# jaba 設定（可選）
JABA_API_URL=http://ching-tech.ddns.net/jaba-api
JABA_API_KEY=your_api_key_here

# 啟用密碼（可選）
REGISTER_SECRET=your_secret_password
```

### Render 部署

1. 到 Render Dashboard → 你的 Web Service
2. 點擊 **Environment**
3. 加入環境變數：

| Key | Value |
|-----|-------|
| LINE_CHANNEL_SECRET | your_channel_secret |
| LINE_CHANNEL_ACCESS_TOKEN | your_access_token |
| JABA_API_URL | http://ching-tech.ddns.net/jaba-api |
| JABA_API_KEY | your_api_key |
| REGISTER_SECRET | your_secret_password |

4. 點擊 **Save Changes**

## 運作模式

根據環境變數設定，Bot 有不同的運作模式：

### 完整模式

設定 `JABA_API_URL` 和 `JABA_API_KEY`：
- 訊息轉發到 jaba 系統
- AI 處理點餐功能
- 白名單驗證

### Echo 模式

未設定 `JABA_API_URL`：
- 直接回傳使用者訊息
- 用於測試 LINE Bot 基本功能
- 不需要 jaba 系統

### 無密碼模式

未設定 `REGISTER_SECRET`：
- 無法透過密碼啟用
- 需要手動將使用者加入白名單
- 或不使用白名單功能

## 驗證設定

### 檢查必填變數

啟動時會檢查必填變數：

```
錯誤：未設定 LINE_CHANNEL_SECRET 環境變數
錯誤：未設定 LINE_CHANNEL_ACCESS_TOKEN 環境變數
```

### 檢查運作模式

啟動訊息會顯示目前模式：

```
# 完整模式
Jaba LINE Bot is running! (jaba 模式)

# Echo 模式
Jaba LINE Bot is running! (Echo 模式)
警告：未設定 JABA_API_URL，將使用 Echo 模式
```

## 安全注意事項

1. **不要提交 .env 檔案**
   - `.gitignore` 已包含 `.env`
   - 確保敏感資訊不會進入 Git

2. **使用環境變數管理密鑰**
   - 不要在程式碼中寫死任何密鑰
   - Render 的環境變數會加密儲存

3. **定期更換密鑰**
   - Channel Access Token 可以重新發行
   - API Key 和 REGISTER_SECRET 可以隨時更換

4. **最小權限原則**
   - 只設定需要的環境變數
   - 不要在 .env.example 中放真實值

## 相關文件

- [LINE 設定指南](line-setup.md) - 取得 LINE 憑證
- [部署指南](deployment.md) - 在 Render 設定環境變數
- [jaba 整合說明](jaba-integration.md) - API Key 與 nginx 設定
