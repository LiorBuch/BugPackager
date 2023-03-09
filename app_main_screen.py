import json
import os
import shutil
import zipfile
from tkinter.filedialog import askopenfile, askdirectory

import win32api
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import partial
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem, OneLineListItem
from kivymd.uix.textfield import MDTextField

import global_funcs
from global_funcs import write_to_json, read_from_json


class AppMainScreen(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        from main import MainApp
        self.json_file = json.load(open(os.path.join(MainApp.get_running_app().exe_loc, "assets\\meta_data.json")))
        self.exe_loc = MainApp.get_running_app().exe_loc
        self.software_dir = self.json_file['software']['spotweld_dir']
        self.output_dir = self.json_file['software']['output_dir']
        Builder.load_file("app_main_screen_ui.kv")
        Builder.load_file("help_ui.kv")
        Builder.load_file("info_popup_ui.kv")
        self.error_list = []
        self.run_list = ["swd.mdb", "Spotweld2.mdb", "Users.mdb", "BMP", "AScans", "Ref", "Logs"]
        self.img_path_list = []
        self.sw_type = "none"
        self.remove_tool_items = False
        self.remove_tool_images = False
        self.stop_touch_tool = False
        from main import HelpDialog
        self.help_center = HelpDialog()
        Clock.schedule_once(partial(self.data_integrity, "1"))
        Clock.schedule_once(partial(self.data_integrity, "2"))
        Clock.schedule_once(self.fill_list)

    def prevent_touch(self, val):
        if val:
            self.stop_touch_tool = True
        else:
            self.stop_touch_tool = False

    def on_touch_down(self, touch):
        if self.stop_touch_tool:
            pass
        else:
            return super().on_touch_down(touch)

    def spotweld_dir_choose(self, instance):
        path = askdirectory()
        if not len(path) == 0:
            if instance == "1":
                self.ids.sw_directory_tf.text = path
            if instance == "2":
                self.ids.zip_directory_tf.text = path
            self.data_integrity(instance, path=path)

    def fill_list(self, type="all", *args):
        def remove_me(obj):
            if self.remove_tool_items:
                self.ids.run_item_list.remove_widget(obj)
                self.run_list.remove(obj.text)

            if self.remove_tool_images:
                self.ids.run_img_list.remove_widget(obj)
                self.img_path_list.remove(obj.secondary_text)

        if type == "all" or "items":
            self.ids.run_item_list.clear_widgets()
            for item in self.run_list:
                self.ids.run_item_list.add_widget(OneLineListItem(text=item, on_press=remove_me))
        if type == "all" or "images":
            self.ids.run_img_list.clear_widgets()
            for item in self.img_path_list:
                self.ids.run_img_list.add_widget(
                    TwoLineListItem(text=os.path.basename(item), secondary_text=item, secondary_font_style="Overline",
                                    on_press=remove_me))

    def add_item_popup(self):
        def terminate(*args):
            pop.dismiss()
            self.run_list.append(str(pop_tf.text))
            self.fill_list(type="items")

        pop = MDDialog(size_hint=(0.5, 0.25), text="add the value here",
                       buttons=[MDFlatButton(text="Add", on_press=terminate)])
        pop_tf = MDTextField(size_hint=(0.5, 1))
        pop.add_widget(pop_tf)
        pop.open()

    def add_img(self):
        path = askopenfile(filetypes=[("Image Files", '.png .bmp .jpeg .jpg')])
        if path is not None:
            self.img_path_list.append(path.name)
        self.fill_list(type="images")

    def remove_item_from_list(self):
        if self.remove_tool_items:
            self.remove_tool_items = False
            self.ids.list_remove_btn.icon = "radiobox-blank"
        else:
            self.remove_tool_items = True
            self.ids.list_remove_btn.icon = "radiobox-marked"

    def remove_img_from_list(self):
        if self.remove_tool_images:
            self.remove_tool_images = False
            self.ids.list_img_remove_btn.icon = "radiobox-blank"
        else:
            self.remove_tool_images = True
            self.ids.list_img_remove_btn.icon = "radiobox-marked"

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
                self.ids.sw_directory_alert.text_color = 51 / 255, 194 / 255, 12 / 255, 1
            else:
                self.ids.sw_directory_alert.icon = "alert"
                self.ids.sw_directory_alert.text_color = 212 / 255, 34 / 255, 34 / 255, 1
                self.ids.sw_sub_lab.text.join("SW Type:")
                self.sw_type = "none"
        elif instance == "2":
            if not first_time:
                self.output_dir = path
                self.ids.zip_directory_tf.text = path
                toast(f"Zip directory changed to:{path}")
                write_to_json("assets\\meta_data.json", [("software", "output_dir", path)])
                self.ids.zip_directory_alert.icon = "check"
                self.ids.zip_directory_alert.text_color = 51 / 255, 194 / 255, 12 / 255, 1
            elif os.path.exists(self.output_dir):
                self.ids.zip_directory_alert.icon = "check"
                self.ids.zip_directory_alert.text_color = 51 / 255, 194 / 255, 12 / 255, 1

    def get_version(self, sw_type):
        langs = win32api.GetFileVersionInfo(f'{self.software_dir}\\{sw_type}', r'\VarFileInfo\Translation')
        key = r'StringFileInfo\%04x%04x\ProductVersion' % (langs[0][0], langs[0][1])
        ver = (win32api.GetFileVersionInfo(f'{self.software_dir}\\{sw_type}', key))
        self.ids.version_lab.text = f"SW version: {str(ver)}"

    def send_data(self):
        if self.ids.zip_directory_alert.icon == "alert" or self.ids.sw_directory_alert.icon == "alert":
            from main import DefiPopup
            DefiPopup("Missing important data! look for the alert to see where the problem might be...").open()
            return
        self.json_file['software']['spotweld_dir'] = self.ids.sw_directory_tf.text
        self.json_file['software']['output_dir'] = self.ids.zip_directory_tf.text
        from main import MainApp
        with open(os.path.join(MainApp.get_running_app().exe_loc, "assets\\meta_data.json"), "w") as file:
            file.write(json.dumps(self.json_file))
            file.close()
        comp = self.json_file['user_data']['company']
        user = self.json_file['user_data']['username']
        doc = global_funcs.create_doc(title=self.ids.bug_title_tf.text, body=self.ids.bug_msg_tf.text,
                                           company=comp, username=user)
        doc.save(f"{self.exe_loc}\\output\\temp.docx")
        zip_obj = zipfile.ZipFile(self.ids.zip_directory_tf.text + "\\output_zip.zip", 'w')
        self.error_list.clear()
        for item in self.run_list:
            try:
                zip_obj.write(os.path.join(self.software_dir, item))
            except:
                self.error_list.append(f"{item} not found")
        for img in self.img_path_list:
            shutil.copyfile(img, f"{self.exe_loc}\\output\\{os.path.basename(img)}")

        for path, name, dir in os.walk(f"{self.exe_loc}\\output"):
            for item in dir:
                if item != "alive.txt":
                    zip_obj.write("output\\" + str(item))
                    os.remove("output\\" + str(item))

        zip_obj.close()
        toast(f"File created at {self.output_dir}")
        pop = Popup(title="Missing Items!", size_hint=(0.5, 0.3))
        lb = MDLabel(
            text=f"Zip file was created but there are some missing items!\nhere is a list of missing files: {self.error_list}")
        pop.add_widget(lb)
        pop.open()

    def remove_advance(self, active):
        from main import MainApp
        if not active:
            self.ids.advance_switch_label.text = MainApp.get_running_app().load_lang("text-inactive",
                                                                                     "advance_switch_label")
            self.remove_widget(self.ids.bug_title_tf)
            self.remove_widget(self.ids.bug_msg_tf)
            self.remove_widget(self.ids.version_lab)
            self.remove_widget(self.ids.sw_sub_lab)
            self.remove_widget(self.ids.item_list_layout)
            self.remove_widget(self.ids.img_list_layout)
        else:
            self.ids.advance_switch_label.text = MainApp.get_running_app().load_lang("text-active",
                                                                                     "advance_switch_label")
            self.add_widget(self.ids.bug_title_tf)
            self.add_widget(self.ids.bug_msg_tf)
            self.add_widget(self.ids.version_lab)
            self.add_widget(self.ids.sw_sub_lab)
            self.add_widget(self.ids.item_list_layout)
            self.add_widget(self.ids.img_list_layout)
