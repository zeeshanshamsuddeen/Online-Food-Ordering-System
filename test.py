import sqlite3

conn=sqlite3.connect('TLY.db')
cur=conn.cursor()
item="fish"
def1="fry"
price='50'
username="KFC"
#cur.execute("INSERT INTO {}(item,def,price) VALUES(?,?,?); ".format(username) ,(item,def1,price))
#conn.commit()
cur.execute("SELECT * FROM KFC")
var=cur.fetchall()
for x in var:
	print(x)
conn.close()