import sqlite3 
from flask import Flask ,flash,session,render_template,redirect,escape, url_for,request, send_from_directory
import sys
import cgi, os
import cgitb; cgitb.enable()
from werkzeug import secure_filename


app = Flask(__name__)
app.secret_key = 'any random string'

#homepage
@app.route('/')
def homepage():
	return render_template('homepage.html')







#page for displaying login for customers
@app.route('/customer')
def customer():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	var=cur.fetchall()
	conn.close()
	return render_template('customer.html',var=var)
	#from customer.html , goes to homepage_customer()

#customer session is created after log in
@app.route('/customer_logged_in',methods=['GET','POST'])
def customer_logged_in():
	session['username']=request.form['username']              #session is a dictionery with username its key.. value is nm variable
	return redirect(url_for('homepage_customer'))

#customer session created after sign up
@app.route('/customer_signed_up',methods=['GET','POST'])
def customer_signed_up():
	session['username']=request.form['username']             #session is a dictionery with username its key.. value is nm variable
	password=request.form['password']
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO customers(username,password) VALUES (?,?)",(session['username'],password))
	cur.execute("CREATE TABLE {}(item text NOT NULL ,price INTEGER , qty TEXT ,total INTEGER , place TEXT ,rest TEXT)".format(session['username']))
	conn.commit()
	return redirect(url_for('homepage_customer'))

#homepage of customer where restaurants are needed to be selected
@app.route('/homepage_customer')
def homepage_customer():
	return render_template('homepage_customer.html')

#when customer wants to logout
@app.route('/customer_logout')
def customer_logout():
	session.pop('username', None)					#used to logout of current session
	return redirect(url_for('homepage'))




@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/contact_form')
def contact_form():
	return render_template('contact_form.html')	

@app.route('/contact_form_submitted',methods=['GET','POST'])
def contact_form_submitted():
	subject=request.form['subject']
	message=request.form['message']
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO messages(username,subject,message) VALUES(?,?,?)",(session['username'],subject,message,))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage_customer'))



