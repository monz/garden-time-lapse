import os
import pandas as pd
import numpy as np

from PIL import Image, ExifTags
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from datetime import datetime
from joblib import dump
from src.features import build_features


def train(X_train, y_train, model_path = None, persist = False):
    # instantiate the model (using the default settings)
    clf = LogisticRegression()

    # fit the model with data
    clf.fit(X_train,y_train)

    # persist model to disk
    if persist:
        if model_path == None:
            model_path = './{}_logreg-clr.joblib'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        dump(clf, model_path)

    return clf


def train_default(img_path, model_path = None):
    exif_tags = {
        'exposure_time': 0x829a,
        # 'f_number': 0x829d,
        'shutter_speed': 0x9201,
        # 'aperture': 0x9202,
        'brightness': 0x9203,
        # 'focal_length': 0x920a,
        'iso_speed': 0x8827
    }

    # load data
    open_exif_data = build_features.get_exif_data(os.path.sep.join((img_path, "open")), exif_tags)
    open_exif_data['label'] = 0  # set label column to '0', open

    closed_exif_data = build_features.get_exif_data(os.path.sep.join((img_path, "closed")), exif_tags)
    closed_exif_data['label'] = 1  # set label column to '1', closed

    all_exif_data = pd.concat([open_exif_data, closed_exif_data], ignore_index = True)

    # split dataset in features and target variable
    feature_cols = ['exposure_time', 'shutter_speed', 'brightness', 'iso_speed']
    X = all_exif_data[feature_cols]  # Features
    y = all_exif_data.label  # Target variable

    # split X and y into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    clf = train(X_train, y_train, model_path = model_path, persist = True)
    return {'model': clf, 'data': {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}}


if __name__ == '__main__':
    img_path = "../../data/interim"
    model_path = '../../models/{}_logreg-clr.joblib'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    train_default(img_path, model_path = model_path)