from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import requests
import mysql.connector;

help_str = '''
ScreenManager:
    WelcomeScreen:
    MainScreen:
    LoginScreen:
    SignupScreen:

<WelcomeScreen>:
    name: 'welcomescreen'
    MDLabel:
        text: 'Skill'
        font_style: 'H3'
        halign: 'center'
        pos_hint: {'center_y': 0.8}
    MDLabel:
        text: 'And'
        font_style: 'H3'
        halign: 'center'
        pos_hint: {'center_y': 0.7}
    MDLabel:
        text: 'Workout Tracker'
        font_style: 'H3'
        halign: 'center'
        pos_hint: {'center_y': 0.6}

    MDRaisedButton:
        text: 'Login'
        pos_hint: {'center_x': 0.35, 'center_y': 0.3}
        size_hint: (0.25, 0.08)
        on_press: 
            root.manager.current = 'loginscreen'
            root.manager.transition.direction = 'left'
    MDRaisedButton:
        text: 'Signup'
        pos_hint: {'center_x': 0.65, 'center_y': 0.3}
        size_hint: (0.25, 0.08)
        on_press:
            root.manager.current = 'signupscreen'
            root.manager.transition.direction = 'left'

<LoginScreen>:
    name: 'loginscreen'
    MDLabel:
        text: 'Login'
        font_style: 'H4'
        halign: 'center'
        pos_hint: {'center_y': 0.9}

    MDTextField:
        id: login_email
        pos_hint: {'center_y': 0.6, 'center_x': 0.5}
        size_hint: (0.8, None)
        height: '40dp'
        hint_text: 'Email'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        required: True
        mode: 'rectangle'

    MDTextField:
        id: login_password
        pos_hint: {'center_y': 0.45, 'center_x': 0.5}
        size_hint: (0.8, None)
        height: '40dp'
        hint_text: 'Password'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'key'
        required: True
        mode: 'rectangle'

    MDRaisedButton:
        text: 'Login'
        size_hint: (0.3, 0.08)
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        on_press: 
            app.login()
            app.username_changer()

    MDTextButton:
        text: 'Create an account'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        on_press:
            root.manager.current = 'signupscreen'
            root.manager.transition.direction = 'up'


<SignupScreen>:
    name: 'signupscreen'
    MDLabel:
        text: 'Signup'
        font_style: 'H4'
        halign: 'center'
        pos_hint: {'center_y': 0.9}

    MDTextField:
        id: signup_username
        pos_hint: {'center_y': 0.7, 'center_x': 0.5}
        size_hint: (0.8, None)
        height: '40dp'
        hint_text: 'Username'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        required: True

    MDTextField:
        id: signup_email
        pos_hint: {'center_y': 0.55, 'center_x': 0.5}
        size_hint: (0.8, None)
        height: '40dp'
        hint_text: 'Email'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'email'
        required: True

    MDTextField:
        id: signup_password
        pos_hint: {'center_y': 0.4, 'center_x': 0.5}
        size_hint: (0.8, None)
        height: '40dp'
        hint_text: 'Password'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'key'
        required: True

    MDRaisedButton:
        text: 'Signup'
        size_hint: (0.3, 0.08)
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_press: app.signup()

    MDTextButton:
        text: 'Already have an account'
        pos_hint: {'center_x': 0.5, 'center_y': 0.15}
        on_press:
            root.manager.current = 'loginscreen'
            root.manager.transition.direction = 'down'
<MainScreen>:
    name: 'mainscreen'
    MDLabel:
        id:username_info
        text:'Hello Main'
        font_style:'H3'
        halign:'center'

'''


class WelcomeScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='loginscreen'))
sm.add_widget(MainScreen(name='mainscreen'))
sm.add_widget(LoginScreen(name='loginscreen'))
sm.add_widget(SignupScreen(name='signupscreen'))


class LoginApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.strng = Builder.load_string(help_str)
        self.auth = 'Kew8mzt1nv6YaadgWRDBNdwSaYbRJGfDSHLbn4nJ'
        self.url = "https://skill-workout-tracker-default-rtdb.firebaseio.com/.json"
        return self.strng

    def signup(self):
        signupEmail = self.strng.get_screen('signupscreen').ids.signup_email.text
        signupPassword = self.strng.get_screen('signupscreen').ids.signup_password.text
        signupUsername = self.strng.get_screen('signupscreen').ids.signup_username.text
        if signupEmail.split() == [] or signupPassword.split() == [] or signupUsername.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        if len(signupUsername.split()) > 1:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Username', text='Please enter username without space',
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(signupEmail, signupPassword)
            signup_info = str(
                {f'\"{signupEmail}\":{{"Password":\"{signupPassword}\","Username":\"{signupUsername}\"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            to_database = json.loads(signup_info)
            print((to_database))
            requests.patch(url=self.url, json=to_database)
            self.strng.get_screen('loginscreen').manager.current = 'loginscreen'


    def login(self):
        loginEmail = self.strng.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.strng.get_screen('loginscreen').ids.login_password.text

        self.login_check = False
        supported_loginEmail = loginEmail.replace('.', '-')
        supported_loginPassword = loginPassword.replace('.', '-')
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        email = set()
        for key, value in data.items():
            email.add(key)
        if supported_loginEmail in email and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.username = data[supported_loginEmail]['Username']
            self.login_check = True
            self.strng.get_screen('mainscreen').manager.current = 'mainscreen'
        else:
            print("user no longer exists")


    def close_username_dialog(self, obj):
                 self.dialog.dismiss()
    def username_changer(self):
             if self.login_check:
                 self.strng.get_screen('mainscreen').ids.username_info.text = f"welcome {self.username}"


LoginApp().run()
