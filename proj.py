import sqlite3 
from flask import Flask ,flash,session,render_template,redirect,escape, url_for,request, send_from_directory
import sys
import cgi, os
import cgitb; cgitb.enable()
from werkzeug import secure_filename
import time
import collections



app = Flask(__name__)
app.secret_key = 'any random string'

#homepage
@app.route('/')
def homepage():
	if session:
		session.pop('username', None)					#used to logout of current session
	return render_template('homepage.html')



@app.route('/privacy_policy')
def privacy_policy():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('privacy_policy.html',path=path)

@app.route('/terms')
def terms():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('terms.html',path=path)


@app.route('/about')
def about():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('about.html',path=path)


@app.route('/security')
def security():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('security.html',path=path)



@app.route('/help')
def help():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('help.html',path=path)



@app.route('/contact')
def contact():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('contact.html',path=path)


@app.route('/contact_form')
def contact_form():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
		temp="unknown"
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
				temp="customer"
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
				temp=x[3]
	return render_template('contact_form.html',path=path,temp=temp)


@app.route('/contact_form_submitted/<temp>',methods=['GET','POST'])
def contact_form_submitted(temp):
	subject=request.form['subject']
	message=request.form['message']
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	if not session:
		cur.execute("INSERT INTO messages(username,subject,message) VALUES(?,?,?)",('unknown',subject,message,))
	else:
		cur.execute("INSERT INTO messages(username,subject,message) VALUES(?,?,?)",(session['username'],subject,message,))
	conn.commit()
	conn.close()
	if(temp =='unknown'):
		return redirect(url_for('homepage'))
	elif(temp=='customer'):
		return redirect(url_for('homepage_customer'))	
	else:
		return redirect(url_for('manager_homepage',place=temp))	









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
	cur.execute("CREATE TABLE {}(item text NOT NULL ,price INTEGER , qty TEXT ,total INTEGER , place TEXT ,rest TEXT,dish_image TEXT)".format(session['username']))
	temp=session['username']+'_orders'
	cur.execute("CREATE TABLE IF NOT EXISTS {}(item text NOT NULL ,price INTEGER , qty TEXT ,total INTEGER , place TEXT ,rest TEXT,dish_image TEXT);".format(temp))
	conn.commit()
	return redirect(url_for('homepage_customer'))


#when customer wants to logout
@app.route('/customer_logout')
def customer_logout():
	session.pop('username', None)					#used to logout of current session
	return redirect(url_for('homepage'))




#homepage of customer where restaurants are needed to be selected
@app.route('/homepage_customer')
def homepage_customer():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM response WHERE username=?",(session['username'],))
	response=cur.fetchall()
	cur.execute("SELECT * FROM most_ordered ORDER BY orders DESC limit 4")
	most_ordered=cur.fetchall()
	conn.close()
	return render_template('homepage_customer.html',response=response,most_ordered=most_ordered)







