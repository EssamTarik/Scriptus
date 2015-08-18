from Cookie import SimpleCookie
from cgi import FieldStorage
import urlparse
import os
class File(object):
	def __init__(self,fileobject):
		self.fileobject=fileobject
		self.name=fileobject.filename

	def read(self):
		return self.fileobject.value

	def save(self,path=''):
		if(not os.path.exists(path)):
			os.mkdir(path)
		output=open(os.path.join(path,self.name),'wb')
		output.write(self.read())
		output.close()


class POST(object):
	def __init__(self,fields={}):
		self.fields=fields

	def __getitem__(self,key):
		return self.fields[key].value

	def file(self,name):
		return File(self.fields[name])




class Request(object):
	def __init__(self,environ):
		self.method=environ['REQUEST_METHOD']
		self.path=environ.get('PATH_INFO','/')
		self.environ=environ
		self.GET=urlparse.parse_qs(environ['QUERY_STRING'])
		for key in self.GET.keys():
			self.GET[key]=self.GET[key][0]
		if self.method=='POST' :
			self.POST=FieldStorage(fp=self.environ['wsgi.input'],environ=self.environ,keep_blank_values=True)
			self.POST=POST(self.POST)


class Response(object):


	
	def __init__(self,text="",status="200 Ok",headers={'Content-Type':'text/html'},redirect=False):
		self.cookies=SimpleCookie()
		statusCodes={
		'200':'200 Ok',
		'404':'404 Not Found'
		}
		self.text=text
		self.headers=headers
		self.status=statusCodes.get(str(status),str(status))
		self.headers=headers
		if(redirect != False):
			self.status='302 Found'
			headers.append(('Location',str(redirect)))

		


	def removecookie(self,name):
		self.cookies[name]=None
		self.cookies[name]['expires']=-1

	def setcookie(self,name,value,expires=None):
		self.cookies[str(name)]=str(value)
		self.cookies[name]['path']='/'
		if expires is not None:
			self.cookies[name]['expires']=int(expires)

	def __call__(self,environ,start_response):
		
		self.headers['Content-Length']=str(len(self.text))
		print str(self.cookies)
		self.headers['Set-Cookie']=self.cookies.output()[11:]
		self.headers=[(x,self.headers[x]) for x in self.headers.keys()]
		print self.headers
		start_response(self.status,self.headers)
		return [self.text]