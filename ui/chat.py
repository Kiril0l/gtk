import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,GdkPixbuf
from ui import login
import socket
import select
import json
import os
import redis
from ui import event

HOST = "127.0.0.1"
PORT = 5000


class ChatWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Mega Chat | Chat")
        event.Event(name="login", callback=self.regy_date)
        self.login_win = login.LoginWindow()
        self.login_win.show_all()
        self.connection = None
        self.__interfase()

    def __interfase(self):
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(800, 600)

        master_box=Gtk.Box()
        master_box.set_spacing(5)
        self.add(master_box)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_box.set_size_request(200, -1)
        master_box.pack_start(left_box, False, True, 0)
        separator = Gtk.VSeparator()
        master_box.pack_start(separator, False, True, 0)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "Avatar.png"
            ),
            width = 190,
            height = 190,
            preserve_aspect_ratio=True,
        )

        avatar = Gtk.Image.new_from_pixbuf(pixbuf)
        left_box.pack_start(avatar, False, True, 5)
        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, True, 5)


        user_label= Gtk.Label(label="User name")
        left_box.pack_start(user_label, False, True, 5)
        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, True, 5)

        l_space = Gtk.Alignment()
        left_box.pack_start(l_space, True, True, 5)
        separator = Gtk.HSeparator()
        left_box.pack_start(separator, False, True, 0)

        b_box = Gtk.ButtonBox()
        left_box.pack_start(b_box, False, True, 5)
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", Gtk.main_quit)
        b_box.pack_start(close_button, True, True, 5)

        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        master_box.pack_start(center_box, True, True, 0)
        separator = Gtk.VSeparator()
        master_box.pack_start(separator, False, True, 0)

        scroll_box = Gtk.ScrolledWindow()
        scroll_box.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        center_box.pack_start(scroll_box, True, True, 5)

        self.chat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll_box.add(self.chat_box)
        separator = Gtk.HSeparator()
        center_box.pack_start(separator, False, False, 5)


        send_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        send_box.set_spacing(5)
        center_box.pack_start(send_box, False, True, 5)
        separator = Gtk.HSeparator()
        center_box.pack_start(separator, False, False, 5)
        smile_buttom = Gtk.Button(label = ":-}")
        send_box.pack_start(smile_buttom, False, False, 0)
        message_entry = Gtk.Entry()
        send_box.pack_start(message_entry, True, True, 0)
        send_button = Gtk.Button(label = "Send")
        send_box.pack_start(send_button, False, False, 0)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_size_request(200, 1)
        master_box.pack_start(right_box, False, True, 0)


        favorit_label = Gtk.Label(label="Избранное")
        right_box.pack_start(favorit_label, False, True, 5)


        # test_input = {
        #     "message": (
        #         "Компиля́ция — сборка программы, включающая трансляцию всех модулей программы, "
        #         "написанных на одном или нескольких исходных языках программирования высокого "
        #         "уровня и/или языке ассемблера, в эквивалентные программные модули на "
        #         "низкоуровневом языке, близком машинному коду"
        #     ),
        #     "user": "Vasia"
        # }
        #
        # test_output = {
        #     "message": (
        #         "Инициализация — создание, активация, подготовка к работе, определение параметров. " "Приведение программы или устройства в состояние готовности к использованию. "
        #     ),
        #     "user": "User"
        # }
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_output, False)
        # self.__add_message_box(test_input)
        # self.__add_message_box(test_output, False)


    def __add_message_box(self, data, input=True):
        message_frame = Gtk.Frame()
        message_box = Gtk.Box()
        message_frame.add(message_box)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                f".contacts/{data['user']}.png" if input
                else "Avatar.png"
            ),
            width = 100,
            height = 100,
            preserve_aspect_ratio=True,
        )
        avatar = Gtk.Image.new_from_pixbuf(pixbuf)
        text_label = Gtk.Label()
        text_label.set_markup(data["message"])
        text_label.set_selectable(True)
        text_label.set_line_wrap(True)
        if input:
            message_box.pack_start(avatar, False, True, 5)
        else:
            text_label.set_justify(Gtk.Justification.RIGHT)
            message_box.pack_end(avatar, False, True, 5)
        message_box.pack_start(text_label, True, False, 5)
        self.chat_box.pack_start(message_frame, False, True, 5)

    def regy_date(self, *args, **kwargs):
        self.login_win.hide()
        storage = redis.StrictRedis()  #подключаемся к мем кэшу. ссылка на доступ к базе данных
        try:
            self.login_win = str(storage.get("login"))
            self.password = str(storage.get("password"))
        except:
            redis.RedisError
            print("Данных почемуто нет")
            Gtk.main_quit()
        else:
            self.__create_conntection()
            self.show_all()




def __create_conntection(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # self.sock.setblocking(0)
    self.sock.connect((HOST,PORT))
    result = self.connection.recv(2048)
    data = json.load(result.decode("utf-8")) #преобразуем строку обратно в объект при помощи лоад
    if data.get("status") != "OK":
        print(data.get("message"))
        Gtk.main_quit()
    else:
        data = json.dumps({"login": self.login, "password": self.password})
        self.connection.send(data.encode("utf-8"))
        self.__run()



    def __run(self):
        pass
        # self.epoll = select.epoll()
        # self.epoll.register(self.sock.fileno(), select.EPOLLIN)
