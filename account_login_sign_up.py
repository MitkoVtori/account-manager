# ---- Imports ----
import re
from colorama import Fore


# ---- Regex patterns ----
password_pattern = r"^([\S+]{6,25})$"
email_pattern = r"^([\w\.\-]{1,20}\@\w{1,7}\.[a-zA-Z]{1,6})$"
username_pattern = r"^(\w{3,15})$"


# ---- Dictionaries ----
accounts = {
    "example_password": [
        "example_email",
        "example_username"
    ]
}

ssh = {
    "example_username":
        "example_password"
}


# ---- login variables ----
input_email_or_username = ''
input_password = ''


# ---- signup variables ----
username = ''
email = ''
password = ''
confirm_password = ''
age = 0


# ---- ALTS ----
save_ssh_alts = {"yes", "y", "ye", "yeah", "yeh"}
login_alts = {"login", "log in", "l", "log", "in", "signin", "sign in"}
signup_alts = {"signup", "sign up", "s", "sign", "up", "logup", "log up"}


# ---- Login code ----
class Login:

    def __init__(self, accounts: dict, input_password: str, input_email_or_username: str):
        self.accounts = accounts
        self.password = input_password
        self.email_or_username = input_email_or_username

    def password_validity(self):
        if self.password in self.accounts.keys():
            return True
        return False

    def valid_email_or_username(self):
        if self.email_or_username in self.accounts[self.password]:
            return True
        return False


def valid_login(log):
    if log.password_validity():
        if log.valid_email_or_username():
            return True
        return False
    return False


# login = Login(accounts, input_password, input_email_or_username)
# signed_in = valid_login(login)
# ---- Login code ----


#######################
#######################


# ---- Signup code ----
class CAPTCHA:

    def __init__(self):
        print("Human CAPTCHA test.")
        print("Guess the number:")

    def captcha(self):
            counter = 0

            for num in range(1, 10 + 1):
                number = int(input(f"{num}: "))

                if number == num:
                    counter += 1

                if counter == 3:
                    return True

            return False


class Signup:

    def __init__(self, accounts: dict, username: str, email: str, password: str, confirm_password: str, age: int):
        self.accounts = accounts
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.age = age

    def username_email_password(self):
        '''
            This function checks if the username, email and password already exist
        '''

        if self.password not in accounts.keys():
            if self.email not in accounts.values():
                if self.username not in accounts.values():
                    return True
                return "Username already exists"
            return "Email address already exists"
        return "Password already exists"

    def password_confirmed(self):
        if self.password == self.confirm_password:
            return True
        return "The password is different from the confirmation password"

    def how_old(self):
        if age > 12:
            return True
        return "You are too young to use this app"

    def human_captcha(self):
        captcha = CAPTCHA()
        return captcha.captcha()


def successful_signup(sign):
    if sign.username_email_password() is True:
        if sign.password_confirmed() is True:
            if sign.how_old() is True:
                if sign.human_captcha is True:
                    return True
                return "Failed human captcha"
            return sign.how_old()
        return sign.password_confirmed()
    return sign.username_email_password()


# signup = Signup(accounts, username, email, password, confirm_password, age)
# logged_in = successful_signup(signup)
# ---- Signup code ----


def log_in():
    # ---- global login variables ----
    global input_email_or_username
    global input_password

    # ---- Flags ----
    go_back = False

    # ---- changing the values ----
    input_email_or_username = input(Fore.GREEN + "Email address or Username: ")

    if input_email_or_username in ssh.keys():
        print(Fore.WHITE + "Password filled by ssh")
        input_password = ssh[username]
    else:
        input_password = input(Fore.GREEN + "Password: ")

    login = Login(accounts, input_password, input_email_or_username)
    signed_in = valid_login(login)

    if not signed_in:
        print(Fore.YELLOW + "Invalid Email address, Username or Password")
        go_back = True

    if not go_back:
        print(Fore.WHITE + f"Welcome {accounts[input_password][1]}!")


def sign_up():
    # ---- global signup variables ----
    global username
    global email
    global password
    global confirm_password
    global age

    # ---- Flags ----
    go_back = False

    # ---- changing values ----
    username = input(Fore.LIGHTGREEN_EX + '''
    Username must be between 3 and 15 characters long.
    Cannot include spaces. Can only contain: letters, numbers and underscore '_': ''')

    username_check = re.findall(username_pattern, username)

    while not username_check:
        print(Fore.RED + "Invalid username")
        username = input(Fore.LIGHTGREEN_EX + '''
            Username must be between 3 and 15 characters long.
            Cannot include spaces. Can only contain: letters, numbers and underscore '_': ''')

        username_check = re.findall(username_pattern, username)

    email = input(Fore.LIGHTGREEN_EX + "Email address: ")

    email_check = re.findall(email_pattern, email)

    while not email_check:
        print(Fore.RED + "Invalid email address")
        email = input(Fore.LIGHTGREEN_EX + "Email address: ")

        email_check = re.findall(email_pattern, email)

    password = input(Fore.LIGHTGREEN_EX + "Password must be between 6 and 25 characters long. Cannot include spaces: ")

    password_check = re.findall(password_pattern, password)

    while not password_check:
        print(Fore.RED + "Invalid password")
        password = input(Fore.LIGHTGREEN_EX + "Password must be between 6 and 25 characters long. Cannot include spaces: ")

        password_check = re.findall(password_pattern, password)

    confirm_password = input(Fore.LIGHTGREEN_EX + "Confirm password: ")

    while confirm_password != password:
        print(Fore.RED + "The password is different from the confirmation password")
        confirm_password = input(Fore.LIGHTGREEN_EX + "Confirm password: ")

    age = int(input(Fore.LIGHTGREEN_EX + "How old are you: "))

    if age < 12:
        print(Fore.RED + "You are too young to use this app")
        go_back = True

    if not go_back:
        signup = Signup(accounts, username, email, password, confirm_password, age)
        logged_in = successful_signup(signup)

        if not logged_in:
            Fore.RED + logged_in
            go_back = True

        if not go_back:
            accounts[password] = [email, username]

            save_ssh_password = input(Fore.LIGHTGREEN_EX + "Do you wanna save password in list of password \"yes\", \"no\": ").lower()

            if save_ssh_password in save_ssh_alts:
                ssh[username] = password
                print(Fore.GREEN + "Saved!")

            print(Fore.YELLOW + "Welcome home!")


def login_signup():

    while True:
        login_or_signup = input(Fore.BLUE + "Login or Signup: ").lower()

        if login_or_signup in login_alts:
            log_in()
            break

        elif login_or_signup in signup_alts:
            sign_up()
            break

        print(Fore.RED + "An Error Occurred: Invalid command, please try again!")


while True:
    login_signup()
