from flask import Flask, render_template, request, redirect, url_for, session

import hashlib, os
from utils.makeLeague import newLeague, maxplayers, joinLeague, getLeagues,getAllLeagues,addPlayer,getLeagueAthletes
from utils.playerPicker import addAthlete
from utils.auth import addUser, userLogin
from utils.getData import packageAllPlayers
from utils.playerIDGet import getPlayerIDs
from utils.dayStats import getStats, storeStats
from utils.gameScraper import getRando, getPlayID, getDayData
import random

app = Flask(__name__)
app.secret_key=os.urandom(32)

@app.route("/")
def logCheck():
    if 'user' in session:
        return redirect("/leagueform")
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'rmsg' in session:
        rmsg = session['rmsg']
        session.pop('rmsg')
        return render_template("home.html",rmsg=rmsg)
    if 'lmsg' in session:
        lmsg = session['lmsg']
        session.pop('lmsg')
        return render_template("home.html",lmsg=lmsg)
    return render_template("home.html")


@app.route("/auth", methods=['POST'])
def auth():
    if 'register' in request.form.keys():
        rmsg=addUser(request.form['user'], request.form['pass'])
        if 'succ' not in rmsg:
            session['rmsg'] = [False, rmsg]
        else:
            session['rmsg'] = [True, rmsg]
        return redirect("/home#register")
    else:
        info = userLogin(request.form['user'], request.form['pass'])
        lmsg=info[1]
        if(info[0]):
            session['user']=request.form['user']
            return redirect("/leagueform")
        else:
            session['lmsg'] = [False, lmsg]
            return redirect("/home#login")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/leagueform")
def leagueform():
    if 'user' in session:
        user = session['user']
        leagues = getLeagues(user)
        allLeagues=getAllLeagues(user)
        empl=[]
        msg=''
        if 'msg' in session:
            msg=session['msg']
            session.pop('msg')
        for g in leagues:
            if (maxplayers(g,session['user'])):
                empl.append(g)
        return render_template("leagueform.html", leagues=leagues, allLeagues=allLeagues, tenList=empl,msg=msg)
    if 'user' not in session:
        return redirect("/")
    if 'lerror' in session:
        lerror = session['lerror']
        session.pop('lerror')
        return render_template("leagueform.html", lerror=lerror, leagues=leagues)
    if 'jerror' in session:
        jerror = session['jerror']
        session.pop('jerror')
        return render_template("leagueform.html", jerror=jerror, leagues=leagues)
    return redirect("/")


@app.route("/authleague", methods=["POST"])
def authleague():
    if 'user' in session:
        name = request.form['name'].replace(" ","")
        user = request.form['user']
        if (name == ""):
            return redirect("/home")

        multiplier = request.form['points']
        multiplier += request.form['assists']
        multiplier += request.form['blocks']
        multiplier += request.form['steals']
        r = newLeague(name, user, multiplier)
        if r[0]:
            return redirect('/leagueform')
        else:
            session['lerror'] = r[1]
            return redirect('leagueform#makeLeague')
    else:
        return redirect("/")


@app.route("/authjoin", methods=["POST"])
def authjoin():
    if 'user' in session:
        name = request.form['name'].replace(" ","")
        user = request.form['user']
        r = joinLeague(name, user)
        if r[0]:
            return redirect("/leagueform")
        else:
            session['jerror'] = r[1]
            return redirect("/leagueform#joinLeague")
    else:
        return redirect("/home")


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('home'))




@app.route('/join/<leagueID>', methods=["POST", "GET"])
def joinNewLeague(leagueID):
    if 'user' in session:
        LID=leagueID
        username=session['user']
        leagues=getAllLeagues(username)
        if (session['user'] not in leagues[LID]):
            r = joinLeague(LID, username)
            if r[0]:
                return redirect("/leagueform")
            else:
                session['jerror'] = r[1]
                return redirect("/leagueform")

    else:
        redirect(url_for('home'))

