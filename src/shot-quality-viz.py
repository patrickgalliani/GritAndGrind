# Ricky Galliani
# Grit and Grind
# 6/27/18


from graphics import draw_court
from utils import get_logger

from sklearn.externals import joblib

# import matplotlib
# matplotlib.use("tkagg")
# import matplotlib.pyplot as plt
import pandas as pd
import sys


if __name__ == '__main__':

    # Read in command-line arguments
    shot_feature_path = sys.argv[1]  # Path to the ShotFeature csv
    model_path = sys.argv[2]  # Path to the predictive model

    # Set up a logger
    logger = get_logger("shot-quality-viz")

    # Read in the shot features
    shot_features = pd.read_csv(shot_feature_path)[[
        'PTS_TYPE',
        'SHOT_DIST',
        'CLOSE_DEF_DIST',
    ]]

    # Read in the model
    model = joblib.load(model_path) 
    shot_predicted_vals = model.predict(shot_features)
    print("shot_predicted_vals = {}".format(shot_predicted_vals))

    # plt.figure(figsize=(15, 11.5))

    # Plot the movemnts as scatter plot
    # using a colormap to show change in game clock
    # plt.scatter(harden.x_loc, -harden.y_loc, c=harden.game_clock,
    #             cmap=plt.cm.Blues, s=1000, zorder=1)
    # Darker colors represent moments earlier on in the game
    # cbar = plt.colorbar(orientation="horizontal")
    # invert the colorbar to have higher numbers on the left
    # cbar.ax.invert_xaxis()

    # draw_court()
    # plt.xlim(0, 101)
    # plt.ylim(-50, 0)
    # plt.show()
