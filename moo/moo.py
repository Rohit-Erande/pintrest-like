"""
6, Apr 2013

Example bottle (python) RESTful web service.

This example provides a basic setup of a RESTful service

Notes
1. example should perform better content negotiation. A solution is
   to use minerender (https://github.com/martinblech/mimerender)
"""

import time
import sys
import socket
import json
import couchdb

# bottle framework
from bottle import request, response, route, run, template

# moo
from classroom import Room
from data.storage import Storage
# virtual classroom implementation
room = None

def setup(base,conf_fn):
   print '\n**** service initialization ****\n'
   global room
   room = Room(base,conf_fn)


#
# setup the configuration for our service
@route('/')
def root():
   print "--> root"
   return 'welcome'

#
#
@route('/moo/ping', method='GET')
def ping():
   return 'ping %s - %s' % (socket.gethostname(),time.ctime())

#
# Development only: echo the configuration of the virtual classroom.
#
# Testing using curl:
# curl -i -H "Accept: application/json" http://localhost:8080/moo/conf
#
# WARN: This method should be disabled or password protected - dev only!
#
@route('/moo/conf', method='GET')
def conf():
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   return room.dump_conf(fmt)

#
# example of a RESTful method. This example is very basic, it does not 
# support much in the way of content negotiation.
#
@route('/moo/echo/:msg')
def echo(msg):
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   if fmt == Room.html:
      return '<h1>%s</h1>' % msg
   elif fmt == Room.json:
      rsp = {}
      rsp["msg"] = msg
      return json.dumps(all)
   else:
      return msg


#
# example of a RESTful query
#
@route('/moo/data/:name', method='GET')
def find(name):
   print '---> moo.find:',name
   return room.find(name)

#
# example adding data using forms
#
@route('/moo/data', method='POST')
def add():
   print '---> moo.add'

   # example list form values
   for k,v in request.forms.allitems():
      print "form:",k,"=",v

   name = request.forms.get('name')
   value = request.forms.get('value')
   return room.add(name,value)

#
# Sign-up functionality
#   
@route('/users/signUp',method='POST')
def signUp():
	print '---> moo.signUp'

    	Fname = request.POST.get('fname')
        Lname = request.POST.get('lname')
        emailId = request.POST.get('emailId')
        password = request.POST.get('password')
        global storage
        storage = Storage()
        user_id=storage.insertUser(Fname,Lname, emailId,password)
        return user_id

# function to login
@route('/moo/users/login', method='POST')
def login():
   print '---> moo.login'
   # example list form values
   for k,v in request.forms.allitems():
      print "form:",k,"=",v
   global couchdb
   name = request.POST.get('name')
   value = request.POST.get('value')
   print "name ",name
   print "value ",value
   couch=couchdb.Server()
   global userdb
   userdb=couch['userdb']
   for i in userdb:
        if userdb[i].get('Fname') == name and userdb[i].get('password') == value :
            print "value found now returning success"
            return "success "
   return "false"


#create board

@route('/users/:userId/boards',method ='POST')
def createBoard(userId):
    couch = couchdb.Server()
    myUserdb = couch['userdb']
    print myUserdb

    if userId in myUserdb:
        bname=request.POST.get('boardName')
        bdesc = request.POST.get('boardDesc')
        category=request.POST.get('category')
        boardType=request.POST.get('isPrivate')

        global storage
        storage = Storage()
        boardId = storage.insertBoard(userId,bname,bdesc,category,boardType)
        return boardId
    else:
        return "User not Authorized!"

#
# Get list of Board names for the user that has logged in
#
#def getList
@route('/users/:userId/boards',method ='GET')
def getBoardList(userId):
    print '--in moo.getBoardList'
    L = list()
    couch = couchdb.Server()
    print "id is ----",userId
    myUserdb = couch['userdb']
    if userId in myUserdb:
        storage = Storage()
        L = storage.getBoardNames(userId)
        return L
    else:
        return "User Id does not exist!"
#
# Get Board names for the user that has logged in
#
#def getList
@route('/users/:userId/boardDetails/:boardName',method ='GET')
def getBoardDetails(userId,boardName):
    print '--in moo.getBoardList'

    couch = couchdb.Server()
    myUserdb = couch['userdb']
    myboardDB = couch['boards']
    storage = Storage()
    bId = storage.getBoardId(boardName)

    if userId in myUserdb:
         if bId in myboardDB:
             doc = storage.viewBoard(bId)
             return doc
         else:
             return "Board Id does not exist"
    else:
        return "User not Authorized!"



# update board of the user logged in

@route('/users/:userId/boards/:boardName', method='PUT')
def updateBoard(userId,boardName):
    print '--in moo.createBoard'
    global storage
    storage = Storage()
    couch = couchdb.Server()
    mydb = couch['userdb']
    myboardDB = couch['boards']
    bId = storage.getBoardId(boardName)
    if userId in mydb:
        if bId in myboardDB:
            bname = request.POST.get('name')
            bdesc = request.POST.get('boardDesc')
            category = request.POST.get('category')
            boardType = request.POST.get('isPrivate')

            boardId = storage.updateBoard(userId,bId, bname, bdesc, category, boardType)
            return boardId
        else:
            return "Board not Authorized!"
    else:
        return "User not authorized"




# delete board

