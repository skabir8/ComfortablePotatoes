import sqlite3
from statsScraper import getPrevSeasonHeaders



def makeDB():
    db=sqlite3.connect('../data/users.db')
    c=db.cursor()
    q="CREATE TABLE users( \'userID\' integer, \'username\' text, \'password\' text, \'points\' integer, \'players\' text, \'group\' integer )"
    c.execute(q)
    db.commit()
    db.close()


makeDB()

def prevSeasonCommand():
    q = "CREATE TABLE prevSeason("
    headers = getPrevSeasonHeaders()
    q += "\'PID\' integer, \'name\' text, \'img\' text," 
    for x in headers:
        q += "\'" + x + "\' text,"
    return q.rstrip(',')+  ")"

def makeDB2():
    db=sqlite3.connect('../data/athletes.db')
    c=db.cursor()
    c.execute(prevSeasonCommand())
    db.commit()
    db.close()

makeDB2()
