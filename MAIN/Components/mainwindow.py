import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from sqlite3 import Error
from configwindow import ConfigWindow
from kitchenwindow import KitchenWindow
from createorders import CreateOrders
from Database import Database

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()


        self.win_width = 600
        self.win_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(
            f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(1, 1)
        self.title('Ресторан')

        self.m_frame = ttk.Frame(self, width=600, height=400)
        self.m_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        icon_path = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'assets', 'icon_m.png')
        self.icon_image = Image.open(icon_path)
        self.python_image = ImageTk.PhotoImage(self.icon_image)

        self.iconphoto(True, self.python_image)

        self.menubar = tk.Menu(self.m_frame)
        self.filebar = tk.Menu(self.menubar, tearoff=0)
        self.filebar.add_cascade(
            label="Кухня", command=self.kitchen_win, state=tk.DISABLED)
        self.filebar.add_cascade(
            label="Создать заказ", command=self.customer_win, state=tk.DISABLED)
        self.filebar.add_cascade(
            label="Редактировать Ресторан/Меню", command=self.config_window)
        self.filebar.add_separator()
        self.filebar.add_cascade(label="Выход", command=self.quit)
        self.menubar.add_cascade(label="Файл", menu=self.filebar)




        self.config(menu=self.menubar)

        self.img = Image.open(os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'assets', 'main_win_ph.png'))
        self.img = self.img.resize((250, 250), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = tk.Label(
            self.m_frame,
            image=self.img,
            text="Ресторан",
            compound='top',
            font=("Helvetica Bold", 20)
        )
        self.panel.image = self.img
        self.panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.check_databases()

    def check_databases(self):
        try:
            self.fac_db = Database("restaurant.db")
            load_query = """SELECT * FROM menu_config"""
            res = self.fac_db.read_val(load_query)
            customer_state = tk.NORMAL if res else tk.DISABLED
            self.filebar.entryconfig(1, state=customer_state)

            load_query1 = """SELECT * FROM orders"""
            res1 = self.fac_db.read_val(load_query1)

            kitchen_state = tk.NORMAL if res1 else tk.DISABLED
            self.filebar.entryconfig(0, state=kitchen_state)

        except Error as e:
            print(e)

    def config_window(self):
        config_window = ConfigWindow(self, self.check_databases)
        config_window.grab_set()

    def kitchen_win(self):
        kitchen_win = KitchenWindow(self, self.check_databases)
        kitchen_win.grab_set()

    def customer_win(self):
        customer_win = CreateOrders(self, self.check_databases)
        customer_win.grab_set()



