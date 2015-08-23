from Cookie import SimpleCookie
from cgi import FieldStorage
import urlparse
import os
import session

#File class , used to wrap file fields sent from POST objects
class File(object):

	#fileobject is received from the POST object
	def __init__(self,fileobject):
		self.fileobject=fileobject
		self.name=fileobject.filename

	#returns the contents of the file
	def read(self):
		return self.fileobject.value

	#saves the file to 'path'
	def save(self,path=''):
		#creates the path if it doesnt exist
		if(not os.path.exists(path)):
			os.mkdir(path)

		#write the contents to a file
		output=open(os.path.join(path,self.name),'wb')
		output.write(self.read())
		output.close()

#POST class , wraps data sent over a POST request,used by Request objects 
class POST(object):

	#fields are received from the Request object
	def __init__(self,fields={}):
		self.fields=fields

	#it's easire to use the POST object as a dict
	def __getitem__(self,key):
		return self.fields[key].value

	#returns a File object based on its field's name
	def file(self,name):
		return File(self.fields[name])



#a Request object is passed to each route function
class Request(object):
	def __init__(self,environ):
		#set request method,path and environ from the environ dict
		self.method=environ['REQUEST_METHOD']
		self.path=environ.get('PATH_INFO','/')
		self.environ=environ

		#parse GET query_string
		self.GET=urlparse.parse_qs(environ['QUERY_STRING'])
		#parse_qs returns a list dict containing {key:[value]}
		#this loop turns it into {key:value}
		for key in self.GET.keys():
			self.GET[key]=self.GET[key][0]

		#parses the data of a POST request
		if self.method=='POST' :
			self.POST=FieldStorage(fp=self.environ['wsgi.input'],environ=self.environ,keep_blank_values=True)
			self.POST=POST(self.POST)

	#reads cookies from environ's HTTP_COOKIE
	#a KeyError is raised if either HTTP_COOKIE or the required cookie doesnt exist , default is returned in either case
	def getcookie(self,key,default=''):
		try:
			#load the cookies from the environ dict's HTTP_COOKIE
			c=SimpleCookie()
			c.load(self.environ['HTTP_COOKIE'])

			#return the value of the cookie
			return str(c[key].value)
		
		except KeyError:
			return default


#Response class handles cookie setting/removing and returns headers and text to the server
class Response(object):


	
	def __init__(self,text="",status="200 Ok",headers={'Content-Type':'text/html'},redirect=False,session=False):
		#initiate cookies with an empty SimpleCookie object
		self.cookies=SimpleCookie()

		#initiates the status code
		statusCodes={
		'200':'200 Ok',
		'404':'404 Not Found'
		}
		self.status=statusCodes.get(str(status),str(status))

		#initiates the object's session , default is False
		self.session=session

		#text to be returned
		self.text=text

		#initiate the response headers and add a Location header if there's a redirect
		self.headers=headers

		#set the proper status code and add a Location header in case of a redirect
		if(redirect != False):
			self.status='302 Found'
			headers['Location']=str(redirect)


	#removes cookies by setting them to None and an expired expiration time
	def removecookie(self,name):
		self.cookies[name]=None
		self.cookies[name]['expires']=-1
		self.cookies[name]['path']='/'

	#adds a new cookie to the object's cookies property
	def setcookie(self,name,value,expires=None):
		self.cookies[str(name)]=str(value)

		#adds cookie expiration time if specified
		if expires is not None:
			self.cookies[str(name)]['expires']=int(expires)
		
		#adds cookie's path property
		self.cookies[str(name)]['path']='/'

	#the Response object is called after all work in both the object and the Scriptus object's app function is done
	def __call__(self,environ,start_response):

		#starts a session if a session dict is assigned to the object's session property
		if self.session is not False:

			#only dict objects are accepted
			if type(self.session) is dict:

				#sets the sid(session id) cookie
				self.setcookie('sid',session.startsession(self.session))
			
			else:
				#raised if the session variable is not a dict
				raise TypeError('session takes a dict as an argument')

		#sets the Content-Length header
		self.headers['Content-Length']=str(len(self.text))

		#sets the Set-Cookie header , the first 11 letters of SimpleCookie.output() are ignored as they're 'Set-Cookie:'
		self.headers['Set-Cookie']=self.cookies.output()[11:]
		#puts the headers in a list of (key,value) pairs
		self.headers=[(x,self.headers[x]) for x in self.headers.keys()]
		
		#optional , i put it for debugging purposes of my own
		print self.headers

		#answer back to the server
		start_response(self.status,self.headers)
		return [self.text]