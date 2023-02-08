import json
import multiprocessing
import os.path
from tkinter.filedialog import askdirectory
import zipfile
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import partial
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon
from kivymd.uix.tooltip import MDTooltip
from win32com.client import Dispatch


class WindowMaster(ScreenManager):
    pass


class ToolTipIcon(MDIcon, MDTooltip):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DefiPopup(MDDialog):
    def __init__(self, msg, **kwargs):
        super().__init__(**kwargs, buttons=[MDFlatButton(text="close", on_press=lambda x: self.dismiss())])
        self.text = msg


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
        if self.ui_flag:
            pass


class AppMainScreen(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.json_file = json.load(open("assets\\meta_data.json"))
        self.software_dir = self.json_file['software']['spotweld_dir']
        self.output_dir = self.json_file['software']['output_dir']
        Builder.load_file("app_main_screen.kv")
        self.error_list = []
        self.run_list = ["swd.mdb", "Spotweld2.mdb", "Users.mdb", "BMP", "AScans", "Ref", "Logs"]
        self.sw_type = "none"
        Clock.schedule_once(partial(self.data_integrity, "1"))
        Clock.schedule_once(partial(self.data_integrity, "2"))

    def spotweld_dir_choose(self, instance):
        path = askdirectory()
        if not len(path) == 0:
            if instance == "1":
                self.ids.sw_directory_tf.text = path
            if instance == "2":
                self.ids.zip_directory_tf.text = path
            self.data_integrity(instance, path=path)

    def data_integrity(self, instance, first_time=False, path=None):
        if instance == "1":
            if os.path.exists(os.path.join(self.ids.sw_directory_tf.text, "Users.mdb")):
                if path is not None:
                    self.software_dir = path
                    write_to_json("assets\\meta_data.json", [("software", "spotweld_dir", path)])
                    toast(f"Spotweld directory changed to:{path}")
                if os.path.exists(os.path.join(self.ids.sw_directory_tf.text, "SpotWeld PA.exe")):
                    self.ids.sw_sub_lab.text = "SW Type: PA"
                    self.sw_type = "pa"
                    self.get_version("SpotWeld PA.exe")
                elif os.path.exists(os.path.join(self.ids.sw_directory_tf.text, "SpotWeld NG.exe")):
                    self.ids.sw_sub_lab.text = ("SW Type: NG")
                    self.sw_type = "ng"
                    self.get_version("SpotWeld NG.exe")
                self.ids.sw_directory_alert.icon = "check"
            else:
                self.ids.sw_directory_alert.icon = "alert"
                self.ids.sw_sub_lab.text.join("SW Type:")
                self.sw_type = "none"
        elif instance == "2":
            if not first_time:
                self.output_dir = path
                self.ids.zip_directory_tf.text = path
                toast(f"Zip directory changed to:{path}")
                write_to_json("assets\\meta_data.json", [("software", "output_dir", path)])
            self.ids.zip_directory_alert.icon = "check"

    def disable_send(self, *args):

        if self.dir_textfield_alert.disabled:
            self.send_btn.set_disabled(True)

    def get_version(self, type):
        parser = Dispatch("Scripting.FileSystemObject")
        version = parser.GetFileVersion(f'{self.software_dir}\\{type}')
        self.ids.version_lab.text = f"SW version: {str(version)}"

    def send_data(self):
        if not self.ids.zip_directory_alert.disabled or not self.ids.sw_directory_alert.disabled:
            DefiPopup("Missing important data! look for the alert to see where the problem might be...").open()
            return
        self.json_file['software']['spotweld_dir'] = self.ids.sw_directory_tf.text
        self.json_file['software']['output_dir'] = self.ids.zip_directory_tf.text
        with open("assets\\meta_data.json", "w") as file:
            file.write(json.dumps(self.json_file))
            file.close()
        data = {'title': self.ids.bug_title_tf.text, 'body': self.ids.bug_msg_tf.text}
        json_str = json.dumps(data)
        json_file = open("output\\data.json", "w")
        json_file.write(json_str)
        json_file.close()
        zip_obj = zipfile.ZipFile(self.ids.zip_directory_tf.text + "\\output_zip.zip", 'w')
        zip_obj.write("output\\data.json")
        for item in self.run_list:
            try:
                zip_obj.write(os.path.join(self.software_dir, item))
            except:
                self.error_list.append(f"{item} not found")

        zip_obj.close()
        toast(f"File created at {self.output_dir}")

    def remove_advance(self, active):
        if not active:
            self.ids.advance_switch_label.text = "Quick Mode"
            self.remove_widget(self.ids.bug_title_tf)
            self.remove_widget(self.ids.bug_msg_tf)
            self.remove_widget(self.ids.version_lab)
            self.remove_widget(self.ids.sw_sub_lab)
        else:
            self.ids.advance_switch_label.text = "Advance Mode"
            self.add_widget(self.ids.bug_title_tf)
            self.add_widget(self.ids.bug_msg_tf)
            self.add_widget(self.ids.version_lab)
            self.add_widget(self.ids.sw_sub_lab)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Bug Packager"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = read_from_json("assets\\meta_data.json", "user_data", "theme")
        self.theme_cls.primary_palette = read_from_json("assets\\meta_data.json", "user_data", "palette")

    def build(self):
        pass


def write_to_json(file_to_modify, data_list: list):
    with open(file_to_modify, "r") as jsonFile:
        data = json.load(jsonFile)
        for item in data_list:
            data[item[0]][item[1]] = item[2]
    with open(file_to_modify, "w") as jsonFile:
        json.dump(data, jsonFile)


def read_from_json(file, where_index, what_index):
    with open(file, "r") as jsonFile:
        data = json.load(jsonFile)
        return data[where_index][what_index]


if __name__ == '__main__':
    MainApp().run()
