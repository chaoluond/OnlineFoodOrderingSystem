''' Implements handler for /items
Imported from handler for /categories/{id} '''
import logging
import cherrypy
import mysql.connector
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import os
import os.path
import json
import pprint
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from itemid import ItemID

class Items(object):
    ''' Handles resources /restaurants{restID}/menus/{menuID}/categories/{catID}/items
        Allowed methods: GET, POST, OPTIONS  '''
    exposed = True

    def __init__(self):
        self.id = ItemID()
        self.db=dict()
        self.db['name']='foodND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self, menuID, catID):
        cnx = mysql.connector.connect(user=self.db['user'],host=self.db['host'],database=self.db['name'])
        cursor = cnx.cursor()
        qn="select sectionName from Categories where menuID=%s and sectionID=%s" % (menuID, catID)
        cursor.execute(qn)
        catName=cursor.fetchone()[0]
        q="select itemID, name, price, description from Items where menuID=%s and sectionID=%s" % (menuID, catID)
        cursor.execute(q)
        result=cursor.fetchall()
        return catName, result

    def GET(self, restID, menuID, catID):
        ''' Return list of items for categories for restaurant id'''
        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        try:
            catName,result=self.getDataFromDB(menuID, catID)
            pp=pprint.PrettyPrinter(indent=6)
            pp.pprint(result)
        except mysql.connector.Error as e:
            logging.error(e)
            raise
        
        if output_format == 'text/html':
            return env.get_template('items-tmpl.html').render(rID=restID,mID=menuID, cID=catID,cName=catName,items=result,base=cherrypy.request.base.rstrip('/') + '/')
        else:
            data = [{
                    'href': '/restaurants/%s/menus/%s/categories/%s/items/%s' % (restID, menuID, catID, itemID),
                    'name': itemName,
                    'description': desc,
                    'price' : unicode(price)
                    } for itemID, itemName, price, desc in result]
            return json.dumps(data, encoding='utf-8')
        
    def POST(self, restID, menuID, catID,  **kwargs):
        result= "POST /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}/items     ...     Items.POST\n" % (restID, menuID, catID)
        result+= "POST /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}items body:\n" % (restID, menuID, catID)
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self,restID, menuID, catID):
        return "<p>/restaurants/{restID=%s}/menus/{menuID}/categories/{catID=%s}/items allows GET, POST, and OPTIONS</p>"

