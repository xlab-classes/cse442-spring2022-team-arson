import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), pass VARCHAR(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS images (username VARCHAR(255), imageID INT, setting VARCHAR(255))")

cursor.execute('INSERT INTO images (username, imageID, setting) VALUES ("admin", 100, "private")')

connection.commit()
connection.close()