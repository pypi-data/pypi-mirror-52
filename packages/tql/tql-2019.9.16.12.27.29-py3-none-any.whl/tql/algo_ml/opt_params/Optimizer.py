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

    def __init__(self, X, y):
        """https://www.cnblogs.com/wzdLY/p/9867719.html
        """
        self.X = X
        self.y = y

    def maximize(self, n_iter=3, seed=2019, return_best_params=True):
        self.optimizer = BayesianOptimization(
            f=self.objective,
            pbounds=self.pbounds,
            random_state=seed,
            verbose=2
        )
        self.optimizer.maximize(init_points=5, n_iter=n_iter)

        if return_best_params:
            return self.optimizer.max  # TODO 把固定参数更新进来

    @abstractmethod
    def objective(self, **params):
        """重写目标函数"""
        self.params = params

        # 超参
        params['num_leaves'] = int(params['num_leaves'])
        params['min_child_samples'] = int(params['min_child_samples'])

        # 固定参数：TODO 更方便的方式
        params['n_estimators'] = 3000
        params['subsample_freq'] = 6  # 需要调参不
        params['verbosity'] = -1
        params['n_jobs'] = 16

        # self.params = params
        self.clf = LGBMClassifier(**params)
        _ = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc', cv=5, n_jobs=5).mean()
        return _

    @abstractmethod
    @staticmethod
    def pbounds():
        """通过左边界判断参数数据类型"""
        _ = {
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
        return _
