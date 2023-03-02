# all the funcs for the help center
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivymd.uix.label import MDLabel

import global_funcs
from app_main_screen import AppMainScreen


class InfoPopup(Popup):
    def __init__(self, pt_list: list, total_pages: list, wt: bool, **kwargs):
        super().__init__(**kwargs)
        self.wt = wt
        self.overlay_color = (0, 0, 0, 0.01)
        self.size_hint = 0.6, 0.4
        self.total_pages = total_pages
        self.point_list = pt_list
        self.step = 1
        self.reminder_counter = 0
        self.title = f"Step {str(self.step)}/{str(len(self.total_pages))}"
        self.lb = MDLabel(text=self.total_pages[self.step - 1], id="rect_lb")
        self.content = self.lb
        with self.lb.canvas:
            Color(1, 0, 0, 1)
            Line(width=2, rectangle=(self.point_list[0]))

    def on_open(self):
        from main import MainApp
        super().on_open()
        if not self.wt:
            MainApp.get_running_app().root.ids.tab_manager.screens[0].prevent_touch(val=True)

    def on_dismiss(self):
        from main import MainApp
        super().on_dismiss()
        if not self.wt:
            MainApp.get_running_app().root.ids.tab_manager.screens[0].prevent_touch(val=False)

    def _progress(self):
        self.lb.text = self.total_pages[self.step - 1]
        self.title = f"Step {self.step}/{len(self.total_pages)}"
        for child in self.lb.canvas.children:
            if isinstance(child, Line):
                self.lb.canvas.remove(child)
        with self.lb.canvas:
            Line(width=2, rectangle=(self.point_list[self.step - 1]))

    def on_touch_down(self, touch):
        if self.step == len(self.total_pages):
            self.step = 1
            self.dismiss()
            return
        if self.wt:
            if self.collide_point(touch.pos[0], touch.pos[1]):
                self.step += 1
                self._progress()
            else:
                self.reminder_counter += 1
                if self.reminder_counter == 3:
                    toast("Reminder! you need to press in the popup area in the walk through mode!")
                    self.reminder_counter = 0
        else:
            self.step += 1
            self._progress()


def run_tutorial(lang, tutorial_name,wt=False):
    text_list = global_funcs.read_from_json(f"assets\\texts\\{tutorial_name}.json", lang)
    pt_list = global_funcs.read_from_json(f"assets\\texts\\{tutorial_name}.json", "cords")
    InfoPopup(pt_list, text_list,wt).open()
