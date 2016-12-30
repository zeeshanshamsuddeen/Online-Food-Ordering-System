import sqlite3


conn=sqlite3.connect('TLY.db')
#conn.row_factory = sqlite3.Row
cur=conn.cursor()

cur.execute("SELECT COUNT(*) FROM RARAVIS")
print(cur.fetchone())
var=cur.fetchall()
for x in var:
	x=x+1
	print(x)




conn.close()
