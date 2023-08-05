import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
from escam_toolbox.process import Worker, WorkerProcess


def center_and_raise_window(top_level, settings=None):
    top_level.update()
    if not settings:
        w = top_level.winfo_width()
        h = top_level.winfo_height()
    else:
        w = settings.get('width', top_level.winfo_screenwidth())
        h = settings.get('height', top_level.winfo_screenheight())
    x = int((top_level.winfo_screenwidth() - w) / 2)
    y = int((top_level.winfo_screenheight() - h) / 2)
    top_level.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    top_level.attributes('-topmost', 1)
    top_level.attributes('-topmost', 0)


########################################################################################################################
class MainWindow(tk.PanedWindow):

    def __init__(self, master, title, width, height, control_area=True, main_area=True, log_area=True, h_ratio=None, v_ratio=None):
        super(MainWindow, self).__init__(master, bg='gray')
        master.geometry('{}x{}'.format(width, height))
        self.pack(fill=tk.BOTH, expand=1)
        self.settings = Settings()
        master.title(title)
        master.update()
        w = self.settings.get('width', width)
        h = self.settings.get('height', height)
        self.h_ratio = h_ratio
        self.v_ratio = v_ratio
        if not self.h_ratio:
            self.h_ratio = self.settings.get('h_ratio', [.2, .8])
        if not self.v_ratio:
            self.v_ratio = self.settings.get('v_ratio', [.8, .2])
        if control_area and main_area and log_area:
            self.control_area = tk.Frame(self, width=int(self.h_ratio[0] * w), height=int(h))
            self.add(self.control_area)
            self.x = tk.PanedWindow(orient=tk.VERTICAL, bg='gray')
            self.add(self.x)
            self.main_area = ImageCanvas(self.x, width=int(self.h_ratio[1] * w), height=int(self.v_ratio[0] * h))
            self.x.add(self.main_area)
            self.log_area = LogArea(self.x, width=int(self.h_ratio[1] * w), height=int(self.v_ratio[1] * h))
            self.x.add(self.log_area)
            pass
        elif control_area and main_area:
            self.control_area = tk.Frame(self, width=int(self.h_ratio[0] * w))
            self.add(self.control_area)
            self.main_area = ImageCanvas(self, width=int(self.h_ratio[1] * w))
            self.add(self.main_area)
            pass
        elif control_area and log_area:
            self.control_area = tk.Frame(self, width=int(self.h_ratio[0] * w))
            self.add(self.control_area)
            self.log_area = LogArea(self, width=int(self.h_ratio[1] * w))
            self.add(self.log_area)
            pass
        elif control_area:
            self.control_area = tk.Frame(self)
            self.add(self.control_area)
            pass
        else:
            raise RuntimeError('Areas cannot ALL be disabled!')
        self.about_text = None
        self.components = {}
        self.worker = Worker(self)
        center_and_raise_window(self.master, self.settings)
        # Make sure to bind the resize event AFTER restoring the window!
        self.control_area.bind('<Configure>', self.on_resize_control_area)
        self.main_area.bind('<Configure>', self.on_resize_main_area)
        self.bind('<Configure>', self.on_resize)
        self.master.bind('<Key>', self.on_key_press)
        self.master.protocol('WM_DELETE_WINDOW', self.on_quit)

    def add_label(self, name, text):
        label = tk.Label(self.control_area, text=text, anchor=tk.W, justify=tk.LEFT)
        self.add_component(name, label)

    def add_button(self, name, text, callback):
        button = tk.Button(self.control_area, text=text,  command=callback)
        self.add_component(name, button)

    def add_quit_button(self):
        button = tk.Button(self.control_area, text='Quit', command=self.on_quit)
        button.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.W)

    def add_about_button(self, about_text):
        self.about_text = about_text
        button = tk.Button(self.control_area, text='About...', command=self.show_about)
        button.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.W)

    def add_quit_and_about_buttons(self, about_text):
        self.add_quit_button()
        self.add_about_button(about_text)

    def add_text_field(self, name, default=None):
        text_field = tk.Entry(self.control_area)
        if default:
            text_field.insert(tk.END, default)
        self.add_component(name, text_field)

    def add_slider(self, name, callback=None):
        slider = tk.Scale(self.control_area, from_=0, to=100, orient=tk.HORIZONTAL, command=callback)
        self.add_component(name, slider)

    def add_checkbox(self, name, text, var, callback):
        check_box = tk.Checkbutton(self.control_area, text=text, variable=var, command=callback)
        self.add_component(name, check_box)

    def add_combobox(self, name, items):
        combo_box = ttk.Combobox(self.control_area, values=items)
        self.add_component(name, combo_box)

    def add_progressbar(self, name, **kwargs):
        if 'orient' not in kwargs.keys():
            kwargs['orient'] = 'horizontal'
        if 'mode' not in kwargs.keys():
            kwargs['mode'] = 'determinate'
        progressbar = ttk.Progressbar(self.control_area, **kwargs)
        self.add_component(name, progressbar)

    def get(self, name):
        return self.components[name]

    def add_component(self, name, component):
        if name not in self.components.keys():
            self.components[name] = component
            component.pack(side=tk.TOP, fill=tk.X, anchor=tk.W)
        else:
            raise RuntimeError('Name {} already in component list'.format(name))

    def show_about(self):
        # TODO: Message box disappears behind main window
        messagebox.showinfo('About', message=self.about_text)

    @staticmethod
    def show_msg(message):
        messagebox.showinfo('Info', message=message)

    def on_quit(self):
        print('Quiting application....')
        self.settings.save()
        self.master.destroy()

    def on_resize(self, event):
        self.settings.set('width', event.width)
        self.settings.set('height', event.height)

    def on_resize_control_area(self, event):
        self.h_ratio = [
            float(event.width / self.winfo_width()),
            float((self.winfo_width() - event.width) / self.winfo_width())
        ]
        self.settings.set('h_ratio', self.h_ratio)

    def on_resize_main_area(self, event):
        self.v_ratio = [
            float(event.height / self.winfo_height()),
            float((self.winfo_height() - event.height) / self.winfo_height())
        ]
        self.settings.set('v_ratio', self.v_ratio)

    def on_worker_update(self, message):
        self.log_area.log_text(message)

    def on_key_press(self, event):
        pass


