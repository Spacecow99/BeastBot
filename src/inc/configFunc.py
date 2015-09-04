import mainFunc
import ircFunc
import errorhandling
import sqlite3

'''
Configuration Management
'''

def ensureConf():
    # Makes sure that the configuration database exists
    # If it does not, then it populates it with the entered values
    import os
    if not os.path.isfile('conf/conf.db'):
        errorhandling.inputInfo('No configuration database found. Creating and configuring it.')
        con = sqlite3.connect('conf/conf.db')
        # Creates the database file
        errorhandling.inputInfo('Created conf/conf.db')
        errorhandling.inputInfo('Setting up configuration tables')
        while con:
            # Creates the database tables
            cur = con.cursor()
            cur.execute('''CREATE TABLE bot
                (var TEXT NOT NULL, 
                content TEXT);''')
            cur.execute('''CREATE TABLE modules
                (location TEXT,
                exist INT,
                name TEXT,
                loaded INT,
                defaultload INT)''')
            cur.execute('''CREATE TABLE commands
                (help TEXT,
                perm TEXT,
                loaded INT,
                init TEXT,
                module TEXT, 
                function TEXT,
                enabled INT);''')
            con.commit()
            break
        errorhandling.inputInfo('Tables created')
        errorhandling.inputInfo('Asking user for default values for configuration')
        # Asks the user for configuration values for the database
        serverAddress = raw_input("Default server address: ")
        serverPort = raw_input("Default server port: ")
        botNickname = raw_input("Default bot nickname: ")
        botUsername = raw_input("Default bot username: ")
        botRealname = raw_input("Default bot realname: ")
        botPassword = raw_input("Bot nickserv password: ")
        botComInit = raw_input("Bot command initializer ( such as !): ")
        botChannel = raw_input("Bot default channel: ")
        botAdmins = raw_input("Bot admin username: ")
        while con:
            # Inserts the users values into the configuration database
            cur = con.cursor()
            cur.execute("INSERT INTO bot (var,content) VALUES ('server', '%s')" % serverAddress)
            cur.execute("INSERT INTO bot (var,content) VALUES ('port', '%s')" % serverPort)
            cur.execute("INSERT INTO bot (var,content) VALUES ('nickname', '%s')" % botNickname)
            cur.execute("INSERT INTO bot (var,content) VALUES ('tempnickname', '%s')" % botNickname)
            cur.execute("INSERT INTO bot (var,content) VALUES ('username', '%s')" % botUsername)
            cur.execute("INSERT INTO bot (var,content) VALUES ('realname', '%s')" % botRealname)
            cur.execute("INSERT INTO bot (var,content) VALUES ('nickservpassword', '%s')" % botPassword)
            cur.execute("INSERT INTO bot (var,content) VALUES ('cominit', '%s')" % botComInit)
            cur.execute("INSERT INTO bot (var,content) VALUES ('channels', '%s')" % botChannel)
            cur.execute("INSERT INTO bot (var,content) VALUES ('tempchannels', '%s')" % botChannel)
            cur.execute("INSERT INTO bot (var,content) VALUES ('botbanned', '')")
            cur.execute("INSERT INTO bot (var,content) VALUES ('botadmins', '%s')" % botAdmins)
            con.commit()
            break
        print 'Configuration complete'
        print 'Starting bot'
        errorhandling.inputInfo('Done inserting default values')
        errorhandling.inputInfo('Done creating configuration database')



def getAllBotConf():
    # Receives all values from the configuration database and the table 'bot'
    # Receives things such as server address, port, nickname etc.....
    conf = {}
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bot")
        rows = cur.fetchall()
        break
    for row in rows:
        if row[1] == None:
            row[1] = ''
        conf[row[0]] = row[1]
    return conf


def getBotConf(option):
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("SELECT content FROM bot WHERE var='%s'" % option)
        row = cur.fetchone()
        break
    if row == None:
        errorhandling.inputError('warning', 'botconf option doesnt exist', 'Option: %s' % option)
    else:
        if row[0] == None:
            row[0] = ''
        return str(row[0])


def setBotConf(var, content):
    # Updates a value in the configuration database, 'bot' table.
    con = sqlite3.connect('conf/conf.db')
    while con:
        cur = con.cursor()
        cur.execute("UPDATE bot SET content='%s' WHERE var='%s'" % (content, var))
        con.commit()
        break


def CleanModulesDB():
    # Should run at startup
    # Resets module exist to 0
    # Resets module loaded to 0
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("UPDATE modules SET exist=0 WHERE exist=1")
        cur.execute("UPDATE modules SET loaded=0 WHERE loaded=1")
        con.commit()


def CleanCommandsDB():
    # Should run at startup
    # Resets commands loaded to 0
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("UPDATE commands SET loaded=0 WHERE loaded=1")
        con.commit()

def CleanTemps():
    # Should run at startup
    # Sets the temp vars to empty sense the bot shouldnt be on any channels when it connects.
    con = sqlite3.connect('conf/conf.db')
    with con:
        cur = con.cursor()
        cur.execute("UPDATE bot SET content='' WHERE var='tempnickname'")
        cur.execute("UPDATE bot SET content='' WHERE var='tempchannels'")
