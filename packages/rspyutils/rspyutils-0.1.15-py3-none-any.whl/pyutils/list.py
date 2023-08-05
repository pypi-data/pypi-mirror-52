# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zhanglanhui
homepage recommender:ffm
"""
import copy
import itertools


def merge_list(l1, l2):
    # 将所有的漫画按照type分类
    tmp = copy.deepcopy(l1)
    tmp.extend([x for x in l2 if x not in l1])
    return tmp


def get_first_col_str(l):
    return [str(x[0]) for x in l]


def filter_lists(l1, l2):
    return [x for x in l1 if x not in l2]


def get_flat_list(l):
    # 使用itertools內建模块
    return list(itertools.chain.from_iterable(l))


def check_length(l, length):
    if len(l) < length:
        raise ValueError("len of list is less then {}".format(length))