#when customer wants to remove responses
@app.route('/remove_response')	
def remove_response():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM response WHERE username=?",(session['username'],))
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
	cur.execute("SELECT username FROM managers WHERE place='TLY'")
	var_username_TLY=cur.fetchall()
	cur.execute("SELECT username FROM managers WHERE place='KANNUR'")
	var_username_KANNUR=cur.fetchall()
	cur.execute("SELECT username FROM managers WHERE place='CALICUT'")
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
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,dish_image) VALUES(?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'TLY',x[0],y[4],))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	conn=sqlite3.connect('KANNUR.db')
	cur=conn.cursor()
	for x in var_username_KANNUR:
		cur.execute("SELECT * FROM {} WHERE item LIKE ?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,dish_image) VALUES(?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'KANNUR',x[0],y[4],))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	conn=sqlite3.connect('CALICUT.db')
	cur=conn.cursor()
	for x in var_username_CALICUT:
		cur.execute("SELECT * FROM {} WHERE item LIKE ?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,dish_image) VALUES(?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'CALICUT',x[0],y[4],))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	return redirect(url_for('search_result',data=data))

#to access after search is completed
@app.route('/search_result/<data>')
def search_result(data):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	cur.execute("SELECT * FROM SEARCH")
	var=cur.fetchall()
	cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
	var_rest=cur.fetchall()	
	for rest in var_rest:
		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		count=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		total_stars=cur.fetchall()
		sum=0
		for x in total_stars:
			sum=sum+x[0]
		if(count[0]==0):
			sum=0
		else:		
			sum=sum/count[0]			
		dict[rest[0],rest[3]]=sum
	conn.close()

	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)

#to access after search sort for dishes is selected
@app.route('/search_result_sort/<sort>/<data>')
def search_result_sort(sort,data):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	if(sort=="desc"):
		cur.execute("SELECT * FROM SEARCH ORDER BY price DESC")
		var=cur.fetchall()
	if(sort=="asc"):
		cur.execute("SELECT * FROM SEARCH ORDER BY price ")
		var=cur.fetchall()	
	if(sort=="AtoZ"):
		cur.execute("SELECT * FROM SEARCH ORDER BY item")
		var=cur.fetchall()
	if(sort=="ZtoA"):
		cur.execute("SELECT * FROM SEARCH ORDER BY item DESC")
		var=cur.fetchall()	
	cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
	var_rest=cur.fetchall()	
	for rest in var_rest:
		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		count=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		total_stars=cur.fetchall()
		sum=0
		for x in total_stars:
			sum=sum+x[0]
		if(count[0]==0):
			sum=0
		else:		
			sum=sum/count[0]			
		dict[rest[0],rest[3]]=sum
	conn.close()

	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)



#to access when search sort for restaurants is selected
@app.route('/search_result_sort_rest/<sort>/<data>')
def search_result_sort_rest(sort,data):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	cur.execute("SELECT * FROM SEARCH")
	var=cur.fetchall()
	if(sort=="asc"):
			cur.execute("SELECT * FROM managers WHERE username LIKE ? ORDER BY username",('%'+data+'%',))
			var_rest=cur.fetchall()
			for rest in var_rest:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0],rest[3]]=sum
	elif(sort=="desc"):
		cur.execute("SELECT * FROM managers WHERE username LIKE ? ORDER BY username DESC",('%'+data+'%',))
		var_rest=cur.fetchall()
		for rest in var_rest:
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]			
			dict[rest[0],rest[3]]=sum
	elif(sort=="rating"):	
		cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
		var_rest=cur.fetchall()
		for rest in var_rest:
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]			
			dict[rest[0],rest[3]]=sum
		#to arrange dictionery in reverse order	
		conn.close()
		ord_dict = collections.OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
		return render_template('search_result_rating.html',var=var,var_rest=var_rest,data=data,ord_dict=ord_dict)

	conn.close()	
	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)




#to access when location is selected from homepage_customer
@app.route('/<place>')			
def location(place):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM managers WHERE place=?",(place,))
	var=cur.fetchone()
	#if database in nonempty
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		cur.execute("SELECT * FROM managers WHERE place=?",(place,))
		var=cur.fetchall()

		for rest in var:
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]	
			#single key dictionery is used because no 2 restaurants will have same name			
			dict[rest[0]]=sum

		conn.close()
		return render_template('restaurants.html',var=var,place=place,dict=dict)		
		#from restaurants.html , goes to /menu/<var>
	else:
		return render_template('norestaurants.html')


#to access when location sort is selected 
@app.route('/sort/<place>/<sort>')			
def sort_location(place,sort):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM managers WHERE place=?",(place,))
	var=cur.fetchone()
	#if database in nonempty
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		if(sort=="asc"):
			cur.execute("SELECT * FROM managers WHERE place=? ORDER BY username",(place,))
			var=cur.fetchall()
			for rest in var:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0]]=sum
		elif(sort=="desc"):
			cur.execute("SELECT * FROM managers WHERE place=? ORDER BY username DESC",(place,))
			var=cur.fetchall()
			for rest in var:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0]]=sum
		elif(sort=="rating"):	
			cur.execute("SELECT * FROM managers WHERE place=? ORDER BY username DESC",(place,))
			var=cur.fetchall()
			for rest in var:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0]]=sum	
			#to arrange dictionery in reverse order	
			conn.close()
			ord_dict = collections.OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
			return render_template('restaurants_sort_rating.html',var=var,place=place,ord_dict=ord_dict)

		conn.close()
		return render_template('restaurants.html',var=var,place=place,dict=dict)		
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


