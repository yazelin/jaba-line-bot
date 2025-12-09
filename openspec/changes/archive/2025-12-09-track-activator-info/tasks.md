# Tasks: track-activator-info

## Implementation Tasks

- [x] 1. 修改 LINE Bot `register_to_whitelist()` 函數
  - 新增 `activated_by_id` 和 `activated_by_name` 參數
  - 傳送到 jaba API

- [x] 2. 修改 LINE Bot `handle_special_command()` 啟用邏輯
  - 取得啟用者的 user_id 和 display_name
  - 傳遞給 `register_to_whitelist()`

- [x] 3. 修改 jaba `/api/linebot/register` API
  - 接收 `activated_by` 物件
  - 儲存到白名單資料中

- [x] 4. 更新文件
  - 更新 `docs/jaba-integration.md` 說明新的 API 參數

## Verification

- [ ] 5. 測試驗證
  - 群組啟用時檢查是否記錄啟用者
  - 個人啟用時檢查是否記錄啟用者
  - 確認舊資料不受影響
