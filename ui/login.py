import gi
gi.require_versions("Gtk", "3.0")
from gi.repository import Gtk


class loginWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Mega Chat | Login")
        self.set_border_width(15) #устанавливаем границы
