import telegram

from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_CHANNEL_ID

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def post_new_365(text, to_chat=True, to_channel=True):
    if to_chat:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, disable_web_page_preview=True, disable_notification=True)

    if to_channel:
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=text, disable_web_page_preview=True, disable_notification=True)


def post_picture(image, to_chat=True, to_channel=True):
    if to_chat:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image, disable_notification=True)

    if to_channel:
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, photo=image, disable_notification=True)
