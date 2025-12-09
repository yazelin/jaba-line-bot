# Tasks: add-group-ordering-session

## Phase 1: jaba 系統 - Session 管理

- [x] 1. 新增 Session 資料結構與儲存
  - 建立 `data/linebot/sessions/` 目錄
  - 每個群組一個 JSON 檔案 `{group_id}.json`
  - 包含 status, started_at, started_by, orders

- [x] 2. 新增 `GET /api/linebot/session/{group_id}` API
  - 回傳群組的 session 狀態
  - 不存在或已結束時回傳 `{ "ordering": false }`
  - 點餐中時回傳 `{ "ordering": true, ... }`

- [x] 3. 修改 `/api/chat` 支援群組點餐
  - 新增 `group_id` 參數（可選）
  - AI 識別「開始點餐」→ 建立 session
  - AI 識別「結束點餐/收單」→ 關閉 session，回傳摘要
  - 有 group_id 時，訂單記錄到群組 session

## Phase 2: LINE Bot - 觸發邏輯

- [x] 4. 新增 `check_group_session()` 函數
  - 呼叫 `GET /api/linebot/session/{group_id}`
  - 回傳群組是否在點餐中

- [x] 5. 修改 `should_respond()` 邏輯
  - **非點餐中**：只回應「開始點餐」這 4 個字，其他訊息完全忽略
  - **點餐中**：所有訊息都轉發給 jaba

- [x] 6. 修改 `call_jaba_api()` 傳送 group_id
  - 群組訊息時傳送 `group_id` 參數

## Phase 3: 文件與測試

- [ ] 7. 更新文件

- [ ] 8. 測試驗證
  - 測試非點餐中，一般訊息不處理
  - 測試「開始點餐」→ 開始處理
  - 測試點餐中訊息自動處理
  - 測試「結束點餐」或「收單」→ 停止處理
