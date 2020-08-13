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


def train_default(features_file, model_path = None, feature_cols = ['exposure_time', 'shutter_speed', 'brightness', 'iso_speed'], label ='label'):
    # load data
    all_features = pd.read_csv(features_file)
    # split dataset in features and target variable
    X = all_features[feature_cols]  # Features
    y = all_features[label]  # Target variable

    # split X and y into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    clf = train(X_train, y_train, model_path = model_path, persist = True)
    return {'model': clf, 'data': {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}}


if __name__ == '__main__':
    features_file = "../../data/processed/training-features.txt"
    model_path = '../../models/{}_logreg-clr.joblib'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    train_default(features_file, model_path = model_path)