@app.route('/viewleague/<leagueID>/')
def draft(leagueID):
    i=leagueID
    if 'user' in session:
        leagues = getLeagues(session['user'])
        leagueID=i
        emp=[]
        retDict={}
        y=''
        for x in leagues:
            if x == leagueID:
                for y in leagues[x]:
                    emp=[]
                    holdy={}
                    newName=''
                    allHold= getLeagueAthletes(leagueID, y)
                    if (allHold != []):
                        for k in allHold:
                            holdy={}
                            #print y, k,getPlayID(k),getStats(getPlayID(k))
                            if (getStats(getPlayID(k)) != {} and getStats(getPlayID(k)) not in emp ):
                                newName=k
                                holdy[getPlayID(newName)]=getStats(getPlayID(k))
                                emp.append(holdy)

                        retDict[y]=emp
        finalDict={}
        finalL=[]
        for x in retDict:

            finalL=[]
            for otherPlayers in retDict[x]:

                for l in otherPlayers:

                    #print x,otherPlayers[l]
                    empt={'PTS':0,'AST':0,'BLK':0,'STL':0,'FGA':0,'FG':0,'PF':0,'TOV':0}
                    for z in otherPlayers[l]:

                        empt['PTS']=int(empt['PTS'])+int(otherPlayers[l][z]['PTS'])
                        empt['AST']=int(empt['AST'])+int(otherPlayers[l][z]['AST'])
                        empt['BLK']=int(empt['BLK'])+int(otherPlayers[l][z]['BLK'])
                        empt['STL']=int(empt['STL'])+int(otherPlayers[l][z]['STL'])
                        empt['FGA']=int(empt['FGA'])+int(otherPlayers[l][z]['FGA'])
                        empt['FG']=int(empt['FG'])+int(otherPlayers[l][z]['FG'])
                        empt['PF']=int(empt['PF'])+int(otherPlayers[l][z]['PF'])
                        empt['TOV']=int(empt['TOV'])+int(otherPlayers[l][z]['TOV'])
                    finalL.append({otherPlayers.keys()[0]:empt})
            finalDict[x]=finalL
        return render_template('viewLeague.html', leagues=leagues,leagueID=leagueID, data=finalDict)
    else:
        return redirect(url_for("home"))
    return redirect(url_for("home"))

@app.route('/draft/<leagueID>')
def stats1(leagueID):

    LID=leagueID
    stats = packageAllPlayers()
    return render_template("playerStats2.html", list=stats, LID=LID)


@app.route('/add/<leagueID>', methods=["POST"])
def players4444(leagueID):
    LID=leagueID
    if 'user' in session:
        leagues = getLeagues(session['user'])
        if LID in leagues:
            LID=leagueID
            emp=[]
            for keys in request.form:
                numHolder= random.randint(0,2)
                if numHolder==0:
                    emp.append(request.form[keys])
            lol=[]
            lol=getRando(emp)
            for x in lol:
                g= addPlayer(LID, session['user'], x)

        else:
            return redirect(url_for("home"))
        return redirect(url_for("draft", leagueID=LID))
    else:
        return redirect(url_for("home"))
    return render_template("playerStats2.html")



@app.route('/players/<name>')
def player(name):
    pName = name
    if 'user' in session:
        data=getStats(name)
        retList=[]
        for x in data:
            retList.append(x)
        retList.sort()
        return render_template("playerStats.html", name=pName, days=retList,data=data)
    return redirect(url_for("home"))

@app.route('/update', methods=["POST"])
def update():

    if ('user' in session and 'day' in request.form):
        try:
            day=int(request.form['day'])
            storeStats(day, getDayData(day))
            session['msg']="Day has been updated, Please view one of your leagues to see."
            return redirect(url_for("leagueform"))
        except ValueError:
            return redirect(url_for("home"))
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
