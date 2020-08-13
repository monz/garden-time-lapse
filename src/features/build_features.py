import pandas as pd
import numpy as np
import os
import re
import datetime

from PIL import Image, ExifTags


EXIF_TAGS = {
    'exposure_time': 0x829a,
    'shutter_speed': 0x9201,
    'brightness': 0x9203,
    'iso_speed': 0x8827
}

EXIF_TAGS_ALL = {
    'exposure_time': 0x829a,
    'f_number': 0x829d,
    'shutter_speed': 0x9201,
    'aperture': 0x9202,
    'brightness': 0x9203,
    'focal_length': 0x920a,
    'iso_speed': 0x8827
}

TIMESTAMP_PATTERN = re.compile("pic_(\d{10,}).jpg")


def __get_exif_data(file_path, exif_tags):
    img = Image.open(file_path)
    img_exif = img.getexif()

    if img_exif is None:
        return
    else:
        exif_data = {'file': file_path}
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


def __get_timestamp(filename):
    m = TIMESTAMP_PATTERN.match(filename)

    timestamp = None
    if m != None:
        timestamp = m.group(1)

    return timestamp

def extract_timestamps(path):
    timestamps = np.empty(0)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            timestamps = np.append(timestamps, __get_timestamp(file))
    timestamps.sort()
    return timestamps


def get_timestamps_in_range(timestamps, hour, frame=5):
    """
    Return timestamps which are in range of `hour` +/- `frame`, for each day.
    Starting at first day found in given timestamps, ending at last
    day found in given timestamps. Closest timestamp in the range of
    `hour` +/- `frame` will be selected.
        Parameters
        ----------
        timestamps : array_like
            Timestamps array.
        hour : int
            Given timestamps will be normalized to `hour` value, by setting
            the hour of the day to `hour` and reset all other values,
            e.g. minute, seconds to zero.
        frame : int, optional
            The range to look for timestamps +/- around the `hour` in seconds.  If `frame` is not
            given, it defaults to 5 seconds.
        Returns
        -------
        get_timestamp_in_range : ndarray
            Timestamps found in range of `hour` +/- `frame` for each day.
    """
    # get first and last entry
    first_timestamp = timestamps.head(1).iloc[0, 0]
    last_timestamp = timestamps.tail(1).iloc[0, 0]

    # get dates
    first_day = datetime.datetime.fromtimestamp(first_timestamp)
    last_day = datetime.datetime.fromtimestamp(last_timestamp)

    # get time range, total amount of days
    timedelta = last_day - first_day
    total_number_of_days = timedelta.days

    # we want one image for each day at 'hour' hour
    # therefore we search for images each day within a
    # range of +/- 'frame' minutes around 'hour' because image
    # capturing was not scheduled at 'hour' but images
    # were captured about every other minute

    # get start/end timestamp, first_day/last_day at noon
    first_day_center = first_day.replace(hour=hour, minute=0, second=0, microsecond=0)
    last_day_center = last_day.replace(hour=hour, minute=0, second=0, microsecond=0)

    # jump one day each iteration, 3600s*24h
    timestamps_selected = np.zeros(total_number_of_days)
    for idx, timestamp in enumerate(
            range(int(first_day_center.timestamp()), int(last_day_center.timestamp()), 3600 * 24)):

        # get our time frame
        start = timestamp - 60 * frame
        end = timestamp + 60 * frame

        time_frame = timestamps.where(
            np.logical_and(
                timestamps['timestamp'] >= start,
                timestamps['timestamp'] <= end) ).dropna()

        # when there is no image within this time range, continue with next day
        if (time_frame.empty):
            continue

        # select closest timestamp
        closest_ts_idx = time_frame['timestamp'].sub(timestamp).abs().idxmin()
        # save to list
        timestamps_selected[idx] = time_frame.loc[closest_ts_idx].values[0]

    # drop zero values, indicating empty values
    timestamps_selected = timestamps_selected[timestamps_selected > 0]

    # add to data frame, e.g. for convenient csv export
    timestamps_selected = pd.DataFrame(timestamps_selected, columns=['timestamp'], dtype=np.int64)

    return timestamps_selected