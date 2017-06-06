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
    return q.rstrip(",") + ")"

def insertPrevSeasonData(PID):
    q = "SELECT * FROM prevSeason WHERE PID=" + str(PID)
    c.execute(q)
    r = c.fetchone()
    print r
    if r == None:
        c.execute(prevSeasonDataCommand(PID))
        print "done"

def storeAllPlayersPrev():
    for x in getPlayerIDs():
        try:
            insertPrevSeasonData(x)
            print x
        except:
            print "Broke at" + str(x)
            break

def getPrevSeasonData(PID):
    q = "SELECT * FROM prevSeason WHERE PID=" + str(PID)
    c.execute(q)
    info = c.fetchone()
    headers = ['PID', 'name' , 'img']
    headers = headers + getPrevSeasonHeaders()
    pdic = {}
    i = 0
    print(info)
    for x in info:
        pdic[headers[i]] = x
        i += 1
    return pdic

def getPlayerPic(PID):
    PID= str(PID)
    imageLink='http://stats.nba.com/media/players/230x185/'+PID+'.png'
    return imageLink

def getPlayerName(PID):
    f = open("players.txt", "r")
    for line in f:
        player = line.split(",")
        if player[0] == str(PID):
            return player[1]

def packagePlayer(PID):
    playerItems = {}
    playerItems['name'] = getPlayerName(PID)
    playerItems['image'] = getPlayerPic(PID)
    avgs = getPrevSeasonData(str(PID))
    playerItems['stats'] = avgs
    return playerItems

def packagePlayers(listPID):
    playerStats = []
    for PID in listPID:
        playerStats.append(packagePlayer(PID))
    return playerStats
#insertPrevSeasonData('201566')
#storeAllPlayersPrev()

print getPrevSeasonData('201566')
#insertPrevSeasonData('2210')
#print(packagePlayers([201566,2544]))
db.commit()
db.close()


