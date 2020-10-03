from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self, uname, pword):
        
        with open("users.json") as file:
            users = json.load(file)
        
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or passwor"
    
    def get_password(self):
        self.manager.transition.direction = 'left'
        self.manager.current= "forgot_password_screen"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_press(self, uname,pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {"username": uname,
        "password": pword,
        "created": datetime.now().strftime("%Y-%M-%D %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users,file)
        self.manager.current = "sign_up_screen_success"
        
class SignUpScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    
    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings= glob.glob("quotes/*txt")

        available_feelings= [Path(filename).stem for filename in available_feelings]
       

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    """always write ButtonBehavior object at start or else button wil not perform it's function"""
    pass

class ForgotPasswordScreen(Screen):
    def getpassword(self, uname):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users:
            self.ids.fpassword.text= users[uname]['password']
        else:
            self.ids.fpassword.text= "Incorrect Username"
    
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()

