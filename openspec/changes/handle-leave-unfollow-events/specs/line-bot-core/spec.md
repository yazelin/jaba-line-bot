# line-bot-core Spec Delta

## ADDED Requirements

### Requirement: 離開事件處理
系統 SHALL 監聽 LINE 的離開事件，並自動將對應的群組或使用者從 jaba 白名單移除。

#### Scenario: Bot 被移出群組
- **WHEN** Bot 被踢出或移除出群組
- **THEN** 系統呼叫 jaba API 將該群組 ID 從白名單移除

#### Scenario: Bot 被移出聊天室
- **WHEN** Bot 被踢出或移除出多人聊天室
- **THEN** 系統呼叫 jaba API 將該聊天室 ID 從白名單移除

#### Scenario: 使用者封鎖或取消追蹤 Bot
- **WHEN** 使用者在 1對1 聊天中封鎖或取消追蹤 Bot
- **THEN** 系統呼叫 jaba API 將該使用者 ID 從白名單移除

#### Scenario: API 呼叫失敗
- **WHEN** 呼叫 jaba unregister API 失敗
- **THEN** 系統記錄錯誤訊息但不中斷服務
