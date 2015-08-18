#Scriptus is a python micro-framework aimed at easing basic web development tasks in python , inspired by werkzeug

from wsgiref.simple_server import make_server
import re
from wrappers import Request,Response
from Cookie import SimpleCookie
import pickle,os


class Scriptus(object):
	def __init__(self):
		self.routes={}
		self.session=None


	def __call__(self,environ,start_response):
		return self.app(environ,start_response)

	#defines a new route
	def route(self,address,function):
		self.routes[address]=function

	#searches for the path in defined routes 
	def checkRoute(self,request):
		
		#checks routes one by one for the request's path
		#returns the return of route's function or None if no match was found
		for route in self.routes.keys():
			match=re.match(route,request.path)
			if( match is not None):
				urlargs=match.groups()
				return self.routes[route](request,*urlargs)
		return None

	def getcookie(self,name,default=''):
		try:
			c=SimpleCookie()
			c.load(self.environ['HTTP_COOKIE'])
			return str(c[name].value)
		except KeyError:
			return default


	#main function that processes requests from server
	def app(self,environ,start_response):
	
		self.environ=environ
		#create request object from environ
		request=Request(environ)
		
		#get the response object from the function and if create one if the function doesn't return a response
		returnobject=self.checkRoute(request)

		if returnobject is None:
			returnobject=Response('Not Found',status=404)
		if type(returnobject) is not Response:
			returnobject=Response(str(returnobject))


		return returnobject(environ,start_response)

		
	def run(self,host='localhost',port=8000):
		server=make_server(host,port,self.app)
		print "now serving on %s:%s"%(str(host),str(port))
		server.serve_forever()