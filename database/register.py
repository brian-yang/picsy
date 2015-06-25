#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========


# =================== IMPORTS ========================
import hashlib
import cgi
import cgitb
#cgitb.enable()  #diag info --- comment out once full functionality achieved


# ~~~~~~~~~~~~~~~ support functions ~~~~~~~~~~~~~~~
def FStoD():
    '''
    Converts cgi.FieldStorage() return value into a standard dictionary
    '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~ auxiliary files ~~~~~~~~~~~~~~~~~
#file to store users and their passwords:
userfile="../site_data/users.csv"

#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#login page:
loginPage="../index.html"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#store querystring var/val pairs in dictionary
fsd=FStoD()


#validate user input
def valid():
    if not ('uname' in fsd) or not ('upass1' in fsd) or not ('upass2' in fsd):
        return False
    if fsd['uname'] == '':
        return False
    if fsd['upass1'] != fsd['upass2']:
        return False
    if len(fsd['uname']) > 20:
        return False
    return True


#makes sure only alphanumeric input was used
def alphanumeric(username):
    allowed = "abcdefghijklmnopqrstuvwxyz1234567890"
    for i in username:
        if i not in allowed:
            return False
    return True


#check for existence of a user in CSV file
def userExists(u):
    try:
        userlist = open(userfile,'r').readlines()
    except:
        return False
    for row in userlist:
        if row.strip().split(',')[0]==u:
            return True
    return False


#write new entries to widgets csvs
def writeWidgetsCSV(csv, user):
    file = open(csv,'a')
    entry = user + "\n"
    file.write(entry)
    file.close()


#create a user, as long as she does not yet exist
def createUser(u,p):
    if userExists(u) or not alphanumeric(u):
        return False
    f = open(userfile,'a')
    f.write(u + "," + hashlib.md5(p).hexdigest() + "\n")
    f.close()

    caps = open('userCaps.csv', 'a')
    caps.write(u + "\n")
    caps.close()

    imgs = open('userImgs.csv', 'a')
    imgs.write(u + "\n")
    imgs.close()

    tags = open('userTags.csv', 'a')
    tags.write(u + "\n")
    tags.close()

    profiles = open('userProfiles.csv', 'a')
    profiles.write(u + ",I am awesome!,profpics/new-user.jpg" + "\n")
    profiles.close()

    return True


# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title> User Account Creation Results </title>"
htmlStr += """
        <link rel="stylesheet" type="text/css" href="../interiorpage.css">

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    </head>

"""
htmlStr += "<body>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
#htmlStr += "<h4>Dictionary of form data:</h4>"
#htmlStr += str( fsd )
#htmlStr += str( userExists(fsd[uname]) )
if not valid():
    htmlStr += "<h3>invalid input</h3>"
else:
    if createUser( fsd['uname'], fsd['upass1'] ):
        htmlStr += "<h3>Account created.</h3>"
        htmlStr += '<br><a class="btn btn-success" href="'+ loginPage + '">'
        htmlStr += "Log In</a>"
    else:
        htmlStr += "<br><h3>Account creation failed. Click back to try again.</h3>"
        htmlStr += "<br><p>Your username may have been registered already<br> \
                    or maybe your passwords don't match.</p>"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


htmlStr += "</body></html>"


print htmlStr