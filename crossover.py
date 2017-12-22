# -*- coding: utf-8 -*-

import numpy as np


def cycle_crossover(ind1, ind2):
    """循環交叉"""
    size = len(ind1)    # 個体の大きさ
    old1, old2 = ind1.copy(), ind2.copy()   # 親
    new1, new2 = [-1] * size, [-1] * size   # 子孫
    # 残す遺伝子を決める
    index = np.random.randint(size)
    while new1[index] == -1:
        # 現在の位置にある遺伝子を子に受け継ぐ
        new1[index], new2[index] = old1[index], old2[index]
        # 他方の親での遺伝子の位置で現在の位置を更新
        index = old1.index(old2[index])
    # 残りの遺伝子はそれぞれ他方の親から受け継ぐ
    old1, old2 = [x for x in old1 if x not in new1], [x for x in old2 if x not in new2]
    for i in range(size):
        if new1[i] == -1:
            new1[i], new2[i] = old2.pop(0), old1.pop(0)

    return new1, new2
