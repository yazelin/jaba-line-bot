"""Jaba LINE Bot - 呷爸 AI 午餐訂便當系統 LINE 介面"""
import os
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
from linebot.v3.webhooks import MessageEvent, TextMessageContent
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


def call_jaba_api(username: str, message: str) -> str:
    """呼叫 jaba API 取得回應"""
    if not jaba_api_url:
        return message  # Echo 模式

    try:
        headers = {"Content-Type": "application/json"}
        if jaba_api_key:
            headers["X-API-Key"] = jaba_api_key

        response = requests.post(
            f"{jaba_api_url}/api/chat",
            json={
                "username": username,
                "message": message,
                "is_manager": False
            },
            headers=headers,
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


# 觸發關鍵字（訊息開頭需包含這些詞才會回應）
TRIGGER_KEYWORDS = ["呷爸", "點餐", "jaba"]

# 管理指令（用於取得 ID 等）
ADMIN_COMMANDS = ["id", "群組id", "群組ID", "userid", "groupid"]


def should_respond(event: MessageEvent, user_text: str) -> tuple[bool, str]:
    """判斷是否應該回應此訊息

    Returns:
        (should_respond, cleaned_message) - 是否回應、清理後的訊息
    """
    # 1對1 聊天：永遠回應
    if event.source.type == "user":
        return True, user_text

    # 群組/聊天室：檢查觸發條件
    text_lower = user_text.lower().strip()

    # 檢查 @mention（LINE 的 mention 會在 message.mention 中）
    if hasattr(event.message, 'mention') and event.message.mention:
        # 有 @mention，移除 mention 文字後回應
        # mention 的文字格式通常是 @BotName
        cleaned = user_text
        for mentionee in event.message.mention.mentionees:
            # 移除 @mention 部分
            if mentionee.type == "user":
                # 取得 mention 的文字範圍並移除
                start = mentionee.index
                length = mentionee.length
                cleaned = cleaned[:start] + cleaned[start + length:]
        return True, cleaned.strip()

    # 檢查關鍵字開頭
    for keyword in TRIGGER_KEYWORDS:
        if text_lower.startswith(keyword.lower()):
            # 移除關鍵字，保留後面的內容
            cleaned = user_text[len(keyword):].strip()
            # 如果移除關鍵字後還有內容，就用清理後的；否則用原文
            return True, cleaned if cleaned else user_text

    # 不符合觸發條件
    return False, user_text


def handle_admin_command(event: MessageEvent, command: str) -> str | None:
    """處理管理指令，回傳回應訊息或 None（非管理指令）"""
    cmd_lower = command.lower().strip()

    # 檢查是否為 ID 查詢指令
    if cmd_lower in ["id", "群組id", "groupid", "userid"]:
        user_id = event.source.user_id
        source_type = event.source.type

        if source_type == "group":
            group_id = event.source.group_id
            return f"📋 ID 資訊\n\n群組 ID:\n{group_id}\n\n你的用戶 ID:\n{user_id}"
        elif source_type == "room":
            room_id = event.source.room_id
            return f"📋 ID 資訊\n\n聊天室 ID:\n{room_id}\n\n你的用戶 ID:\n{user_id}"
        else:
            return f"📋 ID 資訊\n\n你的用戶 ID:\n{user_id}"

    return None


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    """處理文字訊息 - 轉發到 jaba 系統"""
    user_text = event.message.text

    # 忽略空白訊息
    if not user_text or not user_text.strip():
        return

    # 檢查是否應該回應（群組中需要 @mention 或關鍵字觸發）
    should_reply, cleaned_message = should_respond(event, user_text)
    if not should_reply:
        return

    # 檢查是否為管理指令
    admin_response = handle_admin_command(event, cleaned_message)
    if admin_response:
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=admin_response)]
                )
            )
        return

    # 取得使用者名稱（支援群組）
    username = get_user_display_name(event)

    # 呼叫 jaba API 取得回應
    reply_text = call_jaba_api(username, cleaned_message)

    # 回覆訊息
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )


@app.route("/", methods=["GET"])
def index():
    """首頁 - 顯示服務狀態"""
    mode = "jaba 模式" if jaba_api_url else "Echo 模式"
    return f"Jaba LINE Bot is running! ({mode})"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
