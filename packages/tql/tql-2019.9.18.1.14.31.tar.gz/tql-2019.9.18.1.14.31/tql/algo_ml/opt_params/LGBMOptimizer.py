#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
import numpy as np
from ..cv import LGBMClassifierCV
from .Optimizer import Optimizer


class LGBMOptimizer(Optimizer):

    def __init__(self, X, y, params_bounds=None):
        super().__init__(X, y, params_bounds)
        self.params_bounds['n_estimators'] = 3000

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        for p in ('max_depth', 'depth', 'num_leaves', 'subsample_freq', 'min_child_samples'):
            if p in params:
                params[p] = int(np.round(params[p]))
        _params = {**self.params_bounds, **params}

        # 核心逻辑
        self.clf = LGBMClassifierCV(_params)
        return self.clf.fit(self.X, self.y, self.X[:1], early_stopping_rounds=300)
