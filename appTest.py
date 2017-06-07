from flask import Flask, render_template, request, redirect, url_for, session

from utils.getData import packageAllPlayers


app = Flask(__name__)



@app.route('/')
def stats():
    stats = packageAllPlayers()
    return render_template("playerStats2.html", list=stats)

if __name__ == "__main__":
    app.debug = True
    app.run()
