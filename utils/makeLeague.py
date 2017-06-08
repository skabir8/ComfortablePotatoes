import sqlite3

def newLeague(name, user, multipliers):
    db = sqlite3.connect("data/league.db")
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
    db = sqlite3.connect("data/league.db")
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
    db = sqlite3.connect("data/league.db")
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
        print users
        if user in users:
            myleagues[x[0]] = users
    return myleagues

def addPlayer(league, user, athlete):
    db = sqlite3.connect("data/league.db")
    c = db.cursor()
    c.execute("SELECT users FROM " + league + "WHERE users==?", (user,))
    r = c.fetchone()
    return r

def getAllLeagues(user):
    db = sqlite3.connect("data/league.db")
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
    db = sqlite3.connect("data/league.db")
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
    print myids
    if PID in myids:
        return [False, "You already have this player"]
    if PID in otherids:
        return [False, "Someone in your league already has this player"]
    if len(myids) >= 11:
        return [False, "You own the maximum number of athletes"]
    print myids
    newids = "'" + athletesToString(myids + [PID]) + "'"
    print newids
    userq = "'" + user + "'"
    q = "UPDATE %s SET athletes = %s WHERE users=%s" % (league, newids, userq,)
    print q
    c.execute(q)
    db.commit()
    return [True, "Player added to your roster"]

def getAthletes(sqlr):
    if len(sqlr) < 2 or sqlr[1] == None:
        return []
    return sqlr[1].split(',')

def athletesToString(lis):
    if lis == []:
        return ""
    else:
        return ','.join(lis)

def getAllLeagues(user):
    db = sqlite3.connect("data/league.db")
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
