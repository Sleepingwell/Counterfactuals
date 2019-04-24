"""
Script for learning about how to use random forests.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.forest import (
        _generate_unsampled_indices,
        _generate_sample_indices)
from sklearn.datasets import make_classification

# generate some dummy data
X, y = make_classification(
    n_samples=1000,
    n_features=4,
    n_informative=2,
    n_redundant=0,
    random_state=0,
    shuffle=False)

feature_names = ['x' + str(i) for i in range(X.shape[1])]
data = pd.DataFrame(data=X, columns=feature_names)
data['y'] = y

# fit a random forest
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=2,
    random_state=0,
    oob_score=True)

clf.fit(data[feature_names], data['y'])

# print some stuff about it
print(clf.feature_importances_)
print
print(clf.apply([[0, 0, 0, 0]]))

# this can be used as estimate of the propensity score. It is only produced if
# the argument *oob_score* is passed to the constructor. It is possible that it
# is NaN if an observation makes it into all trees
print(clf.oob_decision_function_)

# We can find out which rows of X were/were not used in a tree using the random
# state attributed of the tree like...
print(_generate_sample_indices(clf.estimators_[0].random_state, X.shape[0]))
print(_generate_unsampled_indices(clf.estimators_[0].random_state, X.shape[0]))