#search option
@app.route('/search',methods=['GET','POST'])
def search():
	data=request.form['data']
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM search")
	cur.execute("SELECT username,filename FROM managers WHERE place='TLY'")
	var_username_TLY=cur.fetchall()
	cur.execute("SELECT username,filename FROM managers WHERE place='KANNUR'")
	var_username_KANNUR=cur.fetchall()
	cur.execute("SELECT username,filename FROM managers WHERE place='CALICUT'")
	var_username_CALICUT=cur.fetchall()
	conn.commit()
	conn.close()

	conn=sqlite3.connect('TLY.db')
	cur=conn.cursor()
	for x in var_username_TLY:
		cur.execute("SELECT * FROM {} WHERE item LIKE ?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,filename) VALUES(?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'TLY',x[0],x[1],))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	conn=sqlite3.connect('KANNUR.db')
	cur=conn.cursor()
	for x in var_username_KANNUR:
		cur.execute("SELECT * FROM {} WHERE item=?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,filename) VALUES(?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'KANNUR',x[0],x[1],))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	conn=sqlite3.connect('CALICUT.db')
	cur=conn.cursor()
	for x in var_username_CALICUT:
		cur.execute("SELECT * FROM {} WHERE item=?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,filename) VALUES(?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'CALICUT',x[0],x[1],))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	return redirect(url_for('search_result'))

#to access after search is completed
@app.route('/search_result')
def search_result():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM SEARCH")
	var=cur.fetchall()
	return render_template('search_result.html',var=var)







#to access when location is selected from homepage_customer
@app.route('/<place>')			
def location(place):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM managers WHERE place=?",(place,))
	var=cur.fetchone()
	#if database in nonempty
	print(var[0])
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		cur.execute("SELECT * FROM managers WHERE place=?",(place,))
		var=cur.fetchall()
		conn.close()
		return render_template('restaurants.html',var=var,place=place)		
		#from restaurants.html , goes to /menu/<var>
	else:
		return render_template('norestaurants.html')



#to access different menus of restaurants
@app.route('/<place>/menu/<rest>')
def menu(place,rest):
	#checks which place is selected ie which database 
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(rest))
	var=cur.fetchone()
	if(var['count(*)']>0):	#since row_factory=Row,col name is used
		cur.execute("SELECT * FROM {} WHERE category='veg'".format(rest)) 
		var_veg=cur.fetchall()
		cur.execute("SELECT * FROM {} WHERE category='non-veg'".format(rest)) 
		var_non_veg=cur.fetchall()
		cur.execute("SELECT * FROM {} WHERE category='others'".format(rest)) 
		var_others=cur.fetchall()
		conn.close()

		conn=sqlite3.connect('members.db')
		cur=conn.cursor()
		cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
		temp=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
		var_stars=cur.fetchone()
		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
		count=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
		total_stars=cur.fetchall()
		sum=0
		for x in total_stars:
			sum=sum+x[0]
		if(count[0]==0):
			sum=0
		else:		
			sum=sum/count[0]
		conn.close()
		#<var> variables contains all items in table, each row is accessed and displayed by colname
		return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
		#from menu.html , goes to /quantity/<item>/<price>
	else:
		return render_template('nomenu.html',place=place)


#rating...since windows.location.href="URL" is used in html , the url will be preceeded by previous url
@app.route('/<place>/menu/rating/<rest>/<stars>')		
def rating(place,rest,stars):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO rating(place,rest,username,stars) VALUES(?,?,?,?) ",(place,rest,session['username'],stars,))
	conn.commit()
	conn.close()
	return redirect(url_for('menu',place=place,rest=rest))


#when sorting is selected from menu
@app.route('/<place>/menu/<rest>/<sort>')
def menu_sort(place,rest,sort):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	if(sort=="nameasc"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()

		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY item ASC".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY item ASC".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY item ASC".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	

	elif(sort=="namedes"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()
		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY item DESC".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY item DESC".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY item DESC".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	

	elif(sort=="pricelh"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()
		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY price".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY price".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY price".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	

	elif(sort=="pricehl"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()
		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY price DESC".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY price DESC".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY price DESC".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	




#to submit quantity of item selected	
@app.route('/quantity/<place>/<rest>/<item>/<price>',methods=['GET','POST'])
def quantity(place,rest,item,price):
	return render_template('quantity.html',item=item,price=price,place=place,rest=rest)
	#from quantity.html , goes to /postquantity/<item>/<price>



#to insert quantity in CART table
@app.route('/postquantity/<place>/<rest>/<item>/<price>',methods=['GET','POST'])
def postquantity(place,rest,item,price):
	print('postquantity')
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	qty=request.form['qty']
	var=int(price)*int(qty)
	cur.execute("INSERT INTO {}(item,price,qty,total,place,rest) VALUES(?,?,?,?,?,?); ".format(session['username']) ,(item,price,qty,var,place,rest))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage_customer'))



#to show items in cart
@app.route('/cartshow')
def cartshow():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM managers")
	var2=cur.fetchall()
	cur.execute("SELECT COUNT(*) FROM {}".format(session['username']))
	var1=cur.fetchone()
	if(var1[0]>0):
		cur.execute("SELECT * FROM {}".format(session['username']))
		var=cur.fetchall()
		
		#for checking whether deleted restaurants dish is in cart
		for x in var:
			temp=0
			for y in var2:
				if(x[4]==y[3] and x[5]==y[0]):
					temp=temp+1
					break
			if(temp==0):
				cur.execute("DELETE FROM {} WHERE place=? and rest=?;".format(session['username']),(x[4],x[5],))
			
		conn.commit()				
		conn.close()
		return render_template('cartshow.html',var=var,var2=var2)
		#from cartshow.html , goes to cartremove/<item> 
	else:
		return render_template("nocart.html")

#to delete an <item> from cart
@app.route('/cartremove/<item>/<place>/<rest>')
def cartremove(item,place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(session['username']))
	var1=cur.fetchone()
	if(var1[0]>0):
		cur.execute("DELETE FROM {} WHERE item=? AND place=?;".format(session['username']),(item,place))
		conn.commit()
		conn.close()
		return redirect(url_for('cartshow'))
	else:
		return render_template("nocart.html")

#to display total and proceed to pay
@app.route('/cartpay')
def cartpay():
	return render_template('cartpay.html')
	#two options in cartpay, card and COD

#to access if card is selected as mode of payment
@app.route('/paycard')
def paycard():
	return render_template('paycard.html')
	#from paycard.html , goes to /cartclear



#clear items in cart
@app.route('/cartclear')
def cartclear():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM {}".format(session['username']))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage_customer'))
















#to access when manager_login is selected from homepage
@app.route('/manager_login',methods=['GET','POST'])
def manager_login():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT username,password FROM managers")
	var=cur.fetchall()
	conn.close()
	return render_template('manager_login.html',var=var)
	#from manager_login.html , if valid username , goes to /manager_logged_in	

#to access for new manager 
@app.route('/manager_signup')
def manager_signup():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT username,place FROM managers")
	var=cur.fetchall()
	conn.close()
	return render_template('manager_signup.html',var=var)


app.config['UPLOAD_FOLDER'] = 'static/'

#when manager submites sign up form
@app.route('/manager_signed_up',methods=['GET','POST'])
def manager_signed_up():
	upload='static/'
	place=request.form['place']
	username=request.form['username']
	password=request.form['password']
	location=request.form['location']
	phone=request.form['phone']
	start_time=request.form['start_time']
	close_time=request.form['close_time']

	#The image file of restarant is received here
	file = request.files['filename']
	filename = secure_filename(file.filename)
	#The image is stored in static folder
	file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
	#renaming image file
	source=upload+filename
	destination=upload+place+'_'+username+'.jpg'
	os.rename(source,destination)


	#to create entry in approval table 
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO approval(username,password,filename,place,location,phone,start,stop) values(?,?,?,?,?,?,?,?)",(username,password,place+'_'+username+'.jpg',place,location,phone,start_time,close_time))
	conn.commit()
	conn.close()
	return render_template('manager_processing.html')


#when manager wants to logout
@app.route('/manager_logout')
def manager_logout():
	   session.pop('username', None)					#used to logout of current session
	   return redirect(url_for('homepage'))

#manager session created after manager login
@app.route("/manager_logged_in",methods=['GET','POST'])
def manager_logged_in():
	username=request.form['username']
	place=request.form['location']
	session['username']=username
	return redirect(url_for('manager_homepage',place=place))	

#to check for table in place
@app.route('/manager_homepage/<place>',methods=['GET','POST'])
def manager_homepage(place):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	username=session['username']
	#to select all table names in database
	cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchall()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))
	
	
#shows manager's menu
@app.route('/manager_menu/<place>/<username>')
def manager_menu(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("SELECT * FROM {}".format(username))	#username is table name
	var=cur.fetchall()
	conn.close()
	return render_template('manager_menu.html',var=var,place=place,username=username)
	#from manager_menu.html , goes to manager_edit based on action choice
	


#to access when manager wants to edit items for manager_menu display
@app.route('/manager_edit/<place>/<username>/<action>',methods=['GET','POST'])
def manager_edit(place,username,action):
	if(action=="add"):
		if(place=='TLY'):
			conn=sqlite3.connect('TLY.db')
		elif(place=='KANNUR'):
			conn=sqlite3.connect('KANNUR.db')
		else:
			conn=sqlite3.connect('CALICUT.db')	
		cur=conn.cursor()
		cur.execute("SELECT item FROM {}".format(username))	
		var=cur.fetchall()
		conn.close()
		return render_template('manager_add.html',var=var,place=place,username=username)
	elif(action=="delete"):
		return redirect(url_for('manager_delete',place=place,username=username))
	elif(action=="editprice"):
		return redirect(url_for('manager_editprice',place=place,username=username))
	







#to access when manager wants to add items 
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
	category=request.form['category']
	cur.execute("INSERT INTO {}(item,def,price,category) VALUES(?,?,?,?); ".format(username) ,(item,def1,price,category))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))








#to access when manager wants to delete items 
@app.route('/manager_delete/<place>/<username>')
def manager_delete(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(username))
	var1=cur.fetchone()
	#if table in nonempty
	if(var1[0]>0):
		cur.execute("SELECT * FROM {}".format(username))
		var=cur.fetchall()
		conn.close()
		return render_template('manager_delete.html',place=place,username=username,var=var)
	else:
		return render_template("no_managermenu.html",place=place,username=username)


#to delete items from database after manager selects delete items
@app.route('/manager_delete_database/<place>/<username>/<item>/<defen>')
def manager_delete_database(place,username,item,defen):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("DELETE FROM {} WHERE item=? and def=?".format(username),(item,defen,))
	conn.commit()
	return redirect(url_for('manager_menu',place=place,username=username))



#to access when manager wants to edit price of items 
@app.route('/manager_editprice/<place>/<username>')
def manager_editprice(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(username))
	var1=cur.fetchone()
	#if table is nonempty
	if(var1[0]>0):
		cur.execute("SELECT * FROM {}".format(username))
		var=cur.fetchall()
		conn.close()
		return render_template('manager_editprice.html',place=place,username=username,var=var)
	else:
		return render_template("no_managermenu.html",place=place,username=username)



#to edit price of item from database after manager selects edit price
@app.route('/manager_editprice_newprice/<place>/<username>/<item>',methods=['GET','POST'])
def manager_editprice_newprice(place,username,item):
	return render_template('manager_editprice_newprice.html',place=place,username=username,item=item)



#to enter new price in database
@app.route('/manager_editprice_database/<place>/<username>/<item>',methods=['GET','POST'])
def manager_editprice_database(place,username,item):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	price=request.form['price']
	cur.execute("UPDATE {} SET price=? WHERE item=?".format(username),(price,item,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))


















@app.route('/admin')
def admin():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute('SELECT * FROM approval')
	var=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('TLY',))
	var_TLY=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('KANNUR',))
	var_KANNUR=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('CALICUT',))
	var_CALICUT=cur.fetchall()
	cur.execute("SELECT * FROM messages")
	var_message=cur.fetchall()
	
	conn.close()
	return render_template('admin.html',var=var,var_TLY=var_TLY,var_KANNUR=var_KANNUR,var_CALICUT=var_CALICUT,var_message=var_message)


