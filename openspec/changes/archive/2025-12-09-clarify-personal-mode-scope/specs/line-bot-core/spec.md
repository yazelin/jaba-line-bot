# line-bot-core Spec Delta

## ADDED Requirements

### Requirement: 個人模式功能範圍
系統 SHALL 限制 1對1 聊天（個人模式）僅提供偏好設定功能，不提供點餐功能。

#### Scenario: 個人模式 Help 訊息
- **WHEN** 使用者在 1對1 聊天中呼叫 `@jaba 呷爸`
- **THEN** 顯示偏好設定功能說明
- **AND** 提示點餐功能請透過 LINE 群組使用

#### Scenario: 個人模式偏好設定
- **GIVEN** 使用者已在 1對1 聊天中啟用
- **WHEN** 使用者說「我不吃辣」或「叫我小明」
- **THEN** 系統記錄使用者偏好
- **AND** 這些偏好會在群組點餐時被參考

#### Scenario: 個人模式嘗試點餐
- **GIVEN** 使用者已在 1對1 聊天中啟用
- **WHEN** 使用者嘗試點餐（如「我要雞腿便當」）
- **THEN** 系統回覆引導訊息，說明點餐請透過 LINE 群組

## MODIFIED Requirements

### Requirement: 記錄啟用者資訊（修改）
系統 SHALL 在白名單註冊時，記錄執行啟用動作的使用者資訊。個人啟用成功後引導使用者設定偏好。

#### Scenario: 個人啟用時記錄啟用者（修改）
- **WHEN** 使用者在 1對1 聊天中輸入啟用密碼
- **THEN** 系統記錄該使用者 ID 以及啟用者資訊
- **AND** 回覆啟用成功訊息，引導設定個人偏好
- **AND** 說明點餐功能請透過 LINE 群組使用
