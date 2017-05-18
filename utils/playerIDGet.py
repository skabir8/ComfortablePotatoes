import requests
import urllib2 

# Headers required to receive NBA response
headers1 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
                     'referer': 'http://stats.nba.com/scores/'
                    }



r = requests.get("http://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2016-17&SeasonType=Playoffs&StatCategory=PTS", headers = headers1)
data = r.json()


def makeIDFile(file):
    #seperates data in playerID rows
    playerID=data['resultSet']['rowSet']
    playerDict={}
    #makes a dict with ID being key and value as name
    f = open(file, 'w')
    for x in playerID:
        f.write(str(x[0]) + "," + str(x[2]) + "\n")
        #playerDict[str(x[0])]= x[2]
    
    

makeIDFile("players.txt")
