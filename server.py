import sys,os
from time import time
import importlib
from wsgiref.simple_server import make_server
import re





if(len(sys.argv)<2):
	print 'not enough arguments'
	print 'usage : server.py filename\n (Sciptus object name must be app)'
	exit()
filename=sys.argv[1]
modname=re.match(r'^(.+)\..+',sys.argv[1]).group(1)
mod=importlib.import_module(modname)
mtime=os.path.getmtime(filename)
past=int(time())


def tick():
	global past
	now=int(time())
	if(now-past>=1):
		past=now
		return True
	return False


server=make_server('localhost',8000,mod.app)



while(True):
	if(tick() and int(os.path.getmtime(filename)) != int(mtime)):
		mtime=int(os.path.getmtime(filename))
		reload(mod)
		print 'reloaded'
		del server
		server=make_server('localhost',8000,mod.app)
	server.handle_request()