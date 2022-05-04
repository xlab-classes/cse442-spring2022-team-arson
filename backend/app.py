import imghdr
import json
import sqlite3
import os
import PIL
from PIL import Image
import numpy as np
import urllib.request
import datetime
from flask import (Flask, render_template, request, redirect, send_from_directory, session)
from werkzeug.utils import secure_filename

app = Flask(__name__)

folder_path = 'static/images/'
app.config['UPLOAD_FOLDER'] = folder_path
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "amongus" # change to urandom later
PIL.Image.MAX_IMAGE_PIXELS = 999999999


def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    return conn

@app.route("/")
def index():
    if session['username']:
        return redirect('/home')
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
            session['username'] = username

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
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        privacy = request.form['privacy']
        image = request.files['img']
        
        if image and privacy:
            image.save(os.path.join('static', image.filename))
            return redirect('/mosaicify/' + privacy + '/' + image.filename)
            
    return render_template("index.html")

@app.route("/home/upload", methods = ('GET', 'POST'))
def home_upload():
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        privacy = request.form['privacy']
        image = request.files['img']
        
        if image and privacy:
            image.save(os.path.join('static', image.filename))
            return redirect('/mosaicify/' + privacy + '/' + image.filename)
            
    return render_template("index.html")

@app.route("/home/keyword", methods = ('GET', 'POST'))
def home_keyword():
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        keyword = request.form['keyword']
        privacy = request.form['privacy']

        if keyword and privacy:
            print (keyword)
            
    return render_template("index.html")

@app.route("/home/random", methods = ('GET', 'POST'))
def home_random():
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        privacy = request.form['privacy']

        print ("image status: " + privacy)

    return render_template("index.html")

@app.route("/myprofile")
def profile_redirect():
    if session['username'] == "":
        return redirect('/')

    return redirect('/profile/' + session['username'])

@app.route("/profile/<user>")
def profile(user):
    if not session['username']:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    poss_users = cursor.execute('SELECT * FROM users WHERE username = ?', (user,)).fetchall()

    cursor.close()
    conn.close()

    if len(poss_users) == 0:
        return redirect('/home')

    return render_template("index.html")

@app.route("/profile/images")
def profileimages():
    print('Profile Stuff')
    # Return the users profile 
    # session['username'] = '123'
    # username = session['username']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Grab from new table here
    userimages = cursor.execute('SELECT * FROM images WHERE username = ?', (session['username'],)).fetchall()
    print(userimages)

    # Create metadata if not any
    for images in userimages:
        imageID = images[1]
        # print(imageID)
        metadata = cursor.execute('SELECT * FROM meta WHERE imageID = ?',(imageID,)).fetchall()
        if not metadata:
            # userimages = cursor.execute('SELECT * FROM images WHERE imageID = ?', (imageID,)).fetchall()
            # print(metadata)
            filename = images[3]
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static', filename))
            size = os.path.getsize(image_path)
            creation_time = os.path.getctime(image_path)
            cursor.execute('INSERT INTO meta (dataname, data, imageID) VALUES (?, ?, ?)', ('size',str(size),imageID))
            cursor.execute('INSERT INTO meta (dataname, data, imageID) VALUES (?, ?, ?)', ('ctime',str(int(creation_time)),imageID)) # Time to epoch
            conn.commit()

    # Retrieve metadata
    dictionary = []
    for images in userimages:
        entry = {}
        entry['imageID'] = images[1]
        metadata = cursor.execute('SELECT * FROM meta WHERE imageID = ?',(images[1],)).fetchall()
        for meta in metadata:
            dataname, data = meta[0],meta[1]
            entry[dataname] = data
        dictionary.append(entry)

    cursor.close()
    conn.close()

    return json.dumps(dictionary)


