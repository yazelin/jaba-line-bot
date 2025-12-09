# Tasks: fix-personal-profile-sync

## Phase 1: 修正 jaba-line-bot API 呼叫

### 1.1 修改 call_jaba_api 傳送 line_user_id
- [x] **檔案**: `app.py`
- [x] **位置**: `call_jaba_api()` 函式（約第 179-190 行）
- [x] **變更**:
  - 無論是否有 `group_id`，都要傳送 `line_user_id` 和 `display_name`
  - 修改邏輯：將 `line_user_id` 和 `display_name` 移到 `if group_id:` 區塊外面
- [x] **驗證**: 個人模式下 API payload 包含 `line_user_id`

## Phase 2: 更新 jaba 群組點餐邏輯

### 2.1 修改 build_context 使用 preferred_name
- [x] **檔案**: `/home/ct/SDD/jaba/app/ai.py`
- [x] **位置**: `build_context()` 群組模式區段（約第 88-133 行）
- [x] **變更**:
  - 從 `user_profile` 讀取 `preferred_name`
  - 設定 `ai_display_name = preferred_name or ai_username`
  - 將 `context["username"]` 設為 `ai_display_name`（而非 LINE 顯示名稱）
- [x] **驗證**: Python 語法檢查通過

### 2.2 簡化 group_ordering_prompt.md 使用者識別
- [x] **檔案**: `/home/ct/SDD/jaba/data/system/prompts/group_ordering_prompt.md`
- [x] **位置**: 「使用者識別」區段
- [x] **變更**:
  - 簡化說明：`username` 已經是正確的稱呼（系統自動處理 preferred_name）
  - AI 只需直接使用 `username` 即可
- [x] **驗證**: 檢視 prompt 內容

### 2.3 新增語氣調整指引（所有對話 prompts）
- [x] **檔案**:
  - `/home/ct/SDD/jaba/data/system/prompts/group_ordering_prompt.md`
  - `/home/ct/SDD/jaba/data/system/prompts/personal_prompt.md`
  - `/home/ct/SDD/jaba/data/system/prompts/manager_prompt.md`
- [x] **變更**:
  - 新增「語氣調整」小節
  - 若稱呼包含職稱（總、經理、主管、老闆等）→ 使用正式語氣、敬語（您）
  - 一般稱呼 → 親切口語（你）
- [x] **驗證**: 檢視各 prompt 內容

## Phase 3: 驗證整體流程

### 3.1 端對端測試
- [ ] 在 1對1 聊天中測試：
  1. 設定「叫我小明」→ 檢查 `data/users/{line_user_id}/profile.json` 存在
  2. 設定「我不吃辣」→ 檢查 profile 包含 dietary_restrictions
- [ ] 在群組中測試：
  1. 開單 → 點餐 → 確認呷爸使用「小明」稱呼
  2. 點麻辣類餐點 → 確認呷爸提醒不吃辣
