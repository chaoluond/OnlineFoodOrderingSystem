''' Implements handler for /categories
Imported from handler for /restaurants/{restID}/menus/{menuID} '''

import os, os.path, json, logging, mysql.connector
import cherrypy
from jinja2 import Environment, FileSystemLoader
from categoryid import CategoryID
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from categoryid import CategoryID

class Categories(object):
    ''' Handles resources /categories/{catID}
        Allowed methods: GET, POST, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.id = CategoryID()
        self.db = dict()
	self.db['name']='foodND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self, menuID):
        cnx = mysql.connector.connect(
            user=self.db['user'],
            host=self.db['host'],
            database=self.db['name'],
        )
        cursor = cnx.cursor()
        qn="select sectionID, sectionName from Categories where menuID=%s order by sectionID" % menuID
        cursor.execute(qn)
        result=cursor.fetchall()
        return result

    def GET(self, restID, menuID):
        
	''' Return list of categories for menus menuID'''

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        try:
            result=self.getDataFromDB(menuID)
        except mysql.connector.Error as e:
            logging.error(e)
            raise

        if output_format == 'text/html':
            return env.get_template('categories-tmpl.html').render(
                rID=restID,
                rName=restName,
		mID = menuID,
                data=result,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            data = [{
                'href': 'restaurants/%s/menus/%s/categories/%s/items' % (restID, menuID, categoryID),
                'name': categoryName
            } for categoryID, categoryName in result]
            return json.dumps(data, encoding='utf-8')

    def POST(self, restID, menuID, **kwargs):
        result= "POST /restaurants/{restID=%s}/menus/{menuID=%s}/categories     ...     Categories.POST\n" % (restID,menuID)
        result+= "POST /restaurants/{restID=%s}/menus/{menuID=%s}/categories body:\n" % (restID, menuID)
	for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self,restID):
	return "<p>/restaurants/{restID=%s}/menus/{menuID=%s}/categories allows GET, POST, and OPTIONS</p>"
