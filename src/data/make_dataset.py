# -*- coding: utf-8 -*-
import click
import logging
import os
import pandas as pd

from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from src.features import build_features


def __get_train_data_features(img_path, exif_tags):
    open_exif_data = build_features.get_exif_data(os.path.sep.join((img_path, "open")), exif_tags)
    open_exif_data['label'] = 0  # set label column to '0', open

    closed_exif_data = build_features.get_exif_data(os.path.sep.join((img_path, "closed")), exif_tags)
    closed_exif_data['label'] = 1  # set label column to '1', closed

    all_exif_data = pd.concat([open_exif_data, closed_exif_data], ignore_index=True)

    return all_exif_data


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw/raw/) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # extract all images' timestamps
    # UNIX tools would be way faster than the following
    timestamps_file = os.path.sep.join((output_filepath, "image-timestamps.txt"))
    timestamps = build_features.extract_timestamps(os.path.sep.join((input_filepath, "raw/"))) # trailing slash required due to symlink
    pd.DataFrame(timestamps, columns=['timestamp']).to_csv(timestamps_file, header=False, index=False)

    # extract features for learning logistic-regression model
    features_file = os.path.sep.join((output_filepath, "training-features.txt"))

    training_features = __get_train_data_features(os.path.sep.join((input_filepath, "by-class")), build_features.EXIF_TAGS)
    training_features.to_csv(features_file, header=True, index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()