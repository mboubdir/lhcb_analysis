import ROOT

import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.axis as ax 
import pandas as pd

def add_weights(df, to_weight, data_x, data_y, bins, weights_x=None, weights_y=None, range=None):
    """
    Args:
      df: DataFrame
      to_weight: Column to reweight
      data_x: Column to reweight to
      data_y: Column to reweight from
      bin: Number of bins or bin edges
      range: Left and right edge
    Returns:
      df: DataFrame with weights
    """
    # Make histograms.
    if weights_x is not None:
        weights_x = df[weights_x]
    b_x, bin_edges = np.histogram(df[data_x], range=range, bins=bins, normed=True, weights=weights_x)
    if weights_y is not None:
        weights_y = df[weights_y]
    b_y, _ = np.histogram(df[data_y], bins=bin_edges, normed=True, weights=weights_y)

    # Divide histograms safely.
    b_y[b_y == 0.] = -1.0
    weights = b_x / b_y
    weights[b_y == -1.0] = 0.

    # Remove values outside of histogram.
    include = (df[to_weight] >= bin_edges[0]) & (df[to_weight] <= bin_edges[-1])
    df = df[include]

    # Return DataFrame with weights.
    idx = pd.cut(df[to_weight], bin_edges, labels=False)
    df['weight'] = weights[idx]
    return df


# Generate data.
x = np.random.normal(0, 1, size=(100000,))
y = np.random.normal(0.5, 1, size=(100000,))
df = pd.DataFrame({'x': x, 'y': y})

# Plot histograms.
plt.hist(df['x'], bins=100, histtype='step', normed=True, label='Daten')
plt.hist(df['y'], bins=100, histtype='step', normed=True, label='MC')

# Make and plot reweighted histogram.
df_new = add_weights(df, 'y', 'x', 'y', 100)
plt.hist(df_new['x'], bins=100, histtype='step', normed=True, weights=df_new['weight'], label='Reweighted MC')

plt.legend()
plt.show()
