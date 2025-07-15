import re
import hashlib
from User_DB_handler import SecurityMonitor

class Portal:
    def __init__(self):
        self.user_id=None
        self.username=None
        self.password=None
        self.db=SecurityMonitor()
    def check_user_id(self):
        while True:
            self.user_id=input("Please enter your user ID: ")
            if re.search(r"\d", self.user_id) is None:
                print("User ID must contain at least one digit")
            elif len(self.user_id) <= 5:
                print("User ID has to be atleaste 5 characters long")
            elif self.db.validate(self.user_id):
                print("User ID already exists, try a different one")
            else:
                print("User ID is valid")
                break
        return self.user_id
    def check_username(self):
        while True:
            self.username=input("Please enter your username: ")
            if  re.search(r"\d", self.username) is None:
                print("Username must contain contain at least one digit")
            else:
                print("Username is valid")
                break
        return self.username
    def check_password(self):
        while True:
            self.password=input("Please enter your password: ")
            if len(self.password)<8:
                print("Password must be more than or equal to 8 characters")
            elif re.search(r'[A-Z]', self.password) is None:
                print("Password must contain at least one uppercase letter")
            elif re.search(r"[!@|~`#$%+*?<>=]",self.password) is None:
                print("Password must contain at least one special character")
            elif re.search(r'\d', self.password) is None:
                print("password must contain at least one digit")
            else:
                print("Password is Valid")
                self.password = hashlib.sha256(self.password.encode()).hexdigest()
                break
        return self.password
    def signup(self):
        user_id=self.check_user_id()
        username=self.check_username()
        password=self.check_password()
        self.db.add_user(user_id,username,password)
    def login(self):
        while True:
            user_id = input("Enter your UserID: ")
            password = input("Enter your password: ")
            hash_pass = hashlib.sha256(password.encode()).hexdigest()

            if self.db.validate_login(user_id, hash_pass):
                print("Login successful!")
                return True

            print("Invalid credentials!")
            retry = input("Try again? (y/n): ")
            if retry.lower() != 'y':
                return False

p= Portal()
print ("""Welcome to the Login portal:
       press 1 to signup for New User
       press 2 to login as Existing User
       press 3 to exit\n""")
while True:
    choice=input("Enter your choice: ")
    if choice == "1":
        print("You have chosen to sign up")
        p.signup()
    elif choice == "2":
            p.login()
    elif choice == "3":
        print("Exiting...")
        p.db.close_connection()
        break