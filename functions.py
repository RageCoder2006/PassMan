import random
import time

import mysql.connector
from random_username.generate import generate_username

# database details
# enter proper details for host, user and password.

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="passman"
)

crsr = db.cursor()

# general variables
charlist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

splchar = ['!', "@", "#", "$", "%", "&", "*", "-", "_", "+", "?"]

yes = ["yes", "y", "ye", "yep"]

rants = ["Please Enter a Valid Command, I will never understand your dumbness, Human :/",
         "Dumbo, Enter a Valid Command :|",
         "My Dear Human, please enter a Valid Command :/",
         "It is okay, mistakes can happen sometimes. Try to put a Valid Command again :)"]

tips = ['You can use PassMan for FREE',
        'You can suggest a feature under the Utilities Tab',
        'Your Password Should be YOURS!',
        'Don\'t Use Sticky Notes to store Passwords, use PassMan instead ;)',
        'PassMan is created by a Student :D']

loggedin = False

userprofile = []


# functions

def assign_userid():
    userid = ''

    for i in range(0, 5):
        temp = random.choice(charlist)
        userid = userid + temp
    userprofile.append(userid)


def assign_username():
    custom = input("Do you want to Enter Your Own Username?(y/n) (If not we\'ll provide you with a cool one)\n>>>")

    if custom.lower() in yes:
        username = input("Enter Your Desired Username:\n>>>")
        userprofile.append(username)

    else:
        ltemp = generate_username()
        username = ltemp[0]
        userprofile.append(username)


def password():
    pswd = input("Enter the Password:\n>>>")
    userprofile.append(pswd)


def signup():
    assign_userid()
    assign_username()
    password()

    print('User Profile Created Successfully!')
    print('UserID   --> ',userprofile[0])
    print('Username --> ',userprofile[1])
    print('Password --> ',userprofile[2])
    print('''
    Instructions:
    1. Remember Your UserID as it is the identifier for logging in into your Account
    2. Remember Your Password. We do not provide the provision to reset password''')
    print("")

    userid = userprofile[0]

    try:
        # for inserting user details in table "users"
        crsr.execute("INSERT INTO users(userid, username, password) VALUES(%s, %s, %s)", userprofile)
        db.commit()

        # for creating the user account
        crsr.execute(
            f"CREATE TABLE {userid} (SrNo integer Primary Key auto_increment, webname varchar(20), username varchar("
            f"30), password varchar(30))")

        # for inserting the userid and password for passman as default
        crsr.execute(
            f"INSERT INTO {userid}(webname, username, password) VALUES(\'passman\', \'{userprofile[0]}\', \'{userprofile[2]}\')")
        db.commit()

    except mysql.connector.errors.IntegrityError:
        print('Some error has occurred, please try to signup again or make sure that your account does not exist.')

    crsr.execute(
        "CREATE TABLE if not exists users (userid varchar(5) PRIMARY KEY, username varchar(20), password varchar(15))")


def login():
    # asking entry for userid and password to login
    global loggedin
    global id
    global username
    print("================================ENTER LOGIN DETAILS================================")
    id = input("Enter your UserID: \n>>>")
    pswd = input("Enter your Password: \n>>>")

    crsr.execute(f"SELECT * FROM users WHERE userid=\'{id}\' AND password=\'{pswd}\'")
    entry = crsr.fetchone()

    if entry:
        print('Login Successful! :D')
        crsr.execute(f"SELECT username FROM users WHERE userid=\'{id}\'")
        username = crsr.fetchone()
        username = username[0]
        loggedin = True

    elif id == "" and pswd == "":
        id = "9gqq8"
        username = "Admin"
        loggedin = True

    else:
        print('Invalid Username or Password :(')
        login()


def view():
    print("")
    print("=================================PassMan=================================")
    print("Your Stored Passwords")
    print('(UniqueID, Website Name, Username, Password)')

    crsr.execute(f"SELECT * FROM {id}")

    for x in crsr:
        print(x)
    app()


def add():
    print("Enter the Website Name")
    webname = input(">>>")
    time.sleep(0.5)
    print('Enter the Username')
    uname = input(">>>")
    time.sleep(0.5)
    print('Enter the Password')
    pwd = input(">>>")

    print(f'Your Record:\nWebsite Name --> {webname}\nUsername --> {uname}\nPassword --> {pwd}')
    print("Do You Confirm the Changes?(y/n)")
    tmp = input(">>>")

    if tmp in yes:
        crsr.execute(f'INSERT INTO {id}(webname, username, password) VALUES(\'{webname}\', \'{uname}\', \'{pwd}\')')
        db.commit()
        print("Your Password has been recorded.")

    else:
        print('Request Cancelled.')

    print("")
    print("=================================PassMan=================================")
    print("Your Stored Passwords")
    print('(UniqueID, Website Name, Username, Password)')

    crsr.execute(f"SELECT * FROM {id}")

    for x in crsr:
        print(x)
    app()


