import gi
gi.require_versions("Gtk", "3.0")
from gi.repository import Gtk
from ui import login


if __name__ == "__main__":
    win.login.LoginWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
