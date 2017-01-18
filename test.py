import sqlite3

conn=sqlite3.connect('bucket.db')
cur=conn.cursor()
#cur.execute("ALTER TABLE CART ADD rest TEXT")
#cur.execute("CREATE TABLE GREENLEAF(item text NOT NULL ,def TEXT , price INTEGER NOT NULL)")
#cur.execute("INSERT INTO PHOTOS (PHOTO) VALUES ('sree.jpg')")
cur.execute("SELECT * FROM CART")
var=cur.fetchall()
for x in var:
	print(x)
conn.commit()
conn.close()	
