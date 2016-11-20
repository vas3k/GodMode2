import telegram

from settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_CHANNEL_ID

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def post_new_story(text, url, disable_web_page_preview=False):
    if disable_web_page_preview:
        full_text = "{} {}".format(text, url)
    else:
        full_text = "{}\n\n{}".format(text, url)

    bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=full_text, disable_web_page_preview=disable_web_page_preview)
    bot.sendMessage(chat_id=TELEGRAM_CHANNEL_ID, text=full_text, disable_web_page_preview=disable_web_page_preview)
