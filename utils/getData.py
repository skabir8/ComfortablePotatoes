import sqlite3
from statsScraper import getPrevSeasonHeaders, getPlayerPic, getPlayerName, getPrevSeasonAvg
from playerIDGet import getPlayerIDs
import json

def getPrevSeasonData(PID):
    db = sqlite3.connect('data/athletes.db')
    c = db.cursor()
    q = "SELECT * FROM prevSeason WHERE PID=" + str(PID)
    c.execute(q)
    info = c.fetchone()
    q = "SELECT * FROM prevSeason WHERE PID=\'PID\'"
    c.execute(q)
    headers = c.fetchone()
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
    playerItems['pid'] = str(PID)
    playerItems['name'] = getPlayerName(PID)
    playerItems['image'] = getPlayerPic(PID)
    avgs = getPrevSeasonData(str(PID))
    playerItems['stats'] = avgs
    playerItems['str'] = json.dumps(playerItems)
    return playerItems

def packagePlayers(listPID):
    playerStats = []
    for PID in listPID:
        playerStats.append(packagePlayer(PID))
    return playerStats



