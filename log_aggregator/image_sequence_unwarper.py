from PIL import Image
from tqdm import tqdm
#dirty workaround to fix api bug
tqdm.monitor_interval = 0

import os
import re
import struct




class Img_stack_wrapper():
        def __init__(self, size_x, size_y, data_type, camera_type, stack_path,
                     frame_offset=0, endianess=None):
            """

            :param size_x: Width of one frame of the frame stack/raw file
            :param size_y: Height of one frame of the frame stack/ raw file
            :param data_type: Give information on the type of data composing one pixel of the image, for now only
            support rgb8
            :param camera_type: Let us know which camera of the robot outputed the raw file assigned to this wrapper
            object
            :param stack_path: Path to the  raw file assigned to this wrapper
            :param frame_offset: If some data is interlaced between frames, we inform here the size of this data
            :param endianess: optional and not used for now but can be relevant for further developments
            """
            self.valid = True
            self.camera_type = camera_type

            self.size_x = size_x
            self.size_y = size_y
            self.stack_path = stack_path

            if data_type == 'rgb8':
                self.bytes_per_pixel = 3
                self.data_type = 'rgb'
            else:
                raise Exception("Type error: %s is an unknown data type" % (data_type))

            try:
                self.fp = open(stack_path, "rb")
            except IOError:
                print("Video stack file not found")
                self.valid = False

            if self.valid:
                self.stack_size_byte = os.path.getsize(self.stack_path)
                self.pixel_per_frame = self.size_x * self.size_y
                self.byte_per_frame = self.pixel_per_frame * self.bytes_per_pixel
                self.frame_offset = frame_offset
                self.valid_frames = self.stack_size_byte / (self.byte_per_frame + self.frame_offset)
                self.endianess = endianess
            else:
                self.valid_frames = 0
            self.read = 0

        def __del__(self):
            """
            If the assigned raw file to a wrapper instance is considered as correct a file pointer is opened on this
            same raw file, we need to close it at object destruction
            """
            if self.valid:
                self.fp.close()

        def get_nb_read_frames(self):
            """
            Getter
            :return: the number of frames already requested read by the wrapper from the raw file
            """
            return str(self.read)

        def get_next_raw_img_and_extra_data(self):
            """
            return the next raw image data and if the interlacing data exist in the raw file assigned to this wrapper
            it will be also returned
            :return: next raw frame data or next raw frame data and next raw i
            """
            if (self.read < self.valid_frames):
                img_binary = self.fp.read(self.byte_per_frame)
                self.read += 1
                if (self.frame_offset > 0):
                    extra_data = self.fp.read(self.frame_offset)
                    return img_binary, extra_data
                return img_binary
            if (self.frame_offset > 0):
                return None, None
            else:
                return None

        def get_percent_read(self):
            """
            Getter
            :return: The percent of frames already read with the method get_next_raw_img_and_extra_data
            """
            return (self.read / float(self.valid_frames)) * 100

        def is_valid(self):
            """
            Getter
            :return: Let the object user know if the raw data assigned to the wrapper is valid to be used, this of
            course does not give any warranty on the data quality
            """
            return self.valid

        def get_camera_type(self):
            """
            Getter
            :return: The camera name of the robot which outputed the raw file assigned to this wrapper instance
            """
            return self.camera_type


def gen_stack_wrapper(video_stack_path):
    """
    Assing and configure a Img_stack_wrapper object with the given raw file/stack path given as argument
    :param video_stack_path: path to the raw file/stack containing frames from video. The raw filename should be formated as
    video_CAMERATYPE_FRAMEWIDTH_FRAMEHEIGHT_ENDIANESS_TYPEOFDATA
    The only type of data supported for now is rgb8
    :return: A configured Img_stack_wrapper object configured with the given raw file/stack path given as argument
    """
    # number of info contained in filename
    info_count = 6
    # size of data interlaced beetween frames, for now according to our usage a hard setted value is enough, it can
    # become a function argument for further developments
    offset = 8
    stack_filename = video_stack_path.split('/')[-1]
    info_list = stack_filename.split('_')

    if len(info_list) != info_count:
        return None

    camera_type = info_list[1]
    size_x = int(info_list[2])
    size_y = int(info_list[3])
    endianess = info_list[4]
    data_type = info_list[5]
    stack_wrapper = Img_stack_wrapper(size_x, size_y, data_type, camera_type, video_stack_path,
                                frame_offset=offset, endianess=endianess)
    return stack_wrapper


