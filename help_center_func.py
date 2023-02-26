# all the funcs for the help center
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel

import global_funcs


class InfoPopup(Popup):
    def __init__(self, total_pages: list, **kwargs):
        super().__init__(**kwargs)
        self.overlay_color = (0, 0, 0, 0)
        # self.background_color = 0,0,0,1
        self.size_hint = 0.6, 0.4
        self.total_pages = total_pages
        self.step = 1
        self.title = f"Step {str(self.step)}/{str(len(self.total_pages))}"
        self.lb = MDLabel(text=self.total_pages[self.step - 1])
        self.content = self.lb

    def _progress(self):
        self.lb.text = self.total_pages[self.step - 1]
        self.title = f"Step {self.step}/{len(self.total_pages)}"

    def on_touch_down(self, touch):
        if self.step == len(self.total_pages):
            self.step = 1
            self.dismiss()
            return
        self.step += 1
        self._progress()


def quick_mode_tutorial(lang):
    text_list = global_funcs.read_from_json("assets\\texts\\quick_mode_tutorial_texts.json",lang)
    InfoPopup(text_list).open()


def advance_mode_tutorial():
    pass
