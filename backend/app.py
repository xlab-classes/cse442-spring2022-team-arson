import sqlite3
<<<<<<< HEAD
import os
from PIL import Image
import numpy as np
import urllib.request
from flask import (Flask, render_template, request, redirect, send_from_directory)

local_user = ""

app = Flask(__name__)

folder_path = 'static/images/'
app.config['UPLOAD_FOLDER'] = folder_path
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

=======
from flask import (Flask, render_template, request, redirect)

app = Flask(__name__)

>>>>>>> dev
def get_db_connection():
    conn = sqlite3.connect('../database/database.db')
    return conn

@app.route("/")
def index():
<<<<<<< HEAD
    local_user = ""
=======
>>>>>>> dev
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

<<<<<<< HEAD
        if privacy:
            return redirect('/mosaicify/' + privacy + '/trew.png')
            
=======
        print ("image status: " + privacy)

        return redirect('/results')
>>>>>>> dev
    return render_template("index.html")

@app.route("/home/upload", methods = ('GET', 'POST'))
def home_upload():
    if request.method == "POST":
        privacy = request.form['privacy']

<<<<<<< HEAD
        if privacy:
            return redirect('/mosaicify/' + privacy + '/trew.png')
            
=======
        print ("image status: " + privacy)

        return redirect('/results')
>>>>>>> dev
    return render_template("index.html")

@app.route("/home/keyword", methods = ('GET', 'POST'))
def home_keyword():
    if request.method == "POST":
        privacy = request.form['privacy']

<<<<<<< HEAD
        if privacy:
            return redirect('/results/' + privacy)
            
=======
        print ("image status: " + privacy)

        return redirect('/results')
>>>>>>> dev
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

<<<<<<< HEAD
@app.route("/mosaicify/<privacy>/<user_image>")
def mosaicify(privacy, user_image):
    # edit = request.GET.get('edit',None)
    # filename = request.GET.get('filename',None)

    # if filename.startswith('/image'):

    #     filename = filename.split('/')[3]
    filename = 'trew.png'
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
        # scale input images to size of largest image so they are g.t.e. the largest image of the set
        # img.thumbnail( (largest_image.size[0] / resolution[1], largest_image.size[1] / resolution[0]) )
        # img.resize( (largest_image.size[0] // resolution[1], largest_image.size[1] // resolution[0]) )
        ### OR ###
        # scale input images down to keep target_image aspect ratio
        # img.resize((target_image.size[0] // resolution[1], target_image.size[1] // resolution[0]))
        img.resize((target_image.size[0] // resolution[0], target_image.size[1] // resolution[1]), Image.LANCZOS)

    output_mosaic = CreateMosaic(target_image, input_images, resolution)
    print('Mosaic Complete!')

    new_img = "trew_out.png"

    link = os.path.join('static', new_img)
    output_mosaic.save(link)

    return redirect('/results/' + privacy + "/" + new_img)

@app.route("/results/<privacy>/<user_image>", methods = ('GET', 'POST'))
def results(privacy, user_image):
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
    
    return render_template('index.html')

@app.route('/image/<path:filename>') 
def send_file(filename):
    return send_from_directory('static', filename)

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
=======
@app.route("/results")
def results():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("index.html")
>>>>>>> dev
