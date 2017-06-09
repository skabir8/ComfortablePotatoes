import requests
import urllib2
from bs4 import BeautifulSoup
from lxml import etree
import ast
import random


headersList=['MP','FG','FGA','FGPercent','3P','3PA','3PPercent','FT','FTA','FTPercent','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','+/-']

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


playerDict={'David West': '2561', 'Kelly Oubre Jr.': '1626162', 'Pau Gasol': '2200', 'George Hill': '201588', 'Glenn Robinson III': '203922', 'LaMarcus Aldridge': '200746', 'Draymond Green': '203110', 'Kyle Lowry': '200768', 'James Ennis III': '203516', 'Raymond Felton': '101109', 'Nene': '2403', 'Robin Lopez': '201577', 'Marcus Smart': '203935', 'Kevin Love': '201567', 'Iman Shumpert': '202697', 'JJ Redick': '200755', 'Ryan Anderson': '201583', 'Lance Stephenson': '202362', 'Meyers Leonard': '203086', 'Mike Conley': '201144', 'Shaun Livingston': '2733', 'Serge Ibaka': '201586', 'Andrew Harrison': '1626150', 'Isaiah Thomas': '202738', 'Jae Crowder': '203109', 'Shabazz Napier': '203894', 'Tim Hardaway Jr.': '203501', 'Paul Millsap': '200794', 'Jeff Teague': '201952', 'Avery Bradley': '202340', 'Joe Johnson': '2207', 'Evan Turner': '202323', 'Trevor Ariza': '2772', 'Kyle Korver': '2594', 'Amir Johnson': '101161', 'Cory Joseph': '202709', 'Jerami Grant': '203924', 'Monta Ellis': '101145', 'Michael Carter-Williams': '203487', 'Tony Snell': '203503', 'Jonathon Simmons': '203613', 'Shelvin Mack': '202714', 'Jose Calderon': '101181', 'Marc Gasol': '201188', 'Richard Jefferson': '2210', 'LeBron James': '2544', 'JaMychal Green': '203210', 'Kevin Seraphin': '202338', 'Zach Randolph': '2216', 'Kent Bazemore': '203145', 'James Harden': '201935', 'Enes Kanter': '202683', 'Kevin Durant': '201142', 'Dewayne Dedmon': '203473', 'Troy Daniels': '203584', 'JaVale McGee': '201580', 'Boris Diaw': '2564', 'Damian Lillard': '203081', 'Tomas Satoransky': '203107', 'Terry Rozier': '1626179', 'Alex Abrines': '203518', 'Kyrie Irving': '202681', 'Eric Gordon': '201569', 'Thon Maker': '1627748', 'Jerian Grant': '1626170', 'Myles Turner': '1626167', 'Patrick McCaw': '1627775', 'Thaddeus Young': '201152', 'Rudy Gobert': '203497', 'Maurice Harkless': '203090', 'Lavoy Allen': '202730', 'Otto Porter Jr.': '203490', 'Marcin Gortat': '101162', 'Allen Crabbe': '203459', 'Giannis Antetokounmpo': '203507', 'Al-Farouq Aminu': '202329', 'Brandon Jennings': '201943', 'Al Horford': '201143', 'Kawhi Leonard': '202695', 'Chris Paul': '101108', 'Channing Frye': '101112', 'Dwyane Wade': '2548', 'Pat Connaughton': '1626192', 'Vince Carter': '1713', 'Bradley Beal': '203078', 'Klay Thompson': '202691', 'Patrick Patterson': '202335', 'Gordon Hayward': '202330', 'Mike Dunleavy': '2399', 'Rodney Hood': '203918', 'CJ McCollum': '203468', 'DeMarre Carroll': '201960', 'Ersan Ilyasova': '101141', 'Noah Vonleh': '203943', 'Jonas Valanciunas': '202685', 'Kyle Anderson': '203937', 'JR Smith': '2747', 'Jason Smith': '201160', 'Taurean Prince': '1627752', 'Malcolm Brogdon': '1627763', 'PJ Tucker': '200782', 'Ian Clark': '203546', 'Delon Wright': '1626153', 'Jimmy Butler': '202710', 'James Michael McAdoo': '203949', 'Zaza Pachulia': '2585', 'Andre Roberson': '203460', 'Jason Terry': '1891', 'Bojan Bogdanovic': '202711', 'Norris Cole': '202708', 'Paul Pierce': '1718', 'Jamal Crawford': '2037', 'Joe Ingles': '204060', 'Markieff Morris': '202693', 'Paul Zipser': '1627835', 'Dwight Howard': '2730', 'David Lee': '101135', 'Matthew Dellavedova': '203521', 'Norman Powell': '1626181', 'Patty Mills': '201988', 'Greg Monroe': '202328', 'Khris Middleton': '203114', 'Tristan Thompson': '202684', 'Manu Ginobili': '1938', 'Raul Neto': '203526', 'Cristiano Felicio': '1626245', 'Deron Williams': '101114', 'Bobby Portis': '1626171', 'Marreese Speights': '201578', 'Gerald Green': '101123', 'Nikola Mirotic': '202703', 'Mike Muscala': '203488', 'DeAndre Jordan': '201599', 'Patrick Beverley': '201976', 'Victor Oladipo': '203506', 'Derrick Favors': '202324', 'Lou Williams': '101150', 'Stephen Curry': '201939', 'Dennis Schroder': '203471', 'John Wall': '202322', 'Taj Gibson': '201959', 'Clint Capela': '203991', 'Davis Bertans': '202722', 'Danny Green': '201980', 'Andre Iguodala': '2738', 'Wayne Selden': '1627782', 'Russell Westbrook': '201566', 'Paul George': '202331', 'Jaylen Brown': '1627759', 'Doug McDermott': '203926', 'Luc Mbah a Moute': '201601', 'DeMar DeRozan': '201942', 'Kelly Olynyk': '203482', 'Steven Adams': '203500', 'CJ Miles': '101139'}
playerDictRev = dict(map(reversed, playerDict.items()))
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
    file = open("testfile.txt","w")
    for y in store.keys():
        r = requests.get(store['game_'+str(i)])

        #print
        data = r.text
        soup=BeautifulSoup(data,"html.parser")
        for x in soup.find_all('a'):
            if (('/boxscores/' in x.get('href')) and (x.get('href') != '/boxscores/')) and ('index.fcgi?' not in x.get('href')) and ('pbp' not in x.get('href')) and ('shot-chart' not in x.get('href')) and ('month=' not in x.get('href')) and ('http://www.basketball-reference.com'+x.get('href') not in retList):
                retList.append('http://www.basketball-reference.com'+x.get('href'))
        dayLog['day_'+str(i)]=retList
        retList=[]
        i+=1
        #print dayLog.values()[0]
    file.write(str(dayLog))
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
    nameL=[]
    for elements in allData:
        advanced = elements.find_all('th')
        name = elements.find_all('th')
        AB=False
        if name[0].string == None or advanced[0].string == None:
            name =  "0"
            advanced = "0"
        else:
            name = name[0].string.strip()

        col = elements.find_all('td')
        i=0
        hold=[]
        gameScores={}
        hold.append(name)
        gameScores[name]={}

        if (name not in nameL):
            for column in col:
                if (name != 'Team Totals'):
                    if col[i].string== None:
                        column_dat = '0'
                    else:
                        column_dat = col[i].string.strip()
                    gameScores[name][headersList[i]]=column_dat
                    i+=1
        nameL.append(name)
        store.append(name)
        hold.append(gameScores)
        endL.append(hold)


    #print column_dat
    return endL[2:]

