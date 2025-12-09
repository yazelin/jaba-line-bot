# line-bot-core Spec Delta

## ADDED Requirements

### Requirement: 群組點餐 Session 觸發
系統 SHALL 根據群組的點餐 Session 狀態決定是否處理訊息。

#### Scenario: 非點餐中收到「開始點餐」
- **WHEN** 群組不在點餐中
- **AND** 收到訊息「開始點餐」
- **THEN** 系統轉發訊息給 jaba，開始群組點餐 session

#### Scenario: 非點餐中收到一般訊息
- **WHEN** 群組不在點餐中
- **AND** 收到非「開始點餐」的訊息
- **THEN** 系統不處理該訊息（完全忽略）

#### Scenario: 點餐中收到任何訊息
- **WHEN** 群組在點餐中
- **AND** 收到任何訊息
- **THEN** 系統轉發訊息給 jaba 處理

#### Scenario: 點餐中收到「結束點餐」或「收單」
- **WHEN** 群組在點餐中
- **AND** 收到「結束點餐」或「收單」
- **THEN** 系統轉發訊息給 jaba，結束群組點餐 session

### Requirement: 傳送群組 ID
系統 SHALL 在群組訊息中傳送 group_id 給 jaba API。

#### Scenario: 群組訊息包含 group_id
- **WHEN** 在群組中發送訊息給 jaba
- **THEN** API 呼叫包含 `group_id` 參數