#rating..
@app.route('/<place>/<rest>/rating/<stars>')		
def rating(place,rest,stars):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO rating(place,rest,username,stars) VALUES(?,?,?,?) ",(place,rest,session['username'],stars,))
	cur.execute("UPDATE reviews SET rating=? WHERE place=? AND rest=? AND username=?",(stars,place,rest,session['username'],))
	conn.commit()
	conn.close()
	return redirect(url_for('menu',place=place,rest=rest))



#rating..when user wants to change rating
@app.route('/<place>/<rest>/rating_change/<stars>')
def rating_change(place,rest,stars):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("UPDATE rating SET stars=? WHERE place=? AND rest=? AND username=?",(stars,place,rest,session['username'],))
	cur.execute("UPDATE reviews SET rating=? WHERE place=? AND rest=? AND username=?",(stars,place,rest,session['username'],))
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
@app.route('/quantity/<place>/<rest>/<item>/<price>/<dish_image>',methods=['GET','POST'])
def quantity(place,rest,item,price,dish_image):
	return render_template('quantity.html',item=item,price=price,place=place,rest=rest,dish_image=dish_image)
	#from quantity.html , goes to /postquantity/<item>/<price>



#to insert quantity in CART table
@app.route('/postquantity/<place>/<rest>/<item>/<price>/<dish_image>',methods=['GET','POST'])
def postquantity(place,rest,item,price,dish_image):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	qty=request.form['qty']
	var=int(price)*int(qty)
	cur.execute("INSERT INTO {}(item,price,qty,total,place,rest,dish_image) VALUES(?,?,?,?,?,?,?); ".format(session['username']) ,(item,price,qty,var,place,rest,dish_image,))
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
		cur.execute("SELECT * FROM managers")
		managers=cur.fetchall()

		#to check whether deleted restaurant dishes are in cart	
		for x in var:
			temp=0
			for man in managers:
				if(x[4]==man[3] and x[5]==man[0]):
					temp=1
			if(temp==0):
				cur.execute("DELETE FROM {} WHERE place =? and rest=?".format(session['username']),(x[4],x[5],))

		conn.commit()
		conn.close()	

		conn=sqlite3.connect('members.db')
		cur=conn.cursor()	
		cur.execute("SELECT * FROM {}".format(session['username']))
		var=cur.fetchall()
		#for checking whether deleted dish is in cart
		for x in var:
			if(x[4]=='TLY'):
				conn_temp=sqlite3.connect('TLY.db')
			elif(x[4]=='KANNUR'):
				conn_temp=sqlite3.connect('KANNUR.db')
			else:
				conn_temp=sqlite3.connect('CALICUT.db')
			cur_temp=conn_temp.cursor()
			cur_temp.execute("SELECT * FROM {} WHERE item=?".format(x[5]),(x[0],))	
			var_temp=cur_temp.fetchone()
			if not var_temp:
				cur.execute("DELETE FROM {} WHERE item=? AND place=? AND rest=?".format(session['username']),(x[0],x[4],x[5],))
			conn_temp.close()	



		
		cur.execute("SELECT * FROM {}".format(session['username']))
		var=cur.fetchall()
		conn.commit()				
		conn.close()
		if var:
			return render_template('cartshow.html',var=var,var2=var2)
			#from cartshow.html , goes to cartremove/<item> 
		else:
			return render_template("nocart.html")
	else:
		conn.close()
		return render_template("nocart.html")

