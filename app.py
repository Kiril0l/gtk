import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import redis
from ui import chat



if __name__ == "__main__":
    win = chat.ChatWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
