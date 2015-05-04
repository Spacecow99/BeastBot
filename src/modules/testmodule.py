import ConfigParser
import ircFunc
import errorhandling


def init():
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'testmodule', 'loaded')
    #config.set('Functions', 'commandhere', 'testmodule.functionname')

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()


def functionname(line, irc):
    splitline = line.split(" :")
    try:
        message = splitline[1]
        origmessage = message
        messagechars = message
        message = message.split(" ")
        username = line.split("!")[0].replace(':', '')
        msgto = line.split(" ")[2]
        command = message[0]
    except IndexError:
        errorhandling.errorlog('information', e, line)
    except Exception:
        errorhandling.errorlog('critical', e, line)
    to = msgto
    msg = origmessage.split(" ", 1)[1]
    ircFunc.ircSay(msgto, msg, irc)