#to delete an <item> from cart
@app.route('/cartremove/<item>/<place>/<rest>/<qty>')
def cartremove(item,place,rest,qty):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(session['username']))
	var1=cur.fetchone()
	if(var1[0]>0):
		cur.execute("DELETE FROM {} WHERE item=? AND place=? AND qty=?".format(session['username']),(item,place,qty,))
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
	cur.execute("SELECT * FROM {}".format(session['username']))
	var=cur.fetchall()
	temp=session['username']+'_orders'
	for x in var:
		cur.execute("INSERT INTO {} VALUES(?,?,?,?,?,?,?)".format(temp),(x[0],x[1],x[2],x[3],x[4],x[5],x[6],))
		#to insert into most ordered table for each item in cart
		cur.execute("SELECT * FROM most_ordered WHERE place=? AND rest=? AND item=?",(x[4],x[5],x[0],))
		check=cur.fetchone()
		if check:
			cur.execute("UPDATE most_ordered SET orders=orders+? WHERE place=? AND rest=? AND item=?",(x[2],x[4],x[5],x[0],))
		else:
			cur.execute("INSERT INTO most_ordered VALUES(?,?,?,?,?,?)",(x[4],x[5],x[0],x[2],x[6],x[1],))
	
	cur.execute("INSERT INTO response VALUES(?,?,?,?)",(session['username'],'confirmation','order confirmed','admin',))
	cur.execute("DELETE FROM {}".format(session['username']))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage_customer'))


#when user wants to see past orders
@app.route('/orders')	
def orders():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	temp=session['username']+'_orders'
	cur.execute("SELECT * FROM {}".format(temp))
	var=cur.fetchall()
	conn.close()
	if var:
		return render_template('orders.html',var=var)
	else:
		return render_template('no_orders.html')






#for submitting feedback to manager from customer
@app.route('/feedback/<place>/<rest>',methods=['GET','POST'])
def feedback(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	message=request.form['message']
	cur.execute("INSERT INTO feedback VALUES(?,?,?,?)",(place,rest,session['username'],message,))
	conn.commit()
	conn.close()
	return redirect(url_for('menu',place=place,rest=rest))



#to show reviews of restaurants
@app.route('/reviews/<place>/<rest>')
def reviews(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM reviews WHERE place=? AND rest=?",(place,rest,))
	reviews=cur.fetchall()
	return render_template('reviews.html',place=place,rest=rest,reviews=reviews)


#to insert review in reviews table
@app.route('/review_post/<place>/<rest>',methods=['GET','POST'])
def review_post(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	review=request.form['review']
	date=time.strftime("%x")
	cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
	stars=cur.fetchone()
	#if user has not rated the restaurant
	if not stars:
		cur.execute("INSERT INTO reviews(username,rest,place,date,rating,review) VALUES(?,?,?,?,?,?)",(session['username'],rest,place,date,0,review,))
	else:		
		cur.execute("INSERT INTO reviews(username,rest,place,date,rating,review) VALUES(?,?,?,?,?,?)",(session['username'],rest,place,date,stars[0],review,))
	conn.commit()
	conn.close()
	return redirect(url_for('reviews',place=place,rest=rest))

















#to access when manager_login is selected from homepage
@app.route('/manager_login',methods=['GET','POST'])
def manager_login():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM managers")
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
	cur.execute("SELECT username,place FROM approval")
	approval=cur.fetchall()
	conn.close()
	return render_template('manager_signup.html',var=var,approval=approval)


app.config['UPLOAD_FOLDER_REST']='static/restaurants/'
#when manager submites sign up form
@app.route('/manager_signed_up',methods=['GET','POST'])
def manager_signed_up():
	upload='static/restaurants/'
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
	file.save(os.path.join(app.config['UPLOAD_FOLDER_REST'],filename))
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

	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM notification WHERE place=? AND rest=?",(place,username,))
	notification=cur.fetchall()
	cur.execute("SELECT * FROM feedback WHERE place=? AND rest=?",(place,username,))
	feedbacks=cur.fetchall()
	cur.execute("SELECT * FROM managers WHERE username=? AND place=?",(username,place,))	
	var1=cur.fetchone()
	cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,username,))
	total_stars=cur.fetchall()
	cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,username,))
	count=cur.fetchone()
	conn.close()
	sum=0
	for x in total_stars:
		sum=sum+x[0]
	if(count[0]==0):
		sum=0
	else:		
		sum=sum/count[0]
	return render_template('manager_menu.html',var=var,var1=var1,place=place,username=username,sum=sum,feedbacks=feedbacks,notification=notification)
	#from manager_menu.html , goes to manager_edit based on action choice





