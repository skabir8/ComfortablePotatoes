import sqlite3
from statsScraper import getPrevSeasonHeaders

db=sqlite3.connect('../data/Comfy.db')
c=db.cursor()

def makeDB():
    q="CREATE TABLE users( \'username\' text, \'password\' text, \'points\' integer, \'players\' text, \'group\' integer )"
    c.execute(q)


makeDB()
db.commit()
db.close()

db2 = sqlite3.connect('../data/Comfy.db')
c2 = db2.cursor()

def prevSeasonCommand():
    q = "CREATE TABLE prevSeason("
    headers = getPrevSeasonHeaders()
    q += "\'PID\' integer, \'name\' text, \'img\' text," 
    for x in headers:
        q += "\'" + x + "\' text,"
    return q.rstrip(',')+  ")"

def makeDB2():
    c2.execute(prevSeasonCommand())

makeDB2()
db2.commit()
db2.close()
