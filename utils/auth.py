import hashlib, string
from pymongo import MongoClient

server = MongoClient("149.89.150.100")
db = server.ComfortablePotatoes
u = db.users

def addUser(user, password):
    if (special(user)):
        return "invlaid character in username"
    if (len(password)<8):
        return "password too short"
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    cursor = u.find()
    listUsernames = []
    for dic in cursor:
        listUsernames.append( dic["username"] )
    for data in listUsernames:
        if user == data:
            db.close()
            return "ERROR: username already in use"
    newUser = {"username":user, "password":myHashObj.hexdigest()}
    u.insert_one( newUser )
    return "registration succesful, enter user and pass to login"

def userLogin(user, password):
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    if u.find_one({"$and":[{"username":user}, {"password":myHashObj.hexdigest()}]}) == None:
        return ['False', 'bad user/pass']
    return ['True', str(stuff[0][0])]

def special(user):
    return any((ord(char)<48 or (ord(char)>57 and ord(char)<65) or (ord(char)>90 and ord(char)<97) or ord(char)>123) for char in user)

