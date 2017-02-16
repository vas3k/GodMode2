import telegram

from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_CHANNEL_ID

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def post_new_story(text, to_chat=True, to_channel=True):
    if to_chat:
        bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=text, disable_web_page_preview=False)

    if to_channel:
        bot.sendMessage(chat_id=TELEGRAM_CHANNEL_ID, text=text, disable_web_page_preview=False)
