import json
import os.path
from tkinter.filedialog import askdirectory
import zipfile

from kivy.lang import Builder
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDIcon
from kivymd.uix.tooltip import MDTooltip


class WindowMaster(ScreenManager):
    pass


class ToolTipIcon(MDIcon, MDTooltip):
    pass


class ContactWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "contact_window"


class AppMainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.software_dir = json.load(open("assets\\meta_data.json"))["spotweld_dir"]
        self.output_dir = json.load(open("assets\\meta_data.json"))["output_dir"]
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

    def switch_tab(self, *args):
        self.manager.current = "contact_window"

    def disable_send(self, *args):
        if self.dir_textfield_alert.disabled:
            self.send_btn.set_disabled(True)

    def send_data(self, instance):
        data = {'title': self.msg_title.text, 'body': self.msg_body.text}
        json_str = json.dumps(data)
        json_file = open("output\\data.json", "w")
        json_file.write(json_str)
        json_file.close()
        zip_obj = zipfile.ZipFile(self.out_textfield.text + "\\output_zip.zip", 'w')
        zip_obj.write("output\\data.json")
        zip_obj.write(f"{self.dir_textfield.text}")
        zip_obj.close()
        toast(f"File created at {self.dir_textfield.text}")


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        pass


MainApp().run()
