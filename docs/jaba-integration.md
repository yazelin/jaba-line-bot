# jaba 整合說明

本文件說明 LINE Bot 如何與 jaba 午餐訂便當系統整合。

## 系統關係

```
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│   LINE Bot      │  HTTPS   │     nginx       │  HTTP    │   jaba 系統      │
│   (Render)      │ ───────> │  (API Gateway)  │ ───────> │  (FastAPI)      │
│                 │          │                 │          │                 │
│  轉發 LINE 訊息  │          │  驗證 API Key   │          │  AI 點餐核心    │
└─────────────────┘          └─────────────────┘          └─────────────────┘
```

## jaba 系統簡介

jaba 是一個 AI 午餐訂便當系統，提供：

- **AI 對話**：理解自然語言點餐指令
- **訂單管理**：新增、修改、取消訂單
- **店家管理**：管理合作店家與菜單
- **統計報表**：訂餐統計與結算

LINE Bot 作為 jaba 的前端介面，讓使用者可以透過 LINE 與 jaba 互動。

## API 端點

LINE Bot 會呼叫以下 jaba API：

### 1. 對話 API

用於轉發使用者訊息到 jaba AI。

```
POST /api/chat
```

**Request：**
```json
{
    "username": "王小明",
    "message": "我要一個雞腿便當",
    "is_manager": false
}
```

**Response：**
```json
{
    "message": "好的，已為王小明點了一個雞腿便當（85元）",
    "actions": [...],
    "action_results": [...]
}
```

### 2. 白名單檢查 API

檢查使用者/群組是否已啟用。

```
GET /api/linebot/check/{id_value}
```

**Response：**
```json
{
    "registered": true
}
```

### 3. 白名單註冊 API

註冊新的使用者/群組到白名單。

```
POST /api/linebot/register
```

**Request：**
```json
{
    "type": "user",
    "id": "U1234567890abcdef",
    "name": "王小明"
}
```

**Response：**
```json
{
    "success": true,
    "already_registered": false
}
```

## nginx 設定

nginx 作為 API Gateway，負責：

1. **路徑轉發**：將 `/jaba-api/*` 轉發到 jaba 系統
2. **API Key 驗證**：只允許帶有正確 API Key 的請求

### 設定範例

```nginx
# 預設 server
server {
    listen 80 default_server;
    server_name _;

    # LINE Bot jaba API（需要 API Key 驗證）
    location /jaba-api/ {
        # API Key 驗證
        if ($http_x_api_key != "your_secret_api_key") {
            return 403;
        }

        # 代理到 jaba 服務
        proxy_pass http://192.168.11.9:8098/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 延長 timeout（AI 回應需要時間）
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

### 設定步驟

1. 編輯 nginx 設定檔：
   ```bash
   sudo vim /etc/nginx/sites-available/default
   ```

2. 加入上述 location 區塊

3. 測試設定：
   ```bash
   sudo nginx -t
   ```

4. 重新載入 nginx：
   ```bash
   sudo systemctl reload nginx
   ```

### 驗證設定

測試 API Key 驗證是否正常：

```bash
# 無 API Key - 應該回傳 403
curl http://ching-tech.ddns.net/jaba-api/api/status

# 有 API Key - 應該正常回應
curl -H "X-API-Key: your_secret_api_key" http://ching-tech.ddns.net/jaba-api/api/status
```

## jaba 白名單 API

jaba 系統需要有以下 API 端點來支援白名單功能：

### 新增端點（在 jaba 的 main.py）

```python
# LINE Bot 白名單 API
@app.get("/api/linebot/check/{id_value}")
async def check_linebot_whitelist(id_value: str):
    """檢查是否在白名單中"""
    whitelist = data.get_linebot_whitelist()
    registered = id_value in whitelist
    return {"registered": registered}


