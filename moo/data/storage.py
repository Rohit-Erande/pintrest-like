"""
Storage interface
"""

import time
import couchdb.client

class Storage(object):

   def insertPin(self,user_id,bname,pname,pdesc,image):
        print "Inside insert pin"
        couch = couchdb.Server()
        mydb = couch['pinsdb']

        # Code to read the image and save it into the database
        #f = open(image)
        doc = {'user_id':user_id,'boardName':bname,'pinName':pname,'pinDescription':pdesc,'image':image}
        # doc_id,doc_rev = mydb.save(doc)
        # print doc_rev, doc_id
        # f = open(image)
        # mydb.put_attachment(doc,f,image)
        doc_id,doc_rev = mydb.save(doc)
        db_id= mydb[doc_id].id
        return db_id


   def deletePin(self, user_id, bName,pId):
        couch = couchdb.Server()
        mydb = couch['pinsdb']
        del mydb[pId]
        if pId in mydb:
            doc = mydb[pId]
            print doc
            comments = doc.get("comment")
            print comments.get("userId")
            if comments.get("userId") == user_id:
                print comments.get("userId")


   def __init__(self):
      # initialize our storage, data is a placeholder
      self.data = {}

      # for demo
      self.data['created'] = time.ctime()

   def insert(self,name,value):
      print "---> insert:",name,value
      try:
         self.data[name] = value
         return "added"
      except:
         return "error: data not added"

# Method for creating Db object to be used globally
   def getDB(self):
       global couch
       couch = couchdb.Server()
       #couch = couchdb
       global mydb
       #mydb = couch['userdb']
       return None

# This is a storage function used for storing details of new user registered

   def insertUser(self, Fname, Lname,emailId,password):
       couch = couchdb.Server()
       mydb = couch['userdb']
       print Fname
       doc_id,doc_rev = mydb.save({'Fname':Fname,'Lname':Lname,'emailID':emailId,'password':password})
       print doc_id
       dbid= mydb[doc_id].id
       print dbid
       return dbid

# This is a function to get the name of the board created by the user that has logged in
   def getBoardNames(self,user_id):
        L= list()
        couch = couchdb.Server()
        mydb = couch['boards']
        for row in mydb:
            uID = mydb[row].get("user_id")
            if user_id == uID:
                doc  = mydb[row].get("boardName")
                L.append(doc)
                return L

# Function created which retrieves board Id when board name is sent by user
   def getBoardId(self,bName):
        couch = couchdb.Server()
        myboardDB = couch['boards']
        for row in myboardDB:
            b = myboardDB[row].get("boardName")
            if b == bName:
                bId=myboardDB[row].get("_id")
                return bId

#Function to update board for the user that has logged in

   def updateBoard(self, user_id, bName, bname, bdesc, bcategory, bType):
        couch = couchdb.Server()
        mydb = couch['boards']
        print bname
        doc = mydb[bName]
        doc['boardName'] = bname
        doc['boardDescription'] = bdesc
        doc['boardCategory'] = bcategory
        doc['boardType'] = bType
        mydb[bName] = doc
        return bName

#Function to delete board for the user that has logged in

   def deleteBoard(self, user_id, bId):
        couch = couchdb.Server()
        mydb = couch['boards']
        del mydb[bId]

# Function to fetch pins of the specific user of a particular board id selected by the user
   def viewAllPins(self,userId,boardId):
        couch = couchdb.Server()
        mydb = couch['pinsdb']
        L=list()
        for row in mydb:
            uID = mydb[row].get("user_id")
            bId  = mydb[row].get("boardName")
            if userId == uID:
                if bId==boardId:
                    doc  = mydb[row].get("pinName")
                    L.append(doc)
                    return L

   def viewPin(self,userId,boardId,pinId):
       couch = couchdb.Server()
       mydb = couch['pinsdb']
       doc=mydb[pinId]
       #doc.update()
       #doc = mydb.get_attachment(pinId,"DSC01341.jpg")
       return doc

# Function to insert details of Board
   def insertBoard(self, user_id,bname,bdesc ,bcategory,bType ):
       couch = couchdb.Server()
       mydb = couch['boards']
       print bname
       doc_id,doc_rev = mydb.save({'user_id':user_id,'boardName':bname,'boardDescription':bdesc,'boardCategory':bcategory,'boardType':bType})
       db_id= mydb[doc_id].id
       return db_id


    # region Description

# Function to view details of a Board created by the user that has logged in
   def viewBoard(self,bId):
       couch = couchdb.Server()
       mydb = couch['boards']
       doc=mydb[bId]
       return doc

 # Function to update Pin of board that has been created by the logged in user
   def updatePin(self, user_id,boardId, pinId,pname, pdesc,image):
        couch = couchdb.Server()
        mydb = couch['pinsdb']
        doc = mydb[pinId]
        doc['pinName'] = pname
        doc['pinDesc'] = pdesc
        doc['image'] = image

        # # Code to read the image and save it into the database
        # f = open(image)
        # doc = {'user_id':user_id,'boardName':bname,'pinName':pname,'pinDescription':pdesc,'image':f.name}
        # doc_id,doc_rev = mydb.save(doc)
        # print doc_rev, doc_id
        # f = open(image)
        # mydb.put_attachment(doc,f,image)
        # db_id= mydb[doc_id].id


        mydb[pinId] = doc
        return pinId

    # Function to create comment by user on pins
   def createComment(self, user_id,boardId, pinId,comment):
        couch = couchdb.Server()
        mydb = couch['pinsdb']
        doc = mydb[pinId]
        comments = {"description":comment,"userId":user_id}
        doc['comment'] = [comments]
        mydb[pinId]=doc
        return pinId




     #function to delete a comment
   def deleteComment(self, user_id,boardId, pinId):
        couch = couchdb.Server()
        mydb = couch['pinsdb']
        commentDoc=list()
        if pinId in mydb:
            doc = mydb[pinId]
            if doc.userId == user_id:
                print "yes"
            #
            # map_fun = '''function(doc) {
            #      if (doc.userId == user_id)
            #         emit(doc.comment, null);
            #         }'''
            # for row in mydb.query(map_fun):
            #   print row.key
            #
            #
            # for i in doc:
            #     print doc.get("userId")


            # if user_id in commentDoc:
            #     comment = commentDoc["userId"]
            #     print comment

# def remove(self,name):
#print "---> remove:",name
#
#    def names(self):
#       print "---> names:"
#       for k in self.data.iterkeys():
#         print 'key:',k
#
#    def find(self,name):
#       print "---> storage.find:",name
#       if name in self.data:
#          rtn = self.data[name]
#          print "---> storage.find: got value",rtn
#          return rtn
#       else:
#          return None
# endregion
