import requests
import urllib2
import os
# Headers required to receive NBA response
headers1 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
                     'referer': 'http://stats.nba.com/scores/'
                    }



r = requests.get("http://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2016-17&SeasonType=Playoffs&StatCategory=PTS", headers = headers1)
data = r.json()

def getPlayerIDs():
    ids = []
    for x in data['resultSet']['rowSet']:
        ids.append(x[0])
    #f = open("players.txt", 'r')
    #for line in f.read():
    #   info = line.split(',')
    #  ids.append(info[0])
    return ids


def makeIDFile(file):
    #seperates data in playerID rows
    playerID=data['resultSet']['rowSet']
    playerDict={}
    #makes a dict with ID being key and value as name
    f = open(file, 'w')
    i = 0
    for x in playerID:
        PID= str(x[0])
        imageLink='http://stats.nba.com/media/players/230x185/'+PID+'.png'
        f.write(str(x[0]) + "," + str(x[2]) +","+imageLink+ "," +str(i) + "\n")
        i = i + 1
        #playerDict[str(x[0])]= x[2]



#makeIDFile("players.txt")

#print(getPlayerIDs())