@app.route("/settings", methods = ('GET', 'POST'))
def settings():
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        currentPass = request.form['currentPass']
        newUser1 = request.form['newUser1']
        newUser2 = request.form['newUser2']
        newPass1 = request.form['newPass1']
        newPass2 = request.form['newPass2']

        conn = get_db_connection()
        cursor = conn.cursor()

        pass_db = cursor.execute('SELECT pass FROM users WHERE username = ?', (session['username'],)).fetchall()[0][0]

        if not pass_db == currentPass:
            return redirect('/settings')

        if newUser1 and newUser2 and newPass1 and newPass2:
            if not newUser1 == newUser2:
                return redirect('/settings')
            elif not newPass1 == newPass2:
                return redirect('/settings')
            cursor.execute('UPDATE users SET username = ?, pass = ? WHERE pass = ?', (newUser1, newPass1, currentPass))
            conn.commit()
            session['username'] = newUser1
            return redirect('/settings/updated')
        
        if newUser1 and newUser2:
            if not newUser1 == newUser2:
                return redirect('/settings')
            
            all_users = cursor.execute('SELECT * FROM users WHERE username = ?', (newUser1,)).fetchall()
            if len(all_users) > 0:
                return redirect('/settings')

            cursor.execute('UPDATE users SET username = ? WHERE pass = ?', (newUser1, currentPass))
            conn.commit()
            session['username'] = newUser1
            return redirect('/settings/updated')

        if newPass1 and newPass2:
            if not newPass1 == newPass2:
                return redirect('/settings')
            cursor.execute('UPDATE users SET pass = ? WHERE pass = ?', (newPass1, currentPass))
            conn.commit()
            return redirect('/settings/updated')

        cursor.close()
        conn.close()

        print(pass_db)
    
    return render_template("index.html")

@app.route("/settings/updated")
def settings_updated():
    if session['username'] == "":
        return redirect('/')

    return render_template("index.html")

