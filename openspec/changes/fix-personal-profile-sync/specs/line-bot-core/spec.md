# line-bot-core Spec Delta

## ADDED Requirements

### Requirement: 個人模式傳送 LINE User ID
系統 SHALL 在個人模式（1對1 聊天）呼叫 jaba API 時傳送 `line_user_id`，以確保偏好設定正確儲存到使用者的 profile。

#### Scenario: 個人模式 API 呼叫包含 line_user_id
- **WHEN** 使用者在 1對1 聊天中發送訊息
- **AND** 系統呼叫 jaba API
- **THEN** API payload 包含 `line_user_id` 欄位
- **AND** API payload 包含 `display_name` 欄位

#### Scenario: 偏好設定正確儲存
- **GIVEN** 使用者在 1對1 聊天中設定偏好（如「叫我小明」）
- **WHEN** jaba 收到包含 `line_user_id` 的請求
- **THEN** 偏好儲存到 `data/users/{line_user_id}/profile.json`
- **AND** 群組點餐時可正確讀取該偏好

### Requirement: 群組點餐自動使用偏好稱呼
系統 SHALL 在群組點餐時，自動將使用者的 `preferred_name`（若有設定）作為 AI 的 `username` context，確保 AI 使用正確的稱呼。

#### Scenario: 使用 preferred_name 稱呼使用者
- **GIVEN** 使用者已在個人模式設定 preferred_name 為「小明」
- **WHEN** 該使用者在群組中點餐
- **THEN** AI 收到的 context 中 `username` 為「小明」
- **AND** 呷爸使用「小明」稱呼該使用者

#### Scenario: 無 preferred_name 時使用 LINE 顯示名稱
- **GIVEN** 使用者未設定 preferred_name
- **WHEN** 該使用者在群組中點餐
- **THEN** AI 收到的 context 中 `username` 為 LINE 顯示名稱
- **AND** 呷爸使用 LINE 顯示名稱稱呼該使用者
