from pathlib import Path
from datetime import datetime
import piexif
import re
import os
import time


def filename2date(str_filename):
    """

    :param str_filename:
    :return:
    """
    re_date_new = re.search(r"IMG-(\d\d\d\d)(\d\d)(\d\d)-WA", str_filename, flags=0)
    return datetime(int(re_date_new[1]), int(re_date_new[2]), int(re_date_new[3]), 0, 0, 0)


def set_image_dates(path_file, new_date):
    """

    :param path_file:
    :param new_date:
    """
    # exif
    str_date = new_date.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict = piexif.load(path_file)
    exif_dict['0th'][piexif.ImageIFD.DateTime] = str_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = str_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = str_date
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, path_file)

    # access mod times
    tup_date = time.mktime(new_date.timetuple())
    os.utime(path_file, (tup_date, tup_date))


def get_filelist(dir_imgs, recursive=False):
    """

    :param dir_imgs:
    :param recursive:
    :return:
    """
    pattern = r"IMG-" + "[0-9]" * 8 + "-WA" + "[0-9]" * 4 + ".jpg"  # whatsapp
    if recursive:
        pattern = r"**\\" + pattern

    if isinstance(dir_imgs, str):
        dir_imgs = Path(dir_imgs)
    return list(dir_imgs.glob(pattern))


def change_date_from_name(path_file):
    """

    :param path_file:
    """
    new_date = filename2date(path_file.name)
    print(f"Setting date {new_date} for {path_file.name}")
    set_image_dates(str(path_file), new_date)

