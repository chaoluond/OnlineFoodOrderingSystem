''' /users/registration resource
This is run as a WSGI application through CherryPy and Apache with mod_wsgi
Date: Mar. 12, 2015
Web Applications'''
import apiutil
from apiutil import errorJSON
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import cherrypy
import os
import os.path
import json
import mysql.connector
from mysql.connector import Error
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
import logging
from passlib.apps import custom_app_context as pwd_context
from config import conf
from pyvalidate import validate, ValidationException

class UserRegistration(object):
    ''' Handles resource /users/registration
        Allowed methods: GET, POST, OPTIONS '''
    exposed = True

    def __init__(self):
        self.db = dict()
        self.db['name']='foodND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'


    def GET(self):
        ''' Prepare user registration page '''

        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        if output_format == 'text/html':
            return env.get_template('userregistration-tmpl.html').render(
                base=cherrypy.request.base.rstrip('/') + '/'
            )
 

    @cherrypy.tools.json_in(force=False)

    @validate(requires=['firstName', 'lastName', 'email', 'address', 'password', 'phone'],
              types={'firstName':str, 'lastName':str, 'email':str, 'address':str, 'password':str, 'phone':str},
              values={'email':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'phone':'^\d*$', 
			'password':'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[?!_#%^&@-]).{9,}'}
             )
    def check_params(self, firstName, lastName, email, address, password, phone):
              print 'adding user "%s:%s" "%s:%s" with address: %s:%s email: %s:%s phone: %s:%s password: %s:%s' % (firstName, type(firstName),
			 lastName, type(lastName),
			 address, type(address),
                         email, type(email),
                         phone, type(phone),
                         password, type(password))


    def POST(self, firstName=None, lastName=None, email=None, address=None, password=None, confirmPassword=None, phone=None):
        ''' Add a new user '''
	if not firstName:
          try:
            firstName = cherrypy.request.json["firstName"]
            print "firstName received: %s" % firstName
          except:
            print "firstName was not received"
            return errorJSON(code=8002, message="Expected text 'firstName' for user as JSON input")
        if not lastName:
          try:
            lastName = cherrypy.request.json["lastName"]
            print "lastName received: %s" % lastName
          except:
            print "lastName was not received"
            return errorJSON(code=8002, message="Expected text 'lastName' for user as JSON input")

        if not email:
          try:
            email = cherrypy.request.json["email"]
            print "email received: %s" % email
          except:
            print "email was not received"
            return errorJSON(code=8002, message="Expected email 'email' for user as JSON input")
        
	if not address:
          try:
            address = cherrypy.request.json["address"]
            print "address received: %s" % address
          except:
            print "address was not received"
            return errorJSON(code=8002, message="Expected email 'address' for user as JSON input")
        
	if not password:
          try:
            password = cherrypy.request.json["password"]
            print "password received: %s" % password
          except:
            print "password was not received"
            return errorJSON(code=8002, message="Expected password 'password' for user as JSON input")
        
	if not phone:
          try:
            phone = cherrypy.request.json["phone"]
            print "phone received: %s" % phone
          except:
            print "phone was not received"
            return errorJSON(code=8002, message="Expected phone 'phone number' for user as JSON input")




        try:
            self.check_params(firstName=firstName, lastName=lastName, email=email, address=address, password=password, phone=phone)
        except ValidationException as ex:
            print ex.message
            return errorJSON(code=8002, message=ex.message)


        cnx = mysql.connector.connect(user=self.db['user'],host=self.db['host'],database=self.db['name'])
        cursor = cnx.cursor()
        # WARNING: Need to do validation

	#Add in def POST: after connecting to DB and before INSERT statement:
        # Check if email already exists
        q="SELECT EXISTS(SELECT 1 FROM User WHERE email='%s')" % email
        cursor.execute(q)
        if cursor.fetchall()[0][0]:
            #email already exists
            print "User with email %s Already Exists" % email
            return errorJSON(code=8000, message="User with email %s Already Exists") % email

        hash = pwd_context.encrypt(password)


        q="INSERT INTO User (firstName, lastName, email, address, password, phone) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" \
            % (firstName, lastName, email, address, hash, phone)
        try:
            cursor.execute(q)
            #userID=cursor.fetchall()[0][0]
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert user
            print "mysql error: %s" % e
            return errorJSON(code=8001, message="Failed to add user")
        result = {'firstName':firstName, 'lastName': lastName, 'email':email, 'address':address, 'password':hash, 'phone':phone, 'errors':[]}
        return json.dumps(result)

    def OPTIONS(self):
        ''' Allows GET, POST, OPTIONS '''
        #Prepare response
        return "<p>/users/registration allows GET, POST, and OPTIONS</p>"

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
    cherrypy.tree.mount(UserRegistration(), '/users/registration', {
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
    application = cherrypy.Application(UserRegistration(), None, conf)


