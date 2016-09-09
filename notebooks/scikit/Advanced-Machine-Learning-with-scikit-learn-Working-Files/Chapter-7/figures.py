import matplotlib.pyplot as plt
import numpy as np

def plot_grid_1d(grid_search_cv, ax=None):
    if ax is None:
        ax = plt.gca()
    if len(grid_search_cv.param_grid.keys()) > 1:
        raise ValueError("More then one parameter found. Can't do 1d plot.")
        
    score_means, score_stds = zip(*[(np.mean(score.cv_validation_scores), np.std(score.cv_validation_scores))
                                for score in grid_search_cv.grid_scores_])
    score_means, score_stds = np.array(score_means), np.array(score_stds)
    parameters = grid_search_cv.param_grid.values()[0]
    artists = []
    artists.extend(ax.plot(score_means))
    artists.append(ax.fill_between(range(len(parameters)), score_means - score_stds,
                   score_means + score_stds, alpha=0.2, color="b"))
    ax.set_xticklabels(parameters)
    return artists