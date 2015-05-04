'''
    UrbanDictionary module for BeastBot
'''

import ConfigParser
import urllib
import json
import ircFunc
import mainFunc
import errorhandling


def init():
    modulename = "urban"
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'urban', 'loaded')
    config.set('Functions', 'ud', 'urban.urban')
    config.set('Functions', 'urban', 'urban.urban')
    config.set('Functions', 'wtf', 'urban.urban')

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()


def urban(line, irc):
    conf = mainFunc.getConfig()
    splitline = line.split(" :")
    message, whole, username, msgto = ircFunc.ircMessage(line.strip(), whl=True)
    try:
        if len(message) > 1:
            if msgto == conf['nick']:
                msgto = username
            msg2 = message[1].lower()
            if msg2.strip() in conf['admins'].lower().split(" "):
                msg = message[1].strip()
                definition = "The coolest god damn person you will ever know!"
                thumbsup = "1337"
                thumbsdown = "0"
                output = msg + ": " + definition + " Up: " + thumbsup + " Down: " + thumbsdown
                ircFunc.ircSay(msgto, output, irc)
            else:
                url = 'http://api.urbandictionary.com/v0/define?term=' + whole
                info = urllib.urlopen(url)
                try:
                    data = json.loads(info.read())
                    definition = data['list'][0]['definition'].replace("\n", " ").replace("\r", "")
                    thumbsup = data['list'][0]['thumbs_up']
                    thumbsdown = data['list'][0]['thumbs_down']
                    thumbsdown = str(thumbsdown)
                    thumbsup = str(thumbsup)
                    msg = whole.strip()
                    output = msg + ": " + definition + " Up: " + thumbsup + " Down: " + thumbsdown
                    ircFunc.ircSay(msgto, output, irc)
                except IndexError:
                    ircFunc.ircSay(msgto, 'No definition for: ' + whole, irc)
                except ValueError:
                    output = "Bad search term, bro"
                    # print output
                    ircFunc.ircSay(msgto, output, irc)
                except Exception, e:
                    errorhandling.errorlog('critical', e, line)
        else:
            output = "Please enter a search term"
            # print output
            ircFunc.ircSay(msgto, output, irc)
    except Exception, e:
        errorhandling.errorlog('critical', e, line)
