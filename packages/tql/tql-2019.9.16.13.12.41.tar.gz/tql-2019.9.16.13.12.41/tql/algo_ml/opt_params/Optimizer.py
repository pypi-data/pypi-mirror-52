#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
import numpy as np
from abc import abstractmethod
from bayes_opt import BayesianOptimization
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score


class Optimizer(object):

    def __init__(self, X, y):
        """https://www.cnblogs.com/wzdLY/p/9867719.html
        """
        self.X = X
        self.y = y

    def maximize(self, n_iter=3, seed=2019, return_best_params=True):
        self.optimizer = BayesianOptimization(
            f=self.objective,
            pbounds=self.params_bounds,
            random_state=seed,
            verbose=2
        )
        self.optimizer.maximize(init_points=5, n_iter=n_iter)

        if return_best_params:
            _ = self.optimizer.max
            return _['params'].update(self.constant_params)

    @property
    def params_bounds(self):
        """通过左边界判断参数数据类型"""
        params = {
            'num_leaves': (2 ** 2, 2 ** 8),
            'subsample_freq': (2, 6),
            'min_child_samples': (16, 128),

            'learning_rate': (0.001, 0.1),
            'min_split_gain': (0.001, 1),
            'min_child_weight': (0.001, 100),
            'subsample': (0.3, 1),
            'colsample_bytree': (0.3, 1),
            'reg_alpha': (0.01, 10),
            'reg_lambda': (0.01, 10)
        }
        return params

    def objective(self, **params):
        """重写目标函数"""

        # 超参纠正参数类型
        for p, (l, r) in params.items():
            if isinstance(l, int) and r - l > 1:
                params[p] = np.round(params[p])

        # 固定参数：
        self.constant_params = {'n_estimators': 3000,
                                'subsample_freq': 0,
                                'verbosity': -1,
                                'n_jobs': 32,
                                'random_state': 666
                                }

        self.clf = LGBMClassifier(**{**self.constant_params, **params})
        _ = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc', cv=5, n_jobs=5).mean()
        return _

if __name__ == '__main__':
    from sklearn.datasets import make_classification

    X, y = make_classification(10000)
    opt = Optimizer(X, y)
    print(opt.maximize(1))