import json
import os.path
from tkinter.filedialog import askdirectory
import zipfile
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDSwitch, MDCheckbox
from kivymd.uix.tooltip import MDTooltip


class WindowMaster(ScreenManager):
    pass


class ToolTipIcon(MDIcon, MDTooltip):
    pass


class DefiPopup(MDDialog):
    def __init__(self, msg, **kwargs):
        super().__init__(**kwargs, buttons=[MDFlatButton(text="close", on_press=lambda x: self.dismiss())])
        self.text = msg


class ContactWindow(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "contact_window"
        Builder.load_file("contact_screen.kv")


class AppMainScreen(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.json_file = json.load(open("assets\\meta_data.json"))
        self.software_dir = self.json_file['software']['spotweld_dir']
        self.output_dir = self.json_file['software']['output_dir']
        Builder.load_file("app_main_screen.kv")

    def spotweld_dir_choose(self, instance):
        path = askdirectory()
        if not len(path) == 0:
            toast(f"Spotweld directory changed to:{path}")
            if instance == "1":
                self.software_dir = path
                self.ids.sw_directory_tf.text = path
                if os.path.exists(os.path.join(self.ids.sw_directory_tf.text, "swd")) and os.path.exists(
                        os.path.join(self.ids.sw_directory_tf.text, "SpotWeld NG")):
                    self.remove_widget(self.ids.sw_directory_alert)
            elif instance == "2":
                self.output_dir = path
                self.ids.zip_directory_tf.text = path
                self.remove_widget(self.ids.zip_directory_alert)

    def integrity_check(self):
        if os.path.exists(os.path.join(self.ids.sw_directory_tf.text, "swd")) and os.path.exists(
                os.path.join(self.ids.sw_directory_tf.text, "SpotWeld NG")):
            self.remove_widget(self.ids.sw_directory_alert)
        print("working")

    def disable_send(self, *args):
        if self.dir_textfield_alert.disabled:
            self.send_btn.set_disabled(True)

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
        zip_obj.write(f"{self.dir_textfield.text}")
        zip_obj.close()
        toast(f"File created at {self.dir_textfield.text}")

    def remove_advance(self, active):
        if active:
            self.ids.advance_switch_label.text = "Quick Mode"
            self.remove_widget(self.ids.bug_title_tf)
            self.remove_widget(self.ids.bug_msg_tf)
        else:
            self.ids.advance_switch_label.text = "Advance Mode"
            self.add_widget(self.ids.bug_title_tf)
            self.add_widget(self.ids.bug_msg_tf)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

    def build(self):
        pass


MainApp().run()
