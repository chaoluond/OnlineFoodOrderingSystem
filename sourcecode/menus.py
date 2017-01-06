''' Implements handler for /menus
Imported from handler for /restaurants/{id} '''
import os, os.path, json, logging, mysql.connector
import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from menuid import MenuID

class Menus(object):
    ''' Handles resources /menus/{menuID}
        Allowed methods: GET, POST, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.id = MenuID()
	self.db=dict()
        self.db['name']='foodND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self, id):
        cnx = mysql.connector.connect(
            user=self.db['user'],
            host=self.db['host'],
            database=self.db['name'],
        )
        cursor = cnx.cursor()
        qn="select name from Restaurants where restID='%s'" % id
        cursor.execute(qn)
        restName=cursor.fetchone()[0]
        q="select menuID, menuName from Menus where restID='%s' order by menuID" % id
        cursor.execute(q)
        result=cursor.fetchall()
        return restName,result

    def GET(self, restID):
        ''' Return list of menus for restaurant with restID'''

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        try:
            restName,result=self.getDataFromDB(restID)
        except mysql.connector.Error as e:
            logging.error(e)
            raise
        if output_format == 'text/html':
            return env.get_template('menu-tmpl.html').render(
                rID=restID,
                rName=restName,
                data=result,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            data = [{
                'href': 'restaurants/%s/menus/%s/categories' % (restID, menuID),
                'name': menuName
            } for menuID, menuName in result]
            return json.dumps(data, encoding='utf-8')
	
    def POST(self, restID, **kwargs):
        result= "POST /restaurants/{restID}/menus     ...     Menus.POST\n"
        result+= "POST /restaurants/{restID}/menus body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self, restID):
        return "<p>/restaurants/{restID}/menus/ allows GET, POST, and OPTIONS</p>"
