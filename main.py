from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation

import app_main_screen


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ms = None
        self.sm = None

    def build(self):
        self.sm = ScreenManager()
        self.ms = app_main_screen.AppMainScreen()
        self.sm.add_widget(self.ms)
        self.sm.current = "main_screen"
        return self.sm


MainApp().run()
