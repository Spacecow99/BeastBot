import ConfigParser
import time
import sys
import traceback


def init():
    config = ConfigParser.ConfigParser()
    config.read('conf/beastbot.conf')
    config.set('Modules', 'errorhandling', 'loaded')

    with open('conf/beastbot.conf', 'wb') as configfile:
        config.write(configfile)

init()


def errorinfo():
    info = traceback.extract_tb(sys.exc_info()[-1])
    info = str(info)
    info = ''.join(info)
    info = info.replace("[('", '').replace("')]", '').replace("'", '')
    info = info.split(",")
    var = {}
    var['filename'] = info[0]
    var['linenumber'] = info[1]
    var['functionname'] = info[2]
    var['linetext'] = info[3]
    return var


def log(level, message, info, additional=None):
    try:
        additional = additional.strip('\n').strip('\r')
    except Exception:
        pass
    date = time.strftime("%Y-%m-%d") # this is the global standard
    file = open('log/%s.log' % (date), 'a')
    log = level
    log = log + ' - ' + time.strftime("%H:%M:%S")
    log = log + ' - ' + message
    log = log + ' - Filename: ' + info['filename']
    log = log + ' - Line Number: ' + info['linenumber']
    log = log + ' - Function: ' + info['functionname']
    log = log + ' - Line Text: ' + info['linetext']
    if additional:
        log = log + ' - Additional Information: ' + additional
    file.write(log + "\n")
    file.close()


def errorlog(option, message, additional=None):
    info = errorinfo()
    message = str(message)
    option = option.upper()
    log(option, message, info, additional)


def loginfo(info):
    info = str(info)
    date = time.strftime("%Y-%m-%d") # this is the global standard
    logtime = time.strftime("%H:%M:%S")
    file = open("log/%s.log" % (date), 'a')
    output = logtime + " - " + info
    file.write(output + "\n")
    file.close()