@app.post("/api/linebot/register")
async def register_linebot(request: Request):
    """註冊到白名單"""
    body = await request.json()
    id_type = body.get("type")  # "user" 或 "group"
    id_value = body.get("id")
    name = body.get("name", "")

    if not id_type or not id_value:
        return JSONResponse({"success": False, "message": "缺少必要參數"}, status_code=400)

    whitelist = data.get_linebot_whitelist()

    if id_value in whitelist:
        return {"success": True, "already_registered": True}

    # 加入白名單
    whitelist[id_value] = {
        "type": id_type,
        "name": name,
        "registered_at": datetime.now().isoformat()
    }
    data.save_linebot_whitelist(whitelist)

    return {"success": True, "already_registered": False}
```

### 資料儲存

白名單資料儲存在 jaba 的 data 目錄：

```
jaba/
└── data/
    └── linebot_whitelist.json
```

格式：
```json
{
    "U1234567890abcdef": {
        "type": "user",
        "name": "王小明",
        "registered_at": "2024-01-15T10:30:00"
    },
    "C9876543210fedcba": {
        "type": "group",
        "name": "",
        "registered_at": "2024-01-15T11:00:00"
    }
}
```

## 訊息流程

### 一般點餐

```
使用者                LINE Bot              jaba
  │                     │                    │
  │ "我要雞腿便當"      │                    │
  │ ──────────────────> │                    │
  │                     │ 1. 檢查白名單       │
  │                     │ ─────────────────> │
  │                     │ <───────────────── │
  │                     │    registered:true │
  │                     │                    │
  │                     │ 2. 轉發訊息        │
  │                     │ ─────────────────> │
  │                     │                    │ AI 處理
  │                     │ <───────────────── │
  │                     │   "已點雞腿便當"   │
  │ "已點雞腿便當"      │                    │
  │ <────────────────── │                    │
```

### 啟用流程

```
使用者                LINE Bot              jaba
  │                     │                    │
  │ "<啟用密碼>"        │                    │
  │ ──────────────────> │                    │
  │                     │ 識別為啟用指令      │
  │                     │                    │
  │                     │ 呼叫註冊 API        │
  │                     │ ─────────────────> │
  │                     │                    │ 加入白名單
  │                     │ <───────────────── │
  │                     │   success:true    │
  │ "啟用成功！"        │                    │
  │ <────────────────── │                    │
```

## Echo 模式

如果未設定 `JABA_API_URL`，LINE Bot 會進入 Echo 模式：

- 不連接 jaba 系統
- 直接回傳使用者發送的訊息
- 用於測試 LINE Bot 是否正常運作

## 錯誤處理

### API 連線錯誤

```python
except requests.exceptions.RequestException as e:
    print(f"呼叫 jaba API 錯誤: {e}")
    return "系統連線錯誤，請稍後再試"
```

### 逾時處理

```python
except requests.exceptions.Timeout:
    return "系統回應逾時，請稍後再試"
```

## 除錯技巧

### 1. 檢查 nginx 日誌

```bash
# 存取日誌
sudo tail -f /var/log/nginx/access.log

# 錯誤日誌
sudo tail -f /var/log/nginx/error.log
```

### 2. 檢查 jaba 日誌

```bash
# 查看 jaba 輸出
journalctl -u jaba -f
```

### 3. 測試 API 連線

```bash
# 從 Render 測試連線（模擬 LINE Bot）
curl -X POST "http://ching-tech.ddns.net/jaba-api/api/chat" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"username": "測試", "message": "今天吃什麼", "is_manager": false}'
```

## 安全注意事項

1. **API Key 保密**：不要將 API Key 寫在程式碼中
2. **HTTPS**：Render 自動提供 HTTPS，確保傳輸安全
3. **白名單**：只有啟用的使用者才能使用功能
4. **密碼啟用**：啟用密碼透過環境變數設定

## 相關文件

- [系統架構](architecture.md)
- [環境變數說明](configuration.md)
- [部署指南](deployment.md)
