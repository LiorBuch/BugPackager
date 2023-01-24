import json
from tkinter.filedialog import askdirectory

from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.button import MDRaisedButton, MDRoundFlatIconButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class AppMainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "main_screen"
        self.software_dir = json.load(open("assets\\meta_data.json"))["spotweld_dir"]
        self.msg_title = MDTextField(hint_text="Bug Title")
        self.msg_body = MDTextField(hint_text="Bug Text")
        self.dir_textfield = MDTextField(hint_text="Spotweld Main Directory")
        self.dir_chosse_bnt = MDRaisedButton(text = "Choose directory")
        self.nav_bar = MDBottomNavigation()
        self.send_btn = MDRaisedButton(text="send", on_press=self.spotweld_dir_choose,
                                       pos_hint={'right': 0.95, 'center_y': 0.15})
        self.contact_btn = MDFillRoundFlatIconButton(text="Contact", icon="assets\\icons\\person-icon.png",
                                                     pos_hint={'right': 0.95, 'center_y': 0.95})
        self.add_widget(self.send_btn)
        self.add_widget(self.contact_btn)
        self.add_widget(self.nav_bar)

    def spotweld_dir_choose(self, instance):
        path = '{}'.format(askdirectory())
        toast(f"Spotweld directory changed to:{path}")
        self.software_dir = path
