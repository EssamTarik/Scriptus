from Scriptus import Scriptus
from Scriptus.wrappers import Response
from Scriptus import session

#get Scriptus object
app=Scriptus()


# a simple hello world

def helloworld(request):
	return 'hello world'

app.route(r'^/$',helloworld)

# to get variables from a url, they're sent by order
#name and age are by order ([a-z]+) and ([0-9]+)
def welcome(request,name,age):
	return 'welcome %s who is %s years old'%(name,age)

app.route(r'^/welcome/([a-z]+)/([0-9]+)/?$',welcome)


#to add a cookie
# use Response objects to set cookies
#setcookie takes name,value,expiration time(seconds)
def addcookie(request):
	response=Response()
	response.setcookie('name','user')
	response.text='cookie set'
	return response

app.route(r'^/addcookie/?$',addcookie)



#to read a cookie , second argument is returned if the cookie isn't found
def getcookie(request):
	return app.getcookie('name','no cookie')

app.route(r'^/getcookie/?$',getcookie)


#to process get request
#for example ?name=user should be read here
def readget(request):
	return request.GET['name']
app.route(r'^/readget/?$',readget)

#read post request
#this will just read the name field
def readpost(request):
	return request.POST['name']
app.route(r'^/readpost/?$',readpost)



#this will read and save a file from post request
#this function will read the myfile field
def readfile(request):
	fileobject=request.POST.file('myfile')
	#send the save directory to save()
	fileobject.save('saved_file')
	return "%s was saved"%fileobject.name

app.route(r'^/readfile/?$',readfile)

#you can use this run function or the object's app function to operate from another server
if __name__='__main__':
	app.run()