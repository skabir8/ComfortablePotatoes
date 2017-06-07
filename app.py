from flask import Flask, render_template, request, redirect, url_for, session
import thread
import hashlib, os
from utils.makeLeague import newLeague, joinLeague, getLeagues
from utils.playerPicker import addAthlete
from utils.auth import addUser, userLogin
from utils.getData import packageAllPlayers
app = Flask(__name__)
app.secret_key=os.urandom(32)


@app.route("/")
def logCheck():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    print session
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
        print rmsg
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
    user = session['user']
    leagues = getLeagues(user)
    if 'lerror' in session:
        lerror = session['lerror']
        session.pop('lerror')
        return render_template("leagueform.html", lerror=lerror, leagues=leagues)
    if 'jerror' in session:
        jerror = session['jerror']
        session.pop('jerror')
        return render_template("leagueform.html", jerror=jerror, leagues=leagues)
    return render_template("leagueform.html", leagues=leagues)

@app.route("/authleague", methods=["POST"])
def authleague():
    name = request.form['name'].replace(" ","")
    user = request.form['user']
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

@app.route("/authjoin", methods=["POST"])
def authjoin():
    name = request.form['name'].replace(" ","")
    user = request.form['user']
    r = joinLeague(name, user)
    if r[0]:
        return redirect("/leagueform")
    else:
        session['jerror'] = r[1]
        return redirect("/leagueform#joinLeague")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('home'))

@app.route('/draft/<leagueID>')
def stats(leagueID):
    #listOfPlayersinLeague=getPlayersInLeague(leagueID)
    if 'user' in session and 'user' in listOfPlayersinLeague:
        LID=leagueID
        stats = packageAllPlayers()
        return render_template("playerStats.html", list=stats, LID=leagueID)
    else:
        redirect(url_for('home'))

@app.route('/draftresult/<leagueID>/')
def draft(leagueID):
    i=leagueID
    if 'user' in session:
        print request.form
    else:
        return redirect(url_for("/home"))
    return render_template('newLeague.html')





if __name__ == "__main__":
    app.debug = True
    app.run()