########################################################################################################################
class LogArea(ScrolledText):

    def __init__(self, master, **kwargs):
        super(LogArea, self).__init__(master, wrap=tk.WORD, **kwargs)

    def log_text(self, text):
        timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f] ')
        text = timestamp + text + '\n'
        self.insert(tk.INSERT, text)
        self.see('end')


########################################################################################################################
class ImageCanvas(tk.Frame):

    def __init__(self, master, **kwargs):
        super(ImageCanvas, self).__init__(master, **kwargs)
        self.image_label = tk.Label(self, image=None)
        self.image_label.pack(fill=tk.BOTH, expand=1)
        self.image = None
        self.image_tk = None
        self.master.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        self.set_image(self.image)

    def set_image(self, image):
        if image:
            self.image = image
            # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
            # self.image.thumbnail((self.master.winfo_width(), self.master.winfo_height()), PIL.Image.ANTIALIAS)
            w, h = self.resize_image(self.image)
            image = self.image.resize((w, h), PIL.Image.ANTIALIAS)
            self.image_tk = PIL.ImageTk.PhotoImage(image)
            # https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
            self.image_label.configure(image=self.image_tk)

    def resize_image(self, image):
        w, h = self.winfo_width(), self.winfo_height()
        # print('resize_image: w = {}, h = {} (canvas)'.format(w, h))
        if image.width > image.height:
            ratio = w / image.width
        else:
            ratio = h / image.height
        w, h = int(image.width * ratio), int(image.height * ratio)
        # print('resize_image: w = {}, h = {} (image)'.format(w, h))
        return w, h


########################################################################################################################
class Settings(object):

    def __init__(self):
        # When this class is instantiated, it should check if a 'settings.json'
        # exists in the current directory. If not, it will be created. If so, its
        # contents will be loaded.
        self.settings = {}
        try:
            os.stat('settings.json')
            self.settings = json.load(open('settings.json', 'r'))
            print('settings.json:')
            print(json.dumps(self.settings, indent=4))
        except FileNotFoundError:
            json.dump(self.settings, open('settings.json', 'w'))

    def set(self, name, value):
        self.settings[name] = value

    def get(self, name, default=None):
        if name not in self.settings.keys():
            return default
        return self.settings[name]

    def save(self):
        json.dump(self.settings, open('settings.json', 'w'))

    @staticmethod
    def clear():
        try:
            os.remove('settings.json')
        except FileNotFoundError:
            pass
