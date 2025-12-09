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
            timeout=10
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


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    """處理文字訊息 - 轉發到 jaba 系統"""
    user_text = event.message.text

    # 忽略空白訊息
    if not user_text or not user_text.strip():
        return

    # 取得使用者名稱（支援群組）
    username = get_user_display_name(event)

    # 呼叫 jaba API 取得回應
    reply_text = call_jaba_api(username, user_text)

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
