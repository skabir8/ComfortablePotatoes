import sqlite3
from statsScraper import getPrevSeasonHeaders, getPlayerPic, getPlayerName, getPrevSeasonAvg
from playerIDGet import getPlayerIDs
import json


allPid=[201566, 2544, 201939, 201935, 202331, 203081, 202695, 202322, 201142, 101108, 203078, 203507, 203471, 201144, 200794, 202681, 202330, 202738, 202710, 203468, 201942, 201188, 201567, 201952, 202340, 200746, 202362, 200768, 201588, 201599, 201143, 2548, 203114, 202691, 201586, 203109, 203110, 202328, 2216, 201569, 2207, 203501, 201577, 2037, 101150, 203490, 202693, 202329, 201152, 1626181, 203460, 203497, 202685, 1627752, 201976, 203506, 1626167, 2772, 203991, 203613, 201988, 202323, 2403, 203503, 203145, 201959, 201583, 203924, 203482, 1713, 200755, 1627763, 203918, 202711, 202703, 203935, 202684, 203516, 101162, 2730, 203500, 202709, 201980, 2200, 203521, 201601, 202324, 101123, 203546, 101112, 203210, 1627835, 101139, 202338, 203090, 203894, 1626171, 1938, 201578, 1626150, 2738, 204060, 201580, 2594, 202714, 2747, 2585, 1626162, 1627748, 2564, 1626179, 101109, 203937, 203459, 101145, 203926, 203922, 1627759, 200782, 101114, 203518, 202683, 202697, 2733, 203943, 101181, 2561, 201960, 1627775, 101135, 101141, 201160, 1627782, 2210, 203473, 202335, 1626170, 1626245, 1718, 201943, 203488, 203487, 1626153, 202722, 101161, 203526, 1891, 1626192, 203949, 2399, 203584, 202708, 203107, 203086, 202730]

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
    data=getPrevSeasonData(PID)
    playerItems = {}
    playerItems['pid'] = str(PID)
    playerItems['name'] = data['name']
    playerItems['image'] = data['img']
    avgs = getPrevSeasonData(str(PID))
    playerItems['stats'] = avgs
    playerItems['str'] = json.dumps(playerItems)
    return playerItems

def packagePlayers(listPID):
    playerStats = []
    for PID in listPID:
        playerStats.append(packagePlayer(PID))
    return playerStats

def packageAllPlayers():
    return packagePlayers(allPid)
