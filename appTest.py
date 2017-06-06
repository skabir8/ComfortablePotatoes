from flask import Flask, render_template, request, redirect, url_for, session

from utils.getData import packagePlayers
from utils.playerIDGet import getPlayerIDs

app = Flask(__name__)



@app.route('/')
def stats():
    listPlayers = getPlayerIDs()
    stats = packagePlayers(listPlayers)
    return render_template("playerStats.html", list=stats)

if __name__ == "__main__":
    app.debug = True
    app.run()
