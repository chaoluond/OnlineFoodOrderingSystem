#Use this script to create the database tables
#This script does NOT populate the tables with any data

import mysql.connector

#Define database variables
DATABASE_USER = 'root'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'foodND'

#Create connection to MySQL
cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST)
cursor = cnx.cursor()

###################################
## Create DB if it doesn't exist ##
###################################

createDB = (("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET latin1") % (DATABASE_NAME))
cursor.execute(createDB)

#########################
## Switch to foodND ##
#########################

useDB = (("USE %s") % (DATABASE_NAME))
cursor.execute(useDB)

###########################
## Drop all tables first ##
###########################

#Drop OrderDetail
dropTableQuery = ("drop table if exists OrderDetail")
cursor.execute(dropTableQuery)

#Drop FoodOrder
dropTableQuery = ("drop table if exists FoodOrder")
cursor.execute(dropTableQuery)

#Drop User
dropTableQuery = ("drop table if exists User")
cursor.execute(dropTableQuery)

#Drop Items
dropTableQuery = ("drop table if exists Items")
cursor.execute(dropTableQuery)


#Drop Categories
dropTableQuery = ("drop table if exists Categories")
cursor.execute(dropTableQuery)

#Drop Menus
dropTableQuery = ("drop table if exists Menus")
cursor.execute(dropTableQuery)


#Hours
dropTableQuery = ("DROP TABLE IF EXISTS Hours")
cursor.execute(dropTableQuery)


#Restaurants
dropTableQuery = ("DROP TABLE IF EXISTS Restaurants")
cursor.execute(dropTableQuery)


########################
## Create tables next ##
########################


#Restaurants
createTableQuery = ('''CREATE TABLE Restaurants (
						restId VARCHAR(20) NOT NULL,
						name VARCHAR(45) NOT NULL,
						address VARCHAR(100) NOT NULL,
						city VARCHAR(45) NOT NULL,
						state VARCHAR(20) NOT NULL,
						zip VARCHAR(10) NOT NULL,
						phone VARCHAR(20) NOT NULL,
						lat DECIMAL(10,8) NOT NULL,
						lng DECIMAL(11,8) NOT NULL,
                			        url VARCHAR(100),
						PRIMARY KEY (restId));'''
                    )
cursor.execute(createTableQuery)

#Hours
createTableQuery = ('''CREATE TABLE Hours (
						restId VARCHAR(20) NOT NULL,                                                
						day enum ('M','T','W','TH','F','S','SU') not null,
                                                open TIME NOT NULL,
                                                close TIME NOT NULL,
                                                PRIMARY KEY(restId,day,open),
                                                FOREIGN KEY(restId)
                                                REFERENCES Restaurants(restId)
                                                ON DELETE CASCADE
                                          );'''
                    )
cursor.execute(createTableQuery)

#Menus
createTableQuery = (''' create table Menus (
                                                restID varchar(20) not null,
                                                menuID int not null auto_increment,
						menuName varchar(30),
						primary key(menuID),
						foreign key(restID) references Restaurants(restID) on delete cascade 
						);'''

                                        )

cursor.execute(createTableQuery)

#Category
createTableQuery = (''' create table Categories (
						menuID int not null,	
						sectionID int not null auto_increment,
						sectionName varchar(50),			
						primary key(menuID, sectionID),
						foreign key(menuID) references Menus(menuID) on delete cascade
						)engine = myisam;'''
					
					)

cursor.execute(createTableQuery)

#Items
createTableQuery = (''' create table Items (
						menuID int not null,
						sectionID int not null,
						itemID int not null auto_increment,
						name varchar(30) not null,
						price decimal(6,2) not null,
						description varchar(100),
						primary key(itemID),
						foreign key(menuID) references Menus(menuID) on delete cascade
					);'''
					
			)

cursor.execute(createTableQuery)


#User
createTableQuery = (''' create table User (
                                           	userID int not null auto_increment,
						email VARCHAR(45)  CHARACTER SET utf8mb4 NOT NULL,
						firstName varchar(20) not null,
						lastName varchar(20) not null,
						address varchar(100) not null,
						password VARCHAR(120)  CHARACTER SET utf8mb4 NOT NULL,
						phone varchar(20) not null,
						primary key(userID)
          
                                        );'''

                        )

cursor.execute(createTableQuery)

#FoodOrder
createTableQuery = (''' create table FoodOrder (
                                                orderID int not null auto_increment,
          					userID int not null,
						paymentStatus boolean not null,
						primary key(orderID),
						foreign key(userID) references User(userID) on delete cascade
                                        );'''

                        )

cursor.execute(createTableQuery)

#OrderDetail
createTableQuery = (''' create table OrderDetail (
							orderID int not null,
							itemID int not null,
							quantity int not null,
							primary key(orderID, itemID),
							foreign key(orderID) references FoodOrder(orderID) on delete cascade,
							foreign key(itemID) references Items(itemID) on delete cascade 
						);'''

                        )

cursor.execute(createTableQuery)
  
#Commit the data and close the connection to MySQL
cnx.commit()
cnx.close()
