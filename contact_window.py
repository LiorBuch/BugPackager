from kivy.uix.screenmanager import Screen


class ContactWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = "contact_window"
