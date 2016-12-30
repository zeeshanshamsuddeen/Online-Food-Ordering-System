import sqlite3


conn=sqlite3.connect('bucket.db')
#conn.row_factory = sqlite3.Row
cur=conn.cursor()
#cur.execute("SELECT * FROM CART")
#cur.execute("CREATE TABLE KFC(item TEXT NOT NULL, def TEXT , price INTEGER NOT NULL)")
#cur.execute("DELETE FROM CART WHERE =")
cur.execute("SELECT * FROM CART")
#conn.commit();
var=cur.fetchall()
for x in var:#
	print(x)
#cur.execute("SELECT COUNT(*) FROM CART")
#var=cur.fetchone()
#nitem=var[0]
#print(nitem)



conn.close()
