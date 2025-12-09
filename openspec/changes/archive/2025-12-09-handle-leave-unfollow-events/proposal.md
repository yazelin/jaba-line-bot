# Proposal: handle-leave-unfollow-events

## Summary
當 LINE Bot 被移出群組或使用者封鎖/取消追蹤 Bot 時，自動通知 jaba 系統將該群組或使用者從白名單移除。

## Motivation
目前白名單只有新增功能，當以下情況發生時白名單不會更新：
1. Bot 被踢出群組 - 該群組仍在白名單中，佔用資源
2. 使用者封鎖或取消追蹤 Bot - 該使用者仍在白名單中

這會導致：
- 白名單累積無效的 ID
- 無法準確追蹤實際使用者數量

## Proposed Solution
監聽 LINE 的 `LeaveEvent` 和 `UnfollowEvent`，當事件發生時呼叫 jaba 的 `/api/linebot/unregister` API 移除白名單。

### LINE 事件說明
| 事件 | 觸發條件 | 對應動作 |
|------|----------|----------|
| `LeaveEvent` | Bot 被移出群組或聊天室 | 移除群組/聊天室白名單 |
| `UnfollowEvent` | 使用者封鎖或取消追蹤 Bot | 移除使用者白名單 |

### 實作方式
1. 新增 `LeaveEvent` 和 `UnfollowEvent` 的 import
2. 建立 `unregister_from_whitelist()` 函數呼叫 jaba API
3. 新增 `@handler.add(LeaveEvent)` 處理器
4. 新增 `@handler.add(UnfollowEvent)` 處理器

## Scope
- **In Scope**:
  - 處理 `LeaveEvent`（群組/聊天室）
  - 處理 `UnfollowEvent`（1對1 聊天）
  - 呼叫 jaba unregister API
- **Out of Scope**:
  - 處理 `MemberLeftEvent`（群組成員離開，非 Bot 被踢）
  - jaba API 端的修改（已存在）

## Dependencies
- jaba 系統的 `/api/linebot/unregister` API（已存在）

## Risks
- **低風險**：API 呼叫失敗時只會在 console 印出錯誤，不影響主要功能
- 事件處理是非同步的，不需要回覆訊息
