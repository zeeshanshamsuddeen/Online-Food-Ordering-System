import sqlite3 
from flask import Flask ,flash,session,render_template,redirect,escape, url_for,request


app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def homepage():
	return render_template('homepage.html')


#to access when location is selected from homepage
@app.route('/<place>')			
def location(place):
	#checks which place is selected in homepage ie which databse
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')
	cur=conn.cursor()
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchone()
	#if database in nonempty
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' ")
		var=cur.fetchall()
		conn.close()
		return render_template('restaurants.html',var=var,place=place)		
		#from restaurants.html , goes to /menu/<var>
	else:
		return render_template('norestaurants.html')



#to access different menus of restaurants
@app.route('/<place>/menu/<table>')
def menu(place,table):
	#checks which place is selected ie which database 
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(table))
	var=cur.fetchone()
	if(var['count(*)']>0):	#since row_factory=Row,col name is used
		cur.execute("SELECT * FROM {}".format(table)) 
		var=cur.fetchall()
		conn.close()
		#<var> contains all items in table, each row is accessed and displayed by colname
		return render_template('menu.html',var=var)
		#from menu.html , goes to /quantity/<item>/<price>
	else:
		return render_template('nomenu.html',place=place)
	

#to submit quantity of item selected	
@app.route('/quantity/<item>/<price>',methods=['GET','POST'])
def quantity(item,price):
	return render_template('quantity.html',item=item,price=price)
	#from quantity.html , goes to /postquantity/<item>/<price>



#to insert quantity in CART 
@app.route('/postquantity/<item>/<price>',methods=['GET','POST'])
def postquantity(item,price):
	print('postquantity')
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	qty=request.form['qty']
	var=int(price)*int(qty)
	cur.execute("INSERT INTO CART(item,price,qty,total) VALUES(?,?,?,?); " ,(item,price,qty,var))
	conn.commit()
	conn.close()
	return ''









#to show items in cart
@app.route('/cartshow')
def cartshow():
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM CART")
	var=cur.fetchall()
	conn.close()
	return render_template('cartshow.html',var=var)
	#from cartshow.html , goes to cartremove/<item> 


#to delete an <item> from cart
@app.route('/cartremove/<item>')
def cartremove(item):
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM CART WHERE item=?",(item,))
	conn.commit()
	conn.close()
	return redirect(url_for('cartshow'))


#to display total and proceed to pay
@app.route('/cartpay')
def cartpay():
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM CART")
	var=cur.fetchone()
	nitem=var[0]
	cur.execute("SELECT SUM(total) FROM CART")
	var=cur.fetchone()
	ntotal=var[0]
	return render_template('cartpay.html',nitem=nitem,ntotal=ntotal)
	#two options in cartpay, card and COD

#to access if card is selected as mode of paymeny
@app.route('/paycard')
def paycard():
	return render_template('paycard.html')
	#from paycard.html , goes to /cartclear

#to access if COD is selected as mode of payment
@app.route('/paycash')
def paycash():
	return render_template('paycash.html')	
	#from paycash.html , goes to /cartclear

#clear items in cart
@app.route('/cartclear')
def cartclear():
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM CART")
	conn.commit()
	conn.close()
	return redirect(url_for('homepage'))
















#to access when login is selected from homepage
@app.route('/login')
def login():
	return render_template('login.html')
	#from login.html , if valid username , goes to /success	

#to check for table in place
@app.route('/success',methods=['GET','POST'])
def success():
	username=request.form['username']
	place=request.form['location']
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn.sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	#to select all table names in database
	cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchall()
	conn.close()
	for x in var:
		if(username==x[0]):
			#if username table is present in database
			return redirect(url_for('manager_menu',place=place,username=username))
			break
	return render_template('nomanager.html')


@app.route('/manager_menu/<place>/<username>')
def manager_menu(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn.sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("SELECT * FROM {}".format(username))	#username is table name
	var=cur.fetchall()
	conn.close()
	return render_template('manager_menu.html',var=var,place=place,username=username)
	#from manager_menu.html , goes to manager_edit based on action choice

@app.route('/manager_edit/<place>/<username>/<action>')
def manager_edit(place,username,action):
	if(action=="add"):
		return render_template('manager_add.html',place=place,username=username)
	#elif(action=="delete"):
	#	return render_template('manager_delete.html',place=place,username=username)
	#else:
	#	return render_template('manager_update',palce=place,username=username)	


@app.route('/manager_add/<place>/<username>',methods=['GET','POST'])
def manager_add(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	item=request.form['item']
	def1=request.form['def'] 
	price=request.form['price']
	print(username)
	cur.execute("INSERT INTO {}(item,def,price) VALUES(?,?,?); ".format(username) ,(item,def1,price))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))


@app.route('/manager_delete/<place>/<username>',methods=['GET','POST'])
def manager_delete(place,username):
	return render_template('manager_delete',place=place,username=username)







if __name__ == '__main__':
   app.run(debug = True)	

