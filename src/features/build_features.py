import pandas as pd
import numpy as np
import os
from PIL import Image, ExifTags


def __get_exif_data(file_path, exif_tags):
    img = Image.open(file_path)
    img_exif = img.getexif()

    if img_exif is None:
        return
    else:
        exif_data = {}
        for tag in exif_tags:
            exif_data.update({
                tag: img_exif.get(exif_tags[tag])
            })
        return exif_data


def get_exif_data(path, exif_tags):
    exif_data = np.empty(0)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            exif_data = np.append(exif_data, __get_exif_data(os.path.sep.join((dirpath, file)), exif_tags))
    return pd.DataFrame.from_dict(data=exif_data.tolist())
