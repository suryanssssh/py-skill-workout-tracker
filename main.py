from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
import mysql.connector

KV = '''
MDScreenManager:

    HomeScreen:
    LoginScreen:
    SignupScreen:

<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Skill and Workout Tracker"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: (1, 1, 1, 1)

        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            spacing: "20dp"
            padding: "10dp"

            MDRaisedButton:
                text: "Login"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.4
                on_release: app.root.current = "login"

            MDRaisedButton:
                text: "Signup"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.4
                on_release: app.root.current = "signup"

<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Login"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: (1, 1, 1, 1)

        MDTextField:
            id:email
            hint_text: "Enter Email"
            icon_right: "account"
            mode: "rectangle"

        MDTextField:
            id:password
            hint_text: "Enter Password"
            icon_right: "lock"
            mode: "rectangle"
            password: True

        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            on_release: app.receive_data(email.text, password.text)
           

        MDTextButton:
            text: "Create an account"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "signup"

<SignupScreen>:
    name: "signup"

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Signup"
            
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: (1, 1, 1, 1)

        MDTextField:
            hint_text: "Enter Username"
            id:username
            icon_right: "account"
            mode: "rectangle"

        MDTextField:
            hint_text: "Enter Email"
            id: email
            icon_right: "email"
            mode: "rectangle"

        MDTextField:
            hint_text: "Enter Password"
            id: password
            icon_right: "lock"
            mode: "rectangle"
            password: True

        MDRaisedButton:
            text: "Signup"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            on_release: app.send_data(username.text,email.text, password.text)

        MDTextButton:
            text: "Already have an account?"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "login"
'''

class HomeScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class SignupScreen(MDScreen):
    pass

class SkillWorkoutApp(MDApp):
    def build(self):
        # Set the app theme to dark and use a primary palette
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Load the KV layout
        return Builder.load_string(KV)

#this is to get data off database
    def receive_data(self, email, password):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="suryansh3396",
            database="loginform"
        )
        cursor = db.cursor()

        # Fetch all emails from the database
        cursor.execute("SELECT email FROM logindata")
        email_list = [i[0] for i in cursor.fetchall()]

        if email in email_list and email != '':

            query = "SELECT password FROM logindata WHERE email = %s"
            cursor.execute(query, (email,))

            db_password = cursor.fetchone()  # Fetch the first result
            if db_password and password == db_password[0]:
                print("You have successfully logged in.")
            else:
                print("Incorrect password.")
        else:
            print("Incorrect email.")

        db.close()

    def send_data(self,username, email, password):
        # Connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="suryansh3396",
            database="loginform"
        )
        cursor = db.cursor()

        # Insert data into the database
        query = "INSERT INTO logindata (username,email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username,email, password))
        db.commit()
        print("Data sent:", username, email, password)
        username = ' '
        email = ' '
        password = ' '

        db.close()

if __name__ == "__main__":
    SkillWorkoutApp().run()
