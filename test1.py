import sqlite3

conn=sqlite3.connect('bucket.db')
cur=conn.cursor()
qty=3
item='soup'
price=80
#cur.execute("INSERT INTO CART(item,price,qty,total) VALUES(?,?,?,?); " ,(item,price,qty,qty*price))

#cur.execute("DELETE FROM CART")
cur.execute("SELECT COUNT(*) FROM CART	")
var=cur.fetchone()
if(var[0]>0):
	cur.execute("SELECT * FROM CART")
	var=cur.fetchall()
	for x in var:
		print(x)
else:
	print('no values')
conn.commit()
conn.close()

