# Tasks: clarify-personal-mode-scope

## Phase 1: 修正 jaba-line-bot 訊息文案

### 1.1 更新 generate_help_message() 個人模式區段
- [x] **檔案**: `app.py`
- [x] **位置**: `generate_help_message()` 函式的個人模式區段（約第 367-379 行）
- [x] **變更**:
  - 將「直接說出餐點即可點餐」等點餐指引改為偏好設定功能說明
  - 新增說明：點餐請透過 LINE 群組
- [x] **驗證**: 在 1對1 聊天中輸入 `@jaba 呷爸` 確認顯示正確訊息

### 1.2 更新個人啟用成功訊息
- [x] **檔案**: `app.py`
- [x] **位置**: `handle_special_command()` 函式中個人啟用成功的回覆（約第 426、431 行）
- [x] **變更**:
  - 第 426 行（已啟用）：改為「已啟用！你可以在這裡設定個人偏好。要點餐請加入群組喔！」
  - 第 431 行（新啟用）：改為引導設定偏好的訊息
- [x] **驗證**: 在 1對1 聊天中輸入啟用密碼確認顯示正確訊息

## Phase 2: 更新 README 文件

### 2.1 修正功能特色描述
- [x] **檔案**: `README.md`
- [x] **位置**: 功能特色區段（約第 47-51 行）
- [x] **變更**:
  - 「1對1 聊天：直接與 Bot 對話即可點餐」改為「1對1 聊天：設定個人偏好（名稱、飲食限制）」
- [x] **驗證**: 檢視 README 功能特色區段

### 2.2 修正觸發方式表格
- [x] **檔案**: `README.md`
- [x] **位置**: 觸發方式表格（約第 84-91 行）
- [x] **變更**:
  - 「1對1 聊天：任何訊息都會處理」改為「1對1 聊天：偏好設定相關訊息」
- [x] **驗證**: 檢視 README 觸發方式表格

## Phase 3: 更新 OpenSpec

### 3.1 更新 line-bot-core spec
- [x] **檔案**: `openspec/specs/line-bot-core/spec.md`
- [x] **變更**:
  - 新增 Requirement 說明個人模式僅提供偏好設定功能
  - 更新相關 Scenario 描述
- [x] **驗證**: `openspec validate --specs`

## Phase 4: 修正 jaba 系統偏好設定功能

### 4.1 修正 update_user_profile_by_line_id 缺少 preferred_name
- [x] **檔案**: `/home/ct/SDD/jaba/app/data.py`
- [x] **位置**: `update_user_profile_by_line_id()` 函式（約第 374 行）
- [x] **變更**:
  - 在允許更新的欄位清單中加入 `preferred_name`
- [x] **驗證**: Python 語法檢查通過

### 4.2 修正群組模式下 update_user_profile 使用正確識別碼
- [x] **檔案**: `/home/ct/SDD/jaba/app/ai.py`
- [x] **位置**: `execute_action()` 中 `update_user_profile` 處理（約第 700 行）
- [x] **變更**:
  - 群組模式下使用 `line_user_id` 而非 `username`
- [x] **驗證**: Python 語法檢查通過

## Phase 5: 實作 jaba 系統個人偏好設定模式

### 5.1 新增 personal_prompt.md
- [x] **檔案**: `/home/ct/SDD/jaba/data/system/prompts/personal_prompt.md`
- [x] **變更**:
  - 建立個人偏好設定模式的 AI prompt
  - 明確指示只能設定偏好，不能點餐
- [x] **驗證**: 檔案存在

### 5.2 修改 get_system_prompt 支援個人模式
- [x] **檔案**: `/home/ct/SDD/jaba/app/ai.py`
- [x] **變更**:
  - 新增 `personal_mode` 參數
  - 個人模式載入 `personal_prompt`
- [x] **驗證**: Python 語法檢查通過

### 5.3 修改 build_context 支援個人模式
- [x] **檔案**: `/home/ct/SDD/jaba/app/ai.py`
- [x] **變更**:
  - 新增 `personal_mode` 參數
  - 個人模式只提供使用者偏好資訊
- [x] **驗證**: Python 語法檢查通過

### 5.4 修改 call_ai 支援個人模式
- [x] **檔案**: `/home/ct/SDD/jaba/app/ai.py`
- [x] **變更**:
  - 新增 `personal_mode` 參數
  - 傳遞給 `get_system_prompt` 和 `build_context`
- [x] **驗證**: Python 語法檢查通過

### 5.5 修改 /api/chat 允許個人模式
- [x] **檔案**: `/home/ct/SDD/jaba/main.py`
- [x] **變更**:
  - 移除對個人模式的完全阻擋
  - 新增 `personal_mode` 變數判斷
  - 傳遞給 `ai.call_ai` 和 `ai.execute_actions`
- [x] **驗證**: Python 語法檢查通過

### 5.6 在 execute_action 中阻擋個人模式點餐
- [x] **檔案**: `/home/ct/SDD/jaba/app/ai.py`
- [x] **變更**:
  - `execute_actions` 和 `execute_action` 新增 `personal_mode` 參數
  - 個人模式下只允許 `update_user_profile` 動作
- [x] **驗證**: Python 語法檢查通過

### 5.7 修改 get_jaba_prompt 讀取 personal_prompt.md
- [x] **檔案**: `/home/ct/SDD/jaba/app/data.py`
- [x] **變更**:
  - 新增讀取 `personal_prompt.md` 的邏輯
- [x] **驗證**: Python 語法檢查通過

## Phase 6: 驗證整體流程

### 6.1 端對端測試
- [ ] 在 1對1 聊天中測試：
  1. 未啟用時輸入 `@jaba 呷爸` → 顯示未啟用提示
  2. 輸入啟用密碼 → 顯示啟用成功（引導偏好設定）
  3. 已啟用時輸入 `@jaba 呷爸` → 顯示偏好設定功能說明
  4. 嘗試點餐（如「我要雞腿便當」）→ 呷爸回覆引導至群組點餐
  5. 設定偏好（如「叫我小明」）→ 正確儲存到 profile.json
  6. 在群組點餐時確認偏好被正確讀取
