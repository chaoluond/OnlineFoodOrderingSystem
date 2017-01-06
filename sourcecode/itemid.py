''' Controller for /restaurants{restID}/menus/{menuID}/categories/{catID}/items/{itemID}'''
import cherrypy

class ItemID(object):
    ''' Handles resources /items/{itemID}/{id}
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def GET(self, restID, menuID, catID, itemID):
        return "GET /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{cateD=%s}/items/{itemID=%s}   ...   ItemID.GET" % (restID, menuID, catID, itemID)

    def PUT(self, restID, menuID, catID, itemID, **kwargs):
        result = "PUT /restaurants/{restID=%s}/menus/{menuId=%s}/categories/{catID=%s}/items/{itemID=%s}   ...     ItemID.PUT\n" % (restID,menuID, catID,itemID)
        result += "PUT /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}/items/{itemID=%s} body:\n" % (restID, menuID, catID, itemID)
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        return result

    def DELETE(self, restID, menuID, catID, itemID):
        #Validate id
        #Delete restaurant
        #Prepare response
        return "DELETE /restaurants/{restID=%s}/menus/{menuID=%s}/categories/{catID=%s}/items/{itemID=%s}   ...   ItemID.DELETE" % (restID,menuID, catID,itemID)

    def OPTIONS(self, restID, menuID, catID, itemID):
        #Prepare response
        return "<p>/restaurants/{restID}/menus/{menuID=%s}/categories/{catID}/items/{itemID} allows GET, PUT, DELETE, and OPTIONS</p>"

