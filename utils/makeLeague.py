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
    
 