def getPidList():
    f =  open('players.txt', 'r')
    ret={}
    for x in f.readlines():
        ret[x.split(',')[1]]=x.split(',')[0]


def getPid(name):
    return playerDict[name]




def getDayBox(x):
    f = open('testfile.txt', 'r')
    return ast.literal_eval(f.read())['day_'+str(x)]

#print getPid('Al-Farouq Aminu')


#getBoxScoreUrls()
#print getDayBox(12)
#print getBoxScoreUrls()
#print list(set(getBoxScoreUrls()))
#print getBoxScoreUrls()
#getBoxScoreStats('http://www.basketball-reference.com/boxscores/201703130CHO.html')


def getDayData(x):
    boxList=getDayBox(x)
    hold=[]
    retList=[]
    for x in boxList:
        hold+=getBoxScoreStats(x)
    for x in hold:
        if 'FG' in (x[1])[x[0]]:

            retList.append(x)
    return retList



def getRando(listy):
    hold=listy
    num= len(listy)
    if (num > 10):
        return listy[:10]
    elif (num == 10):
        return listy
    else:
        while (num < 10):
            randy= random.choice(playerDict.keys())
            if (playerDict[randy] not in hold):
                listy.append(playerDict[randy])
                num=len(hold)
        return hold
    return hold


def getPlayID(name):
    return playerDictRev[name]


#print getDayData(12)

#print getBoxScoreUrls()
