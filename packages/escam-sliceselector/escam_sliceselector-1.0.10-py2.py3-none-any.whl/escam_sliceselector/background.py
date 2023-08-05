from escam_toolbox.dicom import DicomSeriesList
import threading


class LoadImagesProcess(threading.Thread):

    def __init__(self, queue, directory):
        super(LoadImagesProcess, self).__init__()
        self.queue = queue
        self.directory = directory
        self.image_list = DicomSeriesList(self)

    def nr_images_found(self, count):
        pass

    # This thread should implement this method because it will be called for each
    # image that is loaded
    def on_image_loaded(self, directory):
        self.queue.put(directory)

    def on_slice_loaded(self, progress):
        self.queue.put('Loading slice progress: {}'.format(progress))

    def run(self):
        """ This method will execute the load_from_directory() function of a DicomSeries
        object. """
        self.image_list.load_from_directory(self.directory)

    def get_image_list(self):
        return self.image_list
