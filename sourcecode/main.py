import cherrypy
import sys, operator, os, pickle
import mysql.connector
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from math import radians, cos, sin, asin, sqrt
from operator import itemgetter
from geopy.distance import great_circle





class ExampleApp(object):
    

    def __init__(self):
	self.restData = []

    @cherrypy.expose
    def index(self):
        #return "hello world " + sys.version
        return env.get_template('mainpage.html').render()
    
    @cherrypy.expose
    def orders(self):
	return "Under construction! Please check back later on!"
    
    @cherrypy.expose
    def account(self):
	return "Under construction! Please check back later on!"
    
    @cherrypy.expose
    def restaurants(self):
        #Define database variables
	DATABASE_USER = 'root'
	DATABASE_HOST = '127.0.0.1'
	DATABASE_NAME = 'foodND'
	ndlat = 41.705572
	ndlng = -86.235339
	ndCoord = (ndlat, ndlng)
	#Create connection to MySQL
	cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, database=DATABASE_NAME)
	cursor = cnx.cursor()
	
	#Select all restaurants from database
	cursor.execute("select restID, name, lat, lng, address, url from Restaurants")
	rawData = cursor.fetchall()
	self.restData = [list(t) for t in rawData]
	for it in self.restData: # Calculate the distance from the restaurant to Notre Dame
	    restCoord = (it[2], it[3])
	    distance = great_circle(ndCoord, restCoord).kilometers
	    it.append(distance)
	# Sort restData by distance
	self.restData.sort(key=itemgetter(6))
	tmpl2 = loader.load('restaurants.html')
        stream = tmpl2.generate(data = self.restData)
	return stream.render('html', doctype='html')
    

    @cherrypy.expose
    def restDetails(self, restID = '0'):
        cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='foodND')
        cursor = cnx.cursor()

	restQuery = ("select restID, name, lat, lng, address from Restaurants where restID="+"'"+restID[:-1]+"'")
	cursor.execute(restQuery)
	data = cursor.fetchone()
	#data = next(subl for subl in self.restData if unicode(restID[:-1]) in subl)
	tmpl2 = loader.load('restDetail.html')
        stream = tmpl2.generate(data = data)
        return stream.render('html', doctype='html')
	
    @cherrypy.expose
    def menu(self):
	return "Under construction! Please check back later on!"
	
    @cherrypy.expose
    def showdb(self):
        cnx = mysql.connector.connect(user='test', password='mypass',
                              host='127.0.0.1',
                              database='testdb')
        cursor = cnx.cursor()
        query = ("SELECT firstname,lastname,email FROM Invitations")
        cursor.execute(query)
        info = str()
        print cursor
        for (firstname, lastname, email) in cursor:
           info = info + "Full Name:" + lastname + firstname + "Email: "+email
        return info



application = cherrypy.Application(ExampleApp(), None)
