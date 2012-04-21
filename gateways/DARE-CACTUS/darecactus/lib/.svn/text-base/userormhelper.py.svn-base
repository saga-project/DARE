import darecactus.model as model
import darecactus.model.meta as meta
import time
from sqlalchemy.sql import and_, or_
import random

#contains various job manipulation techniques
    
# used to import the hash library. 
try:
    import hashlib
    hash_md5  = hashlib.md5
    hash_sha1 = hashlib.sha1
except:
    import md5
    import sha
    hash_md5 = md5.new
    hash_sha1 = sha.new

#used to encrypt the password and store int he databas#
def hash_password(password, salt):
    m = hashlib.sha256()
    m.update(password)
    m.update(salt)
    return m.hexdigest()

#this method is used to decrypt the password to compare it with encrypted password it. #todo implement it.
def gen_hash_password(password):
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    p = ''
    random.seed()
    for x in range(32):
        p += letters[random.randint(0, len(letters)-1)]
    return hash_password(password, p), p


def add_user(data):
    
    if  check_email_ifexists(data['email']):
        return "emailexists"
    newuser= model.user() 
    newuser.email = data['email']
    newuser.organization = data['organization']
    
    pass_hash, salt = gen_hash_password(data['password1'])
    newuser.password = pass_hash
    
    newuser.salt =  salt
    meta.Session.add(newuser)
    meta.Session.commit()

def check_email_ifexists(email):
    users = meta.Session.query(model.user)
    a_user = users.filter(model.user.email == str(email)).all()
    
    print "a_user.count()", len(a_user)
    
    if  len(a_user)==0:
        return False
    else:
        return True


def authenticate_user(email, password):
    users = meta.Session.query(model.user)
    try:
        user = users.filter(model.user.email == str(email)).one()
        print user.id
    except:
        print "inv pass"
        return "invalid"
    
    hash_pass = hash_password(str(password), user.salt)
    print "user_app", user.password, hash_pass 
    if (str(user.password) != str(hash_pass)):
        print "inv pass"
        return "invalid"
    
    return user.id