#when manager wants to edit restaurant details
@app.route('/manager_edit_restaurant_form/<place>/<username>/<loc>/<ph>/<st>/<ct>/<di>')
def manager_edit_restarant_form(place,username,loc,ph,st,ct,di):
	return render_template('manager_edit_restaurant_form.html',place=place,username=username,loc=loc,ph=ph,st=st,ct=ct,di=di)


app.config['UPLOAD_FOLDER_REST1']='static/restaurants/'
#when manager wants to edit restaurant details
@app.route('/manager_edit_restaurant/<place>/<username>',methods=['GET','POST'])
def manager_edit_restarant(place,username):
	location=request.form['location']
	phone=request.form['phone']
	start_time=request.form['start_time']
	close_time=request.form['close_time']
	upload='static/restaurants/'

	#The image file of restarant is received here
	file = request.files['filename']
	if file:
		filename = secure_filename(file.filename)
		#to remove existing image
		source=upload+place+'_'+username+'.jpg'
		os.remove(source)

		#The image is stored in static folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER_REST1'],filename))
		#renaming image file
		source=upload+filename
		destination=upload+place+'_'+username+'.jpg'
		os.rename(source,destination)

	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("UPDATE managers SET location=?,phone=?,start=?,stop=?,filename=? WHERE place=? AND username=?".format(username),(location,phone,start_time,close_time,place+'_'+username+'.jpg',place,username,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_homepage',place=place))





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
	






app.config['UPLOAD_FOLDER_DISH'] = 'static/dish/'

#to access when manager wants to add items 
@app.route('/manager_add/<place>/<username>',methods=['GET','POST'])
def manager_add(place,username):
	upload='static/dish/'
	item=request.form['item']
	def1=request.form['def'] 
	price=request.form['price']
	category=request.form['category']
	#The image file of dish is received here
	file = request.files['filename']
	filename = secure_filename(file.filename)
	#The image is stored in static folder
	file.save(os.path.join(app.config['UPLOAD_FOLDER_DISH'],filename))
	#renaming image file
	source=upload+filename
	destination=upload+place+'_'+username+'_'+item+'.jpg'
	os.rename(source,destination)

	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("INSERT INTO {}(item,def,price,category,dish_image) VALUES(?,?,?,?,?); ".format(username) ,(item,def1,price,category,place+'_'+username+'_'+item+'.jpg',))
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
	upload='static/dish/'
	cur.execute("SELECT dish_image FROM {} WHERE item=? and def=?".format(username),(item,defen,))
	var=cur.fetchone()
	os.remove(upload+var[0])
	cur.execute("DELETE FROM {} WHERE item=? and def=?".format(username),(item,defen,))
	conn.commit()
	conn.close()

	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM most_ordered WHERE place=? AND rest=? AND item=?",(place,session['username'],item,))
	conn.commit()
	conn.close()
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



#to enter new price in manager_editprice_database
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







#when manager wants to send response to customers
@app.route('/response_form_manager/<username>/<place>/<message>')
def response_form_manager(username,place,message):
	return render_template('response_form_manager.html',username=username,place=place,message=message)


#insert querys to response table
@app.route('/response_manager/<username>/<place>/<message>',methods=['GET','POST'])
def response_manager(username,place,message):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	response=request.form['message']
	cur.execute("DELETE FROM feedback WHERE username=? AND place=? AND rest=? AND message=?",(username,place,session['username'],message,))
	cur.execute("INSERT INTO response(username,message,sender) VALUES(?,?,?)",(username,response,session['username'],))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_homepage',place=place))	


#when manager wants to remove feedbacks
@app.route('/remove_feedbacks/<place>/<username>')	
def remove_feedbacks(place,username):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM feedback WHERE place=? AND rest=?",(place,username,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))


#when manager wants to remove notifications
@app.route('/remove_notifications/<place>/<username>')	
def remove_notifications(place,username):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM notification WHERE place=? AND rest=?",(place,username,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))	

	

#to show reviews of restaurant
@app.route('/reviews_manager/<place>')
def reviews_manager(place):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM reviews WHERE place=? AND rest=?",(place,session['username'],))
	reviews=cur.fetchall()
	return render_template('reviews_manager.html',place=place,reviews=reviews)















@app.route('/admin_access')
def admin_access():
	return render_template('admin_access.html')




@app.route('/admin')
def admin():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute('SELECT * FROM approval')
	var=cur.fetchall()
	cur.execute("SELECT username FROM customers")
	customers=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('TLY',))
	var_TLY=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('KANNUR',))
	var_KANNUR=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('CALICUT',))
	var_CALICUT=cur.fetchall()
	cur.execute("SELECT * FROM messages")
	var_message=cur.fetchall()
	conn.close()
	return render_template('admin.html',var=var,var_TLY=var_TLY,var_KANNUR=var_KANNUR,var_CALICUT=var_CALICUT,var_message=var_message,customers=customers,)



