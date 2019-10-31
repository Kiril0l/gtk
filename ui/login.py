import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import redis
from ui import event


class LoginWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Mega Chat | Login")
        self.is_login = False
        self.is_password = False
        self.set_border_width(50) #устанавливаем границы
        self.set_resizable(False)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  #добавляем бокс
        self.add(box)

        top_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(top_box, True, True, 0)


        login_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        password_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        top_box.pack_start(login_box, True, False, 5)
        top_box.pack_start(password_box, True, False, 5)
        label_login = Gtk.Label(label="Логин")
        login_box.pack_start(label_login, True, False, 5)
        self.login = Gtk.Entry()
        self.login.connect("changed", self.on_change_login)
        login_box.pack_start(self.login, True, True, 0)
        label_password = Gtk.Label(label="Пароль")
        password_box.pack_start(label_password, True, False, 5)
        self.password = Gtk.Entry()
        self.password.connect("changed", self.on_change_password)
        password_box.pack_start(self.password, True, True, 0)

        separator = Gtk.HSeparator()
        box.pack_start(separator, True, False, 5)

        bottom_box = Gtk.Box()
        bottom_box.set_spacing(5)
        box.pack_start(bottom_box, False, True, 0)

        b_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bottom_box.pack_start(b_box, False, True, 0)
        registration = Gtk.Button(label="Registration")
        registration.connect("clicked", self.on_registration) #привязываем метод
        registration.set_sensitive(False)
        b_box.pack_start(registration, False, True, 0)
        b_space = Gtk.Alignment()
        b_box.pack_start(b_space, True, True, 0)

        c_box = Gtk.ButtonBox(orientation=Gtk.Orientation.VERTICAL)
        c_box.set_spacing(10)
        bottom_box.pack_start(c_box, True, True, 0)
        self.sign_in = Gtk.Button(label="Sign in")
        self.sign_in.connect("clicked", self.on_sign_in)
        self.sign_in.set_sensitive(False)
        c_box.pack_start(self.sign_in, True, True, 0)
        button_close = Gtk.Button(label="Close")
        button_close.connect("clicked", Gtk.main_quit)
        c_box.pack_end(button_close, True, True, 0)


    def on_registration(self, button):
        pass

    @event.Event.origin("login", post=True)
    def on_sign_in(self, button):
        storage = redis.StrictRedis()
        self.storage.set("login", self.login.get_text())
        self.storage.set("password", self.password.get_text())
        storage.expire("login", 10)
        storage.expire("password", 10)
        # login = self.login.get_text()
        # password = self.password.get_text()
        # print(login, password)

    # def __check_entry(self,):
        # if len(entry.get_text()) > 2:
        #     if name == "login":
        #         self.is_login = True
        #     if name == "password":
        #         self.is_password = True
        # else:
        #     if name == "login":
        #         self.is_login = False
        #     if name == "password":
        #         self.is_password = False
        # if self.is_login and self.is_password:
        #     self.sign_in.set_sensitive(True)
        # else:
        #     self.sign_in.set_sensitive(False)




    def on_change_login(self, entry):
        self.is_login = True if len(entry.get_text()) > 2 else False
        self.sign_in.set_sensitive(self.is_login and self.is_password)

    def on_change_password(self, entry):
        self.is_password = True if len(entry.get_text()) > 2 else False
        self.sign_in.set_sensitive(self.is_login and self.is_password)
















              # ФРЭЙМЫ
                # login_frame = Gtk.Frame(label = "Login")
                # password_frame = Gtk.Frame(label = "Password")
                # top_box.pack_start(login_frame, True, False, 0)
                # top_box.pack_start(password_frame, True, False, 0)
                #
                #
                # l_box = Gtk.Box()
                # p_box = Gtk.Box()
                # login = Gtk.Entry()
                # login_frame.add(login)
                # password = Gtk.Entry()
                # password_frame.add(password)
