from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation

import app_main_screen
import contact_window


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contact_screen = None
        self.ms = None
        self.sm = None

    def build(self):
        self.sm = ScreenManager()
        self.ms = app_main_screen.AppMainScreen()
        self.contact_screen = contact_window.ContactWindow()
        self.sm.add_widget(self.ms)
        self.sm.add_widget(self.contact_screen)
        self.sm.current = "main_screen"
        return self.sm


MainApp().run()
