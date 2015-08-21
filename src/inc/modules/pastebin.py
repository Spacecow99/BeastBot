''' requires google module.
    google-1.7
    https://pypi.python.org/pypi/google
    can use pip to install: pip2 install google
    
    It gives warning from internel use of Beautiful soup
      but shouldn't show up in IRC, just in the terminal the
      bot is running on.
'''

from google import search
from inc import *

modFunc.addCommand('paste', 'pastebin', 'pastebin')

def results(term):
    base = "site:pastebin.com "
    fullterm = base+term.strip()
    urls = []
    for s in search(fullterm, num=3, stop=3):
        urls.append(s)

    return urls

def pastebin(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    query = ' '.join(message[1:]).strip()
    urls = results(query)
    for url in urls:
        ircFunc.ircSay(msgto, url, irc)

