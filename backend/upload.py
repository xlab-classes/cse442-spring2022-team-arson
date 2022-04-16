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
# upload.config = './uploads' Not working for some old reason..

@upload.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory('./uploads',filename)

@upload.route("/home", methods = ('GET', 'POST'))
def home():
    if request.method == "POST":
        legal = ['jpg','jpeg','png']
        msg = ""
        if 'file' not in request.files:
            msg = "Nothing Found"
        else:    
            file = request.files['file']
            # See if extension is legal
            file_extension =  file.filename.rsplit('.',1)[1]
            print(request.files)
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
                print(filename)
                # Save in folder
                file.save(os.path.join('./uploads',filename))
                msg ="File uploaded!"
            return render_template("upload.html",msg=msg,img=filename)
        return render_template("upload.html",msg=msg)
        

    elif request.method == "GET":
        if 'user' in session:
            return render_template("upload.html",msg=f"welcome back! {session['user']}")
        else:
            return render_template("upload.html",msg=f"You are currently not logged in.")
    
    return render_template("upload.html")


# @upload.route('/mosiac/')


# @upload.route('/sort')

@upload.route("/profile")
def profile():
    if 'user' in session:
        print(session['user'])
    return render_template("upload.html")

@upload.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/')

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