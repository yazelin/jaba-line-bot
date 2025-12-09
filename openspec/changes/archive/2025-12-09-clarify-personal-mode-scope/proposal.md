# Proposal: clarify-personal-mode-scope

## Problem Statement

目前 jaba 系統已移除個人訂餐功能（僅支援 LINE 群組點餐和管理員模式），但 jaba-line-bot 的訊息文案和文件仍有多處暗示使用者可以透過 1對1 聊天進行點餐，這會造成使用者誤解並導致不好的使用體驗。

### 現狀問題

**jaba-line-bot/app.py**:
1. `generate_help_message()` 個人模式仍顯示「直接說出餐點即可點餐」等指引
2. 個人啟用成功訊息：「啟用成功！現在你可以使用點餐功能了。試試說『今天吃什麼』」
3. 個人已啟用回覆：「已啟用，可以直接使用點餐功能！」

**jaba-line-bot/README.md**:
1. 功能特色：「1對1 聊天：直接與 Bot 對話即可點餐」
2. 觸發方式：「1對1 聊天：任何訊息都會處理」

**jaba/main.py**:
1. 雖然已攔截個人訂餐，但錯誤訊息是 400 狀態碼的 JSON 回應，LINE Bot 顯示不友善

## Proposed Solution

1. **修正個人模式用途**：1對1 聊天僅提供「偏好設定」功能（名稱、飲食偏好等），不提供點餐功能
2. **更新訊息文案**：所有與個人模式相關的訊息改為引導使用者透過群組點餐或設定偏好
3. **更新文件**：README 說明個人模式僅用於偏好設定

## Impact Analysis

### 影響範圍
- jaba-line-bot: app.py 訊息文案、README.md
- jaba: main.py API 回應訊息（可選優化）
- OpenSpec: line-bot-core spec 更新

### 無需變更
- 白名單機制：個人啟用功能保留，用途改為偏好設定
- 群組點餐流程：完全不受影響

## Success Criteria

1. 個人模式 help 訊息清楚說明功能範圍（偏好設定）
2. 個人啟用成功訊息引導設定偏好而非點餐
3. README 文件正確描述個人模式用途
4. 使用者在 1對1 聊天中不會誤以為可以點餐