#when admin wants to remove message
@app.route("/admin_message_remove/<username>/<subject>")
def admin_message_remove(username,subject):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM messages WHERE username=? and subject=?",(username,subject,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))

#when admin wants to remove an existing restaurant	
@app.route('/admin_manage_remove/<username>/<place>')
def admin_manage_remove(username,place):
	upload='static/'
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT filename FROM managers WHERE username=? AND place=?",(username,place,))
	var=cur.fetchone()
	
	#restaurant image is deleted 
	os.remove(upload+var[0])
	cur.execute('DELETE FROM managers WHERE username=? AND place=?',(username,place,))
	cur.execute("DELETE FROM rating WHERE place=? AND rest=?",(place,username,))
	conn.commit()
	conn.close()

	#to delete username table in corresponding place database
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("DROP TABLE {}".format(username))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))


#when admin wants to remove the request of new restaurant
@app.route('/admin_remove/<username>/<place>')
def admin_remove(username,place):
	upload='static/'
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT filename FROM approval WHERE username=? AND place=?",(username,place,))
	var=cur.fetchone()
	#restaurant image is deleted 
	os.remove(upload+var[0])
	cur.execute('DELETE FROM approval WHERE username=? AND place=?',(username,place,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))


#when admin wants to approve the request of new restaurant
@app.route('/admin_approve/<username>/<place>')
def admin_approve(username,place):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()	
	cur.execute('SELECT * FROM approval WHERE username=? AND place=?',(username,place,))
	var=cur.fetchone()

	#to create entry in managers table 
	cur.execute("INSERT INTO managers(username,password,filename,place,location,phone,start,stop) values(?,?,?,?,?,?,?,?)",(var[0],var[1],var[2],var[3],var[4],var[5],var[6],var[7],))
	cur.execute("DELETE FROM approval WHERE username=? AND place=?",(username,place,))
	conn.commit()



	#to create username table in corresponding place database
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("CREATE TABLE {}(item TEXT NOT NULL, def TEXT , price INTEGER NOT NULL,category TEXT)".format(username))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))




if __name__ == '__main__':
   app.run(debug = True)	

