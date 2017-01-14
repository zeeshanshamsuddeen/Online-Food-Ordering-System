import sqlite3

conn=sqlite3.connect('TLY.db')
cur=conn.cursor()
#cur.execute("ALTER TABLE CART ADD place TEXT")
#cur.execute("CREATE TABLE GREENLEAF(item text NOT NULL ,def TEXT , price INTEGER NOT NULL)")
#cur.execute("INSERT INTO PHOTOS (PHOTO) VALUES ('sree.jpg')")
#cur.execute("SELECT * FROM PHOTOS")
conn.commit()
conn.close()	
