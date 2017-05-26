from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, os
#from utils.auth import addUser, userLogin
from utils.statsScraper import packagePlayers

app = Flask(__name__)
app.secret_key=os.urandom(32)

'''
@app.route("/temp")
def send():
    if 'userID' in session:
        return redirect(url_for('loggedIn'))
    if("msg" in request.args.keys()):
        return redirect(url_for('dispLogin')+"?msg="+request.args['msg'])
    return redirect(url_for('dispHome'))
'''

@app.route("/")
def home():
    return render_template("newhome.html")

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
    return redirect(url_for('send')+"?msg="+msg)

@app.route("/logout")
def logout():
    session.pop('userID')
    return redirect(url_for('send'))


@app.route('/loggedIn')
def loggedIn():
    return render_template('loggedIn.html')

@app.route('/stats')
def stats():
    stats = packagePlayers([201566,2544,201935])
    return render_template("playerStats.html", list=stats)

if __name__ == "__main__":
    app.debug = True
    app.run()
