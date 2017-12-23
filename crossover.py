# -*- coding: utf-8 -*-

import numpy as np


def cycle_crossover(ind1, ind2):
    """循環交叉"""
    size = len(ind1)    # 個体の大きさ
    old1, old2 = ind1.copy(), ind2.copy()   # 親
    # 子孫を初期化
    for i in range(size):
        ind1[i], ind2[i] = -1, -1
    # 残す遺伝子を決める
    index = np.random.randint(size)
    while ind1[index] == -1:
        # 現在の位置にある遺伝子を子に受け継ぐ
        ind1[index], ind2[index] = old1[index], old2[index]
        # 他方の親での遺伝子の位置で現在の位置を更新
        index = old1.index(old2[index])
    # 残りの遺伝子はそれぞれ他方の親から受け継ぐ
    old1, old2 = [x for x in old1 if x not in ind1], [x for x in old2 if x not in ind2]
    for i in range(size):
        if ind1[i] == -1:
            ind1[i], ind2[i] = old2.pop(0), old1.pop(0)

    return ind1, ind2


def order_crossover(ind1, ind2):
    """順序交叉"""
    size = len(ind1)  # 個体の大きさ
    # 切断点を決定する
    p1 = np.random.randint(0, size - 1)
    p2 = np.random.randint(p1 + 1, size)
    # 切断点間はそのままコピー
    new1, new2 = ind1[p1:p2], ind2[p1:p2]   # 子孫
    # 第 2 切断点を先頭に並べ替え
    ind1 = ind1[p2:] + ind1[:p1] + ind1[p1:p2]
    ind2 = ind2[p2:] + ind2[:p1] + ind2[p1:p2]
    # 他方の子と衝突するものを除く
    ind1 = list(filter(lambda x: x not in new2, ind1))
    ind2 = list(filter(lambda x: x not in new1, ind2))
    # 残りを継承
    new1 = ind2[size - p2:] + new1 + ind2[:size - p2]
    new2 = ind1[size - p2:] + new2 + ind1[:size - p2]

    return new1, new2
