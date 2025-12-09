# Proposal: track-activator-info

## Summary
在啟用白名單時，記錄是誰（哪個 LINE 使用者）啟用的，包含啟用者的 user_id 和顯示名稱。

## Motivation
目前的問題：
1. **群組啟用**：只記錄 group_id 和 registered_at，不知道是誰啟用的
2. **管理困難**：後台無法分辨是哪個人啟用了哪個群組
3. **無法追蹤**：如果需要封鎖某人，無法知道他啟用了哪些群組

需求：
- 管理員需要知道「誰」啟用了「哪個群組」
- 方便後台管理與黑名單封鎖決策
- 個人啟用時也記錄完整資訊

## Proposed Solution

### 資料結構變更

**現有結構**（群組）：
```json
{
  "id": "C1234567890",
  "name": "",
  "registered_at": "2024-01-15T10:30:00"
}
```

**新結構**（群組）：
```json
{
  "id": "C1234567890",
  "name": "",
  "registered_at": "2024-01-15T10:30:00",
  "activated_by": {
    "user_id": "U9876543210",
    "display_name": "王小明"
  }
}
```

**新結構**（個人）：
```json
{
  "id": "U9876543210",
  "name": "王小明",
  "registered_at": "2024-01-15T10:30:00",
  "activated_by": {
    "user_id": "U9876543210",
    "display_name": "王小明"
  }
}
```

### 變更範圍

1. **LINE Bot (app.py)**：
   - 修改 `register_to_whitelist()` 新增 `activated_by` 參數
   - 啟用時傳送啟用者的 `user_id` 和 `display_name`

2. **jaba (main.py)**：
   - 修改 `/api/linebot/register` 接收並儲存 `activated_by`

## Scope
- **In Scope**:
  - LINE Bot 傳送啟用者資訊
  - jaba 儲存啟用者資訊
  - 向下相容（舊資料不影響）
- **Out of Scope**:
  - 後台管理介面顯示（未來功能）
  - 黑名單封鎖功能（未來功能）

## Risks
- **低風險**：向下相容，舊資料繼續運作
- 新增欄位不影響現有功能
