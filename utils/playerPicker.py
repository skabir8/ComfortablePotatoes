import sqlite3

def addAthlete(leagueNum, user, athlete):
    db=sqlite3.connect("data/league.db")
    c=db.cursor()
    q="select athletes from League"+str(leagueNum)
    c.execute(q)
    fullAthletes=c.fetchall()
    for athletes in fullAthletes:
        if athlete in athletes:
            return "Athlete already picked!"
    q="select athletes from League"+str(leagueNum)+" where user = \'"+user+"\'"
    c.execute(q)
    stringAthletesOld=c.fetchall()[0][0]
    if not stringAthletesOld:
        stringAthletesNew=athlete
    else:
        stringAthletesNew=stringAthletesOld+","+athlete
    q="update League"+str(leagueNum)+" set athletes = \'"+stringAthletesNew+"\' where user = \'"+user+"\'"
    c.execute(q)
    db.commit()
    db.close()

#addAthlete(1, "blarg1", "aaaaaaaaaaaaaaaaaaaaaa")