@route('/users/:userId/boards/:boardName', method='DELETE')
def deleteBoard(userId,boardName):
    print '--in moo.deleteBoard'
    couch = couchdb.Server()
    mydb = couch['userdb']
    myboardDB = couch['boards']
    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)

    if userId in mydb:
        if bId in myboardDB:
            boardId = storage.deleteBoard(userId,bId)
        else:
            return "Board not Authorized!"
    else:
        return "User not authorized"


#create pin for the user that has logged in

@route('/users/:userId/boards/:boardName/pins',method='POST')
def createPin(userId,boardName):
    print '--in moo.createBoard'
    print "id", userId

    couch = couchdb.Server()
    mydb = couch['userdb']
    board = couch['boards']
    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)
    if userId in mydb:
        if bId in board:
            pname=request.POST.get('pinName')
            pdesc = request.POST.get('pinDesc')
            image=request.POST.get('image')
            pinId = storage.insertPin(userId,boardName,pname,pdesc,image)
            return pinId
        else:
            return "Board not found!"

    else:
        return "User not Found!"


#view all pins

@route('/users/:userId/boards/:boardName/pins',method='GET')
def viewAllPin(userId,boardName):
    print
    '--in moo.viewAllPins'
    couch = couchdb.Server()

    board = couch['boards']
    myUserdb = couch['userdb']
    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)

    if id in myUserdb:
        if bId in board:
            doc=storage.viewAllPins(id,bId)
            return doc
        else:
            return "Board Id not Found!"
    else:
        return "User Id Not Found!"

#view a pin based on its name

@route('/users/:userId/boards/:boardName/pins/:pinId', method='GET')
def viewPin(userId,boardName,pinId):
    print
    '--in moo.viewAllPins'

    couch = couchdb.Server()
    mydb = couch['userdb']
    board = couch['boards']
    pins = couch['pinsdb']

    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)

    if userId in mydb:
        if bId in board:
            if pinId in pins:
                doc=storage.viewPin(userId,bId,pinId)
                return doc
            else:
                return "Pin not found!"
        else:
            return "Board not Found!"
    else:
        return "User Not Found!"

#delete a pin
@route('/users/:userId/boards/:boardName/pins/:pinId', method='DELETE')
def deletePin(userId,boardName,pinId):
    print
    '--in moo.viewAllPins'

    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)

    couch = couchdb.Server()
    mydb = couch['userdb']
    board = couch['boards']
    pin = couch['pinsdb']
    if userId in mydb:
        if bId in board:
            if pinId in pin:
               global storage
               storage = Storage()
               storage.deletePin(userId,bId,pinId)
            else:
                return "Pin not found!"
        else:
            return "Board not Found!"
    else:
        return "User Not Found!"


#update a pin
@route('/users/:userId/boards/:boardName/pins/:pinId', method='PUT')
def updatePin(userId,boardName,pinId):

    couch = couchdb.Server()
    mydb = couch['userdb']
    board = couch['boards']
    pin=couch['pinsdb']
    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)

    if userId in mydb:
        if bId in board:
            if pinId in pin:
                pname = request.POST.get('pinName')
                pdesc = request.POST.get('pinDesc')
                image = request.POST.get('image')

                boardId = storage.updatePin(userId,bId, pinId,pname, pdesc,image )
                return boardId
            else:
                return "Invalid Pin Id!"
        else:
            return "Invalid Board Id!"
    else:
        return "User not authorized"


#create comment

@route('/users/:userId/boards/:boardName/pins/:pinId/comment',method='PUT')
def createComment(userId,boardName,pinId):
    print
    '--in moo.createBoard'
    couch = couchdb.Server()
    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)
    mydb = couch['userdb']
    board = couch['boards']
    pins= couch ['pinsdb']
    if userId in mydb:
        if bId in board:
            if pinId in pins:
                description=request.POST.get('description')
                global storage
                storage = Storage()
                pinId = storage.createComment(userId,bId,pinId,description)
                return pinId
            else:
                return "Pin not found!"

        else:
            return "Board not Found!"
    else:
        return "User Not Authorized!"

#delete comment

@route('/users/:userId/boards/:boardName/pins/:pinId/comment',method='DELETE')
def deleteComment(userId,boardName,pinId):
    print
    '--in moo.deleteComment'
    global storage
    storage = Storage()
    bId = storage.getBoardId(boardName)
    couch = couchdb.Server()
    mydb = couch['userdb']
    board = couch['boards']
    pins= couch ['pinsdb']
    if userId in mydb:
        if bId in board:
            if pinId in pins:

               # desc=request.POST.get('description')

                #print desc
                global storage
                storage = Storage()
                pinId = storage.deleteComment(userId,bId,pinId)
                return pinId
            else:
                return "Pin not found!"

        else:
            return "Board not Found!"
    else:
        return "User Not Authorized!"

#
# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
def __format(request):
   #for key in sorted(request.headers.iterkeys()):
   #   print "%s=%s" % (key, request.headers[key])

   types = request.headers.get("Accept",'')
   subtypes = types.split(",")
   for st in subtypes:
      sst = st.split(';')
      if sst[0] == "text/html":
         return Room.html
      elif sst[0] == "text/plain":
         return Room.text
      elif sst[0] == "application/json":
         return Room.json
      elif sst[0] == "*/*":
         return Room.json

      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc

   # default
   return Room.html

#
# The content type on the reply
#
def __response_format(reqfmt):
      if reqfmt == Room.html:
         return "text/html"
      elif reqfmt == Room.text:
         return "text/plain"
      elif reqfmt == Room.json:
         return "application/json"
      else:
         return "*/*"

      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc
