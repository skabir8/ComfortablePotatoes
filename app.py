from flask import Flask, render_template, request, redirect, url_for, session

import hashlib, os
from utils.makeLeague import newLeague, joinLeague, getLeagues,getAllLeagues,addPlayer,getLeagueAthletes
from utils.playerPicker import addAthlete
from utils.auth import addUser, userLogin
from utils.getData import packageAllPlayers
from utils.playerIDGet import getPlayerIDs
from utils.dayStats import getStats
from utils.gameScraper import getRando
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
        return render_template("leagueform.html", leagues=leagues, allLeagues=allLeagues)
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
    print i
    if 'user' in session:
        leagues = getLeagues(session['user'])
        leagueID=i
        emp=[]
        for x in leagues:
            if x == leagueID:
                for y in leagues[x]:
                    emp.append(y)
                    print getLeagueAthletes(leagueID, y)
                return render_template('viewLeague.html', leagues=leagues,leagueID=leagueID)
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
                print g



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


if __name__ == "__main__":
    app.debug = True
    app.run()
