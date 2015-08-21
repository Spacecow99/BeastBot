from inc import *

modFunc.addCommand('suggest', 'suggest', 'suggest')
modFunc.addCommand('sug', 'suggest', 'suggest')
modFunc.addCommand('issue', 'suggest', 'suggest')
modFunc.addCommand('sug-read', 'suggest', 'read')
modFunc.addCommand('sug-clear', 'suggest', 'clear')

def suggest(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    combinedMsg = ' '.join(message[1:])
    numArgs = len(message) - 1
    if numArgs > 0 and combinedMsg.strip() != "":
        f = open('suggestions.txt' , 'a') 
        f.write(username + ': ' + combinedMsg)
        f.close()
        ircFunc.ircSay(username, '%s, thank you for your suggestion... It has been documented and will be reviewed. :)' % username, irc)
    else:
        ircFunc.ircSay(username, 'You didnt even suggest anything... :/   Command usage is : !suggest <suggestion goes here>', irc)


def read(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if username in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username, irc)):
            with open('suggestions.txt') as sugfile:
                print 'in with'
                for sugline in sugfile:
                    ircFunc.ircSay(msgto, sugline, irc)

def clear(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if username.lower() in configFunc.getBotConf('botadmins').split(" "):
        if (ircFunc.isRegged(username, irc)):
            f = open('suggestions.txt', 'w')
            f.write('Suggestions:' + '\n')
            f.close()
            ircFunc.ircSay(username, 'Suggestions Cleared.....', irc)
