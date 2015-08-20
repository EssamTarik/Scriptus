#Scriptus is a python micro-framework , it's a small package that handles routing, POST and GET request processing ,cookies and sessions

from wsgiref.simple_server import make_server
import re
from wrappers import Request,Response
from Cookie import SimpleCookie
import pickle,os

#Sciptus class is the central unit of your app , all work is handled from here

class Scriptus(object):
	def __init__(self):
		#object routes dictionary is formed of url:function pairs
		self.routes={}
	

	#defines a new route
	def route(self,address,function):
		self.routes[address]=function

	#searches for the path in defined routes 
	def checkRoute(self,request):
		
		#checks routes one by one for the request's path
		#returns the return of route's function or None if no match was found
		for route in self.routes.keys():
			match=re.match(route,request.path)
			
			#if there's a url match , pass its variables as arguments to the route's function
			if( match is not None):
				urlargs=match.groups()
				return self.routes[route](request,*urlargs)
		return None


	#main function that processes requests from server
	def app(self,environ,start_response):

		#create a Request object from environ
		request=Request(environ)
		
		#get a Response object from the route's function or create one from the return if it's not a Response object
		returnobject=self.checkRoute(request)

		#a 404 not found and 'not found' message are returned if the returnobject is None
		if returnobject is None:
			returnobject=Response('Not Found',status=404)

		#if the returnobject isn't None but isn't a Response object (str for example) an Response object is with it as text
		if type(returnobject) is not Response:
			returnobject=Response(str(returnobject))

		#now the Response object is ready to respond to the request
		return returnobject(environ,start_response)


	#return the app function if the object itself is called in the server
	def __call__(self,environ,start_response):
		return self.app(environ,start_response)

	#run the application without reload support
	def run(self,host='localhost',port=8000):
		server=make_server(host,port,self.app)
		print "now serving on %s:%s"%(str(host),str(port))
		server.serve_forever()