

import requests

server=raw_input("Please enter the server to which u want to connect: ")
port=raw_input("please enter the port number: ")

choice = int(raw_input("Enter your choice: 1. SignUp , 2. Login,  3. Create Board, 4. List Board names , 5.Create Pin "
                       "6. List Pins, 7. Update Board,  8.Delete Board,  9.Update Pin,  10. Delete Pin, 11. List Details of a Board"
					   "12. List Details of a Pin, 13. Create a Comment, 14. Delete a Comment"))
print choice

if choice == 1:
  fname = raw_input("Enter your First Name: ")
  lname = raw_input("Enter your Last Name: ")
  emailId = raw_input("Enter Email Id :")
  password = raw_input("Enter Password :")
  url = 'http://'+server+':'+port+'/users/signUp'
  payload={'fname':fname,'lname':lname,'emailId':emailId,'password':password}
  response=requests.post('http://'+server+':'+port+'/users/signUp',data=payload)
  print response
elif choice == 2:
  uname=raw_input("enter your email Id ")
  password=raw_input("enter password ")
  name=uname
  value=password
  payload={'emailId':name,'password':value}
  response=requests.post('http://'+server+':'+port+'/users/login',data=payload)
  print response
 
elif choice == 3:
  userid= raw_input("Enter your user id")
  boardName = raw_input("Enter the board Name : ")
  boardDesc = raw_input("Enter the board Desc : ")
  category = raw_input("Enter the category : ")
  url='http://'+server+':'+port+'/users/'+userid+'/boards'
  payload={'boardName':boardName,'boardDesc':boardDesc,'category':category,'isPrivate':'false'}
  response=requests.put('http://'+server+':'+port+'/users/'+userid+'/boards',data=payload)
  print response
  
elif choice == 4:
  userid = raw_input("Enter your user id")
  response=requests.get('http://'+server+':'+port+'/users/'+userid+'/boards')
  print response.content
elif choice == 5:
  userid = raw_input("Enter your user id")
  boardname= raw_input("Enter your board name")
  pname = raw_input("Enter pin name")
  pdesc = raw_input("Enter pin desc")
  image = raw_input("Enter image url")
  payload = {'pinName':pname,'pinDesc':pdesc,'image':image}
  response= requests.post('http://'+server+':'+port+'/users/'+userid+'/boards/'+boardname+'/pins',data=payload)
  print response
elif choice == 6:
  userid = raw_input("Enter your user id")
  name = raw_input("Enter your board name")
  response=requests.get('http://'+server+':'+port+'/users/'+userid+'/boards/'+name+'/pins')
  print response.content

  
elif choice == 7:
  uid = raw_input("Enter your user id ")
  boardId= raw_input("Enter the board name ")
  boardName = raw_input("Enter the updated board Name : ")
  boardDesc = raw_input("Enter the board Desc : ")
  category = raw_input("Enter the category : ")
  payload={'name':boardName,'boardDesc':boardDesc,'category':category,'isPrivate':'false'}
  response=requests.put('http://'+server+':'+port+'/users/'+uid+'/boards/'+boardId,data=payload)
  print response
    
  
elif choice == 8:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the board name ")
  response=requests.delete('http://'+server+':'+port+'/users/'+uid+'/boards/'+name)
  print response

elif choice == 9:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the boardname ")
  pin = raw_input ("Enter your pin Id ")
  pname = raw_input("Enter pin name")
  pdesc = raw_input("Enter pin desc")
  image = raw_input("Enter image url")
  payload={'pinName':pname,'pinDesc':pdesc,'image':image}
  response=requests.put('http://'+server+':'+port+'/users/'+uid+'/boards/'+name+'/pins/'+pin,data=payload)
  print response


elif choice == 10:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the boardname ")
  pin = raw_input("Enter pin id")
  response=requests.delete('http://'+server+':'+port+'/users/'+uid+'/boards/'+name+'/pins/'+pin)
  print response 

elif choice == 11:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the board id ")
  response=requests.get('http://'+server+':'+port+'/users/'+uid+'/boardDetails/'+name)
  print response.content 
  
elif choice == 12:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the boardname ")
  pin = raw_input("Enter the pin id ")
  response=requests.get('http://'+server+':'+port+'/users/'+uid+'/boards/'+name+'/pins/'+pin)
  print response.content 
    
elif choice == 13:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the board Id ")
  pin = raw_input("Enter the pin id ")
  comment = raw_input("Enter your comment ")
  payload={'description':comment}
  response=requests.put('http://'+server+':'+port+'/users/'+uid+'/boards/'+name+'/pins/'+pin+'/comment',data=payload)
  print response 

elif choice == 14:
  uid = raw_input("Enter your user id ")
  name = raw_input("Enter the board id ")
  pin = raw_input("Enter the pin id ")
  response=requests.delete('http://'+server+':'+port+'/users/'+uid+'/boards/'+name+'/pins/'+pin+'/comment')
  print response 
