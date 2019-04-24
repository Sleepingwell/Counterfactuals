from warnings import warn
import numpy as np



class RandomSampleDescriptor:
    """Generates a random population. Useful for development and testing."""


    def __init__(self):
        self._clf = None
        self._data = None
        self._betas = None
        self._proximity = None
        self._feature_names = None


    def load_all(self, method, **kwargs):
        import pandas as pd
        from sklearn.datasets import make_classification

        self._clf = None
        self._betas = None
        self._proximity = None

        if method == 'really_simple':
            from math import floor, log, exp

            n_samples = kwargs.get('n_samples', 1000)

            alpha = kwargs.get('weights', [0.5])[0]
            assert 0. < alpha < 1., 'weights must be between zero and 1'

            eps = .01
            k = -log(eps/(1-eps))
            beta = k/(1-alpha)
            pr = np.vectorize(lambda x: 1 / (1 + exp(-(beta*(x-alpha)))))

            x = np.random.uniform(0, 1, [n_samples])
            self._x = x
            self._p = pr(x)
            self._feature_names = ['x']
            self._data = pd.DataFrame.from_dict({
                'x': x,
                'z': np.less(
                    np.random.uniform(0, 1, self._p.shape),
                    self._p).astype(np.int)})

        else:
            defaults = {
                "n_samples": 1000,
                "n_features": 1,
                "n_informative": 1,
                "n_redundant": 0,
                "random_state": 0,
                "shuffle": False}
            defaults.update(kwargs)

            # generate some dummy data
            X, z = make_classification(**defaults)
            self._feature_names = ['x' + str(i) for i in range(X.shape[1])]
            self._data = pd.DataFrame(data=X, columns=self._feature_names)
            self._data['z'] = z


    def gen_response(self, betas=None):
        from functools import reduce

        if callable(betas):
            self._betas = betas(self._data)

        else:
            defaults = {'low': 0.0, 'high': 1.0}
            if betas is not None:
                assert isinstance(betas, dict), 'if betas is not callable, it must be a dict'
                defaults.update(betas)
            defaults['size'] = len(self._feature_names)
            self._betas = np.random.uniform(**defaults)

        self._data['y'] = reduce(
            lambda x, y: x + self._data[y[0]] * y[1],
            zip(self._feature_names, self._betas),
            np.zeros(self._data.shape[0]))


    def fit_ps(self, **kwargs):
        from sklearn.ensemble import RandomForestClassifier

        defaults = {
            'random_state': 0,
            'n_jobs': -1,
            'n_estimators': 100,
            'min_samples_leaf': 15,
            'oob_score': True}

        defaults.update(kwargs)
        if defaults['min_samples_leaf'] < 10:
            if defaults['min_samples_leaf'] < 2:
                warn('min_samples_leaf must be greater than 1: setting to 2')
                defaults['min_samples_leaf'] = 2
            warn('setting min_samples_leaf too small might not be wise!')

        if 'oob_score' in kwargs and not kwargs['oob_score']:
            warn('oob_score cannot be set to False: ignoring')
            defaults['oob_score'] = True

        self._proximity = None
        self._clf = RandomForestClassifier(**defaults)

        self._clf.fit(
            self._data[self._feature_names],
            self._data['z'])



    def _calculate_ps_prox(self):
        """Calculate the out of bag proximities between the rest and the
        treeated, for the rest."""

        from counterfactuals import proximity
        from sklearn.ensemble.forest import _generate_unsampled_indices

        # (2d) array of which whether an element is in each tree
        Zin = np.column_stack((np.isin(
            self._data.index,
            _generate_unsampled_indices(e.random_state, self._data.shape[0])) for
                e in self._clf.estimators_))

        # (2d) array of leaves for each observation in each tree
        leaves = np.array(
            self._clf.apply(self._data[self._feature_names]),
            dtype=np.int32, order='c')

        ZT = Zin[self._data['z'] == 1,:]
        LT = leaves[self._data['z'] == 1,:]

        ZO = np.ascontiguousarray(Zin)
        LO = leaves

        # proximitry matrix (others x treated)
        self._proximity = proximity(
            len(self._clf.estimators_),
            LO.shape[0], LT.shape[0],
            LO, LT,
            ZO, ZT)


    def ps_oob_prox(self, units='other'):
        if self._proximity is None:
            self._calculate_ps_prox()

        if units == 'other':
            tmp = self._proximity[self._data['z'] == 0,:]
        if units == 'treated':
            tmp = self._proximity[self._data['z'] == 1,:]
        else:
            # holy yuck...
            # https://stackoverflow.com/questions/35016092/numpy-3d-array-transposed-when-indexed-in-single-step-vs-two-steps
            return np.apply_along_axis(np.mean, 1, self._proximity)

        return np.apply_along_axis(np.mean, 0, tmp)


    def ps_oob(self, units='other'):
        """Out of bag estimate of the propensity score."""

        # oob_decision_function_ is only produced if the argument *oob_score*
        # is passed to the constructor. It is possible that it is NaN if an
        # observation makes it into all trees.

        if units == 'other':
            return self._clf.oob_decision_function_[self._data['z'] == 0, 1]
        if units == 'treated':
            return self._clf.oob_decision_function_[self._data['z'] == 1, 1]
        return self._clf.oob_decision_function_[:, 1]


    def __getitem__(self, thing):
        return self._data[thing]


    @property
    def treated(self):
        return self._data['z'] == 1


    @property
    def nottreated(self):
        return self._data['z'] == 0


    @property
    def nobs(self):
        return self._data.shape[0]


    @property
    def ntreated(self):
        return np.sum(self.treated)


    @property
    def nother(self):
        return self.nobs - self.ntreated



if __name__ == "__main__":
    rd = RandomSampleDescriptor()
    rd.load_all()
    rd.fit_ps()
    rd.ps_oob_prox()
    rd.ps_oob()
    rd.gen_response()
