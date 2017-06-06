from flask import Flask, render_template, request, redirect, url_for, session
import thread
from flask_socketio import SocketIO, emit, send
import hashlib, os
import eventlet
from utils.makeLeague import newLeague
from utils.playerPicker import addAthlete
from utils.auth import addUser, userLogin
from utils.statsScraper import packagePlayers

eventlet.monkey_patch(os=False)
app = Flask(__name__)
app.secret_key = 'as9pdfuhasodifuhasiodfhuasiodfhuasiodfhuasodifuh'
socketio = SocketIO(app)


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
            return redirect("/profile")
        else:
            session['lmsg'] = [False, lmsg]
            return redirect("/home#login")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for('home'))

@app.route('/stats')
def stats():
    stats = packagePlayers([201566,2544,201935])
    return render_template("playerStats.html", list=stats)

@app.route('/makeLeague', methods=['POST'])
def makeLeague():
    if 'user' in session:
        print request.form
        newLeague(request.form['user1'],request.form['user2'],request.form['user3'],request.form['user4'],request.form['user5'])
    else:
        return redirect(url_for("/home"))
    return redirect(url_for("/home"))

@app.route('/draft/<leagueID>/')
def draft(leagueID):
    i=leagueID
    if 'user' in session:
        print request.form
    else:
        return redirect(url_for("/home"))
    return render_template('newLeague.html')

@socketio.on('swag', namespace='/draft')
def handleSwag(lol):
	print(lol)
@socketio.on('message', namespace='/draft')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@app.route('/league')
def index():
    if 'user' in session:
        user= session["user"]
        print user
    else:
        user = ""
    return render_template('league.html', user = user)

@socketio.on('swag', namespace='/league')
def handleSwag(lol):
	print(lol)
	send(lol, broadcast=True)

@socketio.on('message', namespace='/league')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)



@app.route('/league1')
def index1():
    if 'user' in session:
        user= session["user"]
        print user
    else:
        user = ""
    return render_template('league1.html', user = user)

@socketio.on('swag', namespace='/league1')
def handleSwag(lol):
	print(str(lol)+'loooooooooooooooo')


@socketio.on('message', namespace='/league1')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)




if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
