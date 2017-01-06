#e this script to populate the |restaurant| table of the database

import mysql.connector
import json
from decimal import *
import random

#Define database variables
DATABASE_USER = 'root'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'foodND'

#Create connection to MySQL
cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, database=DATABASE_NAME)
cursor = cnx.cursor()

#Load json file
inputFile = open('/var/www/webappscode/01-27-sql/db/restaurantData.json','r')
restaurantDict = json.load(inputFile)
inputFile.close()


date = {
	'Monday' : 'M',
	'Tuesday' : 'T',
	'Wednesday' : 'W',
	'Thursday' : 'Th',
	'Friday' : 'F',
	'Saturday' : 'S',
	'Sunday' : 'Su'
}

#op through the restaurants and add info and menu to database
for key, restaurant in restaurantDict.iteritems():

        ###############################
        ## Add restaurant info first ##
        ###############################
        inputDict = {
                'restID' : key,
                'name' : restaurant['name'],
                'address' : restaurant['street_address'],
                'city' : restaurant['locality'],
                'state' : restaurant['region'], 
                'zip' : restaurant['postal_code'],
                'phone' : restaurant['phone'],
                'lat' : restaurant['lat'],
                'lng' : restaurant['long'],
                'url' : restaurant['website_url']
        }

        #Insert this info into the database
        addRestaurant = ("INSERT INTO Restaurants (restID, name, address, city, state, zip, phone, lat, lng, url) VALUES (%(restID)s, %(name)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(phone)s, %(lat)s, %(lng)s, %(url)s)")
        cursor.execute(addRestaurant,inputDict)


	###############################
	## Add Hous information     ###
	###############################
	for day, time in restaurant['open_hours'].iteritems():
		if time: #We do not add empty items into this table
			for t in time:
				item = {
					'restID' : key,
					'day' : date[day],
					'open' : t.split()[0],
					'close' : t.split()[2] 
				}	
				# insert this item into Hours table
				addHours = ("insert into Hours (restID, day, open, close) values (%(restID)s, %(day)s, %(open)s, %(close)s)")
				cursor.execute(addHours, item)



	##############################
	## Populate Menus	   ###
	##############################
	for menu in restaurant['menus']: # Populate Menus table
		temp = {'restID' : key,
			'menuName' : menu['menu_name']
			}
		addMenu = ("insert into Menus (restID, menuName) values (%(restID)s, %(menuName)s)")
		cursor.execute(addMenu,temp)	
		for section in menu['sections']: # Populate Category table
			temp = {'sectionName' : section['section_name'][:-1]}
			addSection = ("insert into Categories (menuID, sectionName) values (@menuid, %(sectionName)s)")
			cursor.execute("set @menuid = (select menuID from Menus order by menuID desc limit 1)")
			cursor.execute(addSection, temp)
			for subsection in section['subsections']: # Add item into items
				for item in subsection['contents']:
					if item['type'] == 'ITEM' and 'price' in item.keys(): # If the price exists, we add this item to item table
						if 'description' in item.keys():
							d = item['description']
						else:
							d = 'No description'
						temp = {
							'price' : item['price'],
							'name' : item['name'],
							'description' : d
						}
						cursor.execute("set @sectionid = (select sectionID from Categories where menuID = @menuid order by sectionID desc limit 1)")
                                        	addItem = ("insert into Items (menuID, sectionID, price, name, description) values (@menuid, @sectionid, %(price)s, %(name)s, %(description)s)")
                                        	cursor.execute(addItem, temp)
					elif item['type'] == 'ITEM':
						if 'description' in item.keys():
							d = item['description']
						else:
							d = 'No description'
						temp = {
							'price' : ((random.randint(5, 20)) + 0.99),
							'name' : item['name'],
							'description' : d
						}
					
						cursor.execute("set @sectionid = (select sectionID from Categories where menuID = @menuid order by sectionID desc limit 1)")
						addItem = ("insert into Items (menuID, sectionID, price, name, description) values (@menuid, @sectionid, %(price)s, %(name)s, %(description)s)")
						cursor.execute(addItem, temp)
					




cnx.commit()
cnx.close()
