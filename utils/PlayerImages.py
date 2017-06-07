import requests
import urllib2

# Headers required to receive NBA response
headers1 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
                     'referer': 'http://stats.nba.com/scores/'
                    }



#r = requests.get("http://stats.nba.com/stats/playergamelogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerID=203490&PlusMinus=N&Rank=N&Season=2016-17&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&VsConference=&VsDivision=", headers = headers1)
#data = r.json()

#List of table headers and games
#gamelogs= data['resultSets'][0]['rowSet']
#gameList=[]


#List of each match with indiviudal stats
#for x in gamelogs:
#    gameList.append(x)

#print gameList
