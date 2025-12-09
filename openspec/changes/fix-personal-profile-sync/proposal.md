# Proposal: fix-personal-profile-sync

## Why

個人偏好設定無法在群組點餐中被正確讀取，因為：

1. **jaba-line-bot 問題**：`call_jaba_api()` 只在群組模式（有 `group_id`）時才傳送 `line_user_id`，導致個人模式下 jaba 不知道使用者的 LINE User ID
2. **資料儲存錯誤**：個人模式下 profile 被存到 `data/users/{display_name}/` 而非 `data/users/{line_user_id}/`
3. **群組模式讀取失敗**：群組點餐時查詢 `data/users/{line_user_id}/` 找不到之前在個人模式設定的偏好
4. **Prompt 未使用 preferred_name**：`group_ordering_prompt.md` 沒有指示 AI 使用 `preferred_name` 來稱呼使用者

## What Changes

### jaba-line-bot

1. **修改 `call_jaba_api()`**：無論群組或個人模式，都要傳送 `line_user_id`

### jaba

2. **修改 `build_context()`**：群組模式下自動將 `preferred_name` 作為 `username` 傳給 AI
3. **簡化 `group_ordering_prompt.md`**：說明 `username` 已是正確稱呼，AI 直接使用即可
4. **新增語氣調整指引**：所有對話 prompts（group_ordering、personal、manager）新增根據職稱調整語氣的指引

## Impact Analysis

### 影響範圍
- jaba-line-bot: `app.py` 的 `call_jaba_api()` 函式
- jaba: `group_ordering_prompt.md` 提示詞

### 向下相容
- 現有群組點餐流程不受影響
- 已存在的錯誤 profile 資料（以 display_name 為 key）將被孤立，新資料會正確以 line_user_id 為 key

## Success Criteria

1. 在 1對1 聊天設定「叫我小明」→ profile 正確存到 `data/users/{line_user_id}/`
2. 在群組點餐時，呷爸正確讀取該使用者的偏好並使用「小明」稱呼
3. 使用者的飲食限制（不吃辣等）在群組點餐時被正確提醒
