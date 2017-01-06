''' Implements handler for /categories/{id}
Imported from handler for /categories'''
import cherrypy
from items import Items

class CategoryID(object):
    ''' Handles resource /categories/{catID}
        Allowed methods: GET, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.items = Items()

    def GET(self, restID, menuID, catID):
        ''' Return info of category id for restaurant id'''
        return "GET /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}  ...   CategoryID.GET" % (restID,menuID,catID)

    def PUT(self, restID, menuID, catID, **kwargs):
        ''' Update category id for restaurant id'''
        result = "PUT /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}   ...   CategoryID.PUT\n" % (restID,menuID,catID)
        result += "PUT /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s} body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        return result

    def DELETE(self, restID, catID, menuID):
        #Validate id
        #Delete restaurant
        #Prepare response
        return "DELETE /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}   ...   CategoryID.DELETE" % (restID,menuID,catID)

    def OPTIONS(self,restID, menuID, catID):
        return "<p>/restaurants/{restID}/menus/{menuID}/categories/{catID} allows GET, PUT, DELETE, and OPTIONS</p>"

