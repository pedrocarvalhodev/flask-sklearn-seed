import os
import pickle
import re
import sys
import textwrap

import pandas as pd
from numpy.random import RandomState
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from app import settings
from ..helpers import files as files_helper
from ..utils import files as files_utils


def train(path_to_dataset, version_id):
    data = pd.read_csv(path_to_dataset)
    #data = pd.DataFrame(np.random.randint(0,100,size=(1000, 5)), columns=["x_1","x_2","x_3","x_4","target"])

    # split into training and validation
    training_set, validation_set = _split_dataset(data, 0.25, 1)
    print('training set has %s rows' % len(training_set))
    print('validation set has %s rows' % len(validation_set))

    # train model
    training_set["x_1"] = training_set["x_1"].fillna(425)
    training_set["target"] = training_set["target"].fillna(0)
    clf = LogisticRegression(C=0.1)
    clf.fit(training_set[["x_1", "x_2", "x_3", "x_4"]], training_set["target"])

    # evaluate model
    validation_set["x_1"] = validation_set["x_1"].fillna(423)
    validation_set["target"] = validation_set["target"].fillna(0)
    validation_predictions = clf.predict_proba(validation_set[["x_1", "x_2", "x_3", "x_4"]])[:, 1]

    print(roc_auc_score(validation_set[["target"]], validation_predictions))

    filename = files_helper.make_filename(version_id)

    path_to_model_file = settings.MODELS_ROOT + "/" + filename

    _persist_to_disk(clf, path_to_model_file)


def _split_dataset(df, validation_percentage, seed):
    state = RandomState(seed)
    validation_indexes = state.choice(df.index, int(len(df.index) * validation_percentage), replace=False)
    training_set = df.loc[~df.index.isin(validation_indexes)].copy()
    validation_set = df.loc[df.index.isin(validation_indexes)].copy()
    return training_set, validation_set


def _persist_to_disk(classifier, path_to_file):

    with open(path_to_file, "wb") as f:
        pickle.dump(classifier, f)

    if os.path.isfile(path_to_file):
        print("Successfully saved model at {}".format(path_to_file))
        return 0
    else:
        print("Something went wrong; failed to persist the trained classifier to disk.")
        return 1


def _validate_args(path, model_version):
    """
    Validation function. Does not return anything, only produces side effects
    in case the passed parameters are not valid.
    :param path: string
    :param model_version: string
    :return: None
    """
    if not os.path.isfile(files_utils.to_abs_path(path)):
        raise ValueError("{} is not a valid path.".format(path))

    if not re.match('^v\d+', model_version):
        raise ValueError("{} is not a valid version id. Valid values: v0,v1,v2, etc.".format(model_version))


if __name__ == '__main__':

    args = sys.argv

    if len(args) != 3:
        help = """
            Train a logistic regression classifier on a parquet dataset.
            
            Usage: python -m app.models.train_model <path-to-parquet-dataset> <model-version>
            
            Example: python -m app.models.train_model path/to/my/model.parquet v2
        """

        print(textwrap.dedent(help))
        sys.exit(1)

    path = args[1]
    model_version = args[2]

    _validate_args(path, model_version)

    path_to_dataset = files_utils.to_abs_path(path)

    print("\nWill train model {} using the file at: {} \n\n".format(model_version, path_to_dataset))

    path_to_models_directory = settings.MODELS_ROOT

    train(path_to_dataset, model_version)
