import sqlite3

conn=sqlite3.connect('TLY.db')
cur=conn.cursor()
cur.execute("SELECT * FROM KFC")
var=cur.fetchall()
for x in var:
	print(x)
	

	