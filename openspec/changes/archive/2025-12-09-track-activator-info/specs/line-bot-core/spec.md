# line-bot-core Spec Delta

## ADDED Requirements

### Requirement: 記錄啟用者資訊
系統 SHALL 在白名單註冊時，記錄執行啟用動作的使用者資訊（user_id 和顯示名稱）。

#### Scenario: 群組啟用時記錄啟用者
- **WHEN** 使用者在群組中輸入啟用密碼
- **THEN** 系統記錄該群組 ID 以及啟用者的 user_id 和顯示名稱

#### Scenario: 個人啟用時記錄啟用者
- **WHEN** 使用者在 1對1 聊天中輸入啟用密碼
- **THEN** 系統記錄該使用者 ID 以及啟用者資訊（即自己）

#### Scenario: 向下相容舊資料
- **WHEN** 查詢白名單中沒有 `activated_by` 欄位的舊資料
- **THEN** 系統正常運作，不因缺少欄位而錯誤
