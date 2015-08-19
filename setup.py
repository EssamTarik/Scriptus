import shutil,os

Sdir='Scriptus'
if not os.path.exists(Sdir):
	os.mkdir(Sdir)
tomove=['__init__.py','session.py','wrappers.py']
toremove=['__init__.pyc','session.pyc','wrappers.pyc']

for f in tomove:
	try:
		shutil.move(f,os.path.join(Sdir,f))
	except IOError,error:
		print str(error)
	except OSError,error:
		print str(error)
		

for f in toremove:
	try:
		os.remove(f)
	except IOError,error:
		print str(error)
	except OSError,error:
		print str(error)
		

print 'setup complete'