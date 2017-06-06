from flask import Flask, render_template, request, redirect, url_for, session

from utils.getData import packagePlayers

app = Flask(__name__)



@app.route('/')
def stats():
    stats = packagePlayers([201566,2544,201939])
    return render_template("playerStats.html", list=stats)

if __name__ == "__main__":
    app.debug = True
    app.run()
