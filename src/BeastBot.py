import re
import time
import os
from multiprocessing import Process, Manager
import sys
import importlib


def main():
    global conf
    global module
    # Connect to the socket
    irc = mainFunc.CreateSocket(conf['server'], conf['port'])
    # Authenticate to the IRC server
    mainFunc.Auth(conf['username'], conf['nickname'], conf['realname'], irc)

    while True:
        try:
            line = irc.recv(512)
        except Exception as e:
            # Bot disconnected
            errorhandling.inputInfo('Bot disconnected unexpectedly')
            exit()

        '''
        Commented out sense we usually do not have to see what the bot sees.
        Used for testing and debugging purposes
        '''
        if line:
            print line

        if line[0:4] == "PING":
            # Receives PING from server and sends back PONG
            irc.send("PONG " + line.split(" :")[1])
        elif re.search("PING :", line):
            irc.send("PONG " + line.split(" :")[1])
            try:
                # Sometimes ping messages get sent on the same line.
                irc.send("PONG " + line.split(" :")[2])
            except IndexError:
                pass
                # This is normal
            except Exception as e:
                errorhandling.inputError('critical', e, line)
                
        if ("STATUS") in line and ircFunc.getUsername(line).lower() == 'nickserv':
            if re.search(" 3 " , line):
                ircFunc.updateReg(line.split(" ")[4].strip(), True)
            else:
                ircFunc.updateReg(line.split(" ")[4].strip(), False)
        try:
            # Checks if user is banned from using the bot. If not it proceeds
            username = ircFunc.getUsername(line).lower()
            if username.lower() not in conf['botbanned'].lower().split(" "):
                # Checks if the command starts with the command initializer
                if line.split(" ")[3][1:5] == "http":
                    try:
                        line = line.replace("http", "!http")
                    except Exception:
                        pass
                if line.split(" ")[3][1] == conf['cominit']:
                    command = line.split(" ")[3][2:]
                    if command[0:4] == 'http':
                        command = 'http'
                    try:
                        command = command.strip()
                        # Gets information for the command to run
                        mod, function = modFunc.getCommand(command, loaded=True)
                        # If command doesnt exist, mod will equal Boolean False
                        if mod != False:
                            # Sense the command exists... RUN IT
                            try:
                                functionProc = Process(target=getattr(module[mod], function), args=(line, irc,))
                                functionProc.daemon = True
                                functionProc.start()
                            except KeyError:
                                module[mod] = importlib.import_module(mod)
                                functionProc = Process(target=getattr(module[mod], function), args=(line, irc,))
                                functionProc.daemon = True
                                functionProc.start()
                            except Exception as e:
                                errorhandling.inputError('critical', e, line)

                            #functionProc.join()
                        else:
                            # Command did not exist
                            # Proceed with admin functions
                            if username in conf['botadmins'].lower().split(" "):
                                # Checks if user is a admin
                                if ircFunc.isRegged2(username, irc):
                                    # makes sure user is identified with nickserv
                                    if command == 'quit':
                                        errorhandling.inputInfo('Quiting: Command directed by: ' + username)
                                        irc.close()
                                        exit()
                                    elif command == 'update':
                                        ircFunc.ircSay(ircFunc.getMsgto(line), 'Shutting down for updates....', irc)
                                        errorhandling.inputInfo('Shutting down for updates: Command directed by: ' + username)
                                        irc.close()
                                        os.system('./pullupdates.sh')
                                        # Bot shouldnt go past this point
                                        errorhandling.inputError('critical', 'Bot failed updating by command. Reached the line it wasnt suppose to.', line)
                                        exit()
                                    elif command == 'restart':
                                        ircFunc.ircSay(ircFunc.getMsgto(line), 'Restarting bot...', irc)
                                        errorhandling.inputInfo('Restarting bot: Command directed by: ' + username)
                                        irc.close()
                                        os.system('./restart.sh')
                                        # Bot shouldnt go past this point
                                        errorhandling.inputError('critical', 'Bot failed restarting by command. Reached the line it wasnt suppose to.', line)
                                        exit()
                                    elif command == 'gitpull':
                                        errorhandling.inputInfo("Pulling from git : Command directed by: " + username)
                                        ircFunc.ircSay(ircFunc.getMsgto(line), 'Pulling from github.', irc)
                                        os.system('git pull')
                                        ircFunc.ircSay(ircFunc.getMsgto(line), 'Done pulling from github', irc)
                                    elif command == 'reload':
                                        del module
                                        module = modFunc.reloadMods()
                                        ircFunc.ircSay(ircFunc.getMsgto(line), 'Done reloading all modules', irc)
                                    elif command == 'modmanage-load':
                                        result = modFunc.LoadModule('modmanagement')
                                        if result == True:
                                            ircFunc.ircSay(msgto, 'Module has been loaded successfully', irc)
                                        else:
                                            ircFunc.ircSay(msgto, 'Either the module does not exist or something went wrong and it was NOT loaded successfully.', irc)
                                    elif command == 'purge':
                                        errorhandling.inputInfo("STARTING THY PURGE!!!!!!!! : Command directed by: " + username)
                                        modFunc.purgeMods()
                                        modFunc.purgeCommands()
                                        errorhandling.inputInfo("Purge has finished")
                                        ircFunc.ircSay(ircFunc.getMsgto(line), 'Finished purging commands and modules', irc)
                    except Exception, e:
                        errorhandling.inputError('critical', e, line)

                elif re.match("^:[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9\-\.]+\.(com|org|net|mil|edu|COM|ORG|NET|MIL|EDU) 001 " + conf['tempnickname'] + " :Welcome", line):
                    splitchannels = conf['channels'].split(" ")
                    for chan in splitchannels:
                        ircFunc.ircJoin(chan, irc)
                        #irc.send("JOIN %s\n" % (chan))

                elif re.search(":This nickname is registered and protected.", line):
                    ircFunc.ircSay("NICKSERV", "identify " + conf['nickservpassword'], irc)

                elif line[0:20] == "ERROR :Closing Link:":
                    errorhandling.inputInfo("Bot disconnected due to ping timeout...")
                    errorhandling.inputInfo('Reconnecting in 30 seconds...')
                    time.sleep(30)
                    errorhandling.inputInfo("Reconnecting now....")
                    # Connect to the socket
                    irc = mainFunc.CreateSocket(conf['server'], conf['port'])
                    # Authenticate to the IRC server
                    mainFunc.Auth(conf['username'], conf['nickname'], conf['realname'], irc)
            msgto = ircFunc.getMsgto(line, convert=False)
            if msgto.lower() == conf['tempnickname'].lower():
                if username.lower() not in "nickserv chanserv hostserv".split(" "):
                    functionProc = Process(target=privlog.input, args=(line,))
                    functionProc.daemon = True
                    functionProc.start()
            if line.split()[1] == 'PRIVMSG' and line.split()[2] != conf['tempnickname']:#this is a PM, ignore.
                try:
                    command = 'seen_record'
                    mod, function = modFunc.getCommand(command, loaded=True)
                    # Checks if the module is loaded
                    if mod != False:
                        nick = re.search(':(.*)!', line.lower().split()[0]).group(1)
                        nick = nick.strip()
                        channel = line.lower().split()[2]
                        msg = ' '.join(line.lower().split()[3:])[1:]
                        try:
                            functionProc = Process(target=getattr(module[mod], function), args=(nick, channel, msg, time.time()))
                            functionProc.daemon = True
                            functionProc.start()
                        except KeyError:
                            module[mod] = importlib.import_module(mod)
                            functionProc = Process(target=getattr(module[mod], function), args=(nick, channel, msg, time.time()))
                            functionProc.daemon = True
                            functionProc.start()
                        except Exception as e:
                            errorhandling.inputError('critical', e, line)
                except Exception, e:
                    errorhandling.inputError('critical', e)
        except IndexError:
            # Command does not exist
            pass
        except Exception, e:
            errorhandling.inputError('critical', e, line)


