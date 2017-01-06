import apiutil
import sys
import os.path
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import cherrypy
import os, operator, pickle 
import os.path
from math import radians, cos, sin, asin, sqrt
import json
import mysql.connector
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from config import conf
from operator import itemgetter
from geopy.distance import great_circle
from mysql.connector import Error
import logging
from config import conf
from restaurantid import RestaurantID

class Restaurants(object):
    ''' Handles resource /restaurants
        Allowed methods: GET, POST, OPTIONS '''
    exposed = True

    def __init__(self):
        self.id=RestaurantID()
        self.db = dict()
        self.db['name']='foodND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'
	self.restData = []

    def _cp_dispatch(self,vpath):
            print "Restaurants._cp_dispatch with vpath: %s \n" % vpath
            if len(vpath) == 1: # /restaurants/{id}
                cherrypy.request.params['restID']=vpath.pop(0)
                return self.id
            if len(vpath) == 2: # /restaurants/{id}/menus
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                return self.id.menus
            if len(vpath) == 3: # /restaurants/{restID}/menus/{menuID}
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                return self.id.menus.id 
            if len(vpath) == 4: # /restaurants/{restID}/menus/{menuID}/categories
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                vpath.pop(0) # categories
                return self.id.menus.id.categories
	    if len(vpath) == 5: # /restaurants/{restID}/menus/{menuID}/categories/{categoryID}
		cherrypy.request.params['restID']=vpath.pop(0)
		vpath.pop(0) # menus
		cherrypy.request.params['menuID']=vpath.pop(0)
		vpath.pop(0) # categories
		cherrypy.request.params['catID']=vpath.pop(0)
		return self.id.menus.id.categories.id

            if len(vpath) == 6: # /restaurants/{restID}/menus/{menuID}/categories/{catID}/items
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                vpath.pop(0) # categories
                cherrypy.request.params['catID']=vpath.pop(0)
		vpath.pop(0)
                return self.id.menus.id.categories.id.items

	    if len(vpath) == 7: # /restaurants/{restID}/menus/{menuID}/categories/{catID}/itmes/{itemID}
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                vpath.pop(0) # categories
                cherrypy.request.params['catID']=vpath.pop(0)
                vpath.pop(0) # items
		cherrypy.request.params['itemID']=vpath.pop(0)
                return self.id.menus.id.categories.id.items.id  
	    
	    return vpath

    def getDataFromDB(self):
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
	    ndlat = 41.698318
	    ndlng = -86.236218
	    ndCoord = (ndlat, ndlng) 
	    #Select all restaurants from database
	    cursor = cnx.cursor()
	    cursor.execute("select restID, name, lat, lng, address, city, state, zip, url from Restaurants")
	except Error as e:
            logging.error(e)
            raise
	rawData = cursor.fetchall()
	self.restData = [list(t) for t in rawData]
	for it in self.restData: # Calculate the distance from the restaurant to Notre Dame
	    restCoord = (it[2], it[3])
	    distance = great_circle(ndCoord, restCoord).kilometers
	    it.append(distance)
	    it[2] = str(it[2])
	    it[3] = str(it[3])
	# Sort restData by distance
	self.restData.sort(key=itemgetter(9))
	self.restData = self.restData[:-1]
	
    def GET(self):    
        ''' Get list of restaurants '''
        # Return restaurants in order of distance from lat, long
        # Compute distances of restaurants from DeBartolo Hall for now

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
	output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])
	self.getDataFromDB()
	if output_format == 'text/html':
            return env.get_template('restaurants-tmpl.html').render(data = self.restData, base = cherrypy.request.base.rstrip('/') + '/')
	else:
	    
	    return json.dumps(self.restData, encoding='utf-8')

    def POST(self, **kwargs):
        ''' Add a new restaurant '''
        result= "POST /restaurants     ...     Restaurants.POST\n"
        result+= "POST /restaurants body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data; restID should not be included
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self):
        ''' Allows GET, POST, OPTIONS '''
        #Prepare response
        return "<p>/restaurants/ allows GET, POST, and OPTIONS</p>"

class StaticAssets(object):
    pass

if __name__ == '__main__':
    conf = {
        'global': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    }
    cherrypy.tree.mount(Restaurants(), '/restaurants', {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    })
    cherrypy.tree.mount(StaticAssets(), '/', {
        '/': {
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    application = cherrypy.Application(Restaurants(), None, conf)
