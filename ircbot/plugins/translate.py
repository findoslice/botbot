import requests
import json

from langdetect import detect, detect_langs
from ircbot import bot


def translate(bot, text):
    api_key = bot.config['Yandex']['translate_key']
    lang = detect(text)
    translate_url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}-{}".format(api_key, text, lang, bot.config["System"]["lang"])
    api_response = requests.get(translate_url).text
    api_json = json.loads(api_response)
    print(api_json)
    return api_json['text'][0]


@bot.hook()
def message_hook(bot, channel, sender, message):
    # gibberish messages are still assigned a language, however the level of confidence is always less than 0.9
    if detect(message) != bot.config["System"]["lang"] and float(str(detect_langs(message)[0])[3:]) < 0.9:
        bot.message(channel, "translation: {}").format(translate(bot, message))
