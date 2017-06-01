import sqlite3
from statsScraper import getPrevSeasonHeaders, getPlayerPic, getPlayerName, getPrevSeasonAvg
from playerIDGet import getPlayerIDs

db = sqlite3.connect('../data/athletes.db')
c = db.cursor()

def prevSeasonDataCommand(PID):
    q = "INSERT INTO prevSeason VALUES("
    q += str(PID) + ","
    q += "\'" + getPlayerName(PID) + "\',"
    q += "\'" + getPlayerPic(PID) + "\',"
    datadic = getPrevSeasonAvg(PID)
    #print datadic
    for x in datadic:
        val = str(datadic[x])
        if val.isalpha():
            q += "\'" + val + "\',"
        else:
            q += val + ","
    print q.rstrip(",") + ")"
    return q.rstrip(",") + ")"

def insertPrevSeasonData(PID):
    c.execute(prevSeasonDataCommand(PID))

def storeAllPlayersPrev():
    for x in getPlayerIDs():
        insertPrevSeasonData(x)
        print x

def getPrevSeasonDataCommand(PID):
    q = "SELECT * FROM prevSeason WHERE PID=" + str(PID)
    c.execute(q)
    info = c.fetchone()
    headers = ['PID', 'name' , 'img']
    headers = headers + getPrevSeasonHeaders()
    pdic = {}
    i = 0
    for x in info:
        pdic[headers[i]] = x
    return pdic

#insertPrevSeasonData('201566')
storeAllPlayersPrev()

#getPrevSeasonDataCommand('201566')

db.commit()
db.close()
    
