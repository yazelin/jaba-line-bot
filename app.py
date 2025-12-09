"""Jaba LINE Bot - 呷爸 AI 午餐訂便當系統 LINE 介面"""
import os
import re
import sys

import requests
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, LeaveEvent, UnfollowEvent
from linebot.v3.exceptions import InvalidSignatureError

# 從環境變數載入設定
channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
jaba_api_url = os.environ.get("JABA_API_URL")  # 例: http://ching-tech.ddns.net/jaba-api
jaba_api_key = os.environ.get("JABA_API_KEY")  # API 驗證金鑰

if not channel_secret:
    print("錯誤：未設定 LINE_CHANNEL_SECRET 環境變數")
    sys.exit(1)

if not channel_access_token:
    print("錯誤：未設定 LINE_CHANNEL_ACCESS_TOKEN 環境變數")
    sys.exit(1)

# jaba 設定為可選（未設定時使用 Echo 模式）
if not jaba_api_url:
    print("警告：未設定 JABA_API_URL，將使用 Echo 模式")

# 初始化 Flask 應用
app = Flask(__name__)

# 初始化 LINE Bot SDK
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

# 觸發關鍵字（訊息開頭需包含這些詞才會回應）
TRIGGER_KEYWORDS = ["呷爸", "點餐", "jaba"]

# 啟用密碼（必須透過環境變數設定）
REGISTER_SECRET = os.environ.get("REGISTER_SECRET")


def get_jaba_headers() -> dict:
    """取得呼叫 jaba API 的 headers"""
    headers = {"Content-Type": "application/json"}
    if jaba_api_key:
        headers["X-API-Key"] = jaba_api_key
    return headers


def check_whitelist(id_value: str) -> dict:
    """檢查是否在白名單中"""
    if not jaba_api_url:
        return {"registered": True}  # 無 jaba 時不檢查

    try:
        response = requests.get(
            f"{jaba_api_url}/api/linebot/check/{id_value}",
            headers=get_jaba_headers(),
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"檢查白名單錯誤: {e}")

    return {"registered": False}


