import sys,os
from time import time
import importlib
from wsgiref.simple_server import make_server
import re




#make sure the user gives at least one argument (filename)
if(len(sys.argv)<2):
	print 'not enough arguments'
	print 'usage : server.py filename objectname(optional)\n (default object name is app)'
	exit()

#set the name of the object or function that will be passed to the make_server function
#or take it from the user if one is supplied
objectname='app'
if(len(sys.argv)==3):
	objectname=sys.argv[2]


#extract the module name from the filename and then load the module
filename=sys.argv[1]
modname=re.match(r'^(.+)\..+',sys.argv[1]).group(1)
mod=importlib.import_module(modname)

#get the object or function from that module
app=getattr(mod,objectname)

"""reloading works as follows:
	
	1-the tick function returns True each time a second has passed , so there's a past variable that's initiated with the current time
	the loop checks if 1 second has passed by comparing (now) with previously set (past) , and if so it resets past to the current time and return True
	and the loop goes on

	2-mtime is the modification time of the file , it's compared with each tick() to see if the file has been modified
	if so , the module is reloaded """

mtime=os.path.getmtime(filename)
past=int(time())


def tick():
	global past
	now=int(time())
	if(now-past>=1):
		past=now
		return True
	return False

port=8000
server=make_server('localhost',port,app)


#each second or tick() , file modification date is checked
#if the file was updated , the mtime variable is then updated and reload() is called to reload the module and app variable is updated
#then the server variable is updated with the new and asked to wait for another request
print "now serving on localhost:%d"%port
while(True):
	if(tick() and int(os.path.getmtime(filename)) != int(mtime)):
		
		mtime=int(os.path.getmtime(filename))
		reload(mod)
		
		del app
		app=getattr(mod,objectname)

		del server
		server=make_server('localhost',port,app)

		print 'reloaded'
		continue
	server.handle_request()