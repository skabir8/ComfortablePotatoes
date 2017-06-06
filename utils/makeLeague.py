import sqlite3

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
        lastNum=tableNamesRefined[-1]
    newNum=lastNum+1
    q="create table League"+str(newNum)+"(\'user\' text, \'athletes\' text)"
    c.execute(q)
    listUsers = [user1, user2, user3, user4, user5]
    for user in listUsers:
        q="insert into League"+str(newNum)+" values(\'"+user+"\',\'\')"
        c.execute(q)
    db.commit()
    db.close()

#newLeague("blah1","blah2","blah3","blah4","blah5")
