import sqlite3

conn = sqlite3.connect('personality.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS person(
   id INT PRIMARY KEY,
   name TEXT,
   status TEXT,
   image_path TEXT);
""")
conn.commit()
cur.execute("DELETE FROM person;")
conn.commit()
cur.execute("select * from person;")
print(cur.fetchall())
user = (1, 'Yanina Kondratovich', 'Student', 'face_img/Yana Kondratovich.jpg')
cur.execute("INSERT INTO person VALUES(?, ?, ?, ?);", user)
conn.commit()
user = ('00002', 'Nina Ermak', 'Lector', 'face_img/Nina Ermak.jpg')
cur.execute("INSERT INTO person VALUES(?, ?, ?, ?);", user)
conn.commit()
cur.execute("SELECT * FROM person;")
one_result = cur.fetchall()
print(one_result)
