import os
import pydicom
import SimpleITK as sitk
import PIL.Image


def is_dicom_file(file_path):
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, "rb") as f:
            return f.read(132).decode("ASCII")[-4:] == "DICM"
    except:
        return False


class DicomSeriesProgressCommand(sitk.Command):

    def __init__(self, po, listener):
        super(DicomSeriesProgressCommand, self).__init__()
        self.listener = listener
        self.po = po

    def Execute(self):
        self.listener.on_slice_loaded(self.po.GetProgress())


########################################################################################################################
class DicomSeries(object):

    def __init__(self, listener):
        self.listener = listener
        self.command = None
        self.first = True
        self.directory = None
        self.files = []
        self.patient_id = None
        self.patient_name = None
        self.hu_min = 0
        self.hu_max = 0
        self.image = None
        self.window_level = 0
        self.window_level_org = 0
        self.window_width = 0
        self.window_width_org = 0

    def load_from_directory(self, directory):
        self.directory = directory
        reader = sitk.ImageSeriesReader()
        self.command = DicomSeriesProgressCommand(reader, self.listener)
        reader.AddCommand(sitk.sitkProgressEvent, self.command)
        self.files = reader.GetGDCMSeriesFileNames(directory)
        reader.SetFileNames(self.files)
        image = reader.Execute()
        p = pydicom.read_file(self.files[0])
        self.patient_id = p.PatientID
        self.patient_name = p.PatientName
        min_max = sitk.MinimumMaximumImageFilter()
        min_max.Execute(image)
        self.hu_min = min_max.GetMinimum()
        self.hu_max = min_max.GetMaximum()
        self.window_level_org = self.hu_min + (self.hu_max - self.hu_min) / 2
        self.window_level = self.window_level_org
        self.window_width_org = self.hu_max - self.hu_min
        self.window_width = self.window_width_org
        self.image = image

    def set_window_level(self, window_level):
        self.window_level = window_level

    def set_window_width(self, window_width):
        self.window_width = window_width

    def reset_window_level_and_width(self):
        self.window_level = self.window_level_org
        self.window_width = self.window_width_org

    def get_slice_as_image(self, idx=0):
        size = self.image.GetSize()
        print('size: [{}, {}], idx: {}'.format(size[0], size[1], idx))
        # data = sitk.RegionOfInterest(self.image, (size[0], size[1], idx))
        data = self.image[0:size[0], 0:size[1], idx]
        data = sitk.GetArrayFromImage(data)
        x_min = self.window_level - self.window_width / 2
        x_max = self.window_level + self.window_width / 2
        data[data < x_min] = x_min
        data[data > x_max] = x_max
        data = data - x_min
        data = data / (x_max - x_min)
        data = 255 * data
        data = data.astype('int8')
        image = PIL.Image.fromarray(data)
        return image

    def save_slice_as(self, idx, file_path):
        p = pydicom.read_file(self.files[idx])
        p.save_as(file_path)

    @property
    def nr_rows(self):
        if self.image:
            size = self.image.GetSize()
            return size[0]
        return None

    @property
    def nr_columns(self):
        if self.image:
            size = self.image.GetSize()
            return size[1]
        return None

    @property
    def nr_slices(self):
        if self.image:
            size = self.image.GetSize()
            return size[2]
        return None

    def info(self):
        info = 'IMAGE INFO:'
        info += 'nr. rows: {}'.format(self.nr_rows) + '\n'
        info += 'nr. columns: {}'.format(self.nr_columns) + '\n'
        info += 'nr. slices: {}'.format(self.nr_slices) + '\n'
        info += 'level: {}'.format(self.window_level) + '\n'
        info += 'width: {}'.format(self.window_width) + '\n'
        info += 'storage dir: {}'.format(self.directory) + '\n'
        info += 'HU min: {}'.format(self.hu_min) + '\n'
        info += 'HU max: {}'.format(self.hu_max) + '\n'
        return info


########################################################################################################################
class DicomSeriesList(object):

    def __init__(self, listener, min_nr_images=10):
        self.directory = None
        self.images = []
        self.images_cache = {}
        self.listener = listener
        self.min_nr_images = min_nr_images

    def has_dicoms(self, directory):
        """ The directory should have multiple DICOMs for this method to return
        True. If a single (or just a few) DICOMs are contained then we skip the
        directory. """
        count = 0
        for f in os.listdir(directory):
            f = os.path.join(directory, f)
            if is_dicom_file(f):
                count += 1
            if count > self.min_nr_images:
                return True
        return False

    def load_from_directory(self, directory):
        """ We should make a few assumptions here. First of all, we expect directory to be the root
        directory containing a number of child directories, each containing a single DICOM series
        consisting of multiple slices. Given this assumption we should not use os.walk() because it
        works recursively and we cannot easily calculate how many child directories there are.
        """
        self.directory = directory
        # First count how many DICOM series there are so the listener can set its progress
        # bar accordingly.
        count = 0
        for d in os.listdir(self.directory):
            d = os.path.join(self.directory, d)
            if os.path.isdir(d) and self.has_dicoms(d):
                count += 1
        # Notify listener that we found 'count' DICOM series
        self.listener.nr_images_found(count)
        # Next, do the real loading
        for d in os.listdir(self.directory):
            d = os.path.join(self.directory, d)
            if os.path.isdir(d) and self.has_dicoms(d):
                self.images.append(d)
                self.images_cache[len(self.images) - 1] = None
                self.listener.on_image_loaded(d)
        return len(self.images)

    @property
    def nr_images(self):
        return len(self.images)

    def get(self, index):
        if self.nr_images > 0 and index < self.nr_images:
            image = self.images_cache[index]
            if image:
                print('[{}] found cached image'.format(index))
                return image
            else:
                d = self.images[index]
                image = DicomSeries(self.listener)
                try:
                    print('[{}] loading {}'.format(index, d))
                    image.load_from_directory(d)
                    self.images_cache[index] = image
                except:
                    print('[{}] ERROR: could not load image {}. Removing it and taking the next one'.format(index, d))
                    # We need to remove this image from the list so we don't try
                    # to load it again later. Then we call self.get(index) again and return the image.
                    del self.images[index]
                    if index == len(self.images):
                        index -= 1
                    return self.get(index)
                return image
