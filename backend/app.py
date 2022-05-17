import json
import os
import PIL
from PIL import Image
import numpy as np
import math
import urllib.request
import datetime
from flask import (Flask, render_template, request, redirect, send_from_directory, session, send_file)
from werkzeug.utils import secure_filename
from icrawler.builtin import GoogleImageCrawler
from icrawler import ImageDownloader
from random_word import RandomWords
from flask_mysql_connector import MySQL
from datetime import date

app = Flask(__name__)

folder_path = 'static/images/'
app.config['UPLOAD_FOLDER'] = folder_path
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = "amongus" # change to urandom later
PIL.Image.MAX_IMAGE_PIXELS = 999999999

app.config['MYSQL_HOST'] = 'oceanus.cse.buffalo.edu'
app.config['MYSQL_USER'] = 'jhhou'
app.config['MYSQL_PASSWORD'] = '50292168'
app.config['MYSQL_DATABASE'] = 'cse442_2022_spring_team_u_db'
mysql = MySQL(app)

def get_db_connection():
    conn = mysql.connection
    return conn

@app.route("/")
def index():
    if not session.get('username') is None:
        return redirect('/home')

    return render_template("index.html")

@app.route("/login", methods = ('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['pass']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND pass = %s', (username, passwd))
        all_users = cursor.fetchall()

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

            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            poss_users = cursor.fetchall()            

            if (len(poss_users)== 0):
                cursor.execute('INSERT INTO users (username, pass) VALUES (%s, %s)', (username, passwd))

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
    if session.get('username') is None:
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
    if session.get('username') is None:
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
    if session.get('username') is None:
        return redirect('/')

    if request.method == "POST":
        keyword = request.form['keyword']
        privacy = request.form['privacy']

        if keyword and privacy:
            image = RandomImageScrape(keyword)
            return redirect('/mosaicify/' + privacy + '/' + image)
            
    return render_template("index.html")

@app.route("/home/random", methods = ('GET', 'POST'))
def home_random():
    if session.get('username') is None:
        return redirect('/')

    if request.method == "POST":
        privacy = request.form['privacy']
        
        # no keyword default to random keyword being generated
        image = RandomImageScrape()

        if privacy:
            return redirect('/mosaicify/' + privacy + '/' + image)
           
        print("image status: " + privacy)

    return render_template("index.html")

@app.route("/home/images")
def getRecentImages():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM images WHERE setting = %s ORDER BY imageID DESC', ("public",))
    allImages = cursor.fetchall()
    recentImages = allImages[:12]

    home_dictionary = []
    for image in recentImages:
        entry = {}
        entry['imageID'] = image[1]
        home_dictionary.append(entry)

    cursor.close()
    conn.close()

    return json.dumps(home_dictionary)

@app.route("/downloadImage/<imageID>")
def downloadImage(imageID):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT imageName FROM images WHERE imageID = %s', (imageID,))
    imageName = cursor.fetchall()

    link = os.path.join('static', imageName[0][0])
    return send_file(link, as_attachment = True)

@app.route("/downloadResult/<imageName>")
def downloadResult(imageName):
    link = os.path.join('static', imageName)
    return send_file(link, as_attachment = True)

@app.route("/myprofile")
def profile_redirect():
    if session.get('username') is None:
        return redirect('/')

    return redirect('/profile/' + session['username'])

@app.route("/profile/<user>")
def profile(user):
    if session.get('username') is None:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s', (user,))
    poss_users = cursor.fetchall()

    cursor.close()
    conn.close()

    if len(poss_users) == 0:
        return redirect('/home')

    return render_template("index.html", profile_user = user)

@app.route("/profile/images/<user>")
def profileimages(user):
    # print('Profile Stuff')
    # Return the users profile 
    # session['username'] = '123'
    # username = session['username']

    conn = get_db_connection()
    cursor = conn.cursor()

    if session['username'] == user:
        # Grab from new table here
        cursor.execute('SELECT * FROM images WHERE username = %s', (user,))
        userimages = cursor.fetchall()
        # print(userimages)
    
    else:
        # Grab from new table here
        cursor.execute('SELECT * FROM images WHERE username = %s AND setting = %s', (user, "public"))
        userimages = cursor.fetchall()
        # print(userimages)

    # Create metadata if not any
    for images in userimages:
        imageID = images[1]
        # print(imageID)
        cursor.execute('SELECT * FROM meta WHERE imageID = %s',(imageID,))
        metadata = cursor.fetchall()
        if not metadata:
            # userimages = cursor.execute('SELECT * FROM images WHERE imageID = ?', (imageID,)).fetchall()
            # print(metadata)
            filename = images[3]
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static', filename))
            size = os.path.getsize(image_path)
            creation_time = os.path.getctime(image_path)
            cursor.execute('INSERT INTO meta (dataname, data, imageID) VALUES (%s, %s, %s)', ('size',str(size),imageID))
            cursor.execute('INSERT INTO meta (dataname, data, imageID) VALUES (%s, %s, %s)', ('ctime',str(int(creation_time)),imageID)) # Time to epoch
            conn.commit()

    # Retrieve metadata
    dictionary = []
    for images in userimages:
        entry = {}
        entry['imageID'] = images[1]
        cursor.execute('SELECT * FROM meta WHERE imageID = %s',(images[1],))
        metadata = cursor.fetchall()
        for meta in metadata:
            dataname, data = meta[0],meta[1]
            entry[dataname] = data
        dictionary.append(entry)

    cursor.close()
    conn.close()

    return json.dumps(dictionary)

@app.route("/settings", methods = ('GET', 'POST'))
def settings():
    if session.get('username') is None:
        return redirect('/')

    if request.method == "POST":
        currentPass = request.form['currentPass']
        newUser1 = request.form['newUser1']
        newUser2 = request.form['newUser2']
        newPass1 = request.form['newPass1']
        newPass2 = request.form['newPass2']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT pass FROM users WHERE username = %s', (session['username'],))
        pass_db = cursor.fetchall()[0][0]

        if not pass_db == currentPass:
            return redirect('/settings')

        if newUser1 and newUser2 and newPass1 and newPass2:
            if not newUser1 == newUser2:
                return redirect('/settings')
            elif not newPass1 == newPass2:
                return redirect('/settings')
            cursor.execute('UPDATE users SET username = %s, pass = %s WHERE username = %s', (newUser1, newPass1, session['username']))
            cursor.execute('UPDATE images SET username = %s WHERE username = %s', (newUser1, session['username']))
            conn.commit()
            session['username'] = newUser1
            return redirect('/settings/updated')
        
        if newUser1 and newUser2:
            if not newUser1 == newUser2:
                return redirect('/settings')
            
            cursor.execute('SELECT * FROM users WHERE username = %s', (newUser1,))
            all_users = cursor.fetchall()
            if len(all_users) > 0:
                return redirect('/settings')

            cursor.execute('UPDATE users SET username = %s WHERE username = %s', (newUser1, session['username']))
            cursor.execute('UPDATE images SET username = %s WHERE username = %s', (newUser1, session['username']))
            conn.commit()
            session['username'] = newUser1
            return redirect('/settings/updated')

        if newPass1 and newPass2:
            if not newPass1 == newPass2:
                return redirect('/settings')
            cursor.execute('UPDATE users SET pass = %s WHERE username = %s', (newPass1, session['username']))
            conn.commit()
            return redirect('/settings/updated')

        cursor.close()
        conn.close()

        print(pass_db)

    return render_template("index.html")

@app.route("/settings/updated", methods = ('GET', 'POST'))
def settings_updated():
    if session.get('username') is None:
        return redirect('/')

    if request.method == "POST":
        currentPass = request.form['currentPass']
        newUser1 = request.form['newUser1']
        newUser2 = request.form['newUser2']
        newPass1 = request.form['newPass1']
        newPass2 = request.form['newPass2']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT pass FROM users WHERE username = %s', (session['username'],))
        pass_db = cursor.fetchall()[0][0]

        if not pass_db == currentPass:
            return redirect('/settings')

        if newUser1 and newUser2 and newPass1 and newPass2:
            if not newUser1 == newUser2:
                return redirect('/settings')
            elif not newPass1 == newPass2:
                return redirect('/settings')
            cursor.execute('UPDATE users SET username = %s, pass = %s WHERE username = %s', (newUser1, newPass1, session['username']))
            conn.commit()
            session['username'] = newUser1
            return redirect('/settings/updated')
        
        if newUser1 and newUser2:
            if not newUser1 == newUser2:
                return redirect('/settings')
            
            cursor.execute('SELECT * FROM users WHERE username = %s', (newUser1,))
            all_users = cursor.fetchall()
            if len(all_users) > 0:
                return redirect('/settings')

            cursor.execute('UPDATE users SET username = %s WHERE username = %s', (newUser1, session['username']))
            conn.commit()
            session['username'] = newUser1
            return redirect('/settings/updated')

        if newPass1 and newPass2:
            if not newPass1 == newPass2:
                return redirect('/settings')
            cursor.execute('UPDATE users SET pass = %s WHERE username = %s', (newPass1, session['username']))
            conn.commit()
            return redirect('/settings/updated')

        cursor.close()
        conn.close()

    return render_template("index.html")

@app.route("/mosaicify/<privacy>/<user_image>")
def mosaicify(privacy, user_image):
    if session.get('username') is None:
        return redirect('/')

    filename = user_image
    image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static', filename))
    
    # image to be mosaic'd
    target_image = Image.open(image_path)

    # images to tile
    input_images = []
    images_folder = os.listdir(folder_path)

    for file in images_folder:
        # get absolute path of image, need to join with /images/filename
        file_path = os.path.abspath(os.path.join(folder_path, file))
        try:
            fp = open(file_path, "rb")
            img = Image.open(fp)
            img.load()
            input_images.append(img)
            fp.close()      # best practice to close file after
        except Exception:
            print(f"Error loading image: {file}")


    # size of grid (value just from trial and error, might make this variable)
    resolution = (64, 64)

    # get largest image in input images for dimensions
    largest_image = max(input_images, key=lambda x: x.size[0] * x.size[1])

    #resize images so they're more even when combining
    for img in input_images:
        img.thumbnail((target_image.size[0] // resolution[0], target_image.size[1] // resolution[1]), Image.LANCZOS)

    output_mosaic = CreateMosaic(target_image, input_images, resolution)
    print('Mosaic Complete!')


    img_name = user_image.split('.')
    new_img = "".join(img_name[:len(img_name) - 1]) + '_out.' + img_name[len(img_name) - 1]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM images WHERE imageName = %s', (new_img,))
    poss_images = cursor.fetchall()

    image_num = ""

    if len(poss_images) > 0:
        cursor.execute('SELECT MAX(num) FROM images WHERE imageName = %s', (new_img,))
        image_num = str(cursor.fetchall()[0][0] + 1)
    
    cursor.close()
    conn.close()

    final_new_img = "".join(img_name[:len(img_name) - 1]) + '_out' + image_num + '.' + img_name[len(img_name) - 1]
    print(final_new_img)

    link = os.path.join('static', final_new_img)

    output_mosaic.thumbnail((   (target_image.size[0] * 5),  (target_image.size[1] * 5)), Image.LANCZOS)
    output_mosaic.save(link)
    if image_num == "":
        return redirect('/results/' + privacy + "/" + final_new_img + "/0")
    return redirect('/results/' + privacy + "/" + final_new_img + "/" + image_num)

@app.route("/results/<privacy>/<user_image>/<image_num>", methods = ('GET', 'POST'))
def results(privacy, user_image, image_num):
    if session.get('username') is None:
        return redirect('/')

    if request.method == "POST":
        print(session['username'])
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(imageID) FROM images')
        newID = cursor.fetchall()[0][0] + 1

        curr_date = date.today()

        if image_num == "":
            cursor.execute('INSERT INTO images (username, imageID, setting, imageName, num, date) VALUES (%s, %s, %s, %s, %s, %s)', (session['username'], newID, privacy, user_image, 0, curr_date))
        else:
            cursor.execute('INSERT INTO images (username, imageID, setting, imageName, num, date) VALUES (%s, %s, %s, %s, %s, %s)', (session['username'], newID, privacy, user_image, image_num, curr_date))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/view/id/' + str(newID))
    
    return render_template('index.html')

@app.route('/image/<path:filename>') 
def sendfile(filename):
    if session.get('username') is None:
        return redirect('/')

    return send_from_directory('static', filename)

@app.route('/id/<int:imageID>') 
def sendfile2(imageID):
    if session.get('username') is None:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM images WHERE imageID = %s', (imageID,))
    image_info = cursor.fetchall()

    cursor.close()
    conn.close()

    # image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static', image_info[0][3]))
    # imgpath = Image.open(image_path)
    # imgpath.resize((600,600),Image.ANTIALIAS).save(f"./static/small_{image_info[0][3]}")
    return send_from_directory('static', image_info[0][3])

@app.route("/view/id/<int:image_id>", methods = ('GET', 'POST'))
def view(image_id):
    if session.get('username') is None:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM images WHERE imageID = %s', (image_id,))
    image_info = cursor.fetchall()
    privacy = image_info[0][2]

    if request.method == "POST":
        new_privacy = request.form["privacy"]

        cursor.execute('SELECT * FROM images WHERE imageID = %s', (image_id,))
        image_info = cursor.fetchall()

        if not image_info[0][0] == session['username']:
            return redirect('/view/id/' + str(image_id))

        cursor.execute('UPDATE images SET setting = %s WHERE imageID = %s', (new_privacy, image_id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/view/id/' + str(image_id))

    cursor.close()
    conn.close()

    if ((not image_info[0][0] == session['username']) and (privacy == "private")):
        return redirect('/home')

    curr_date = image_info[0][5].strftime("%m/%d/%Y")

    return render_template('index.html', view_privacy = privacy, image_owner = image_info[0][0], view_date = curr_date)

@app.route("/logout")
def logout():
    session['username'] = None
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

#======================================================================================================

def calcAverageRGB(image):

    img = np.array(image)
    
    # shape[0] - image width || shape[1] - image height || shape[2] - depth of colors, i.e. rgba = 4, rgb = 3
    # create linear array of d-tuple (3 for rgb) for all pixels and average over each rgb tuple
    img = img.reshape(img.shape[0]*img.shape[1], img.shape[2])
    
    # get component-wise rgb weighted average
    return tuple(np.average(img, axis=0))

def tileImage(input_image, resolution):
    """
    _________________
    |_1_|_2_|_3_|_4_|
    |_5_|_6_|_7_|_8_|
    |_9_|_._|_._|_._|
    |_._|_._|_._|_._|
    |_._|_._|_._|_._|
    tile the image, return this as a list of individual images

    i,j         (i+1),j
         ._____.
         |     |  
         |     |
         L-----⅃
    i,(j+1)     (i+1),(j+1)
    """
    w, h = input_image.size[0] // resolution[1], input_image.size[1] // resolution[0]
    imgs = []
    for j in range(resolution[0]):
        for i in range(resolution[1]):
            chunk = image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
            imgs.append(chunk)
    return imgs

def findClosestMatch(input_avg, avgs):

    index = 0               # current index
    min_index = 0           # index of running min avg.
    min_dist = math.inf     # starting dist at infinity so first image check starts the tracking

    # calculate euclidean distance w.r.t the RGB color-space (3-dim)
    # track the minimum distance to get the image w closest avg color
    for sample, index in zip(avgs, range(len(avgs))):
        dist = (
            ((sample[0] - input_avg[0]) ** 2) + # R-value
            ((sample[1] - input_avg[1]) ** 2) + # G-value
            ((sample[2] - input_avg[2]) ** 2)   # B-value
            )
        
        # if lower distance found, update min trackers
        if dist < min_dist:
            min_dist = dist
            min_index = index

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
    MOSAIC = Image.new('RGB', size=(resolution[1] * width, resolution[0] * height))

    # tile images onto original image
    # 1D/2D mapping -> i = n*row + col
    for i in range(len(output_images)):
        row = i // resolution[1]
        col = i - resolution[1] * row
        MOSAIC.paste(output_images[i], (col * width, row * height))

    return MOSAIC

#======================================================================================================

class RandomDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(RandomDownloader, self).get_filename(
            task, default_ext)
        global key
        filename = key + ".jpg"
        return filename

def RandomImageScrape(key_word=None):
    google_crawler = GoogleImageCrawler(
        downloader_cls=RandomDownloader,
        storage={'root_dir': 'static'})

    if not key_word:
        r = RandomWords()
        global key
        key = r.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="noun, adverb",
            minCorpusCount=1,
            maxCorpusCount=100)
        google_crawler.crawl(keyword=key, max_num=1) 
        image = key + ".jpg"
    else:
        key = key_word
        google_crawler.crawl(keyword=key, max_num=1) 

        image = key + ".jpg"

    return image
