import errorhandling
import mainFunc
import ConfigParser


def ircMode(chan, args, irc):
    irc.send("MODE %s %s\n" % (chan, args))


def ircSay(to, msg, irc):
#to=message to, msg=message to send, irc=socket
    irc.send("PRIVMSG %s :%s\n" % (to, msg))


def ircJoin(channel, irc):
#channel=channel to join, irc=socket
    channel = channel.strip()
    irc.send("JOIN %s\n" % (channel))
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    CurrentChannels = mainFunc.getConfig()
    CurrentChannels = CurrentChannels['tempchannels']
    if channel not in CurrentChannels.split(" "):
        NewChannels = str(CurrentChannels) + ' ' + str(channel)
        config.set('Main', 'tempchannels', NewChannels)
        with open('conf/beastbot.conf', 'wb') as configfile:
            config.write(configfile)


def ircPart(channel, irc):
#channel=channel to part, irc=socket
    channel = channel.strip()
    irc.send("PART %s\n" % (channel))
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    CurrentChannels = mainFunc.getConfig()
    CurrentChannels = CurrentChannels['tempchannels']
    NewChannels = CurrentChannels.replace(channel, '')
    config.set('Main', 'tempchannels', NewChannels)
    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)


def ircNick(newnick, irc):
#newnick=New nickname for the bot, irc=socket
    irc.send("NICK %s\n" % (newnick))
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Main', 'tempnick', newnick)
    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)


def isRegged(nick, irc):
    """Function to check is user is identified with nickserv.
        true if Nickserv says he's registered."""
    ircSay("NickServ", "STATUS %s " % (nick), irc)
    line = ""
    while line is "":
        ircSay("NickServ", "STATUS %s " % (nick), irc)
        line = irc.recv(512)
        print "REG TEST" + line
        if line.find("STATUS %s 3" % (nick)) != -1:
            return True
        else:
            return False


def announce(message, username, irc):
    conf = mainFunc.getConfig()
    message = ' '.join(message[1:])
    message = "ANOUNCEMENT FROM: " + str(username) + " - " + str(message)
    for channel in conf['tempchannels'].split(" "):
        ircSay(channel, message, irc)


def getMsgto(line):
    return line.split(" ")[2]


def getUsername(line):
    return line.split("!")[0][1:].lower()


def ircMessage(line, whl=False):
    """Func to process message received from server."""
    conf = mainFunc.getConfig()
    splitline = line.split(" :")
    try:
        origmessage = splitline[1]
        message = origmessage.split(" ")
        username = getUsername(line).lower()
        if getMsgto(line) == conf['nick']:
        # privmsg
            msgto = username
        else:
            msgto = getMsgto(line)
        if whl:
            parts = origmessage.split(" ", 1)
            if (len(parts) > 1):
                whole = parts[1]
            else:
                whole = ""
            return message, whole, username, msgto
        return message, username, msgto
    except IndexError as e:
        errorhandling.errorlog('information', e, line)
    except Exception as e:
        errorhandling.errorlog('critical', e, line)
