import sqlite3
from statsScraper import getPrevSeasonHeaders

db=sqlite3.connect('../data/Comfy.db')
c=db.cursor()

def makeDB():
    q="CREATE TABLE users( \'userID\' integer, \'username\' text, \'password\' text, \'points\' integer, \'players\' text, \'group\' integer )"
    c.execute(q)


makeDB()

def prevSeasonCommand():
    q = "CREATE TABLE prevSeason("
    headers = getPrevSeasonHeaders()
    q += "\'PID\' integer, \'name\' text, \'img\' text," 
    for x in headers:
        q += "\'" + x + "\' text,"
    return q.rstrip(',')+  ")"

def makeDB2():
    c.execute(prevSeasonCommand())

makeDB2()
db.commit()
db.close()
