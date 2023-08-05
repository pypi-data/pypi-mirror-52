from escam_toolbox.ui import *
import threading
import queue
import time


class ExampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        # self.window = MainWindow(root, title='Example App', width=800, height=600)
        # self.window.add_label(name='print_label', text='Click button below')
        # self.window.add_button(name='print_button', text='Click', callback=self.start_client)
        # self.window.add_quit_button()
        self.queue = queue.Queue()
        self.listbox = tk.Listbox(self, width=20, height=5)
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.button = tk.Button(self, text='Start', command=self.start_client)
        self.listbox.pack(padx=10, pady=10)
        self.progress_bar.pack(padx=10, pady=10)
        self.button.pack(padx=10, pady=10)
        self.thread = None

    def start_client(self):
        self.button.config(state='disabled')
        self.thread = ThreadedClient(self.queue)
        self.thread.start()
        self.periodic_check()

    def periodic_check(self):
        self.check_queue()
        if self.thread.is_alive():
            self.after(100, self.periodic_check)
        else:
            self.button.config(state='active')

    def check_queue(self):
        while self.queue.qsize():
            try:
                message = self.queue.get(0)
                self.listbox.insert('end', message)
                self.progress_bar.step(24)
            except queue.Empty:
                pass


class ThreadedClient(threading.Thread):

    def __init__(self, q):
        super(ThreadedClient, self).__init__()
        self.queue = q

    def run(self):
        for x in range(1, 5):
            time.sleep(2)
            message = 'Function %s finished...' % x
            self.queue.put(message)


def main():
    root = ExampleApp()
    # root.geometry('1000x800')
    root.mainloop()


if __name__ == '__main__':
    main()
