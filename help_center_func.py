#all the funcs for the help center
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel


class InfoPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.overlay_color=(0,0,0,0.2)
        # self.background_color = 0,0,0,1
        self.size_hint = 0.6,0.2
        self.title = "Step 1/5"
        lb = MDLabel(text="this is the first step of the tutorial")
        self.add_widget(lb)

def quick_Mode_tutorial():
    pop = InfoPopup()
    pop.open()