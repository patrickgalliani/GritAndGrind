# Ricky Galliani
# Grit and Grind
# 6/27/18


from graphics import draw_court
from utils import get_logger

from sklearn.externals import joblib

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys


if __name__ == '__main__':

    sns.set_color_codes()
    sns.set_style("white")

    # Read in command-line arguments
    shot_feature_path = sys.argv[1]  # Path to the ShotFeature csv
    model_path = sys.argv[2]  # Path to the predictive model
    chart_title = sys.argv[3]  # Title of chart

    # Set up a logger
    logger = get_logger("shot-quality-viz")

    # Read in the shot features
    shot_features = pd.read_csv(shot_feature_path)[[
        'x',
        'y',
        'CLOSE_DEF_DIST',
        'SHOT_DIST',
        'PTS_TYPE'  
    ]]

    # Read in the model
    model = joblib.load(model_path) 
    shot_predicted_vals = [x[0] for x in model.predict(shot_features[[
        'CLOSE_DEF_DIST',
        'SHOT_DIST',
        'PTS_TYPE'  
    ]])]

    Xs = [sf['x'] for i, sf in shot_features.iterrows()]
    Ys = [-1.0 * sf['y'] for i, sf in shot_features.iterrows()]

    # Plot the court with the shots
    plt.figure(figsize=(15, 11.5))

    # Plot the shots as scatter plot and change color based on expected 
    # value of shot
    plt.title("Shot Quality Map {}".format(sys.argv[3]))
    plt.scatter(
        Xs,
        Ys,
        c=shot_predicted_vals,
        cmap=plt.cm.Reds,
        s=250,
        zorder=1
    )
    # Darker colors represent moments earlier on in the game
    cbar = plt.colorbar(orientation="horizontal")
    # Invert the colorbar to have higher numbers on the left
    cbar.ax.invert_xaxis()

    ax = plt.gca()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    draw_court(ax=ax)
    # plt.xlim(0, 101)
    # plt.ylim(-50, 0)
    plt.show()
