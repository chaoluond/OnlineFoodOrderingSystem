''' Implements handler for /orders/{orderID}/items/{itemID}
To add an item to an order '''
import apiutil
import cherrypy
import mysql.connector
from mysql.connector import Error
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import json
from apiutil import errorJSON
from config import conf


class OrderItems(object):
    exposed = True
   
    def __init__(self):
	self.data = []

    def GET(self, orderID, orderitemID):
        ''' GET orderItemID,quantity for orderID and orderitemID or error if no entry with orderID or itemID'''
        cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='foodND',charset='utf8mb4')        
        cursor = cnx.cursor()
        q="select exists(select 1 from OrderDetail where orderID=%s and itemID=%s)" % (orderID, orderitemID)
        cursor.execute(q)
        if not cursor.fetchall()[0][0]:
            #no orderItemID for this orderID / itemID combination
            return errorJSON(code=9004, message="OrderItemID for OrderID %s  and ItemID %s Does Not Exist" % (orderID,orderitemID))
        q="select itemID,quantity from OrderDetail where orderID=%s and itemID=%s" % (orderID, orderitemID)
        cursor.execute(q)
        tmp=cursor.fetchall()
        result={"orderitemID":tmp[0][0],"quantity":tmp[0][1],"errors":[]}
        return json.dumps(result)

    def DELETE(self, orderID, orderitemID):
        ''' Delete orderItem with orderID and orderitemID'''
        cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='foodND',charset='utf8mb4')        
        cursor = cnx.cursor()
        q="set sql_safe_updates=0;"  
        cursor.execute(q)
        q="select exists(select 1 from OrderDetail where orderID=%s and itemID=%s)" % (orderID, orderitemID)
        cursor.execute(q)
        if not cursor.fetchall()[0][0]:
            #no orderItemID for this orderID / itemID combination
            return errorJSON(code=9004, message="itemID for orderID %s  and orderitemID %s Does Not Exist" % (orderID,orderitemID))
        try:
            q="delete from OrderDetail where orderID=%s and itemID=%s" % (orderID, orderitemID)
            cursor.execute(q)
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert orderItem
            print "mysql error: %s" % e
            return errorJSON(code=9005, message="Failed to delete order item from shopping cart")
        result={"errors":[]}
        return json.dumps(result)


    @cherrypy.tools.json_in(force=False)
    def PUT(self, orderID, orderitemID):
        ''' Add or update an item to an order 
        quantity is received in a JSON dictionary
        output is also returned in a JSON dictionary'''
        try:
            quantity = int(cherrypy.request.json["quantity"])
            print "quantity received: %s" % quantity
        except:
            print "quantity was not received"
            return errorJSON(code=9003, message="Expected integer 'quantity' of items in order as JSON input")
        cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='foodND',charset='utf8mb4')        
        cursor = cnx.cursor()
        q="set sql_safe_updates=0;"  
        cursor.execute(q)
        # does orderID exist?
        q="select exists(select 1 from FoodOrder where orderID=%s)" % orderID
        cursor.execute(q)
        if not cursor.fetchall()[0][0]:
            #orderID does not exist
            return errorJSON(code=9000, message="Order with orderID %s Does Not Exist") % orderID
        # does itemID exist?
        q="select exists(select 1 from Items where itemID=%s)" % orderitemID
        cursor.execute(q)
        if not cursor.fetchall()[0][0]:
            #itemID does not exist
            return errorJSON(code=9001, message="Item with itemID %s Does Not Exist") % orderitemID
        q="insert into OrderDetail (orderID, itemID, quantity) values (%s, %s, %s) on duplicate key update quantity=%s;" \
            % (orderID, orderitemID, quantity, quantity)
        cursor.execute(q)
        q="select itemID from orderDetail where orderID=%s and itemID=%s" % (orderID,orderitemID)
        orderItemID=0
        try:
            cursor.execute(q)
            orderItemID=cursor.fetchall()[0][0]
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert orderItem
            print "mysql error: %s" % e
            return errorJSON(code=9002, message="Failed to add order item to shopping cart")
        result = {'orderItemID':orderItemID, 'orderID':orderID, 'itemID':itemID, 'quantity':quantity, 'errors':[]}
        return json.dumps(result)

application = cherrypy.Application(OrderItems(), None, conf)

