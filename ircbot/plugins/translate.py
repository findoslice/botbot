import requests
import json

from ircbot import bot

def translate(bot,text):
    api_key = bot.config['Yandex']['translate_key']
    lang = check_lang(bot, text)
    translate_url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}-{}".format(api_key, text, lang, bot.config["System"]["lang"])
    api_response = requests.get(translate_url).text
    api_json = json.loads(api_response)
    print(api_json)
    return api_json['text'][0]

def check_lang(bot,text):
    api_key = bot.config['Yandex']['translate_key']
    detect_url = "https://translate.yandex.net/api/v1.5/tr.json/detect?key={}&text={}".format(api_key, text)
    detect_response = requests.get(detect_url).text
    detect_json = json.loads(detect_response)
    return detect_json["text"]


@bot.hook()
def message_hook(bot, channel, sender, message):
    if check_lang(bot, message) != bot.config["System"]["lang"]:
        bot.message(channel, "translation: {}").format(translate(bot, message))
