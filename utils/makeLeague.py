import sqlite3

def makeLeague(name, user, multipliers):
    db = sqlite3.connect("../data/league.db")
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
    return [True, "League Successfully Created"]

print makeLeague("jordan","jordan","12121")
    


def newLeague(user1, user2, user3, user4, user5):
    db=sqlite3.connect("data/league.db")
    c=db.cursor()
    q="select name from sqlite_master where type=\'table\'"
    c.execute(q)
    tableNamesRaw=c.fetchall()
    tableNamesRefined=[]
    for tableName in tableNamesRaw:
        tableNamesRefined.append(int(tableName[0][-1]))
    if not tableNamesRefined:
        lastNum=0
    else:
        compareUsers=[user1, user2, user3, user4, user5]
        compareUsers.sort()
        for num in tableNamesRefined:
            q="select user from League"+str(num)
            c.execute(q)
            listUsers1=c.fetchall()
            newListUsers1=[]
            for user in listUsers1:
                newListUsers1.append(user[0])
            newListUsers1.sort()
            if newListUsers1 == compareUsers:
                return "League already exists!"
        lastNum=tableNamesRefined[-1]
    newNum=lastNum+1
    q="create table League"+str(newNum)+"(\'user\' text, \'athletes\' text)"
    c.execute(q)
    listUsers2 = [user1, user2, user3, user4, user5]
    for user in listUsers2:
        q="insert into League"+str(newNum)+" values(\'"+user+"\',\'\')"
        c.execute(q)
    db.commit()
    db.close()

def getLeagueNum(user1, user2, user3, user4, user5):
    db=sqlite3.connect("data/league.db")
    c=db.cursor()
    q="select name from sqlite_master where type=\'table\'"
    c.execute(q)
    tableNamesRaw=c.fetchall()
    tableNamesRefined=[]
    for tableName in tableNamesRaw:
        tableNamesRefined.append(int(tableName[0][-1]))
    compareUsers=[user1, user2, user3, user4, user5]
    compareUsers.sort()
    for num in tableNamesRefined:
        q="select user from League"+str(num)
        c.execute(q)
        listUsers1=c.fetchall()
        newListUsers1=[]
        for user in listUsers1:
            newListUsers1.append(user[0])
        newListUsers1.sort()
        if newListUsers1 == compareUsers:
            return num

#print newLeague("blarg1","blarg2","blarg4","blarg3","blarg5")
#print getLeagueNum("blarg1","blarg2","blarg3","blarg5","blarg4")
