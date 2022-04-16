import sqlite3
from flask import (Flask, render_template, request, redirect)

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['pass']

        conn = get_db_connection()
        cursor = conn.cursor()

        all_users = cursor.execute('SELECT * FROM users WHERE username = ? AND pass = ?', (username, passwd)).fetchall()

        cursor.close()
        conn.close()

        if (len(all_users) > 0):
            global local_user
            local_user = username

            return redirect('/home')
    return render_template("index.html")

@app.route("/signup", methods = ('GET', 'POST'))
def signup():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['pass']

        if username and passwd:
            conn = get_db_connection()
            cursor = conn.cursor()

            poss_users = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchall()

            if (len(poss_users) == 0):
                cursor.execute('INSERT INTO users (username, pass) VALUES (?, ?)', (username, passwd))

                conn.commit()
                cursor.close()
                conn.close()
                return redirect('/login')

            conn.commit()
            cursor.close()
            conn.close()
    return render_template('index.html')

@app.route("/home", methods = ('GET', 'POST'))
def home():
    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

        return redirect('/results')
    return render_template("index.html")

@app.route("/home/upload", methods = ('GET', 'POST'))
def home_upload():
    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

        return redirect('/results')
    return render_template("index.html")

@app.route("/home/keyword", methods = ('GET', 'POST'))
def home_keyword():
    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

        return redirect('/results')
    return render_template("index.html")

@app.route("/home/random", methods = ('GET', 'POST'))
def home_random():
    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

        return redirect('/results')
    return render_template("index.html")

@app.route("/profile/")
def profile():
    return render_template("index.html")

@app.route("/settings")
def settings():
    return render_template("index.html")

@app.route("/settings/updated")
def settings_updated():
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("index.html")