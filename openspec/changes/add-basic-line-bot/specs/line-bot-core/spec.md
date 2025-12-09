## ADDED Requirements

### Requirement: LINE Webhook 接收
系統 SHALL 提供 `/callback` endpoint 接收 LINE Platform 的 Webhook 請求。

#### Scenario: 接收有效 Webhook 請求
- **WHEN** LINE Platform 發送帶有有效簽名的 Webhook 請求
- **THEN** 系統回傳 HTTP 200 OK

#### Scenario: 拒絕無效簽名
- **WHEN** 收到簽名無效的請求
- **THEN** 系統回傳 HTTP 400 Bad Request

### Requirement: 文字訊息回覆
系統 SHALL 能夠接收使用者發送的文字訊息並進行回覆。

#### Scenario: Echo 回覆
- **WHEN** 使用者發送文字訊息 "你好"
- **THEN** Bot 回覆相同的文字 "你好"

#### Scenario: 處理空訊息
- **WHEN** 使用者發送空白訊息
- **THEN** Bot 不進行回覆

### Requirement: 環境變數配置
系統 SHALL 透過環境變數載入 LINE 憑證，不在程式碼中硬編碼。

#### Scenario: 載入 Channel Secret
- **WHEN** 環境變數 `LINE_CHANNEL_SECRET` 已設定
- **THEN** 系統使用該值進行簽名驗證

#### Scenario: 載入 Access Token
- **WHEN** 環境變數 `LINE_CHANNEL_ACCESS_TOKEN` 已設定
- **THEN** 系統使用該值發送回覆訊息

#### Scenario: 缺少必要環境變數
- **WHEN** 環境變數未設定
- **THEN** 系統啟動時顯示錯誤訊息並終止

### Requirement: Render 部署支援
系統 SHALL 支援透過 Render Blueprint 進行一鍵部署。

#### Scenario: 使用 render.yaml 部署
- **WHEN** 使用者在 Render 建立新的 Blueprint 並連結此 repository
- **THEN** 系統自動完成部署配置

#### Scenario: 提示設定環境變數
- **WHEN** 部署過程中
- **THEN** Render 提示使用者輸入 LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN
