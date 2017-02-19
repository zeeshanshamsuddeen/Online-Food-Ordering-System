

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import glob
#import os
import sqlite3
import cgi, os


# support both Python 2.x and 3.x
#try: buffer = buffer
#except NameError:
#    buffer = lambda x: x # on Python 3.x 'rb' mode already returns what we need

#def U(literal_string):
#    if hasattr(literal_string, 'decode'):
#        return literal_string.decode('utf-8') # source code encoding
#    return literal_string

# open db
#conn = sqlite3.connect('images.db')
#conn.execute('''create table if not exists images (
 #                   path unique not null, 
  #                  image blob
  #              )''')

#def genimages():
#    """Generate example images."""
 #   for pngpath in glob.iglob(os.path.expanduser(U('E:\1.jpg'))):
  #      with open(pngpath, 'rb') as f:
   #         yield pngpath, buffer(f.read())


# print image paths
#for path, in conn.execute('select path from images'):
 #   print(path)

#insert images
#with conn: # insert all or nothing
#  conn.executemany('insert into images(path,image) values(?, ?)', genimages())

# print image paths
#for path, in conn.execute('select path from images'):
#    print(path)
#conn.execute('delete from images')
#conn.commit()


#shows all tables
#cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
	
	


conn=sqlite3.connect('members.db')
cur=conn.cursor()

'''
cur.execute("SELECT * FROM search")
var=cur.fetchall()
for x in var:
	print(x)
'''
#cur.execute("DELETE FROM approval")
#upload='static/'
#os.remove(upload+'KANNUR_2.jpg')

#cur.execute("PRAGMA table_info(search)")
#cur.execute("DROP table aaa")
#cur.execute("DESCRIBE managers")
#cur.execute("ALTER TABLE search ADD rest TEXT")
#cur.execute("CREATE TABLE search(item text NOT NULL ,def TEXT,price INTEGER NOT NULL,category TEXT)")
#cur.execute("CREATE TABLE managers(username text NOT NULL ,password text, filename TEXT, place TEXT ,location TEXT, phone INTEGER ,start TEXT, stop TEXT )")
#cur.execute("INSERT INTO managers(username,password,place,location,phone) VALUES ('zeeshan','zeeshan')")
#cur.execute("DELETE FROM managers WHERE username='aaa'")
#cur.execute("SELECT * FROM managers")
#cur.execute("SELECT * FROM managers")
#var=cur.fetchall()
#for x in var:
#	print(x)
conn.commit()
conn.close()	
#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
import sqlite3
import sys


def readImage():

   try:
   	fin = open("Efood.jpg", "rb")
   	img = fin.read()
   	fin.close()
   	return img
   except IOError:
   	print("no file")
   	sys.exit(1)




def writeImage(data):
    
    fout = open('static/food.jpg','wb')
    fout.write(data)
    


con = sqlite3.connect('test.db')
    
cur = con.cursor()
#cur.execute("CREATE TABLE Images(Id INTEGER PRIMARY KEY, Data BLOB)")

data = readImage()
binary = sqlite3.Binary(data)
cur.execute("INSERT INTO Images(Data) VALUES (?)", (binary,) )

#cur.execute("SELECT Data FROM Images LIMIT 1")
#data = cur.fetchone()[0]
#writeImage(data)
cur.execute("delete from Images")


con.commit()    
con.close()    
'''








