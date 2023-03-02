from kivy.lang import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from global_funcs import write_to_json, read_from_json


class ContactWindow(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "contact_window"
        self.ui_flag = False
        Builder.load_file("contact_screen_ui.kv")
        self.current_check = read_from_json("assets\\meta_data.json", "user_data", "active_check")

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids.user_tf.text = read_from_json("assets\\meta_data.json", "user_data", "username")
        self.ids.company_tf.text = read_from_json("assets\\meta_data.json", "user_data", "company")
        self.ids.email_tf.text = read_from_json("assets\\meta_data.json", "user_data", "email")

    def on_enter(self, *args):
        super().on_enter(*args)
        if self.current_check == "light_theme_check":
            self.ids.light_theme_check.active = True
        if self.current_check == "dark_theme_check":
            self.ids.dark_theme_check.active = True
        if self.current_check == "dark_purple_theme_check":
            self.ids.dark_purple_theme_check.active = True

    def switch_themes(self, uui):
        if uui == "1":
            write_to_json("assets\\meta_data.json", [["user_data", "palette", "Blue"]])
            write_to_json("assets\\meta_data.json", [["user_data", "theme", "Light"]])
            write_to_json("assets\\meta_data.json", [["user_data", "active_check", "light_theme_check"]])
        if uui == "2":
            write_to_json("assets\\meta_data.json", [["user_data", "palette", "Orange"]])
            write_to_json("assets\\meta_data.json", [["user_data", "theme", "Dark"]])
            write_to_json("assets\\meta_data.json", [["user_data", "active_check", "dark_theme_check"]])
        if uui == "3":
            write_to_json("assets\\meta_data.json", [["user_data", "palette", "DeepPurple"]])
            write_to_json("assets\\meta_data.json", [["user_data", "theme", "Dark"]])
            write_to_json("assets\\meta_data.json", [["user_data", "active_check", "dark_purple_theme_check"]])

    def save_changes(self):
        write_to_json("assets\\meta_data.json", [["user_data", "username", self.ids.user_tf.text]])
        write_to_json("assets\\meta_data.json", [["user_data", "company", self.ids.company_tf.text]])
        write_to_json("assets\\meta_data.json", [["user_data", "email", self.ids.email_tf.text]])
        from main import app_refresh
        app_refresh()

    def change_lang(self,lang):
        write_to_json("assets\\meta_data.json", [["user_data", "lang", lang]])
        from main import app_refresh
        app_refresh()