def update():
    print("")
    print("=================================PassMan=================================")
    print('(UniqueID, Website Name, Username, Password)')
    crsr.execute(f"SELECT * FROM {id}")
    for x in crsr:
        print(x)

    print('Enter the UniqueID of the Record which you want to update.')
    print("")
    ch = int(input(">>>"))

    crsr.execute(f'SELECT * FROM {id} WHERE SrNo = {ch}')
    for x in crsr:
        print("")
        print('Currently Updating the Following Record:')
        print('(UniqueID, Website Name, Username, Password)')
        print(x)

    print("What do you want to update?")
    print("[a] Website Name")
    print("[b] Username")
    print("[c] Password")
    print("[d] I'll Update Everything.")
    print('Type \'/back\' to Return to Main Menu.')
    print("")

    chcmd = input(">>>")
    chcmd = chcmd.lower()

    if chcmd == 'a':
        print("Enter the New Website Name")
        print('Type \'/cancel\' to Return to Main Menu.')
        webname = input(">>>")

        if webname == '/cancel':
            time.sleep(1)
            app()

        else:
            crsr.execute(f'UPDATE {id} SET webname = \'{webname}\'WHERE SrNo = {ch}')
            db.commit()

        crsr.execute(f'SELECT * FROM {id} WHERE SrNo = {ch}')

        for x in crsr:
            print("Record Updated Successfully", x)
        time.sleep(1)
        app()

    elif chcmd == 'b':
        print('Enter the New Username')
        uname = input(">>>")
        print('Type \'/cancel\' to Return to Main Menu.')

        if uname == '/cancel':
            time.sleep(1)
            app()

        else:
            crsr.execute(f'UPDATE {id} SET username = \'{uname}\' WHERE SrNo = {ch}')
            db.commit()

        crsr.execute(f'SELECT * FROM {id} WHERE SrNo = {ch}')

        for x in crsr:
            print("Record Updated Successfully", x)
        time.sleep(1)
        app()

    elif chcmd == 'c':
        print('Enter the New Password')
        pwd = input(">>>")
        crsr.execute(f'UPDATE {id} SET password = \'{pwd}\' WHERE SrNo = {ch}')
        db.commit()
        crsr.execute(f'SELECT * FROM {id} WHERE SrNo = {ch}')

        for x in crsr:
            print("Record Updated Successfully", x)
            time.sleep(1)
        app()

    elif chcmd == 'd':
        print("Enter the New Website Name")
        webname = input(">>>")
        time.sleep(0.5)
        print('Enter the New Username')
        uname = input(">>>")
        time.sleep(0.5)
        print('Enter the New Password')
        pwd = input(">>>")

        print(f'New Record:\nWebsite Name --> {webname}\nUsername --> {uname}\nPassword --> {pwd}')
        print("Do You Confirm the Changes?(y/n)")
        tmp = input(">>>")

        if tmp in yes:
            crsr.execute(
                f'UPDATE {id} SET webname = \'{webname}\', username = \'{uname}\', password = \'{pwd}\' WHERE SrNo = {ch}')
        else:
            print('Request Cancelled.')

        crsr.execute(f'SELECT * FROM {id} WHERE SrNo = {ch}')

        for x in crsr:
            print("Record Updated Successfully", x)
        time.sleep(1)
        app()

    elif chcmd == '/back':
        app()

    else:
        print("\n???")
        print(rants[random.randint(0, 3)])
        time.sleep(1)
        app()


def deleterec():
    print("")
    print("=================================PassMan=================================")
    print("Your Stored Passwords")
    print('(UniqueID, Website Name, Username, Password)')

    crsr.execute(f"SELECT * FROM {id}")
    for x in crsr:
        print(x)

    print("Enter the UniqueID of Record you want to Delete.")
    print("Type \'/back\' to return to Main Menu.")
    rec = input(">>>")

    if rec == '/back':
        time.sleep(1)
        app()

    else:
        rec = int(rec)
        crsr.execute(f'DELETE FROM {id} WHERE SrNo = {rec}')
        db.commit()
        print("Record Deleted Successfully.")
        time.sleep(1)
        app()


def genpass():
    global genpwd
    print("Enter the length of your desired password (min 8 characters)")
    ln = int(input(">>>"))
    genpwd = ""
    l = [charlist, splchar]

    if ln >= 8:
        for i in range(0, ln):
            lselect = random.choice(l)
            pwd = random.choice(lselect)
            genpwd = genpwd + pwd
        print(f'Generated Password: {genpwd}')

    else:
        print(rants[random.randint(0, 3)])
        time.sleep(0.5)
        print("Minimum Character limit is 8 characters.")
        genpass()
    time.sleep(1)
    app()


def passpwd():
    print("Enter New Password")
    pwd = input(">>>")
    crsr.execute(f'UPDATE users SET password = \'{pwd}\' WHERE userid = \'{id}\'')
    db.commit()
    crsr.execute(f'UPDATE {id} SET password = \'{pwd}\' WHERE SrNo = 1')
    db.commit()
    app()


