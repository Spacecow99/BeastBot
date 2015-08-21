'''define.py
Written by: techb - nulldigit
Requires: BeatifulSoup4, Python2

Written for use with BeastBot from evilzone.org
Has not been tested with the bot.
'''

import urllib
from bs4 import BeautifulSoup
from inc import *

modFunc.addCommand('def', 'define', 'define')

def define(line, irc):
    splitline = line.split(" :")
    message, whole, username, msgto = ircFunc.ircMessage(line.strip(), whl=True)
    word = whole.strip()
    if msgto.lower() == configFunc.getBotConf('nickname').lower():
        msgto = username
    msg2 = message[1].lower()
    if msg2.strip():
        url = "http://dictionary.reference.com/browse/" + word
        info = urllib.urlopen(url)
        soup = BeautifulSoup(info.read(), "lxml")
        try:
            defset = soup.find_all("div", class_="def-content")
            out = "Def: %s" % defset[0].contents[0].strip()
            more = "More found %s%s" % (url, word)
            ircFunc.ircSay(msgto, out, irc)
            ircFunc.ircSay(msgto, more, irc)
        except:
            ircFunc.ircSay(msgto, "Word not found", irc)
