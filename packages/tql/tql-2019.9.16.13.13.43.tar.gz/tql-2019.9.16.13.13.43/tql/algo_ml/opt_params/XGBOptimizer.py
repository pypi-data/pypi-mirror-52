#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : XGBOptimizer
# @Time         : 2019-09-16 11:58
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .Optimizer import Optimizer


class XGBOptimizer(Optimizer):

    def params_bounds(self):
        params = {
            'max_depth': (5, 16),
            'min_child_weight': (1, 10),
            'gamma': (0, 1),

            'subsample': (0.6, 1),
            'colsample_bytree': (0.6, 1),
            'reg_alpha': (0, 1),
            'reg_lambda': (0, 1),
        }
        return params

    def objective(self, **params):
        self.params = params

        # 固定参数
        self.params['n_jobs'] = 32
        self.params['silent'] = True



#
# dict(
#             max_depth=7,
#             learning_rate=(),
#
#             gamma=0.0,  # 描述分裂的最小 gain, 控制树的有用的分裂
#             min_child_weight=1,  # 决定最小叶子节点样本权重和,使一个结点分裂的最小权值之和, 避免过拟合
#
#             subsample=0.8,
#             colsample_bytree=0.8,  # 每棵树的列数
#             colsample_bylevel=0.8,  # 每一层的列数
#
#             reg_alpha=0.0,
#             reg_lambda=0.0,
#
#             scale_pos_weight=scale_pos_weight,
#
#             random_state=seed,
#             n_jobs=n_jobs,
#             silent=True
#         )
