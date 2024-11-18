from kivy.uix.screenmanager import ScreenManager
from screens.welcome_screen import WelcomeScreen
from screens.login_screen import LoginScreen
from screens.signup_screen import SignupScreen
from screens.main_screen import MainScreen

class ScreenManagerApp(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(WelcomeScreen(name="welcomescreen"))
        self.add_widget(LoginScreen(name="loginscreen"))
        self.add_widget(SignupScreen(name="signupscreen"))
        self.add_widget(MainScreen(name="mainscreen"))
