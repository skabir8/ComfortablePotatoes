import sqlite3
from statsScraper import getPrevSeasonHeaders, getPlayerPic, getPlayerName, getPrevSeasonAvg
from playerIDGet import getPlayerIDs

def getPrevSeasonData(PID):
    db = sqlite3.connect('../data/athletes.db')
    c = db.cursor()
    q = "SELECT * FROM prevSeason WHERE PID=" + str(PID)
    c.execute(q)
    info = c.fetchone()
    headers = ['PID', 'name' , 'img']
    headers = headers + getPrevSeasonHeaders()
    pdic = {}
    i = 0
    for x in info:
        pdic[headers[i]] = x
        i += 1
    db.commit()
    db.close()
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

print(packagePlayers([201566,2544]))
