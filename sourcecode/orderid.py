''' Controller for /orders/{id}
    Imported from handler for /orders '''
import cherrypy
import os, json, logging, mysql.connector
from mysql.connector import Error
from apiutil import errorJSON
from orderItems import OrderItems
class OrderID(object):
    ''' Handles resource /restaurants/{id} 
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def __init__(self):
	self.orderitems = OrderItems()

    def GET(self, orderID):
	''' Return a list of items for a given orderID'''
	cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='foodND',charset='utf8mb4')
        q="select exists(select 1 from OrderDetail where orderID=%s)" % orderID
        cursor = cnx.cursor()
        cursor.execute(q)
	if not cursor.fetchall()[0][0]:
	    # If the orderID does not exist, return error message
	    return errorJSON(code=3000, message="orderID for %s does Not Exist" % orderID) 
	q = "select itemID, quantity from OrderDetail where orderID=%s" % orderID
	cursor.execute(q)
	result = [{
		    'itemID' : itemID,
		    'quantity' : quantity
		} for itemID, quantity in cursor.fetchall()]
	result.append({'error' : []})
	return json.dumps(result)   
	


    def DELETE(self, orderID):
        ''' If the orderID exists, delete the order. If the orderID does not exist, return error information. Error code 3000'''
	cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='foodND',charset='utf8mb4')
	q="select exists(select 1 from OrderDetail where orderID=%s)" % orderID
	cursor = cnx.cursor()
	cursor.execute(q)
	if not cursor.fetchall()[0][0]:
	    # orderID does not exist
	    return errorJSON(code=3000, message="orderID for %s does not exist" % orderID)
	q = "delete from OrderDetail where orderID=%s" % orderID
	cursor.execute(q)
	result = "Order with orderID=%s has been sucessfully deleted \n" % orderID
	result += "{'error' : []}"
	return json.dumps(result)

