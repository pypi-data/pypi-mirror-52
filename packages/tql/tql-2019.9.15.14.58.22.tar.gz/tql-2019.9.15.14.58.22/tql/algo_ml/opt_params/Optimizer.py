#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
from abc import abstractmethod
from bayes_opt import BayesianOptimization
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score


class Optimizer(object):

    def __init__(self, X, y, pbounds: dict = None):
        """缩小区间长度（边界）
         Notice how we transform between regular and log scale. While this
         is not technically necessary, it greatly improves the performance
         of the optimizer.
        """
        self.X = X
        self.y = y
        self.pbounds = pbounds  # 参数边界：TODO 默认边界

    @abstractmethod
    def objective(self, **params):
        """重写目标函数"""

        params['n_jobs'] = 16
        params['num_leaves'] = int(params['num_leaves'])
        params['min_child_samples'] = int(params['min_child_samples'])

        self.clf = LGBMClassifier(**params)
        _ = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc', cv=5).mean()
        return _

    def maximize(self, n_iter=5, seed=2019, return_best_params=True):
        self.optimizer = BayesianOptimization(
            f=self.objective,
            pbounds=self.pbounds,
            random_state=seed,
            verbose=2
        )
        self.optimizer.maximize(n_iter=n_iter)

        if return_best_params:
            return self.optimizer.max['params']

    def objective_lgb(self, **params):
        pass
