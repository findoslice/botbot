import requests
import requests.exceptions
import rfc3987
from bs4 import BeautifulSoup
from ircbot import bot


@bot.hook()
def link_title_parse_hook(bot, channel, sender, message):
    for word in message.split(" "):
        try:
            if rfc3987.match(word, rule='URI'):
                r = requests.get(word)
                soup = BeautifulSoup(r.text, 'html.parser')
                bot.message(channel, " :: {}".format(soup.head.title.text))
        except requests.exceptions.InvalidSchema:
            pass
