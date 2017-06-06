import requests
import urllib2
from bs4 import BeautifulSoup
from lxml import etree

headersList=['MP','FG','FGA','FG%','3P','3PA','3P','FT','FTA','FT','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-']

headers1 = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/45.0.2454.101 Safari/537.36'),
                     'referer': 'http://stats.nba.com/scores/'
                    }

gameUrlList=['http://www.basketball-reference.com/leagues/NBA_2017_games-october.html',
'http://www.basketball-reference.com/leagues/NBA_2017_games-november.html',
'http://www.basketball-reference.com/leagues/NBA_2017_games-december.html',
'http://www.basketball-reference.com/leagues/NBA_2017_games-january.html',
'http://www.basketball-reference.com/leagues/NBA_2017_games-february.html',
'http://www.basketball-reference.com/leagues/NBA_2017_games-march.html',
'http://www.basketball-reference.com/leagues/NBA_2017_games-april.html']
def getAllGames():
    #PID = str(PID)
    r = requests.get('http://www.basketball-reference.com/leagues/NBA_2017_games-october.html')
    data = r.text
    soup=BeautifulSoup(data)
    print soup
    retList=[]
    for x in soup.find_all('a'):
        if (('/boxscores/' in x.get('href')) and (x.get('href') != '/boxscores/')) and ('index.fcgi?' not in x.get('href')):
            retList.append(x.get('href'))
    return retList


def get2016GamesURL():
    month = 10
    days = 25
    x = 170
    link=''
    gameCount="game_"
    gameDict={}
    i=1
    while x > 0:

        if (month > 12):
            return gameDict
        if (month == 10 or month == 12):
            if (days < 31):
                link = 'http://www.basketball-reference.com/boxscores/?month='+str(month)+'&day='+str(days)+'&year=2016'
            elif (days > 31):
                month += 1
                days = 0
        elif (month == 11):
            if (days < 30):
                link = 'http://www.basketball-reference.com/boxscores/?month='+str(month)+'&day='+str(days)+'&year=2016'
            elif (days >= 30):
                month += 1
                days = 0
        days = days + 1
        gameDict[gameCount+str(i)]=link
        x-=1
        i+=1
    return gameDict

def get2017GamesURL():
    month = 1
    days = 1
    x = 170
    link=''
    gameCount="game_"
    gameDict={}
    i=71
    while x > 0:
        if (month >= 4 and days > 12):
            return gameDict
        if (month in [1,3]):
            if (days < 31):
                link = 'http://www.basketball-reference.com/boxscores/?month='+str(month)+'&day='+str(days)+'&year=2017'
            elif (days > 31):
                month += 1
                days = 0
        elif (month in [2,4]):
            if (days < 30):
                link = 'http://www.basketball-reference.com/boxscores/?month='+str(month)+'&day='+str(days)+'&year=2017'
            elif (days > 30):
                month += 1
                days = 0
        days = days + 1
        gameDict[gameCount+str(i)]=link
        x-=1
        i+=1
    return gameDict


def getAllGames():
    return dict(get2016GamesURL().items() + get2017GamesURL().items())


def getBoxScoreUrls():
    retList=[]
    dayLog={}
    day=1
    i=1
    store=getAllGames()
    file = open("testfile.txt","a")
    for y in store.keys():
        r = requests.get(store['game_'+str(i)])

        #print
        data = r.text
        soup=BeautifulSoup(data,"html.parser")
        for x in soup.find_all('a'):
            if (('/boxscores/' in x.get('href')) and (x.get('href') != '/boxscores/')) and ('index.fcgi?' not in x.get('href')) and ('pbp' not in x.get('href')) and ('shot-chart' not in x.get('href')) and ('month=' not in x.get('href')):
                retList.append('http://www.basketball-reference.com'+x.get('href'))
        dayLog['day_'+str(i)]=retList
        retList=[]
        i+=1
        #print dayLog.values()[0]
        for url in dayLog.values()[0]:
            file.write(url+"\n")
    file.close()
    return dayLog


def getBoxScoreStats(boxUrl):
    url=boxUrl
    retList = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(r.text, 'lxml')
    allData = soup.find_all('tr')
    #y = allData[1]
    #colH = y.find_all('th')
    #for x in colH:
    #    print x.string
    #
    #print y
    #print y
    endL=[]
    store=[]
    for elements in allData:

        name = elements.find_all('th')
        if name[0].string == None:
            name =  "0"
        else:
            name = name[0].string.strip()

        col = elements.find_all('td')
        i=0
        hold=[]
        gameScores={}
        hold.append(name)
        gameScores[name]={}
        for column in col:
            if (name != 'Team Totals'):
                if col[i].string== None:
                    column_dat = '0'
                else:
                    column_dat = col[i].string.strip()
                    print name, headersList[i], column_dat
                gameScores[name][headersList[i]]=column_dat
                i+=1
        store.append(name)
        hold.append(gameScores)
        endL.append(hold)


            #print column_dat
    print store
    return endL[2:]







#print getBoxScoreUrls()
#print list(set(getBoxScoreUrls()))
#print getBoxScoreUrls()

#getBoxScoreStats('http://www.basketball-reference.com/boxscores/201703130CHO.html')
