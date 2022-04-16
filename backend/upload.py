import uuid
from flask import Blueprint, render_template, send_from_directory, session, redirect, request
from datetime import datetime
from exif import Image
from uuid import uuid4
import os
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    return conn

upload = Blueprint('upload', __name__, template_folder='templates')
upload.config = './uploads'

@upload.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(upload.config['UPLOAD_FOLDER'],filename)

@upload.route('/images/')
def images():
    # Post Form
    if request.method == "POST":
        legal = ['jpg','jpeg','png']
        if 'file' not in request.files:
            msg = "Nothing Found"
        else:    
            file = request.files['file']
            # See if extension is legal
            file_extension =  file.filename.rsplit('.',1)[1]
            if file_extension in legal:

                # file.read()
                # Open file
                # Insert commands here
                # conn = get_db_connection()
                # cursor = conn.cursor()

                # cursor.execute('INSERT * TO')

                # cursor.close()
                # conn.close()

                filename = f"{uuid4()}.{file_extension}"
                # Save in folder
                file.save(os.path.join(upload.config['UPLOAD_FOLDER'],filename))

            render_template("upload.html")

    elif request.method == "GET":
        return render_template("upload.html")


@upload.route("/home", methods = ('GET', 'POST'))
def home():
    if 'user' in session:
        print(session['user'])
    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

        return redirect('/results')
    return render_template("upload.html")

@upload.route("/home/upload", methods = ('GET', 'POST'))
def home_upload():
    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

        return redirect('/results')
    return render_template("upload.html")


@upload.route("/profile")
def profile():
    if 'user' in session:
        print(session['user'])
    return render_template("upload.html")

# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/home/upload
# http://127.0.0.1:5000/profile/


# @upload.route('/sort/date')
# def date():
#     # Get all images
#     # EXIF file
#     return render_template()

# Sort by ascending date
# Sort by descending date 
# In react somehow

# TODO Instead of using EXIF data use mysql records instead...
# TODO Save as a binary file as a record instead of a upload folder