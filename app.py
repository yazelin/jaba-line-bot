"""Jaba LINE Bot - 呷爸 AI 午餐訂便當系統 LINE 介面"""
import os
import sys

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

# 從環境變數載入 LINE 憑證
channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not channel_secret:
    print("錯誤：未設定 LINE_CHANNEL_SECRET 環境變數")
    sys.exit(1)

if not channel_access_token:
    print("錯誤：未設定 LINE_CHANNEL_ACCESS_TOKEN 環境變數")
    sys.exit(1)

# 初始化 Flask 應用
app = Flask(__name__)

# 初始化 LINE Bot SDK
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook endpoint - 接收 LINE Platform 的訊息"""
    # 取得簽名
    signature = request.headers.get("X-Line-Signature", "")

    # 取得請求內容
    body = request.get_data(as_text=True)

    # 驗證簽名並處理事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    """處理文字訊息 - Echo 回覆"""
    # 取得使用者發送的文字
    user_text = event.message.text

    # 忽略空白訊息
    if not user_text or not user_text.strip():
        return

    # Echo 回覆相同的文字
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        messaging_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=user_text)]
            )
        )


@app.route("/", methods=["GET"])
def index():
    """首頁 - 顯示服務狀態"""
    return "Jaba LINE Bot is running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
