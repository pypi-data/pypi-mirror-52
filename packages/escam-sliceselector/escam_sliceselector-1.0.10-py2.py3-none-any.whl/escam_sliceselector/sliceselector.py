from escam_toolbox.ui import *
from escam_toolbox.dicom import *
from escam_sliceselector.background import *
from tkinter import filedialog
import queue


NAME = 'Slice Selector'

VERSION = '1.0.10'  # Should be one patch further than VERSION file

ABOUT = """
{} v{}\n\n
Application for easily selecting and exporting individual slices from many DICOM series. The tool
assumes that each DICOM series is contained in its own sub-directory. If a directory has multiple 
series, the tool will load only the 1st series.\n\n
Author: Ralph Brecheisen, Clinical Data Scientist @ Department of Surgery, Maastricht
University Medical Center, The Netherlands\n
Email: r.brecheisen@maastrichtuniversity.nl
""".format(NAME, VERSION)


class SliceSelector(MainWindow):

    def __init__(self, master):
        super(SliceSelector, self).__init__(master, 'Slice Selector v{}'.format(VERSION), 1000, 800)
        self.add_button(name='open_dir_button', text='Open directory...', callback=self.open_dir)
        self.add_label(name='window_level_slider_label', text='Window level')
        self.add_slider(name='window_level_slider', callback=self.window_level_changed)
        self.add_label(name='window_width_slider_label', text='Window width')
        self.add_slider(name='window_width_slider', callback=self.window_width_changed)
        self.add_button(name='reset_window_level_and_width_button', text='Reset level/width', callback=self.reset_window_level_and_width)
        self.add_label(name='select_slice_label', text='Select slice')
        self.add_slider(name='select_slice_slider', callback=self.selected_slice_changed)
        self.add_button(name='set_target_dir_button', text='Select target directory...', callback=self.open_target_dir)
        self.add_button(name='prev_slice_button', text='Previous slice (^)', callback=self.prev_slice)
        self.add_button(name='next_slice_button', text='Next slice (v)', callback=self.next_slice)
        self.add_button(name='prev_image_button', text='Previous image (<)', callback=self.prev_image)
        self.add_button(name='next_image_button', text='Next image (>)', callback=self.next_image)
        self.add_label(name='file_name_format_label', text='Select file name format')
        self.add_combobox(name='file_name_format_cbx', items=[
            'Manually specify file name',
            'Use patient ID',
            'Use patient\'s name',
        ])
        self.add_button(name='save_slice_button', text='Save slice...', callback=self.save_slice)
        self.add_quit_and_about_buttons(ABOUT)
        self.queue = queue.Queue()
        self.thread = None
        self.image = None
        self.image_list = None
        self.selected_idx = 0
        self.selected_image = 0
        self.target_dir = None

    def open_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.thread = LoadImagesProcess(self.queue, directory)
            self.thread.start()
            self.check_thread_periodically()

    def open_target_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.target_dir = directory
        else:
            self.target_dir = None

    def window_level_changed(self, value):
        if self.image:
            self.image.set_window_level(int(value))
            self.render_slice(self.selected_idx)

    def window_width_changed(self, value):
        if self.image:
            self.image.set_window_width(int(value))
            self.render_slice(self.selected_idx)

    def reset_window_level_and_width(self):
        if self.image:
            self.image.reset_window_level_and_width()
            self.update_window_level_slider()
            self.update_window_width_slider()
            self.render_slice(self.selected_idx)

    def selected_slice_changed(self, value):
        if self.image:
            self.selected_idx = int(value)
            self.render_slice(self.selected_idx)

    def prev_slice(self):
        self.selected_idx -= 1
        self.selected_idx = max(0, self.selected_idx)
        self.render_slice(self.selected_idx)

    def next_slice(self):
        self.selected_idx += 1
        self.selected_idx = min(self.selected_idx, self.image.nr_slices - 1)
        self.render_slice(self.selected_idx)

    def prev_image(self):
        if self.image:
            self.selected_image -= 1
            self.selected_image = max(0, self.selected_image)
            self.image = self.image_list.get(self.selected_image)
            self.log_area.log_text(self.image.directory)
            self.update_window_level_slider()
            self.update_window_width_slider()
            self.update_select_slice_slider_and_render_image()

    def next_image(self):
        if self.image:
            self.selected_image += 1
            self.selected_image = min(self.selected_image, self.image_list.nr_images - 1)
            self.image = self.image_list.get(self.selected_image)
            self.log_area.log_text(self.image.directory)
            self.update_window_level_slider()
            self.update_window_width_slider()
            self.update_select_slice_slider_and_render_image()

    def save_slice(self):
        if not self.target_dir:
            self.show_msg('Select target directory first!')
            return
        if not self.image:
            self.show_msg('Load and select image first!')
            return
        file_name = None
        current_text = self.get('file_name_format_cbx').get()
        if current_text == 'Use patient ID':
            file_name = '{}.dcm'.format(self.image.patient_id)
        elif current_text == 'Use patient\'s name':
            file_name = '{}.dcm'.format(self.image.patient_name)
        else:
            pass
        if not file_name:
            file_name = filedialog.asksaveasfilename(initialdir=self.target_dir)
            if not file_name:
                self.show_msg('You must manually specify a file name or choose a different format option')
                return
            else:
                if not file_name.endswith('.dcm'):
                    file_name = file_name + '.dcm'
        file_path = os.path.join(self.target_dir, file_name)
        self.image.save_slice_as(self.selected_idx, file_path)
        self.show_msg('Saved slice {} to file {}'.format(self.selected_idx, file_path))

    def render_image(self):
        self.log_area.log_text(self.image.directory)
        x = self.image.nr_slices - 1
        y = int(x / 2.0)
        self.selected_idx = y
        self.update_select_slice_slider(x, y)
        self.update_window_level_slider()
        self.update_window_width_slider()
        self.render_slice(self.selected_idx)

    def update_select_slice_slider(self, x, y):
        self.get('select_slice_slider').configure(from_=0, to=x)
        self.get('select_slice_slider').set(y)

    def update_window_level_slider(self):
        self.get('window_level_slider').configure(from_=self.image.hu_min, to=self.image.hu_max)
        self.get('window_level_slider').set(self.image.window_level)

    def update_window_width_slider(self):
        self.get('window_width_slider').configure(from_=self.image.hu_min, to=self.image.hu_max)
        self.get('window_width_slider').set(self.image.window_width)

    def update_select_slice_slider_and_render_image(self):
        if self.image:
            x = self.image.nr_slices - 1
            y = int(x / 2.0)
            self.get('select_slice_slider').configure(to=x)
            self.get('select_slice_slider').set(y)
            self.selected_idx = y
            self.render_slice(self.selected_idx)

    def render_slice(self, idx):
        if self.image:
            self.get('select_slice_slider').set(idx)
            self.main_area.set_image(self.image.get_slice_as_image(idx))

    def check_thread_periodically(self, show_message=False):
        self.check_queue()
        if self.thread.is_alive():
            self.master.after(100, self.check_thread_periodically)
        else:
            if show_message:
                self.show_msg('Finished!')
            self.image_list = self.thread.get_image_list()
            self.thread = None
            if self.image_list.nr_images > 0:
                self.image = self.image_list.get(self.selected_image)
                self.render_image()

    def check_queue(self):
        while self.queue.qsize():
            try:
                message = self.queue.get(0)
                self.log_area.log_text(message)
            except queue.Empty:
                pass

    def on_key_press(self, event):
        if event.keysym == 'Right':
            self.next_image()
        elif event.keysym == 'Left':
            self.prev_image()
        elif event.keysym == 'Up':
            self.prev_slice()
        elif event.keysym == 'Down':
            self.next_slice()
        else:
            pass


def main():
    root = tk.Tk()
    SliceSelector(root)
    root.mainloop()


if __name__ == '__main__':
    main()
