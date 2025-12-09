# Proposal: add-group-ordering-session

## Summary
新增群組點餐 Session 機制，讓群組可以「開始點餐」進入點餐狀態，期間所有訊息自動處理，「結束點餐」後回復正常。

## Why
目前 LINE Bot 在群組中需要每次都使用關鍵字或 @mention 才會觸發。這對於群組點餐場景不方便：
- 使用者需要每則訊息都加關鍵字
- 無法自然地進行團體訂餐流程
- 無法追蹤「這次點餐」的完整訂單

## What Changes

### 群組點餐流程

```
[非點餐中] → 群組訊息完全忽略，只有「開始點餐」會處理

1. 任何人說「開始點餐」（完整 4 個字）
   → 群組進入「點餐中」狀態
   → jaba 建立 group_id 的 session

2. 群組成員發送訊息（不需要關鍵字）
   → 「我要雞腿便當」→ jaba 記錄訂單
   → 「改排骨」→ jaba 修改訂單
   → 「目前訂單」→ jaba 回傳訂單摘要
   → 「今天天氣真好」→ jaba 判斷非點餐，不回應

3. 任何人說「結束點餐」或「收單」
   → 結束「點餐中」狀態
   → 回傳最終訂單摘要
   → 群組訊息恢復忽略
```

### LINE Bot 變更

1. **修改 `should_respond()` 邏輯**：
   - 先呼叫 jaba 檢查群組是否在點餐中
   - **點餐中** → 所有訊息都轉發
   - **非點餐中** → 只處理「開始點餐」，其他訊息忽略

2. **修改 `call_jaba_api()`**：
   - 新增 `group_id` 參數
   - 傳送給 jaba 以區分不同群組的訂單

### jaba 系統變更

1. **新增 Session API**：
   - `GET /api/linebot/session/{group_id}` - 檢查群組是否在點餐中

2. **修改 `/api/chat`**：
   - 新增 `group_id` 參數（可選）
   - 有 group_id 時，根據群組記錄訂單
   - 識別「開始點餐」→ 建立 session
   - 識別「結束點餐/收單」→ 關閉 session

3. **Session 資料結構**：
   ```json
   {
     "group_id": "C1234567890",
     "status": "ordering",
     "started_at": "2024-01-15T12:00:00",
     "started_by": { "user_id": "U...", "display_name": "王小明" },
     "orders": [...]
   }
   ```

## Scope
- **In Scope**:
  - LINE Bot 觸發邏輯修改
  - jaba session 管理
  - 群組訂單獨立記錄
- **Out of Scope**:
  - 個人點餐流程（維持現狀）
  - 訂單付款結算
  - 歷史訂單查詢介面
