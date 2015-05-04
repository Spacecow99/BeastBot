import ConfigParser
import re
import time
import os
from multiprocessing import Process


def main():
    irc = mainFunc.CreateSocket()
    conf = mainFunc.getConfig()
    functions = mainFunc.getFunctions()
    while True:
        try:
            line = irc.recv(512)
        except Exception as e:
            # print "IRC Socket Disconnected"
            errorhandling.errorlog('information', e, 'Bot disconnected')
            exit()

        # if line:
        #   print line
        # Commented out sense we usually do not have to see what the bot sees.

        if line[0:4] == "PING":
            splitline = line.split(" :")
            pong = "PONG %s" % splitline[1]
            irc.send(pong)
            # print pong
        try:
            if ircFunc.getUsername(line) not in conf['botbanned'].split(" "):
                if line.split(" ")[3][1] == conf['cominit']:
                    command = line.split(" ")[3][2:]
                    if command[0:4] == "bot-":
                        if ircFunc.getUsername(line) in conf['admins'].split(" "):
                            if (ircFunc.isRegged(ircFunc.getUsername(line), irc)):
                                command = command.replace("bot-", "").strip()
                                if command == "reload":
                                    mainFunc.reloadImports()
                                    conf = mainFunc.getConfig()
                                    functions = mainFunc.getFunctions()
                                    modules = mainFunc.getModules()
                                    if conf['nick'] == ircFunc.getMsgto(line):
                                        msgto = ircFunc.getUsername(line)
                                    else:
                                        msgto = ircFunc.getMsgto(line)
                                    ircFunc.ircSay(msgto, 'Configuration reloaded...', irc)
                                elif command == "update":
                                    ircFunc.ircSay(ircFunc.getMsgto(line), 'Shutting down for updates...', irc)
                                    mainFunc.cleanConfig()
                                    irc.close()
                                    time.sleep(3)
                                    os.system('./pullupdates.sh')
                                    # Bot should not hit this line
                                    errorhandling.errorlog('critical', 'Error pulling updates.')
                                    exit()
                                elif command == "restart":
                                    ircFunc.ircSay(ircFunc.getMsgto(line), 'Restarting Bot....', irc)
                                    mainFunc.cleanConfig()
                                    irc.close()
                                    time.sleep(3)
                                    os.system('./restart.sh')
                                    #Bot should not hit this line
                                    errorhandling.errorlog('critical', 'Error restarting')
                                    exit()
                                elif command == "quit":
                                    ircFunc.ircSay(ircFunc.getMsgto(line), 'Shutting down...', irc)
                                    mainFunc.cleanConfig()
                                    irc.close()
                                    time.sleep(1)
                                    exit()
                                elif command == "pull":
                                    if conf['nick'] == ircFunc.getMsgto(line):
                                        msgto = ircFunc.getUsername(line)
                                    else:
                                        msgto = ircFunc.getMsgto(line)
                                    ircFunc.ircSay(msgto, 'Pulling from github...', irc)
                                    os.system('git pull')
                                    ircFunc.ircSay(msgto, 'Done pulling from github...', irc)
                    else:
                        try:
                            command = command.strip()
                            function = functions[command]
                            functionProc = Process(target=eval(function), args=(line.strip(), irc,))
                            functionProc.daemon = True
                            functionProc.start()
                            functionProc.join()
                        except KeyError:
                            #Command does not exist
                            pass
                        except Exception, e:
                            errorhandling.errorlog('critical', e)
                elif line.split(" ")[3][1:5] == "http":
                    try:
                        function = functions['http']
                        functionProc = Process(target=eval(function), args=(line, irc,)).start()
                    except Exception, e:
                        errorhandling.errorlog('critical', e)
                elif re.match("^:[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9\-\.]+\.(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU) 001 " + conf['nick'] + " :Welcome", line):
                    splitchannels = conf['channels'].split(" ")
                    for chan in splitchannels:
                        ircFunc.ircJoin(chan, irc)
                        #irc.send("JOIN %s\n" % (chan))
                elif re.search(":This nickname is registered and protected.", line):
                    ircFunc.ircSay("NICKSERV", "identify " + conf['password'], irc)
                elif line[0:20] == "ERROR :Closing Link:":
                    errorhandling.loginfo("Bot disconnected due to ping timeout...")
                    errorhandling.loginfo('Reconnecting in 30 seconds...')
                    time.sleep(30)
                    errorhandling.loginfo("Reconnecting now....")
                    irc = mainFunc.CreateSocket()
        except IndexError:
            # Invalid command or Server sent message
            pass
        except Exception, e:
            errorhandling.errorlog('critical', e)


def cleanConfig():
    config = ConfigParser.RawConfigParser()
    config.read('conf/beastbot.conf')
    config.remove_section('Functions')
    config.remove_section('Modules')
    config.add_section('Modules')
    config.add_section('Functions')
    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)


def loadImports(path):
    files = os.listdir(path)
    imps = []
    for i in range(len(files)):
        name = files[i].split('.')
        if len(name) > 1:
            if name[1] == 'py' and name[0] != '__init__':
                name = name[0]
                imps.append(name)
    file = open(path + '__init__.py', 'w')
    toWrite = '__all__ =' + str(imps)
    file.write(toWrite)
    file.close()
cleanConfig()
loadImports('modules/')
from modules import *

if __name__ == "__main__":
    main()
