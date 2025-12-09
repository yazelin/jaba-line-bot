# Tasks: handle-leave-unfollow-events

## Implementation Tasks

- [x] 1. 新增 LINE SDK imports
  - 在 `app.py` 新增 `LeaveEvent`, `UnfollowEvent` 的 import
  - 來源: `linebot.v3.webhooks`

- [x] 2. 建立 `unregister_from_whitelist()` 函數
  - 呼叫 `DELETE /api/linebot/unregister` API
  - 參數: `id_value` (群組或使用者 ID)
  - 錯誤處理: 印出錯誤訊息但不中斷程式

- [x] 3. 新增 `LeaveEvent` 處理器
  - 使用 `@handler.add(LeaveEvent)` 裝飾器
  - 取得 `group_id` 或 `room_id`
  - 呼叫 `unregister_from_whitelist()`

- [x] 4. 新增 `UnfollowEvent` 處理器
  - 使用 `@handler.add(UnfollowEvent)` 裝飾器
  - 取得 `user_id`
  - 呼叫 `unregister_from_whitelist()`

- [x] 5. 更新文件
  - 更新 `docs/jaba-integration.md` 說明白名單自動移除機制
  - 更新 `README.md` 功能列表

## Verification

- [ ] 6. 測試驗證
  - 測試 Bot 被移出群組後，該群組從白名單移除
  - 測試使用者封鎖 Bot 後，該使用者從白名單移除
  - 確認 API 呼叫失敗時不影響其他功能
