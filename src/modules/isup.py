'''
    ISUP module for BeastBot
'''

import ConfigParser
import urllib
import json
import ircFunc
import mainFunc
import errorhandling

def init():
    modulename = "isup"
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'isup', 'loaded')
    config.set('Functions', 'isup', 'isup.isup')

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()

def isup(line, irc):
    # print line
    conf = mainFunc.getConfig()
    splitline = line.split(" :")
    message, username, msgto = ircFunc.ircMessage(line, whl=False)
    try:
        if (len(message) > 1):
            output = ""
            if (len(message[1].split(".")) > 1):
                if ("http://" not in message[1]):
                    message[1] = "http://"+message[1]
                try:
                    respCode = urllib.urlopen(message[1]).getcode()
                    if (respCode == 200): # OK
                        output = "It's just you - %s seems up from here" % message[1]
                    elif ((respCode == 301) or (respCode == 302)): # Moved temporarily or permanetly
                        output = "It's not just you - %s seems to be moved" % message[1]
                    else:
                        output = "It's not just you - %s seems down from here" % message[1]
                except IOError:
                    output = "It's not just you - %s seems down from here" % message[1]
                ircFunc.ircSay(msgto, output, irc)
            else:
                ircFunc.ircSay(msgto, "Not a proper website address", irc)
        else:
            ircFunc.ircSay(msgto, "No website given", irc)
    except Exception, e:
        errorhandling.errorlog('critical', e, line)