#when admin wants to remove the request of new restaurant
@app.route('/admin_remove/<username>/<place>')
def admin_remove(username,place):
	upload='static/restaurants/'
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
	cur.execute("CREATE TABLE {}(item TEXT NOT NULL, def TEXT , price INTEGER NOT NULL,category TEXT,dish_image TEXT)".format(username))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))



#when admin wants to remove message
@app.route("/admin_message_remove/<username>/<subject>")
def admin_message_remove(username,subject):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM messages WHERE username=? and subject=?",(username,subject,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))



#when admin wants to send response to customers
@app.route('/response_form/<username>/<sub>')
def response_form(username,sub):
	return render_template('response_form.html',username=username,sub=sub)


#insert querys to response table
@app.route('/response/<username>/<sub>',methods=['GET','POST'])
def response(username,sub):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	message=request.form['message']
	cur.execute("DELETE FROM messages WHERE username=? AND subject=?",(username,sub,))
	cur.execute("INSERT INTO response(username,sub,message,sender) VALUES(?,?,?,?)",(username,sub,message,'admin',))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))	



#when admin wants to remove an existing restaurant	
@app.route('/admin_manage_remove/<username>/<place>')
def admin_manage_remove(username,place):
	upload='static/restaurants/'
	upload_dish='static/dish/'
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT filename FROM managers WHERE username=? AND place=?",(username,place,))
	var=cur.fetchone()
	
	#restaurant image is deleted 
	os.remove(upload+var[0])


	cur.execute('DELETE FROM managers WHERE username=? AND place=?',(username,place,))
	cur.execute("DELETE FROM rating WHERE place=? AND rest=?",(place,username,))
	cur.execute("DELETE FROM most_ordered WHERE place=? AND rest=?",(place,username,))
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
	cur.execute("SELECT * FROM {}".format(username))
	var=cur.fetchall()
	for x in var:
		os.remove(upload_dish+x[4])
	cur.execute("DROP TABLE {}".format(username))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))



#when admin wants to send notification to managers
@app.route('/notification_form/<rest>/<place>')
def notification_form(rest,place):
	return render_template('notification_form.html',rest=rest,place=place)


#insert querys to notification table
@app.route('/notification/<place>/<rest>',methods=['GET','POST'])
def notification(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	message=request.form['message']
	cur.execute("INSERT INTO notification VALUES(?,?,?)",(place,rest,message,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))


#to show restaurants table for reviews
@app.route('/admin_review')
def admin_review():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT rest,place FROM reviews GROUP BY rest,place")
	var=cur.fetchall()
	conn.close()
	return render_template('admin_review.html',var=var)


#to show reviews of selected restaurant
@app.route('/admin_review_show/<place>/<rest>')
def admin_review_show(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM reviews WHERE place=? AND rest=?",(place,rest,))
	reviews=cur.fetchall()
	return render_template('admin_review_show.html',reviews=reviews,place=place,rest=rest)


#when admin wants to remove a review
@app.route('/admin_review_remove/<place>/<rest>/<id_>')
def admin_review_remove(place,rest,id_):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM reviews WHERE id=?",(id_,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin_review_show',place=place,rest=rest))


if __name__ == '__main__':
   app.run(debug = True)	

