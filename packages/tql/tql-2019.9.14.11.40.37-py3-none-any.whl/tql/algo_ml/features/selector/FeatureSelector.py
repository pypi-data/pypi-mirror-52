#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : sfs
# @Time         : 2019-07-26 13:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import joblib
from sklearn.feature_selection import RFECV
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_selection import GenericUnivariateSelect, \
    SelectPercentile, SelectKBest, f_classif, mutual_info_classif, RFE

from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt


class FeatureSelector(object):

    def __init__(self, estimator=LGBMClassifier(n_jobs=-1), scoring='roc_auc', selector='sfs', n_jobs=16):
        """
        :param estimator:
        :param scoring:
        :param selector: {'sfs', 'efs', 'rfe'}
        """
        estimator.n_jobs = n_jobs
        if selector == 'sfs':
            """
            efs的优化版：根据 scoring 筛选特征
            顺序特征选择算法的贪婪搜索算法家族，用于减少初始d维特征空间到ķ维特征空间，其中ķ<d 。
            特征选择算法背后的动机是自动选择与问题最相关的特征子集。
            特征选择的目标是双重的：我们希望通过去除不相关的特征或噪声来提高计算效率并减少模型的泛化误差。
            如果嵌入式特征选择（例如，像LASSO这样的正则化惩罚）不适用，则诸如顺序特征选择之类的包装器方法尤其有用。
            """
            self.selector = SFS(estimator,
                                scoring=scoring,
                                cv=5,
                                n_jobs=5,
                                verbose=2,

                                k_features='best',
                                forward=True,
                                floating=False,
                                )
        elif selector == 'efs':  # 枚举：2^n
            self.selector = EFS(estimator,
                                scoring=scoring,
                                cv=5,
                                n_jobs=5,
                                print_progress=True,

                                max_features=1000
                                )
        elif selector == 'rfe':  # 根据树模型特征重要性等权重信息筛选特征
            """https://www.kaggle.com/roydatascience/recursive-feature-selection-new-transactions-elo"""
            self.selector = RFECV(
                estimator,
                scoring=scoring,
                cv=5,
                n_jobs=5,
                verbose=2,

                step=1,  # 每次迭代要删除的特征数/占比
            )

    def fit(self, X, y, model_name=None):
        self.selector.fit(X, y)
        if model_name:
            joblib.dump(self.selector, model_name)

    def plot(self):
        plot_sfs(self.selector.get_metric_dict(), kind='std_dev')
        plt.ylim([0.8, 1])
        plt.title('Sequential Forward Selection (w. StdDev)')
        plt.show()
