import json
import os.path
import shutil
from tkinter.filedialog import askdirectory
import zipfile

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.tooltip import MDTooltip


class TooltipIcon(MDIcon, MDTooltip):
    pass


class AppMainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "main_screen"
        self.software_dir = json.load(open("assets\\meta_data.json"))["spotweld_dir"]
        self.output_dir = json.load(open("assets\\meta_data.json"))["output_dir"]
        self.msg_title = MDTextField(hint_text="Bug Title", pos_hint={'x': 0.02, 'y': 0.7}, size_hint=(0.3, 1))
        self.msg_body = MDTextField(hint_text="Bug Text", multiline=True, pos_hint={'x': 0.02, 'y': 0.35},
                                    size_hint=(0.7, 1))
        self.dir_textfield = MDTextField(hint_text="Spotweld Main Directory", pos_hint={'x': 0.02, 'y': 0.9},
                                         size_hint=(0.3, 1))
        self.dir_textfield_alert = TooltipIcon(icon="alert", theme_text_color="Custom",
                                               text_color=(212 / 255, 34 / 255, 34 / 255, 1),
                                               pos_hint={'x': 0.35, 'y': 0.93},
                                               tooltip_text="SpotWeld was not found in the directory!")
        self.out_textfield = MDTextField(hint_text="Zip Output Directory", pos_hint={'x': 0.02, 'y': 0.8},
                                         size_hint=(0.3, 1))
        self.dir_choose_bnt = MDRaisedButton(text="Choose directory", pos_hint={'x': 0.4, 'y': 0.92},
                                             on_press=self.spotweld_dir_choose, id="1")
        self.dir_output_alert = TooltipIcon(icon="alert", theme_text_color="Custom",
                                            text_color=(212 / 255, 34 / 255, 34 / 255, 1),
                                            pos_hint={'x': 0.35, 'y': 0.83},
                                            tooltip_text="Directory is empty!")
        self.out_dir_choose_bnt = MDRaisedButton(text="Choose directory", pos_hint={'x': 0.4, 'y': 0.82},
                                                 on_press=self.spotweld_dir_choose, id="2")
        self.nav_bar = MDBottomNavigation()
        self.nav_contact = MDBottomNavigationItem(on_tab_press=self.switch_tab, icon="assets\\icons\\person-icon.png")
        self.advance_packager = MDBottomNavigationItem(on_tab_press=self.switch_tab)
        self.simple_pack = MDBottomNavigationItem(on_tab_press=self.switch_tab)

        self.send_btn = MDRaisedButton(text="send", on_press=self.send_data,
                                       pos_hint={'right': 0.95, 'center_y': 0.15})
        self.contact_btn = MDFillRoundFlatIconButton(text="Contact", icon="assets\\icons\\person-icon.png",
                                                     pos_hint={'right': 0.95, 'center_y': 0.95})
        self.add_widget(self.send_btn)
        self.add_widget(self.dir_choose_bnt)
        self.add_widget(self.contact_btn)
        self.add_widget(self.nav_bar)
        self.add_widget(self.dir_textfield)
        self.add_widget(self.dir_textfield_alert)
        self.add_widget(self.msg_title)
        self.add_widget(self.msg_body)
        self.add_widget(self.out_textfield)
        self.add_widget(self.out_dir_choose_bnt)
        self.add_widget(self.dir_output_alert)
        self.nav_bar.add_widget(self.nav_contact)

    def spotweld_dir_choose(self, instance):
        path = askdirectory()
        if not len(path) == 0:
            toast(f"Spotweld directory changed to:{path}")
            if instance.id == "1":
                self.software_dir = path
                self.dir_textfield.text = path
                if os.path.exists(os.path.join(self.dir_textfield.text, "swd")) and os.path.exists(
                        os.path.join(self.dir_textfield.text, "SpotWeld NG")):
                    self.remove_widget(self.dir_textfield_alert)
            elif instance.id == "2":
                self.output_dir = path
                self.out_textfield.text = path
                self.remove_widget(self.dir_output_alert)

    def switch_tab(self, *args):
        self.manager.current="contact_window"

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
