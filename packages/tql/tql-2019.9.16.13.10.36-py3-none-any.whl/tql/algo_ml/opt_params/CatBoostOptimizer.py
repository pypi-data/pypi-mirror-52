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


class CatBoostOptimizer(Optimizer):

    def pbounds(self):
        pass

    def objective(self, **params):
        pass
