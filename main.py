from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.card import MDCard
import mysql.connector

KV = '''
MDScreenManager:

    HomeScreen:
    LoginScreen:
    SignupScreen:
    WelcomeScreen:

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
            id: email
            hint_text: "Enter Email"
            icon_right: "account"
            mode: "rectangle"

        MDTextField:
            id: password
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
            id: username
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
            on_release: app.send_data(username.text, email.text, password.text)

        MDTextButton:
            text: "Already have an account?"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = "login"

<WelcomeScreen>:
    name: "welcome"

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            id: welcome_label
            text: "Welcome!"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: (1, 1, 1, 1)

        MDGridLayout:
            cols: 2
            spacing: "10dp"
            size_hint_y: None
            height: self.minimum_height

            MDCard:
                orientation: "vertical"
                padding: "10dp"
                size_hint: None, None
                size: "150dp", "100dp"
                ripple_behavior: True
                MDLabel:
                    text: "Boxing"
                    halign: "center"
                    font_style: "H6"

            MDCard:
                orientation: "vertical"
                padding: "10dp"
                size_hint: None, None
                size: "150dp", "100dp"
                ripple_behavior: True
                MDLabel:
                    text: "Calisthenics"
                    halign: "center"
                    font_style: "H6"

            MDCard:
                orientation: "vertical"
                padding: "10dp"
                size_hint: None, None
                size: "150dp", "100dp"
                ripple_behavior: True
                MDLabel:
                    text: "Hypertrophy"
                    halign: "center"
                    font_style: "H6"

        MDLabel:
            text: "Recent Activity"
            halign: "center"
            font_style: "H5"
            size_hint_y: None
            height: "40dp"

        ScrollView:
            MDList:
                id: recent_activity_list
'''

class HomeScreen(MDScreen):
    pass

class LoginScreen(MDScreen):
    pass

class SignupScreen(MDScreen):
    pass

class WelcomeScreen(MDScreen):
    pass

class SkillWorkoutApp(MDApp):
    def build(self):
        # Set the app theme to dark and use a primary palette
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        # Load the KV layout
        return Builder.load_string(KV)

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
            # Fetch the password and username for the email
            query = "SELECT password, username FROM logindata WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()  # Fetch the first result

            if result and password == result[0]:
                username = result[1]
                print(f"Welcome, {username}!")
                self.set_welcome_message(username)
                self.set_recent_activity()
                self.root.current = "welcome"
            else:
                print("Incorrect password.")
        else:
            print("Incorrect email.")

        db.close()

    def send_data(self, username, email, password):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="suryansh3396",
            database="loginform"
        )
        cursor = db.cursor()

        # Insert data into the database
        query = "INSERT INTO logindata (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        db.commit()
        print("Data sent:", username, email, password)

        db.close()

    def set_welcome_message(self, username):
        # Access the welcome screen and set the welcome label's text
        welcome_screen = self.root.get_screen("welcome")
        welcome_screen.ids.welcome_label.text = f"Welcome, {username}!"

    def set_recent_activity(self):
        # Use demo data to populate the recent activity list
        demo_data = ["Push-ups: 50 reps", "Pull-ups: 15 reps", "Squats: 70 kg x 8 reps"]
        recent_activity_list = self.root.get_screen("welcome").ids.recent_activity_list
        recent_activity_list.clear_widgets()

        for activity in demo_data:
            recent_activity_list.add_widget(OneLineListItem(text=activity))

if __name__ == "__main__":
    SkillWorkoutApp().run()
