# ONLINE FOOD ORDERING SYSTEM
## INTRODUCTION
 The online food ordering system gives the restaurant the ability to increase sales and expand their business by giving the customers the ability to order food online. With an online restaurant menu ordering system, customers can place orders online 24*7. 

## FRONT END 
 HTML (HyperText Mark-up Language)
 CSS (Cascading Style Sheets)
 JAVASCRIPT
## BACK END
 PYTHON
## QUERY Language
 SQLite 

### members DB

approval(username text NOT NULL ,password text, filename TEXT, place TEXT ,location TEXT, phone INTEGER ,start TEXT, stop TEXT )

customers(username text NOT NULL PRIMARY KEY , password text NOT NULL )

customers(username text NOT NULL PRIMARY KEY , password text NOT NULL )

feedback (place TEXT, rest TEXT, username TEXT, message TEXT)

managers(username text NOT NULL ,password text, filename TEXT, place TEXT ,location TEXT, phone INTEGER ,start TEXT, stop TEXT )

messages(username TEXT, subject TEXT, message TEXT)

most_ordered (place TEXT, rest TEXT, item TEXT, orders INTEGER, dish_image TEXT, price TEXT)

notification (place TEXT, rest TEXT, message TEXT)

rating(place text NOT NULL ,rest TEXT, username TEXT, stars INTEGER)

response (username TEXT, sub TEXT, message TEXT, sender TEXT)

reviews (username TEXT, rest TEXT, place TEXT, date TEXT, rating INTEGER, review TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)

search (item text NOT NULL, def TEXT, price INTEGER NOT NULL, category TEXT, place TEXT, rest TEXT, dish_image text)
