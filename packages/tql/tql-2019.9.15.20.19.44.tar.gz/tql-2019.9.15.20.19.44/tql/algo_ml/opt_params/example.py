#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'demo'
__author__ = 'JieYuan'
__mtime__ = '19-3-19'
"""
from lightgbm import LGBMClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(
    n_samples=1000,
    n_features=45,
    n_informative=12,
    n_redundant=7,
    random_state=134985745,
)

from tql.algo_ml.opt_params.Optimizer import Optimizer


class Opt(Optimizer):

    def objective(self, **params):
        params['n_jobs'] = 16
        params['subsample_freq'] = 6
        params['verbosity'] = -1
        params['num_leaves'] = int(params['num_leaves'])
        params['min_child_samples'] = int(params['min_child_samples'])

        self.clf = LGBMClassifier(**params)
        _ = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc', cv=5, n_jobs=5).mean()
        return _

Opt(X, y).maximize()
