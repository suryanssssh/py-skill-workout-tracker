from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen

# Define the basic layout for the app
KV = '''
Screen:
    MDLabel:
        text: "Welcome to Workout Tracker!"
        halign: "center"
'''

class WorkoutTrackerApp(MDApp):
    def build(self):
        # Load the KV layout
        self.theme_cls.primary_palette = "Blue"  # Optional: Set theme color
        screen = Builder.load_string(KV)
        return screen

if __name__ == "__main__":
    WorkoutTrackerApp().run()