def get_video_file_path_list(log_path):
    """
    Allow to gather a list of path of file contained in the log_path following the "video_*" patern
    :param log_path: Path where to search the video files, in our case it will be always ros log path
    :return: a list of paths corresponding to raw "video" files
    """
    log_content = os.listdir(log_path)
    regex = re.compile('video_*')
    video_stack_path_list = []
    for filename in log_content:
        if (regex.search(filename)):
            video_stack_path_list.append(log_path + '/' + filename)

    return video_stack_path_list


def gen_stack_wrapper_list(video_stack_path_list):
    """
    Generate a Img_stack_wrapper obect for each path contained in the video_stack_path_list.
    :param video_stack_path_list: A list of paths to video files
    :return: A list of Img_stack_wrapper objects
    """
    wrapper_list = []
    for element in video_stack_path_list:
        wrapper = gen_stack_wrapper(element)
        wrapper_list.append(wrapper)
    return wrapper_list

def gen_images_from_wrapper_list(img_stack_wrapper_list, log_path, extra_data_present=False):
    """
    Launch the image generation process for each valid Img_stack_wrapper object contained in the img_stack_wrapper_list
    argument.
    :param img_stack_wrapper_list: A list of Img_stack_wrapper objects already configured to a raw/stack video file
    :param log_path: Path where the wrapper generated images will be outputed, named log_path because in our case
    it should alays be in the ros log directory, naming can be change upon further developments
    :param extra_data_present: Indicate if extra data as been inserted between frames
    """
    for wrapper in img_stack_wrapper_list:
        if wrapper.is_valid():
            print ('Unwarping ' + wrapper.get_camera_type() + '\n')
            gen_images_from_wrapper(wrapper, log_path, extra_data_present=extra_data_present)


def gen_images_from_wrapper(img_stack_wrapper, log_path, extra_data_present=False):
    """
    Create a directory named as Img_stack_wrapper camera_type attribute
    Request all available frames from the Img_stack_wrapper object and save them as png files under the previously
    created directory
    The file naming follow this pattern
    FRAMENUMBER(-EXTRADATA).png
    :param img_stack_wrapper: A valid img_stack_wrapper object
    :param log_path: Path where the wrapper generated images will be outputed, named log_path because in our case
    it should always be in the ros log directory, naming can be change upon further developments
    :param extra_data_present: Indicate if extra data as been inserted between frames
    """
    img_path = log_path + '/' + img_stack_wrapper.camera_type
    subdir_exist = os.path.exists(img_path)

    if (extra_data_present):
        raw_img, extra_data = img_stack_wrapper.get_next_raw_img_and_extra_data()
    else:
        raw_img = img_stack_wrapper.get_next_raw_img_and_extra_data()

    pbar = tqdm(total=100)
    last_percent_read = 0

    while raw_img is not None:
        if not subdir_exist:
            os.mkdir(img_path)
            subdir_exist = True

        filename = img_stack_wrapper.get_nb_read_frames() + "_"
        if (extra_data_present):
            filename += str(struct.unpack('d', extra_data)[0])
        filename += ".png"

        dest_path = img_path + '/' + filename
        pil_img = Image.frombytes("RGB", (img_stack_wrapper.size_x, img_stack_wrapper.size_y), raw_img, decoder_name='raw')
        pil_img.save(dest_path, optimize=True)
        
        new_percent_read = img_stack_wrapper.get_percent_read()
        progress = new_percent_read - last_percent_read
        last_percent_read = new_percent_read
        pbar.update(progress)

        if (extra_data_present):
            raw_img, extra_data = img_stack_wrapper.get_next_raw_img_and_extra_data()
        else:
            raw_img = img_stack_wrapper.get_next_raw_img_and_extra_data()

    del(pbar)
    print('\n')


def convert_video_to_image(log_path, keep_raw):
    """
    Find raw/stack video files, and convert their content to png files under subdirectories named depending the raw file
    name.
    :param log_path: Path where to search for raw/stack video files, named log_path because in our case
    it will always be the path to the ros log directory, naming can be change upon further developments
    """
    video_stack_path_list = get_video_file_path_list(log_path)
    wrapper_list = gen_stack_wrapper_list(video_stack_path_list)
    gen_images_from_wrapper_list(wrapper_list, log_path, extra_data_present=True)
    if keep_raw is False:
        for file in video_stack_path_list:
            os.remove(file)

