import requests
import urllib2

# Headers required to receive NBA response
headers1 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
                     'referer': 'http://stats.nba.com/scores/'
                    }


def getCurrentAll(PID):
    PID = str(PID)
    r = requests.get("http://stats.nba.com/stats/playergamelogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerID="+PID+"&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&VsConference=&VsDivision=", headers = headers1)
    data = r.json()
    #List of table headers and games
    gamelogs= data['resultSets'][0]['rowSet']
    gameList=[]
    #List of each match with indiviudal stats
    for x in gamelogs:
        gameList.append(x)
    return gameList

def getPrevSeasonHeaders():
    r = requests.get("http://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201566&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision=", headers = headers1)
    data = r.json()
    seasonAvgHeader = data['resultSets'][0]['headers']
    return seasonAvgHeader

def getPrevSeasonAvg(PID):

    PID = str(PID)
    r = requests.get("http://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID="+PID+"&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=general&VsConference=&VsDivision=", headers = headers1)
    data = r.json()
    seasonAvgHeader = data['resultSets'][0]['headers']
    try:
        seasonAvg = data['resultSets'][0]['rowSet'][0]
    except IndexError:
        seasonAvg=[]
    prevAvg={}
    i=0
    for x in seasonAvgHeader:
        try:
            prevAvg[str(x)]= seasonAvg[i]
        except IndexError:
            prevAvg[str(x)]= 0
        i+=1
    return prevAvg

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
    avgs = getPrevSeasonAvg(PID)
    playerItems['stats'] = avgs
    return playerItems

def packagePlayers(listPID):
    playerStats = []
    for PID in listPID:
        playerStats.append(packagePlayer(PID))
    return playerStats

#print getPrevSeasonAvg(1627752)
#print getPlayerPic(201566)
#print getPlayerName(2210)
#print packagePlayers([201566,2544,201935,202331,201939])

#print packagePlayer(201566)
