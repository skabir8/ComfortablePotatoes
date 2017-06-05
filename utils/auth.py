import hashlib, sqlite3, string

def addUser(username, password):
    if (special(username)):
        return "invalid character in username"
    if (len(password)<8):
        return "password too short"
    db=sqlite3.connect('data/users.db')
    c=db.cursor()
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    q='SELECT username FROM users'
    c.execute(q)
    userInfo=c.fetchall()
    for data in userInfo:
        if (username == data[0]):
            db.close()
            return "ERROR: username already in use"
    q="SELECT userID FROM users"
    c.execute(q)
    listIDs=c.fetchall()
    print listIDs
    if not listIDs:
        newID=0
    else:
        newID=listIDs[-1][0] + 1
    q="INSERT INTO users VALUES ("+str(newID)+",\""+username+"\", \""+myHashObj.hexdigest()+"\",0,NULL,NULL)"
    c.execute(q)
    db.commit()
    db.close()
    return "registration succesful, enter user and pass to login"
    
def userLogin(user, password):
    db=sqlite3.connect('data/users.db')
    c=db.cursor()
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    q='SELECT username FROM users'
    c.execute(q)
    data=c.fetchall()
    for stuff in data:
        if (user == stuff[0]):
            q='SELECT password FROM users WHERE username = "'+user+'";'
            c.execute(q)
            password=c.fetchall()
            q='SELECT username From users WHERE username = "'+user+'";'
            c.execute(q)
            userID=c.fetchall()
            db.close()
            if(myHashObj.hexdigest()==password[0][0]):
                return ['True', stuff[0]]
    db.close()
    return ['False', 'bad user/pass']

def special(user):
    return any((ord(char)<48 or (ord(char)>57 and ord(char)<65) or (ord(char)>90 and ord(char)<97) or ord(char)>123) for char in user)
