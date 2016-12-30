import sqlite3 
from flask import Flask ,flash,session,render_template,redirect,escape, url_for,request


app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def home():
	return render_template('homepage.html')


#to access when TLY is selected from homepage
@app.route('/TLY')			
def TLY():
	conn=sqlite3.connect('TLY.db')
	cur=conn.cursor()
	#show all tables
	cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchone()
	if(var[0]>0):
		cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' ")
		var=cur.fetchall()
		conn.close()
		return render_template('restaurants.html',var=var)		
		#goes to /menu/<var>


#to access different menus of restaurants
@app.route('/menu/<table>')
def menu(table):
	conn=sqlite3.connect('TLY.db')	
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(table))
	var=cur.fetchone()
	if(var['count(*)']>0):	#because var cannot be takes as integer..it is a row
		cur.execute("SELECT * FROM {}".format(table)) 
		var=cur.fetchall()
		conn.close()
		return render_template('menu.html',var=var)
		#goes to /quantity/<item>/<price>
	

#to submit quantity of item selected	
@app.route('/quantity/<item>/<price>')
def quantity(item,price):
	return render_template('quantity.html',item=item,price=price)
	#goes to /postquantity/<item>/<price>



#to insert quantity in CART 
@app.route('/postquantity/<item>/<price>',methods=['GET','POST'])
def postquantity(item,price):
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	qty=request.form['qty']
	var=int(price)*int(qty)
	cur.execute("INSERT INTO CART(item,price,qty,total) VALUES(?,?,?,?); " ,(item,price,qty,var))
	conn.commit()
	conn.close()
	return ''
	#if non integer entered in qty field	
	#except ValueError:			
	#		return redirect(url_for('quantity',item=item,price=price))





#to access when login is selected from homepage
@app.route('/login')
def login():
	return render_template('login.html')
	
		
@app.route('/success',methods=['GET','POST'])
def success():
	print(request.form['password'])
	return render_template('success.html')


if __name__ == '__main__':
   app.run(debug = True)	

