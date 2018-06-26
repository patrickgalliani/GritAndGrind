# Ricky Galliani
# Grit and Grind
# 6/25/18

from utils import get_logger

from sklearn import svm
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import numpy as np
import pandas as pd

BUNNY = 0
MIDRANGE = 1
HEAVE = 2

def shot_type(row):
    if row['SHOT_DIST'] < 3:
        return BUNNY
    elif row['SHOT_DIST'] > 17:
        return HEAVE
    else:
        return MIDRANGE

if __name__ == '__main__':
    
    # Get logger object
    logger = get_logger('shot_train')

    logger.info('Reading in the shot training set...')

    # Read in the training set
    shots = pd.read_csv('../shots/14-15.csv')

    # Select just the features we need
    logger.info('Preparing the training set...')
    shots = shots[[
        'SHOT_CLOCK',
        'PTS_TYPE',
        'SHOT_DIST',
        'CLOSE_DEF_DIST',
        'SHOT_RESULT'
    ]]

    # Deal with null entries for shot clock
    shots['SHOT_CLOCK'] = shots['SHOT_CLOCK'].fillna(0)

    # Classify shots based on distance
    shots['IS_BUNNY'] = (
        shots['SHOT_DIST'].apply(lambda x: 1 if x < 4 else 0)
    )
    shots['IS_MIDRANGE'] = (
        shots['SHOT_DIST'].apply(lambda x: (
            1 if (x >= 4 and x <= 17) else 0)
        )
    )
    shots['IS_HEAVE'] = (
        shots['SHOT_DIST'].apply(lambda x: 1 if x > 17 else 0)
    )
    
    # Convert 'made'/'missed' labels to binary values
    shots['RESULT'] = (
        shots.apply(lambda row: (
            1 * row['PTS_TYPE'] if row['SHOT_RESULT'] == 'made' else 0
        ), axis=1)
    )

    # Select final feature set
    X = shots[[
        'SHOT_CLOCK',
        'PTS_TYPE',
        'IS_BUNNY',
        'IS_MIDRANGE',
        'IS_HEAVE',
        'CLOSE_DEF_DIST',
    ]]
    y = shots[['RESULT']]

    # Split training examples from labels
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.33,
        random_state=22
    )
    logger.info("X_train:\n{}\n({})\n".format(X_train[:3], len(X_train)))
    logger.info("X_test:\n{}\n({})\n".format(X_test[:3], len(X_test)))
    logger.info("y_train:\n{}\n({})\n".format(y_train[:3], len(y_train)))
    logger.info("y_test:\n{}\n({})\n".format(y_test[:50], len(y_test)))

    # Fit decision tree regressor model
    dt = DecisionTreeRegressor(max_depth=3)
    dt.fit(X_train, y_train.ravel())
    y_pred_dt = dt.predict(X_test)

    # Fit svm model
    svm = svm.SVC()
    svm.fit(X_train, y_train.ravel())
    y_pred_svm = svm.predict(X_test) 

    # Compute mse of model
    mse_dt = mean_squared_error(y_test, y_pred_dt)
    mse_svm = mean_squared_error(y_test, y_pred_svm)
    logger.info("Mean Squared Error (DT): {}".format(mse_dt))
    logger.info("Mean Squared Error (SVM): {}".format(mse_svm)) 
