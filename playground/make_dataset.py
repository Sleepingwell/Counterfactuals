from sklearn.datasets import make_classification
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')

X, y = make_classification(
        n_samples=10,
        n_features=1,
        n_informative=1,
        n_redundant=0,
        n_clusters_per_class=1,
        random_state=0,
        shuffle=False)

from pprint import pprint

pprint(X)
pprint(y)
plt.plot(np.squeeze(X[:,0]), y, 'o', color='black')