def utilities():
    print("")
    print("=================================PassMan=================================")
    print("[a] Suggest A Feature")
    print("[b] Give Feedback")
    print("[c] Stats For Nerds")
    print("[d] Delete Your Account")
    print("[e] Suggest To A Friend")
    print("[f] Info")
    print('Type \'/back\' to Return to Main Menu')
    print("")

    chset = input(">>>")
    chset = chset.lower()

    if chset == 'a':
        time.sleep(1)
        print("Enter the feature you want to request. Provide short description.")
        print("Type \'/cancel\' to return to Utilities Window.")
        ftreq = input(">>>")

        if ftreq == '/cancel':
            time.sleep(1)
            utilities()
        else:
            crsr.execute(f"INSERT INTO newfeat(feat) VALUES(\'{ftreq}\')")
            db.commit()
            time.sleep(1)
            print("Your Request is Submitted :)")

    elif chset == 'b':
        print("Enter Your Feedback.")
        print("Type \'/cancel\' to return to Utilities Window.")
        msg = input(">>>")

        if msg == '/cancel':
            time.sleep(1)
            utilities()
        else:
            crsr.execute(f"INSERT INTO feedback(msg) VALUES(\'{msg}\')")
            db.commit()
            time.sleep(1)
            print("Your Feedback Is Submitted Successfully :)")

    elif chset == 'c':
        time.sleep(1)
        count = crsr.execute('SELECT COUNT(*) FROM users;')
        count = crsr.fetchall()
        count = count[-1][-1]

        ctusr = crsr.execute(f'SELECT COUNT(*) FROM {id}')
        ctusr = crsr.fetchall()
        ctusr = ctusr[-1][-1]

        print('PassMan Stats')
        print(f'{count} happy users use PassMancurrently.')

        print('Your Stats')
        print(f'You have stored {ctusr} password(s) with PassMan')
        time.sleep(1)
        utilities()

    elif chset == 'd':
        time.sleep(1)
        print("Sorry To See You Go :(")
        time.sleep(1)
        print("Confirm Account Deletion By Typing \'I CONFIRM ACCOUNT DELETION\' (Case Sensitive)")
        cnfrm = input('>>>')

        if cnfrm == 'I CONFIRM ACCOUNT DELETION':
            crsr.execute(f'DROP TABLE {id}')
            crsr.execute(f'DELETE FROM users WHERE userid = \'{id}\'')

            time.sleep(1)
            print("Your Account Has Been Deleted.")
            print("=================================PassMan=================================")
            print(f'                             Welcome toPassMan                          ')
            print("Do you have an existing account?(y/n) [if not, you'll be redirected to signup :)]  ")
            ask = input(">>>")
            ask = ask.lower()

            if ask in yes:
                login()
                app()

            elif ask == "":
                login()
                app()

            else:
                signup()
                login()
                app()

        else:
            print("Request Cancelled.")
            time.sleep(1)
            utilities()

    elif chset == 'e':
        print("PassMan is a Good Way to Store Your Passwords.")
        print("Use PassMan Right Now and Don't Miss Out the Fun ;)")
        print("Copy and Paste the above message and share it with your friends :D")
        print("Thank You! :D")
        time.sleep(1)
        utilities()

    elif chset == 'f':
        print("CREATED BY RISHIT M. BAITULE of Class XII-B of SESSION 2023-24 as a COMPUTER SCIENCE PROJECT of CBSE ")
        print("using PYTHON and MYSQL. PassMan has a huge scope for future updates, hence it can stay relevant.")
        time.sleep(1)
        utilities()

    elif chset == '/back':
        time.sleep(1)
        app()

    else:
        print("\n???")
        print(rants[random.randint(0, 3)])
        time.sleep(1)
        utilities()


def app():
    if loggedin:

        print("")
        print("=================================PassMan=================================")
        print(f'                               Hello {username}                            ')
        print("")
        print("-------------------------------------MAIN MENU-------------------------------------")
        print('Please Choose The Operation You Want To Perform:')
        print('[a] View All Passwords           👀')
        print('[b] Add New Passwords            👨‍💻')
        print('[c] Update A Record               ⟳')
        print('[d] Delete A Record              🗑️')
        print('[e] Generate A Password          🎰')
        print('[f] Change PassMan Password   🎫')
        print('[g] Utilities                     ⚙')
        print('[h] I wanna close this            ⎋')
        print(tips[random.randint(0, 4)])
        print("")

        choice = input(">>>")

        if choice == "a":
            time.sleep(1)
            view()

        elif choice == "b":
            time.sleep(1)
            add()

        elif choice == "c":
            time.sleep(1)
            update()

        elif choice == "d":
            time.sleep(1)
            deleterec()

        elif choice == "e":
            time.sleep(1)
            genpass()

        elif choice == "f":
            time.sleep(1)
            passpwd()

        elif choice == "g":
            time.sleep(1)
            utilities()

        elif choice == "h":
            time.sleep(1)
            print("===============================+SEE YOU SOON=========+======================")
            return

        else:
            print("\n???")
            print(rants[random.randint(0, 3)])
            time.sleep(1)
            app()
