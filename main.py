import json
import os.path
import shutil
from tkinter.filedialog import askdirectory, askopenfile
import zipfile
import win32api
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import partial
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.list import OneLineListItem, OneLineIconListItem, IconLeftWidget, TwoLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.tooltip import MDTooltip

DEFAULT_RUN_LIST = ["swd.mdb", "Spotweld2.mdb", "Users.mdb", "BMP", "AScans", "Ref", "Logs"]


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
    def __init__(self, msg, btn_text="close", **kwargs):
        super().__init__(**kwargs, buttons=[MDFlatButton(text=btn_text, on_press=lambda x: self.dismiss())])
        self.text = msg


class HelpDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, buttons=[MDFlatButton(text="Close", on_press=lambda x: self.dismiss())])


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
            process_kill()


class AppMainScreen(MDBottomNavigationItem):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.json_file = json.load(open("assets\\meta_data.json"))
        self.software_dir = self.json_file['software']['spotweld_dir']
        self.output_dir = self.json_file['software']['output_dir']
        Builder.load_file("app_main_screen.kv")
        Builder.load_file("help_ui.kv")
        self.error_list = []
        self.run_list = ["swd.mdb", "Spotweld2.mdb", "Users.mdb", "BMP", "AScans", "Ref", "Logs"]
        self.img_path_list = []
        self.sw_type = "none"
        self.remove_tool_items = False
        self.remove_tool_images = False
        self.help_center = HelpDialog()
        Clock.schedule_once(partial(self.data_integrity, "1"))
        Clock.schedule_once(partial(self.data_integrity, "2"))
        Clock.schedule_once(self.fill_list)

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

    def get_version(self, sw_type):
        langs = win32api.GetFileVersionInfo(f'{self.software_dir}\\{sw_type}', r'\VarFileInfo\Translation')
        key = r'StringFileInfo\%04x%04x\ProductVersion' % (langs[0][0], langs[0][1])
        ver = (win32api.GetFileVersionInfo(f'{self.software_dir}\\{sw_type}', key))
        self.ids.version_lab.text = f"SW version: {str(ver)}"

    def send_data(self):
        if self.ids.zip_directory_alert.icon == "alert" or self.ids.sw_directory_alert.icon == "alert":
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
        self.error_list.clear()
        for item in self.run_list:
            try:
                zip_obj.write(os.path.join(self.software_dir, item))
            except:
                self.error_list.append(f"{item} not found")
        for img in self.img_path_list:
            shutil.copyfile(img, f"output\\{os.path.basename(img)}")
        for path, name, dir in os.walk("output"):
            for item in dir:
                zip_obj.write("output\\" + str(item))
                os.remove("output\\" + str(item))

        zip_obj.close()
        toast(f"File created at {self.output_dir}")
        pop = Popup(title="Missing Items!", size_hint=(0.5, 0.3))
        lb = MDLabel(
            text=f"Zip file was created but there are som missing items!\nhere is a list of missing files: {self.error_list}")
        pop.add_widget(lb)
        pop.open()

    def remove_advance(self, active):
        if not active:
            self.ids.advance_switch_label.text = "Quick Mode"
            self.remove_widget(self.ids.bug_title_tf)
            self.remove_widget(self.ids.bug_msg_tf)
            self.remove_widget(self.ids.version_lab)
            self.remove_widget(self.ids.sw_sub_lab)
            self.remove_widget(self.ids.item_list_layout)
            self.remove_widget(self.ids.img_list_layout)
        else:
            self.ids.advance_switch_label.text = "Advance Mode"
            self.add_widget(self.ids.bug_title_tf)
            self.add_widget(self.ids.bug_msg_tf)
            self.add_widget(self.ids.version_lab)
            self.add_widget(self.ids.sw_sub_lab)
            self.add_widget(self.ids.item_list_layout)
            self.add_widget(self.ids.img_list_layout)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Bug Packager"
        self.kv = Builder.load_file("main_ui.kv")
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = read_from_json("assets\\meta_data.json", "user_data", "theme")
        self.theme_cls.primary_palette = read_from_json("assets\\meta_data.json", "user_data", "palette")

    def build(self):
        return self.kv

    def load_lang(self, field, m_id):
        current_lang = read_from_json("assets\\meta_data.json", "user_data", "lang")
        with open("assets\\lang.json", "r") as j_file:
            lang_dict = json.load(j_file)
            j_file.close()
            return lang_dict[m_id][field][current_lang]

    def label_color(self):
        theme = read_from_json("assets\\meta_data.json", "user_data", "theme")
        if theme == "Dark":
            return "white"
        if theme == "Light":
            return "black"

    def write_to_json(self, file_to_modify, data_list: list):
        with open(file_to_modify, "r") as jsonFile:
            data = json.load(jsonFile)
            for item in data_list:
                data[item[0]][item[1]] = item[2]
        with open(file_to_modify, "w") as jsonFile:
            json.dump(data, jsonFile)


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


def process_kill():
    Builder.unload_file("app_main_screen.kv")
    Builder.unload_file("main_ui.kv")
    Builder.unload_file("contact_screen.kv")
    Builder.unload_file("help_ui.kv")
    MainApp.get_running_app().stop()
    Window.clear()
    MainApp().run()


if __name__ == '__main__':
    MainApp().run()
