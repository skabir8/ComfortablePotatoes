from flask import Flask, render_template, request, redirect, url_for, session
import thread
from flask_socketio import SocketIO, emit, send
import hashlib, os
import eventlet
from utils.auth import addUser, userLogin
from utils.statsScraper import packagePlayers

eventlet.monkey_patch(os=False)
app = Flask(__name__)
app.secret_key = 'as9pdfuhasodifuhasiodfhuasiodfhuasiodfhuasodifuh'
socketio = SocketIO(app)


@app.route("/")
def logCheck():
    if 'userID' in session:
        return redirect(url_for('home'))
    if("msg" in request.args.keys()):
        return redirect(url_for('dispLogin')+"?msg="+request.args['msg'])
    return redirect(url_for('dispLogin'))




@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def dispLogin():
    if 'userID' in session:
        return render_template('alreadyLogged.html', msg=session['userID'])
    if 'msg' in request.args.keys():
        return render_template("login.html", msg=request.args['msg'])
    return render_template("login.html", msg ="")

@app.route("/auth", methods=['POST'])
def auth():
    if 'register' in request.form.keys():
        msg=addUser(request.form['user'], request.form['pass'])
    else:
        info = userLogin(request.form['user'], request.form['pass'])
        if(info[0]=='True'):
            msg=info[1]
            session['userID']=request.form['user']
        msg=info[1]
    return redirect(url_for('logCheck')+"?msg="+msg)

@app.route("/logout")
def logout():
    session.pop('userID')
    return redirect(url_for('logCheck'))

@app.route('/stats')
def stats():
    stats = packagePlayers([201566,2544,201935])
    return render_template("playerStats.html", list=stats)



@app.route('/league')
def index():
    if 'userID' in session:
        user= session["userID"]
        print user
    else:
        user = ""
    return render_template('league.html', user = user)

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('swag')
def handleSwag(lol):
	print(lol)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
