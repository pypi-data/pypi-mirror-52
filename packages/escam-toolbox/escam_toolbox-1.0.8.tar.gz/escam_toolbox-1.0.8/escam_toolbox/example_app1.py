from escam_toolbox.ui import *
from escam_toolbox.dicom import *
import queue
import threading
import time

"""
TODO:

- Remember window size, splitter positions and displayed image (both scan and slice)
- Scroll through scans and slices
- Button click triggers long-running process that periodically logs output

- [DONE] Load DICOM scan and show 1st slice
- [DONE] Rescale image to fit window
- [DONE] Show image
- [DONE] Button click shows logging
- [DONE] Create control, main and log areas
"""


class ExampleThread(threading.Thread):

    def __init__(self, queue):
        super(ExampleThread, self).__init__()
        self.queue = queue

    def run(self):
        for x in range(1, 5):
            time.sleep(2)
            self.queue.put('Finished iteration {}'.format(x))


class ExampleApp(object):

    def __init__(self, root):
        self.window = MainWindow(root, title='Example App', width=800, height=600)
        self.window.add_label(name='print_label', text='Click button below')
        self.window.add_button(name='print_button', text='Click', callback=self.print_it)
        self.window.add_button(name='image_button', text='Load Images', callback=self.load_images)
        self.window.add_button(name='clear_button', text='Clear Settings', callback=self.window.settings.clear)
        self.window.add_progressbar(name='progress')
        self.window.add_button(name='start_button', text='Start thread', callback=self.start_thread)
        self.window.add_quit_button()
        self.window.add_about_button('About text...')
        self.queue = queue.Queue()
        self.thread = None

    def start_thread(self):
        self.window.get('start_button').config(state='disabled')
        self.thread = ExampleThread(self.queue)
        self.thread.start()
        self.check_thread_periodically()

    def check_thread_periodically(self):
        self.check_queue()
        if self.thread.is_alive():
            self.window.master.after(100, self.check_thread_periodically)
        else:
            self.window.get('start_button').config(state='active')
            self.window.show_msg('Finished!')

    def check_queue(self):
        while self.queue.qsize():
            try:
                message = self.queue.get(0)
                self.window.log_area.log_text(message)
                self.window.get('progress').step(25)
            except queue.Empty:
                pass

    def print_it(self):
        self.window.log_area.log_text('Click!')

    def load_images(self):
        d = '/Users/Ralph/data/SliceSelector'
        dicom_series = DicomSeriesList(self)
        dicom_series.load_from_directory(d)
        dicom_image = dicom_series.get(0)
        self.window.main_area.set_image(dicom_image.get_slice_as_image(0))
        self.window.log_area.log_text('Loaded {} images'.format(dicom_series.nr_images))

    def on_image_loaded(self, d):
        print(d)

    def on_slice_loaded(self, progress):
        print('bla: {}'.format(progress))

    def nr_images_found(self, count):
        print(count)


def main():
    root = tk.Tk()
    root.geometry('1000x800')
    ExampleApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
