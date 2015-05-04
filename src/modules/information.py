import ConfigParser
import ircFunc
import mainFunc
import errorhandling
import os.path

def init():
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'information', 'loaded')
    config.set('Functions', 'showip', 'information.showip')
    config.set('Functions', 'about', 'information.about')
    config.set('Functions', 'commands', 'information.help')
    config.set('Functions', 'help', 'information.help')
    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()


def help(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    try:
        fullmsg = '-'.join(message[1:]).strip()
        if fullmsg == '':
            print fullmsg[100000]
        #message[1] = message[1].strip()
        if os.path.exists('conf/info/command-' + fullmsg):
            fh = open('conf/info/command-' + fullmsg)
            commandhelp = fh.readlines()
            for text in commandhelp:
                ircFunc.ircSay(username, text, irc)
        else:
            ircFunc.ircSay(username, 'No help for "' + fullmsg + '" command', irc)
    except IndexError:
        try:
            conf = mainFunc.getConfig()
            fh = open("conf/info/help", "r")
            help = fh.readlines()
            for text in help:
                ircFunc.ircSay(username, text, irc)
            if username in conf['admins'].split(" "):
                if (ircFunc.isRegged(username, irc)):
                    fh = open('conf/info/admin-help', 'r')
                    adminhelp = fh.readlines()
                    for text in adminhelp:
                        ircFunc.ircSay(username, text, irc)
        except Exception as e:
            errorhandling.errorlog('critical', e, line)
    except Exception as e:
        errorhandling.errorlog('critical', e, line)


def about(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    try:
        fh = open('conf/info/about', 'r')
        about = fh.readlines()
        for text in about:
            ircFunc.ircSay(username, text, irc)
    except Exception as e:
        errorhandling.errorlog('critical', e, line)


def showip(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    try:
        ircFunc.ircSay(msgto, username + ", my ip address appears to be 127.0.0.1", irc)
    except Exception, e:
        errorhandling.errorlog('critical', e, line)