@app.route("/mosaicify/<privacy>/<user_image>")
def mosaicify(privacy, user_image):
    if session['username'] == "":
        return redirect('/')

    filename = user_image
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static', filename))
    
    # image to be mosaic'd
    target_image = Image.open(image_path)

    # images to tile
    input_images = getImages(folder_path)

    # size of grid 
    resolution = (64, 64)
    # resolution = (256, 256)

    # get largest image in input images
    largest_image = max(input_images, key=lambda x: x.size[0] * x.size[1])

    for img in input_images:
    # img.resize((target_image.size[0] // resolution[0], target_image.size[1] // resolution[1]), Image.LANCZOS)
        img.thumbnail((target_image.size[0] // resolution[0], target_image.size[1] // resolution[1]), Image.LANCZOS)

    output_mosaic = CreateMosaic(target_image, input_images, resolution)
    print('Mosaic Complete!')

    img_name = user_image.split('.')
    new_img = img_name[0] + '_out.' + img_name[1]
    link = os.path.join('static', new_img)

    output_mosaic.thumbnail((   (target_image.size[0] * 5),  (target_image.size[1] * 5)), Image.LANCZOS)
    output_mosaic.save(link)
    return redirect('/results/' + privacy + "/" + new_img)

@app.route("/results/<privacy>/<user_image>", methods = ('GET', 'POST'))
def results(privacy, user_image):
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        print(session['username'])
        conn = get_db_connection()
        cursor = conn.cursor()

        newID = cursor.execute('SELECT MAX(imageID) FROM images').fetchall()[0][0] + 1

        cursor.execute('INSERT INTO images (username, imageID, setting, imageName) VALUES (?, ?, ?, ?)', (session['username'], newID, privacy, user_image))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/view/id/' + privacy + '/' + str(newID))
    
    return render_template('index.html')

@app.route('/image/<path:filename>') 
def send_file(filename):
    if session['username'] == "":
        return redirect('/')

    return send_from_directory('static', filename)

@app.route('/id/<int:imageID>') 
def send_file2(imageID):
    if session['username'] == "":
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    image_info = cursor.execute('SELECT * FROM images WHERE imageID = ?', (imageID,)).fetchall()

    cursor.close()
    conn.close()

    # image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static', image_info[0][3]))
    # imgpath = Image.open(image_path)
    # imgpath.resize((600,600),Image.ANTIALIAS).save(f"./static/small_{image_info[0][3]}")
    return send_from_directory('static', image_info[0][3])

@app.route("/view/id/<privacy>/<int:image_id>", methods = ('GET', 'POST'))
def view(privacy, image_id):
    if session['username'] == "":
        return redirect('/')

    if request.method == "POST":
        new_privacy = request.form["privacy"]

        conn = get_db_connection()
        cursor = conn.cursor()

        image_info = cursor.execute('SELECT * FROM images WHERE imageID = ?', (image_id,)).fetchall()

        if not image_info[0][0] == session['username']:
            return redirect('/view/id/' + privacy + '/' + str(image_id))

        cursor.execute('UPDATE images SET setting = ? WHERE imageID = ?', (new_privacy, image_id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/view/id/' + new_privacy + '/' + str(image_id))

    conn = get_db_connection()
    cursor = conn.cursor()

    image_info = cursor.execute('SELECT * FROM images WHERE imageID = ?', (image_id,)).fetchall()

    cursor.close()
    conn.close()

    if ((not image_info[0][0] == session['username']) and (image_info[0][2] == "private")):
        return redirect('/home')

    return render_template('index.html')

@app.route("/logout")
def logout():
    session['username'] = ""
    return redirect('/')

#======================================================================================================

def calcAverageRGB(image):

    img = np.array(image)

    # w - image width || h - image height || d - depth of colors, i.e. rgba = 4, rgb = 3
    w, h, d = img.shape

    # get average
    # create linear array of d-tuple (3 for rgb) with length w*h for all pixels and average over each rgb tuple
    return tuple(np.average(img.reshape(w * h, d), axis=0))

def tileImage(image, size):
    """
    _________________
    |_1_|_2_|_3_|_4_|
    |_5_|_6_|_7_|_8_|
    |_9_|_._|_._|_._|
    |_._|_._|_._|_._|
    |_._|_._|_._|_._|
    gridify the image, return this as a list of individual images
    """
    m, n = size
    w, h = image.size[0] // n, image.size[1] // m
    imgs = []
    for j in range(m):
        for i in range(n):
            chunk = image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
            imgs.append(chunk)
    return imgs

def getImages(imageDir):
    files = os.listdir(imageDir)
    imgs = []
    for file in files:
        # get absolute path of image, need to join with /images/filename
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            fp = open(filePath, "rb")
            im = Image.open(fp)
            im.load()
            imgs.append(im)
            fp.close()
        except Exception:
            print(f"Error loading image: {file}")

    # return a list of all the images in the folder
    return imgs

def findClosestMatch(input_avg, avgs):

    index = 0                # current index
    min_index = 0            # index of running min avg.
    min_dist = float('inf')  # starting dist at infinity so first image check starts the tracking

    # calculate euclidean distance w.r.t the RGB color-space (3-dim)
    # track the minimum distance to get the image w closest avg color
    for sample in avgs:
        dist = (((sample[0] - input_avg[0]) ** 2) +
                ((sample[1] - input_avg[1]) ** 2) +
                ((sample[2] - input_avg[2]) ** 2))
        # if lower dist found, update min trackers
        if dist < min_dist:
            min_dist = dist
            min_index = index

        index += 1

    return min_index

def CreateMosaic(target_image, input_images, resolution):

    target_grid = tileImage(target_image, resolution)
    output_images = []

    # calculate average RGB for all the images
    avgs = []
    for img in input_images:
        avgs.append(calcAverageRGB(img))

    # calculate average RGB for each chunk of target image
    # find the closest image
    # add that image to the output images
    for img in target_grid:
        avg = calcAverageRGB(img)
        match_index = findClosestMatch(avg, avgs)
        output_images.append(input_images[match_index])

    # create new image with dimensions = mosaic resolution * largest of the images
    m, n = resolution
    width, height = max([img.size[0] for img in output_images]), max([img.size[1] for img in output_images])
    MOSAIC = Image.new('RGB', size=(n * width, m * height))

    # tile images onto original image
    for i in range(len(output_images)):
        row = int(i / n)
        col = i - n * row
        MOSAIC.paste(output_images[i], (col * width, row * height))

    return MOSAIC