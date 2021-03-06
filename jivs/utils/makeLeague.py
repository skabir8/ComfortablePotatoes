import sqlite3
import os

def newLeague(name, user, multipliers):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    q = " SELECT name from sqlite_master WHERE type=\'table\'"
    c.execute(q)
    r = c.fetchall()
    for x in r:
        if name in x:
            return [False, "League Name Already in Use"]
    q = "CREATE TABLE " + name + "(\'users' text, \'athletes\' text, \'multiplier\')"
    c.execute(q)
    c.execute("INSERT INTO " + name + " VALUES(?, ?, ?)", (user, None, multipliers,))
    db.commit()
    db.close()
    return [True, "League Successfully Created"]

def joinLeague(name, user):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    q = " SELECT name from sqlite_master WHERE type=\'table\'"
    c.execute(q)
    r = c.fetchall()
    if name not in [x[0] for x in r]:
        return [False, "League Does Not Exist!"]
    q = "SELECT * FROM " + name
    c.execute(q)
    r = c.fetchall()
    for x in r:
        if x[0] == user:
            return [False, "User already in League"]
    if len(r) == 5:
        return [False, "League is full"]
    c.execute("INSERT INTO " + name + " VALUES(?, ?, ?)", (user, None, None,))
    db.commit()
    db.close()
    return [True, "User Successfully Added to League"]

def getLeagues(user):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    #q = "DROP TABLE jimmy"
    #c.execute(q)
    q = "SELECT name FROM sqlite_master WHERE type=\'table\'"
    c.execute(q)
    r = c.fetchall()
    myleagues = {}
    for x in r:
        q = "SELECT * FROM " + x[0]
        c.execute(q)
        s = c.fetchall()
        #print s
        users = []
        for y in s:
            users.append(y[0])
        if user in users:
            myleagues[x[0]] = users
    return myleagues



def getAllLeagues(user):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    #q = "DROP TABLE jimmy"
    #c.execute(q)
    q = "SELECT name FROM sqlite_master WHERE type=\'table\'"
    c.execute(q)
    r = c.fetchall()
    myleagues = {}
    for x in r:
        q = "SELECT * FROM " + x[0]
        c.execute(q)
        s = c.fetchall()
        #print s
        users = []
        for y in s:
            users.append(y[0])
        if (len(users) <=5):
            if user not in users:
                myleagues[x[0]] = users
    return myleagues

def addPlayer(league, user, PID):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    c.execute("Select * from " + league)
    r = c.fetchall()
    #print r
    otherids = []
    myids = []
    for x in r:
        if x[0] == user:
            myids = getAthletes(x)
        else:
            otherids.extend(getAthletes(x))
    if PID in myids:
        return [False, "You already have this player"]
    if PID in otherids:
        return [False, "Someone in your league already has this player"]
    if len(myids) >= 11:
        return [False, "You own the maximum number of athletes"]
    newids = "'" + athletesToString(myids + [PID]) + "'"
    userq = "'" + user + "'"
    q = "UPDATE %s SET athletes = %s WHERE users=%s" % (league, newids, userq,)
    c.execute(q)
    db.commit()
    return [True, "Player added to your roster"]




def getAthletes(sqlr):
    if len(sqlr) < 2 or sqlr[1] == None:
        return []
    return sqlr[1].split(',')

def maxplayers(league, user):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    userq = "'" + user + "'"
    q = "Select * from " + league + " WHERE users=" + userq
    c.execute(q)
    r = c.fetchone()
    return len(getAthletes(r)) >= 10

#print maxplayers('swagmonkey','jordan')

def getLeagueAthletes(league, user):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    userq = "'" + user + "'"
    q = "Select * from " + league + " WHERE users=" + userq
    c.execute(q)
    r = c.fetchone()
    db.commit()
    db.close()
    return getAthletes(r)

def athletesToString(lis):
    if lis == []:
        return ""
    else:
        return ','.join(lis)

def getAllLeagues(user):
    DIR=os.path.dirname(__file__)
    DIR+='/'
    db = sqlite3.connect(DIR+"../data/league.db")
    c = db.cursor()
    #q = "DROP TABLE jimmy"
    #c.execute(q)
    q = "SELECT name FROM sqlite_master WHERE type=\'table\'"
    c.execute(q)
    r = c.fetchall()
    myleagues = {}
    for x in r:
        q = "SELECT * FROM " + x[0]
        c.execute(q)
        s = c.fetchall()
        #print s
        users = []
        for y in s:
            users.append(y[0])
        if (len(users) < 5):
            if user not in users:
                myleagues[x[0]] = users
    return myleagues
#print getLeagueAthletes('swagmonkey', 'shariarshariar')
