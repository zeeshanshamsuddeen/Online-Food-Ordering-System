

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
import sqlite3

# support both Python 2.x and 3.x
try: buffer = buffer
except NameError:
    buffer = lambda x: x # on Python 3.x 'rb' mode already returns what we need

def U(literal_string):
    if hasattr(literal_string, 'decode'):
        return literal_string.decode('utf-8') # source code encoding
    return literal_string

# open db
conn = sqlite3.connect('images.db')
conn.execute('''create table if not exists images (
                    path unique not null, 
                    image blob
                )''')

def genimages():
    """Generate example images."""
    for pngpath in glob.iglob(os.path.expanduser(U('E:\sree.jpg'))):
        with open(pngpath, 'rb') as f:
            yield pngpath, buffer(f.read())


# print image paths
for path, in conn.execute('select path from images'):
    print(path)

cur=conn.cursor()

cur.execute("SELECT image FROM images")
var=cur.fetchone()
for x in var:
	print(x)
#conn=sqlite3.connect('test.db')
#cur=conn.cursor()
#cur.execute("PRAGMA table_info(CART)")
#cur.execute("DROP table asd")
#cur.execute("DESCRIBE KFC")
#cur.execute("ALTER TABLE GREENLEAF ADD category TEXT")
#cur.execute("CREATE TABLE zeeshan(item text NOT NULL ,price INTEGER , qty TEXT ,total INTEGER , place TEXT ,rest TEXT)")
#cur.execute("CREATE TABLE customers(username text NOT NULL PRIMARY KEY , password text NOT NULL )")
#cur.execute("INSERT INTO customers(username,password) VALUES ('zeeshan','zeeshan')")
#cur.execute("DELETE FROM customers")
#cur.execute("SELECT * FROM customers")
#var=cur.fetchall()
#for x in var:
#	print(x)
#conn.commit()
#conn.close()	
