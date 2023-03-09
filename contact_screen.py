from kivy.lang import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

from global_funcs import write_to_json


class ContactWindow(MDBottomNavigationItem):
    def __init__(self, **kw):
        from main import MainApp
        self.cur = MainApp.get_running_app().cur
        self.db = MainApp.get_running_app().db
        super().__init__(**kw)
        self.name = "contact_window"
        self.ui_flag = False
        Builder.load_file("contact_screen_ui.kv")
        self.current_check = self.cur.execute("SELECT active_check FROM userdata").fetchone()[0]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.ids.user_tf.text = self.cur.execute("SELECT username FROM userdata").fetchone()[0]
        self.ids.company_tf.text = self.cur.execute("SELECT company FROM userdata").fetchone()[0]
        self.ids.email_tf.text = self.cur.execute("SELECT email FROM userdata").fetchone()[0]

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
            self.cur.execute("UPDATE userdata SET palette = 'Blue' WHERE id = 1")
            self.cur.execute("UPDATE userdata SET theme = 'Light' WHERE id = 1")
            self.cur.execute("UPDATE userdata SET active_check = 'light_theme_check' WHERE id = 1")
        if uui == "2":
            self.cur.execute("UPDATE userdata SET palette = 'Orange' WHERE id = 1")
            self.cur.execute("UPDATE userdata SET theme = 'Dark' WHERE id = 1")
            self.cur.execute("UPDATE userdata SET active_check = 'dark_theme_check' WHERE id = 1")
        if uui == "3":
            self.cur.execute("UPDATE userdata SET palette = 'DeepPurple' WHERE id = 1")
            self.cur.execute("UPDATE userdata SET theme = 'Dark' WHERE id = 1")
            self.cur.execute("UPDATE userdata SET active_check = 'dark_purple_theme_check' WHERE id = 1")
        self.db.commit()
        from main import app_refresh
        app_refresh()

    def save_changes(self):
        self.cur.execute("UPDATE userdata SET username = ? WHERE id = ?",(self.ids.user_tf.text,1))
        self.cur.execute("UPDATE userdata SET company = ? WHERE id = ?",(self.ids.company_tf.text,1))
        self.cur.execute("UPDATE userdata SET email = ? WHERE id = ?",(self.ids.email_tf.text,1))
        self.db.commit()
        from main import app_refresh
        app_refresh()

    def change_lang(self,language):
        self.cur.execute(f"UPDATE userdata SET lang = ? WHERE id=?",(language,1))
        self.db.commit()
        from main import app_refresh
        app_refresh()