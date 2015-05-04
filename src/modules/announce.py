import ConfigParser
import ircFunc
import mainFunc
import errorhandling


def init():
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'announce', 'loaded')
    config.set('Functions', 'announce', 'announce.announceInit')

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()


def announceInit(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    conf = mainFunc.getConfig()
    if username in conf['admins'].split(" "):
        if (ircFunc.isRegged(username, irc)):
            try:
                if message[1]:
                    ircFunc.announce(message, username, irc)
            except IndexError:
                if msgto == conf['tempnick']:
                    msgto = username
                ircFunc.ircSay(msgto, 'You did not enter a announcement to make', irc)
            except Exception as e:
                errorhandling.errorlog('critical', e, line)
