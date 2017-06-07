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
    myleagues = []
    for x in r:
        print x[0]
        q = "SELECT * FROM " + x[0]
        c.execute(q)
        s = c.fetchall()
        print s
        for y in s:
            if user == y[0]:
                myleagues.append(x)
    return myleagues

print getLeagues('jordan')
