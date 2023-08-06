#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : __init__.py
# @Time         : 2019-06-23 20:07
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .LGBMClassifierCV import LGBMClassifierCV
from .XGBClassifierCV import XGBClassifierCV
from .CatBoostClassifierCV import CatBoostClassifierCV
from .KerasCV import KerasCV
from .OOF import OOF


class ModelOOF(object):
    """TODO: 加入各种模型 oof"""

    def __init__(self):
        pass
