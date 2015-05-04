import ConfigParser
import ircFunc
import mainFunc
import errorhandling
import re


def init():
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'botadministration', 'loaded')
    config.set('Functions', 'join', 'botadministration.join')
    config.set('Functions', 'part', 'botadministration.part')
    config.set('Functions', 'nick', 'botadministration.changenick')
    config.set('Functions', 'set', 'botadministration.set')

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()


def set(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    conf = mainFunc.getConfig()
    if username in conf['admins'].split(" "):
        if (ircFunc.isRegged(username, irc)):
            try:
                if message[1].strip() == '':
                    del message[1]
                if message[1].strip() == 'admin':
                    try:
                        if message[2].strip() == '':
                            del message[2]
                        if message[2].strip() == 'add':
                            config = ConfigParser.ConfigParser()
                            config.read('conf/beastbot.conf')
                            CurrentAdmins = mainFunc.getConfig()
                            CurrentAdmins = CurrentAdmins['admins']
                            NewAdmins = str(CurrentAdmins) + ' ' + str(message[3])
                            NewAdmins = NewAdmins.lower()
                            config.set('Main', 'admins', NewAdmins)
                            with open('conf/beastbot.conf', 'wb') as configfile:
                                config.write(configfile)
                            if msgto == conf['tempnick']:
                                msgto = username
                            out = 'Admin list updated to: ' + NewAdmins
                            ircFunc.ircSay(msgto, out, irc)
                            out2 = "Please run '!bot-reload' to run theese new settings..."
                            # Need to find a way to fix this
                            ircFunc.ircSay(msgto, out2, irc)
                        elif message[2].strip() == 'del':
                            config = ConfigParser.ConfigParser()
                            config.read('conf/beastbot.conf')
                            CurrentAdmins = mainFunc.getConfig()
                            CurrentAdmins = CurrentAdmins['admins']
                            NewAdmins = CurrentAdmins.replace(message[3].strip(), '')
                            config.set('Main', 'admins', NewAdmins)
                            with open('conf/beastbot.conf', 'wb') as configfile:
                                config.write(configfile)
                            if msgto == conf['tempnick']:
                                msgto = username
                            out = 'Admin list updated to: ' + NewAdmins
                            ircFunc.ircSay(msgto, out, irc)
                            out2 = "Please run '!bot-reload' to run theese new settings..."
                            # Need to find a way to fix this
                            ircFunc.ircSay(msgto, out2, irc)
                        elif message[2].strip() == 'list':
                            conf = mainFunc.getConfig()
                            if msgto == conf['tempnick']:
                                msgto = username
                            ircFunc.ircSay(msgto, conf['admins'], irc)
                        else:
                            del message[2]
                            print message[2]
                    except IndexError:
                        out = "Options for 'set admin' are: add, del, list"
                        if msgto == conf['tempnick']:
                            msgto = username
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.errorlog('critical', e, line)
                if message[1].strip() == 'botban':
                    try:
                        if message[2].strip() == '':
                            del message[2]
                        if message[2].strip() == 'add':
                            config = ConfigParser.ConfigParser()
                            config.read('conf/beastbot.conf')
                            CurrentBans = mainFunc.getConfig()
                            CurrentBans = CurrentBans['botbanned']
                            NewBans = str(CurrentBans) + ' ' + str(message[3])
                            config.set('Main', 'botbanned', NewBans)
                            with open('conf/beastbot.conf', 'wb') as configfile:
                                config.write(configfile)
                            if msgto == conf['tempnick']:
                                msgto = username
                            out = 'Ban list updated to: ' + NewBans
                            ircFunc.ircSay(msgto, out, irc)
                            out2 = "Please run '!bot-reload' to run theese new settings..."
                            # Need to find a way to fix this
                            ircFunc.ircSay(msgto, out2, irc)
                        elif message[2].strip() == 'del':
                            config = ConfigParser.ConfigParser()
                            config.read('conf/beastbot.conf')
                            CurrentBans = mainFunc.getConfig()
                            CurrentBans = CurrentBans['botbanned']
                            NewBans = CurrentBans.replace(message[3].strip(), '')
                            config.set('Main', 'botbanned', NewBans)
                            with open('conf/beastbot.conf', 'wb') as configfile:
                                config.write(configfile)
                            if msgto == conf['tempnick']:
                                msgto = username
                            out = 'Ban list updated to: ' + NewBans
                            ircFunc.ircSay(msgto, out, irc)
                            out2 = "Please run '!bot-reload' to run theese new settings..."
                            # Need to find a way to fix this
                            ircFunc.ircSay(msgto, out2, irc)
                        elif message[2].strip() == 'list':
                            conf = mainFunc.getConfig()
                            if msgto == conf['tempnick']:
                                msgto = username
                            if conf['botbanned'].strip() == "":
                                out = "There are currently no nicks banned from the bot..."
                            else:
                                out = "Current nicks banned from the bot: " + conf['botbanned']
                            ircFunc.ircSay(msgto, out, irc)
                        else:
                            del message[2]
                            print message[2]
                    except IndexError:
                        out = "Options for 'set ban' are: add, del, list"
                        if msgto == conf['tempnick']:
                            msgto = username
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.errorlog('critical', e, line)
                elif message[1].strip() == 'channel':
                    try:
                        if message[2].strip() == '':
                            del message[2]
                        if message[2].strip() == 'add':
                            if re.search(',0', message[3]):
                                if msgto == conf['tempnick']:
                                    msgto = username
                                ircFunc.ircSay(msgto, 'No.... Just.... No......', irc)
                            else:
                                config = ConfigParser.ConfigParser()
                                config.read('conf/beastbot.conf')
                                CurrentChannels = mainFunc.getConfig()
                                CurrentChannels = CurrentChannels['channels']
                                NewChannels = str(CurrentChannels) + ' ' + str(message[3])
                                config.set('Main', 'channels', NewChannels)
                                with open('conf/beastbot.conf', 'wb') as configfile:
                                    config.write(configfile)
                                if msgto == conf['tempnick']:
                                    msgto = username
                                out = 'Channel list updated to: ' + NewChannels
                                ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'del':
                            config = ConfigParser.ConfigParser()
                            config.read('conf/beastbot.conf')
                            CurrentChannels = mainFunc.getConfig()
                            CurrentChannels = CurrentChannels['channels']
                            NewChannels = CurrentChannels.replace(message[3].strip(), '')
                            config.set('Main', 'channels', NewChannels)
                            with open('conf/beastbot.conf', 'wb') as configfile:
                                config.write(configfile)
                            if msgto == conf['tempnick']:
                                msgto = username
                            out = 'Channel list updated to: ' + NewChannels
                            ircFunc.ircSay(msgto, out, irc)
                        elif message[2].strip() == 'list':
                            conf = mainFunc.getConfig()
                            if msgto == conf['tempnick']:
                                msgto = username
                            ircFunc.ircSay(msgto, conf['channels'], irc)
                        else:
                            del message[2]
                            print message[2]
                    except IndexError:
                        out = "Options for 'set channel' are: add, del, list"
                        if msgto == conf['tempnick']:
                            msgto = username
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.errorlog('critical', e, line)
                elif message[1].strip() == 'nick':
                    try:
                        config = ConfigParser.ConfigParser()
                        config.read('conf/beastbot.conf')
                        config.set('Main', 'nick', message[2])
                        with open('conf/beastbot.conf', 'wb') as configfile:
                            config.write(configfile)
                        if msgto == conf['tempnick']:
                            msgto == username
                        ircFunc.ircSay(msgto, 'Default nickname set to: ' + message[2], irc)
                    except IndexError:
                        out = "You did not specify a new default nickname..."
                        if msgto == conf['tempnick']:
                            msgto = username
                        ircFunc.ircSay(msgto, out, irc)
                    except Exception as e:
                        errorhandling.errorlog('critical', e, line)
                else:
                    del message[1]
                    print message[1]
            except IndexError:
                out = "Options for 'set' are: admin, channel, nick"
                if msgto == conf['tempnick']:
                    msgto = username
                ircFunc.ircSay(msgto, out, irc)
            except Exception as e:
                errorhandling.errorlog('critical', e, line)


def changenick(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    conf = mainFunc.getConfig()
    if username in conf['admins'].split(" "):
        if (ircFunc.isRegged(username, irc)):
            try:
                if message[1]:
                    ircFunc.ircNick(message[1], irc)
                    print message[1]
            except IndexError:
                ircFunc.ircNick(conf['nick'], irc)
            except Exception as e:
                errorhandling.errorlog('critical', e, line)


def part(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    conf = mainFunc.getConfig()
    if username in conf['admins'].split(" "):
        if (ircFunc.isRegged(username, irc)):
            try:
                if message[1]:
                    ircFunc.ircPart(message[1], irc)
            except IndexError:
                ircFunc.ircSay(msgto, "No channel specified...", irc)
            except Exception as e:
                errorhandling.errorlog('critical', e, line)


def join(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    conf = mainFunc.getConfig()
    if username in conf['admins'].split(" "):
        if (ircFunc.isRegged(username, irc)):
            try:
                if re.search(',0', message[1]):
                    if msgto == conf['tempnick']:
                        msgto = username
                    ircFunc.ircSay(msgto, 'No....', irc)
                elif message[1]:
                    ircFunc.ircJoin(message[1], irc)
            except IndexError:
                splitchannels = conf['channels'].split(" ")
                for chan in splitchannels:
                    ircFunc.ircJoin(chan, irc)
            except Exception as e:
                errorhandling.errorlog('critical', e, line)
