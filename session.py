import pickle
from Cookie import SimpleCookie
import sha,base64,os

sessiondir='sessions'


class sessionerror(Exception):
	def __init__(self,msg):
		self.msg=msg
	def __str__(self):
		return self.msg

	
def gensid():
	return str(sha.new(base64.b64encode(os.urandom(16))).hexdigest())



def startsession(sessiondata={}):	
	sid=gensid()
	sessiondata['sid']=sid
	if(not os.path.exists(sessiondir)):
		os.mkdir(sessiondir)
	fileobj=open(os.path.join(sessiondir,sid),'w+')

	pickle.dump(sessiondata,fileobj)
	fileobj.close()
	return sid

def set(key,val,request):
	try:
		c=SimpleCookie(request.environ['HTTP_COOKIE'])
		fileobj=open(os.path.join('sessions',c['sid'].value),'r+')
		dataobj=pickle.load(fileobj)
		dataobj[key]=val
		fileobj.seek(0,0)
		pickle.dump(dataobj,fileobj)
		fileobj.close()
	except KeyError:
		raise sessionerror('wrong cookies')


def get(key,request):
	try:
		c=SimpleCookie(request.environ['HTTP_COOKIE'])
		fileobj=open(os.path.join('sessions',c['sid'].value),'r+')
		dataobj=pickle.load(fileobj)
		fileobj.close()
		return dataobj.get(key,'')
	except KeyError:
		raise sessionerror('wrong cookies')
	except IOError:
		raise sessionerror('session not found')