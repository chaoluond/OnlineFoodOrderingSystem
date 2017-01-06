import apiutil
import sys
import os.path
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import os, json, logging, mysql.connector
import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from apiutil import errorJSON
from config import conf
from orderid import OrderID

class Orders(object):
    ''' Handles resources /orders/{orderID}
        Allowed methods: GET, POST, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.id = OrderID()
	self.db=dict()
        self.db['name']='foodND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'
	self.orderData = []
    

    def _cp_dispatch(self,vpath):
	print "Orders._cp_dispatch with vpath: %s \n" % vpath
	if len(vpath) == 1: # /orders/{orderID}
	    cherrypy.request.params['orderID'] = vpath.pop(0)
	    return self.id
	if len(vpath) == 2: # /orders/{orderID}/orderitems
	    cherrypy.request.params['orderID'] = vpath.pop(0)
	    vpath.pop(0) # orderitems
	    return self.id.orderitems
	if len(vpath) == 3: # /orders/{orderID}/orderitems/{itemID}
            cherrypy.request.params['orderID']=vpath.pop(0)
            vpath.pop(0) # orderitems
            cherrypy.request.params['orderitemID']=vpath.pop(0)
            return self.id.orderitems
        return vpath

    def getDataFromDB(self):
        cnx = mysql.connector.connect(
            user=self.db['user'],
            host=self.db['host'],
            database=self.db['name'],
        )
        cursor = cnx.cursor()
        qn="select * from FoodOrder"
        cursor.execute(qn)
        self.orderData=cursor.fetchall()

    def GET(self):
        ''' Return list of orders'''

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        try:
            self.getDataFromDB()
        except mysql.connector.Error as e:
            logging.error(e)
            raise
        if output_format == 'text/html':
            return env.get_template('orders-tmpl.html').render( # This part is under construction!!!!!!!!!!!!!!!!!!!!!!!!
                data = self.orderData,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            data = [{
                'href': 'orders/%s/orderitems' % orderID,
                'userID': userID,
		'payment': payment
            } for orderID, userID, payment in self.orderData]
	    data.append({'error' : []})
            return json.dumps(data, encoding='utf-8')
	
    def PUT(self, userID):
	''' If a user have an orderID, then return the orderID. If the user does not have any order, create an order and return the orderID'''
        #result= "PUT /orders?userID=%s     ...     Orders.POST\n" % userID
	cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='foodND',charset='utf8mb4')
        q="select exists(select 1 from FoodOrder where orderID=%s)" % userID
	cursor = cnx.cursor()
	cursor.execute(q)
	if not cursor.fetchall()[0][0]:
	    # The user does not have any order, so create one and return the orderID
	    q = "insert into FoodOrder(userID, paymentStatus) values(%s, false)" % userID
	    cursor.execute(q)
	q = "select orderID from FoodOrder where userID=%s" % userID
	cursor.execute(q)
	orderID = cursor.fetchall()[0][0]
	result ={'orderID': orderID, 'error' : []}
	return json.dumps(result) 
	    



application = cherrypy.Application(Orders(), None, conf)

