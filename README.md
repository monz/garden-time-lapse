home-garde-time-lapse
==============================

Image classification to sort out images which are unsuitable for creating a time lapse video. In this example unsuitable images show  *closed shutters*, *reflections*, etc. Before creating a time lapse video, selected images must be cleaned, such that there are only reasonable images considered for video creation.

## Notebooks Online Preview

> **Note:** I used interactive plots using [Plotly Dash](https://plotly.com/dash/). The plots do not render in the online preview. And as long as there is no data publicly available these plots will not work for you. Therefore, some plot previews have been added to the notebooks. I want to integrate [DVC](https://dvc.org/) and provide you some example data, properly. For now, have fun reading the notebooks!

1. [Project Context](https://nbviewer.jupyter.org/github/monz/garden-time-lapse/blob/master/notebooks/1.0-project-context.ipynb)

1. [Exploratory Data Analysis](https://nbviewer.jupyter.org/github/monz/garden-time-lapse/blob/master/notebooks/1.0-exploratory-data-analysis.ipynb)

1. [Model: Logistic Regression](https://nbviewer.jupyter.org/github/monz/garden-time-lapse/blob/master/notebooks/1.0-model-logistic-regression.ipynb)

1. [Image Selection for Time-Lapse](https://nbviewer.jupyter.org/github/monz/garden-time-lapse/blob/master/notebooks/1.0-image-selection-noon.ipynb)

1. [Create Time-Lapse Video](https://nbviewer.jupyter.org/github/monz/garden-time-lapse/blob/master/notebooks/1.0-time-lapse-at-noon.ipynb)


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


## Additional Dependencies

install electron and orca for plotly renderer, e.g. 'svg', 'png', ..., see https://github.com/plotly/orca and https://github.com/electron/electron/issues/11755

- sudo npm install -g electron --unsafe-perm=true --allow-root
- sudo npm install -g orca
