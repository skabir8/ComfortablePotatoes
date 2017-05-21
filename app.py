from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/newLeague')
def newLeague():
    return render_template('newLeague.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
