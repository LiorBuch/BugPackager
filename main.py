import json
import os.path
import sys
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.tooltip import MDTooltip

import help_center_func
from app_main_screen import AppMainScreen
from global_funcs import read_from_json, write_to_json

DEFAULT_RUN_LIST = ["swd.mdb", "Spotweld2.mdb", "Users.mdb", "BMP", "AScans", "Ref", "Logs"]
VERSION = "1.1.0"


class WindowMaster(ScreenManager):
    pass


class ItemLine(OneLineIconListItem):
    def __init__(self, item, *args, **kwargs):
        super().__init__(IconLeftWidget(icon="radiobox-blank"), *args, **kwargs)
        self.text = item
        self.size_hint = (1, 0.1)
        self.my_icon = "radiobox-blank"

    def pressed(self):
        if self.my_icon == "radiobox-blank":
            self.my_icon = "radiobox-marked"
        else:
            self.my_icon = "radiobox-blank"


class ToolTipIcon(MDIcon, MDTooltip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tool_tip_control(self, state):
        if self.icon == "check":
            self.tooltip_text = MainApp.get_running_app().load_lang("tooltip_text_ok", state)
        elif self.icon == "alert":
            self.tooltip_text = MainApp.get_running_app().load_lang("tooltip_text", state)


class ToolTipLabel(MDLabel, MDTooltip):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DefiPopup(MDDialog):
    def __init__(self, msg, **kwargs):
        btn_text = MainApp.get_running_app().load_lang("text", "close_btn_general")
        super().__init__(**kwargs, buttons=[MDFlatButton(text=btn_text, on_press=lambda x: self.dismiss())])
        self.text = msg


class HelpDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, buttons=[
            MDFlatButton(text=MainApp.get_running_app().load_lang("text", "close_btn_general"),
                         on_press=lambda x: self.dismiss())])
        self.quick_tut = help_center_func.run_tutorial

    def begin_tutorial(self, test_name: str):
        self.dismiss()
        if test_name == "quick_tut":
            self.quick_tut(MainApp.get_running_app().app_lang, "quick_mode_tutorial_texts")
            return

        if test_name == "quick_tut_wt":
            self.quick_tut(MainApp.get_running_app().app_lang, "quick_mode_tutorial_texts",wt=True)
            return

        if test_name == "advance_tut":
            self.quick_tut(MainApp.get_running_app().app_lang, "advance_mode_tutorial_texts")
            return

        if test_name == "advance_tut_wt":
            self.quick_tut(MainApp.get_running_app().app_lang, "advance_mode_tutorial_texts",wt=True)
            return


class ContactWindow(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "contact_window"
        self.ui_flag = False
        Builder.load_file("contact_screen.kv")
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
        app_refresh()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prod = True
        if not self.prod:
            self.exe_loc = os.path.dirname(sys.executable)
        else:
            self.exe_loc = os.path.dirname(os.path.realpath(__file__))
        self.title = "Bug Packager"
        self.kv = Builder.load_file("main_ui.kv")
        self.app_lang = read_from_json("assets\\meta_data.json", "user_data", "lang")
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = read_from_json("assets\\meta_data.json", "user_data", "theme")
        self.theme_cls.primary_palette = read_from_json("assets\\meta_data.json", "user_data", "palette")
    def build(self):
        return self.kv

    def load_lang(self, field, m_id):
        current_lang = read_from_json("assets\\meta_data.json", "user_data", "lang")
        with open(os.path.join(MainApp.get_running_app().exe_loc, "assets\\lang.json"), "r") as j_file:
            lang_dict = json.load(j_file)
            j_file.close()
            return lang_dict[m_id][field][current_lang]

    def label_color(self):
        theme = read_from_json("assets\\meta_data.json", "user_data", "theme")
        if theme == "Dark":
            return "white"
        if theme == "Light":
            return "black"


def app_refresh():
    Builder.unload_file(os.path.join(MainApp.get_running_app().exe_loc, "app_main_screen_ui.kv"))
    Builder.unload_file(os.path.join(MainApp.get_running_app().exe_loc, "main_ui.kv"))
    Builder.unload_file(os.path.join(MainApp.get_running_app().exe_loc, "contact_screen.kv"))
    Builder.unload_file(os.path.join(MainApp.get_running_app().exe_loc, "help_ui.kv"))
    Builder.unload_file(os.path.join(MainApp.get_running_app().exe_loc, "info_popup_ui.kv"))
    MainApp.get_running_app().stop()
    MainApp().run()


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        MainApp().run()
    except Exception as e:
        print(e)
        input("Press enter.")
