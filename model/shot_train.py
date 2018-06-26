# Ricky Galliani
# Grit and Grind
# 6/25/18

from utils import get_logger

from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor

import numpy as np
import pandas as pd
import pickle

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
    logger.info("\nX_train:\n{}\n({})\n".format(X_train[:3], len(X_train)))
    logger.info("\nX_test:\n{}\n({})\n".format(X_test[:3], len(X_test)))
    logger.info("\ny_train:\n{}\n({})\n".format(y_train[:3], len(y_train)))
    logger.info("\ny_test:\n{}\n({})\n".format(y_test[:3], len(y_test)))

    # Fit decision tree regressor model
    dt = DecisionTreeRegressor(max_depth=4)
    dt.fit(X_train, y_train)
    dt_params = dt.get_params(deep=True)
    logger.info("\nDT Regressor Model Parameters\n\{}\n".format(dt_params))
    joblib.dump(dt, 'dt.pkl')
    logger.info("Persisted the DT Regressor model to dt.pkl...")
    y_pred_dt = dt.predict(X_test)

    # Fit Linear Regression model
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_params = lr.coef_
    logger.info("\nLinear Regressor Model Parameters\n{}\n".format(lr_params))
    joblib.dump(lr, 'lr.pkl')
    logger.info("Persisted the Linear Regression model to lr.pkl...")
    y_pred_lr = lr.predict(X_test)

    # Compute mse of model
    mse_dt = mean_squared_error(y_test, y_pred_dt)
    mse_lr = mean_squared_error(y_test, y_pred_lr)
    logger.info("Mean Squared Error (DT): {}".format(mse_dt))
    logger.info("Mean Squared Error (LR): {}".format(mse_lr))