def LocalUpdateConf(conf):
    while True:
        a = configFunc.getAllBotConf()
        for key, value in a.iteritems():
            conf[key] = value
        time.sleep(5)


if __name__ == "__main__":
    # Writes imports from inc/ to inc/__init__.py
    file = open('inc/__init__.py', 'w')
    includeFiles = "__all__ =['mainFunc', 'ircFunc', 'errorhandling', 'configFunc', 'modFunc', 'privlog']"
    file.write(includeFiles)
    file.close()
    # Includes *.py files from inc/
    from inc import *
    # Makes sure configuration exists and if not creates it
    configFunc.ensureConf()
    ircFunc.ensureRegDB()
    # Cleans temp nick and chans
    configFunc.CleanTemps()
    # Sets modules exist to 0
    configFunc.CleanModulesDB()
    # Sets commands exist to 0
    configFunc.CleanCommandsDB()
    # Finds loaded modules and marks them as exist = 1
    modFunc.ScanModules()
    # Loads modules marked as Default Load
    module = modFunc.LoadDefaultModules()

    manager = Manager()
    conf = manager.dict()
    conf['conf'] = 'conf'
    functionProc = Process(target=LocalUpdateConf, args=(conf,))
    functionProc.daemon = True
    functionProc.start()

    # Sleep to provide time to grab the conf
    print '5'
    time.sleep(1)
    print '4'
    time.sleep(1)
    print '3'
    time.sleep(1)
    print '2'
    time.sleep(1)
    print '1'
    main()
