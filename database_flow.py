import sqlite3

conn = sqlite3.connect('personality.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS person(
   id INTEGER PRIMARY KEY,
   name TEXT NOT NULL,
   status TEXT NOT NULL,
   image_path TEXT NOT NULL);
''')
conn.commit()
# cur.execute("DELETE FROM person;")
# conn.commit()
# cur.execute("select * from person;")
# print(cur.fetchall())
# user = ('Yanina Kondratovich', 'Student', 'face_img/Yana Kondratovich.jpg')
# cur.execute("INSERT INTO person(name, status, image_path) VALUES(?, ?, ?);", user)
# conn.commit()
# user = ('Nina Ermak', 'Lector', 'face_img/Nina Ermak.jpg')
# cur.execute("INSERT INTO person(name, status, image_path) VALUES(?, ?, ?);", user)
# conn.commit()
cur.execute("SELECT * FROM person;")
one_result = cur.fetchall()
print(one_result)
