import sqlite3
from flask import (Flask, render_template, request, redirect)

local_user = ""

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    return conn

@app.route("/")
def index():
    local_user = ""
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

        if privacy:
            return redirect('/results/' + privacy)
            
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

@app.route("/results/<privacy>", methods = ('GET', 'POST'))
def results(privacy):
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()

        newID = cursor.execute('SELECT MAX(imageID) FROM images').fetchall()[0][0] + 1

        cursor.execute('INSERT INTO images (username, imageID, setting) VALUES (?, ?, ?)', (local_user, newID, privacy))
        conn.commit()

        images = cursor.execute('SELECT * FROM images').fetchall()
        print(images)

        cursor.close()
        conn.close()

        return redirect('/view/id/' + str(newID))
    return render_template("index.html")

@app.route("/view/id/<int:image_id>")
def view(image_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    image_info = cursor.execute('SELECT * FROM images WHERE imageID = ?', (image_id,)).fetchall()

    cursor.close()
    conn.close()

    if ((not image_info[0][0] == local_user) and (image_info[0][2] == "Private")):
        return redirect('/home')

    return render_template('index.html')