def check_group_session(group_id: str) -> bool:
    """檢查群組是否在點餐中"""
    if not jaba_api_url:
        return False

    try:
        response = requests.get(
            f"{jaba_api_url}/api/linebot/session/{group_id}",
            headers=get_jaba_headers(),
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("ordering", False)
    except Exception as e:
        print(f"檢查群組 session 錯誤: {e}")

    return False


def register_to_whitelist(
    id_type: str,
    id_value: str,
    name: str = "",
    activated_by_id: str = "",
    activated_by_name: str = ""
) -> dict:
    """註冊到白名單

    Args:
        id_type: "user" 或 "group"
        id_value: LINE user_id 或 group_id
        name: 顯示名稱（個人啟用時使用）
        activated_by_id: 啟用者的 LINE user_id
        activated_by_name: 啟用者的顯示名稱
    """
    if not jaba_api_url:
        return {"success": False, "message": "系統未設定"}

    try:
        payload = {
            "type": id_type,
            "id": id_value,
            "name": name,
            "activated_by": {
                "user_id": activated_by_id,
                "display_name": activated_by_name
            }
        }
        response = requests.post(
            f"{jaba_api_url}/api/linebot/register",
            json=payload,
            headers=get_jaba_headers(),
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "message": f"註冊失敗 ({response.status_code})"}
    except Exception as e:
        print(f"註冊錯誤: {e}")
        return {"success": False, "message": "系統連線錯誤"}


def unregister_from_whitelist(id_value: str) -> None:
    """從白名單移除（Bot 被踢出群組或使用者封鎖時呼叫）"""
    if not jaba_api_url:
        return

    try:
        response = requests.delete(
            f"{jaba_api_url}/api/linebot/unregister",
            json={"id": id_value},
            headers=get_jaba_headers(),
            timeout=5
        )
        if response.status_code == 200:
            print(f"已從白名單移除: {id_value}")
        else:
            print(f"移除白名單失敗 ({response.status_code}): {id_value}")
    except Exception as e:
        print(f"移除白名單錯誤: {e}")


def call_jaba_api(username: str, message: str, group_id: str | None = None) -> str:
    """呼叫 jaba API 取得回應

    Args:
        username: 使用者名稱
        message: 訊息內容
        group_id: 群組 ID（群組點餐時傳入）
    """
    if not jaba_api_url:
        return message  # Echo 模式

    try:
        payload = {
            "username": username,
            "message": message,
            "is_manager": False
        }
        if group_id:
            payload["group_id"] = group_id

        response = requests.post(
            f"{jaba_api_url}/api/chat",
            json=payload,
            headers=get_jaba_headers(),
            timeout=25  # 增加 timeout 以應對 AI 處理時間
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("message", "處理完成")
        else:
            return f"系統忙碌中，請稍後再試 ({response.status_code})"

    except requests.exceptions.Timeout:
        return "系統回應逾時，請稍後再試"
    except requests.exceptions.RequestException as e:
        print(f"呼叫 jaba API 錯誤: {e}")
        return "系統連線錯誤，請稍後再試"


def get_user_display_name(event) -> str:
    """取得使用者的 LINE 顯示名稱（支援群組和聊天室）"""
    user_id = event.source.user_id

    try:
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)

            # 根據來源類型使用不同 API
            if event.source.type == "group":
                # 群組：用 group_id 取得成員資料
                profile = messaging_api.get_group_member_profile(
                    event.source.group_id, user_id
                )
            elif event.source.type == "room":
                # 多人聊天室
                profile = messaging_api.get_room_member_profile(
                    event.source.room_id, user_id
                )
            else:
                # 1對1 聊天
                profile = messaging_api.get_profile(user_id)

            return profile.display_name
    except Exception:
        return user_id  # 無法取得時回傳 user_id


def get_source_id(event) -> tuple[str, str]:
    """取得來源 ID 和類型

    Returns:
        (id_value, id_type) - ID 值和類型 ("user" 或 "group")
    """
    if event.source.type == "group":
        return event.source.group_id, "group"
    elif event.source.type == "room":
        return event.source.room_id, "group"  # room 也當作 group 處理
    else:
        return event.source.user_id, "user"


@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook endpoint - 接收 LINE Platform 的訊息"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


def should_respond(event: MessageEvent, user_text: str) -> tuple[bool, str]:
    """判斷是否應該回應此訊息

    Returns:
        (should_respond, cleaned_message) - 是否回應、清理後的訊息
    """
    # 1對1 聊天：永遠回應
    if event.source.type == "user":
        return True, user_text

    # 群組/聊天室：使用 Session 機制
    text_stripped = user_text.strip()

    # 取得群組 ID
    if event.source.type == "group":
        group_id = event.source.group_id
    elif event.source.type == "room":
        group_id = event.source.room_id
    else:
        return False, user_text

    # 檢查群組是否在點餐中
    is_ordering = check_group_session(group_id)

    if is_ordering:
        # 點餐中：所有訊息都轉發給 jaba
        return True, user_text
    else:
        # 非點餐中：只回應「開始點餐」這 4 個字
        if text_stripped == "開始點餐":
            return True, user_text

        # 其他訊息完全忽略（包括關鍵字、@mention 等）
        return False, user_text


def handle_special_command(event: MessageEvent, command: str) -> str | None:
    """處理特殊指令（註冊密碼、ID查詢等），回傳回應訊息或 None"""
    cmd = command.strip()
    cmd_lower = cmd.lower()
    user_id = event.source.user_id
    source_type = event.source.type

    # 移除觸發關鍵字前綴（群組中可能帶有關鍵字）
    cmd_without_keyword = cmd
    for keyword in TRIGGER_KEYWORDS:
        if cmd_lower.startswith(keyword.lower()):
            cmd_without_keyword = cmd[len(keyword):].strip()
            break

    # === 啟用密碼 ===
    if REGISTER_SECRET and cmd_without_keyword == REGISTER_SECRET:
        source_id, id_type = get_source_id(event)
        name = get_user_display_name(event) if id_type == "user" else ""

        # 取得啟用者資訊（不論群組或個人，都記錄是誰啟用的）
        activator_id = user_id
        activator_name = get_user_display_name(event)

        result = register_to_whitelist(
            id_type, source_id, name,
            activated_by_id=activator_id,
            activated_by_name=activator_name
        )

        if result.get("success"):
            if result.get("already_registered"):
                if id_type == "group":
                    return "✅ 此群組已啟用，可以直接使用點餐功能！"
                else:
                    return "✅ 已啟用，可以直接使用點餐功能！"
            else:
                if id_type == "group":
                    return "🎉 群組啟用成功！\n\n現在群組成員可以使用點餐功能了。\n\n試試說「呷爸 今天吃什麼」"
                else:
                    return "🎉 啟用成功！\n\n現在你可以使用點餐功能了。\n\n試試說「今天吃什麼」"
        else:
            return f"❌ 啟用失敗：{result.get('message', '未知錯誤')}"

    # === ID 查詢指令 ===
    cmd_without_keyword_lower = cmd_without_keyword.lower()
    if cmd_without_keyword_lower in ["id", "群組id", "groupid", "userid"]:
        if source_type == "group":
            group_id = event.source.group_id
            return f"📋 ID 資訊\n\n群組 ID:\n{group_id}\n\n你的用戶 ID:\n{user_id}"
        elif source_type == "room":
            room_id = event.source.room_id
            return f"📋 ID 資訊\n\n聊天室 ID:\n{room_id}\n\n你的用戶 ID:\n{user_id}"
        else:
            return f"📋 ID 資訊\n\n你的用戶 ID:\n{user_id}"

    return None


def reply_message(event: MessageEvent, text: str):
    """回覆訊息"""
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=text)]
            )
        )


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    """處理文字訊息 - 轉發到 jaba 系統"""
    user_text = event.message.text

    # 忽略空白訊息
    if not user_text or not user_text.strip():
        return

    # 檢查是否應該回應（群組使用 Session 機制）
    should_reply, cleaned_message = should_respond(event, user_text)
    if not should_reply:
        return

    # 檢查是否為特殊指令（註冊、ID 查詢）- 這些不需要白名單
    special_response = handle_special_command(event, cleaned_message)
    if special_response:
        reply_message(event, special_response)
        return

    # 檢查白名單
    source_id, source_type = get_source_id(event)
    whitelist_check = check_whitelist(source_id)

    if not whitelist_check.get("registered"):
        # 未啟用，不提示具體方法（密碼制）
        if event.source.type == "group":
            reply_message(event, "⚠️ 此群組尚未啟用點餐功能。")
        else:
            reply_message(event, "⚠️ 你尚未啟用點餐功能。")
        return

    # 取得使用者名稱（支援群組）
    username = get_user_display_name(event)

    # 取得群組 ID（群組/聊天室時傳入）
    group_id = None
    if source_type == "group":
        group_id = source_id

    # 呼叫 jaba API 取得回應
    reply_text = call_jaba_api(username, cleaned_message, group_id)

    # 回覆訊息（空訊息不回覆，用於群組點餐時過濾非訂餐訊息）
    if reply_text and reply_text.strip():
        reply_message(event, reply_text)


@handler.add(LeaveEvent)
def handle_leave(event: LeaveEvent):
    """處理 Bot 被移出群組/聊天室事件 - 從白名單移除"""
    if event.source.type == "group":
        group_id = event.source.group_id
        print(f"Bot 被移出群組: {group_id}")
        unregister_from_whitelist(group_id)
    elif event.source.type == "room":
        room_id = event.source.room_id
        print(f"Bot 被移出聊天室: {room_id}")
        unregister_from_whitelist(room_id)


@handler.add(UnfollowEvent)
def handle_unfollow(event: UnfollowEvent):
    """處理使用者封鎖/取消追蹤事件 - 從白名單移除"""
    user_id = event.source.user_id
    print(f"使用者取消追蹤: {user_id}")
    unregister_from_whitelist(user_id)


@app.route("/", methods=["GET"])
def index():
    """首頁 - 顯示服務狀態"""
    mode = "jaba 模式" if jaba_api_url else "Echo 模式"
    return f"Jaba LINE Bot is running! ({mode})"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
