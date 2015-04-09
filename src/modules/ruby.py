#
# =================
# === RUBINATOR ===
# =================
#
# A module that makes this bot have ruby modules
#
# Author: Lenoch
#

import ConfigParser
import json
import ircFunc
import errorhandling
import os
from subprocess import Popen, PIPE, STDOUT

def init():
    modulename = "urban"
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'ruby_modules', 'loaded')
    
    files = os.listdir('ruby_modules/')
    
    for i in range(len(files)):
        config.set('Functions', files[i].split('.')[0], 'ruby.ruby')
    

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()
def getConfig():
    config = ConfigParser.RawConfigParser()
    config.read('conf/beastbot.conf')
    conf = dict(config.items('Main'))
    return conf
 
def ruby(line, irc):
    splitline = line.split(" :")
    script_to_execute = splitline[1].rstrip() + ".rb"
    
    conf = getConfig()
    
    # Open the script associated with the command
    ruby_script = Popen(['ruby', 'ruby_modules/' + script_to_execute[1:]], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    
    print script_to_execute[1:]
    
    result = []
    
    while True:
        if ruby_script.poll() is not None:
            break
        
        ruby_line = ruby_script.stdout.readline().rstrip()
        
        result.append(ruby_line)
        
        if line == '[end]':
            break
        

    for i in range(len(result)):
        output = result[i]
        
    sendinfo = output.split(":")
    msgto = ""
    
    if sendinfo[0] == "channel":
        msgto = line.split(" ")[2]
    elif sendinfo[0] == "user":
        msgto = line.split(" :")[0]
        
    ircFunc.ircSay(msgto, sendinfo[1], irc)
        

