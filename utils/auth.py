import hashlib, sqlite3, string


def addUser(user, password):
    if (special(user)):
        return "invlaid character in username"
    if (len(password)<8):
        return "password too short"
    db=sqlite3.connect('data/tables.db')
    c=db.cursor()
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    q='SELECT * FROM users'
    c.execute(q)
    userInfo=c.fetchall()
    for data in userInfo:
        if (user in data):
            db.close()
            return "ERROR: username already in use"
    q="INSERT INTO users VALUES (NULL, \""+user+'\", \"'+myHashObj.hexdigest()+'\")'
    print q
    c.execute(q)
    db.commit()
    db.close()
    return "registration succesful, enter user and pass to login"

def userLogin(user, password):
    db=sqlite3.connect('data/tables.db')
    c=db.cursor()
    myHashObj=hashlib.sha1()
    myHashObj.update(password)
    q='SELECT username FROM users'
    print "hi"
    c.execute(q)
    data=c.fetchall()
    for stuff in data:
        if(user in stuff):
            print "bye"
            q='SELECT password FROM users WHERE username = "'+user+'";'
            c.execute(q)
            password=c.fetchall()
            q='SELECT userID From users WHERE username = "'+user+'";'
            c.execute(q)
            stuff=c.fetchall()
            db.close()
            if(myHashObj.hexdigest()==password[0][0]):
                return ['True', str(stuff[0][0])]
    db.close()
    return ['False', 'bad user/pass']

def special(user):
    return any((ord(char)<48 or (ord(char)>57 and ord(char)<65) or (ord(char)>90 and ord(char)<97) or ord(char)>123) for char in user)
