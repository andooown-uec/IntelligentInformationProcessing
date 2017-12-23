# -*- coding: utf-8 -*-

import numpy as np


def insert_mutation(individual):
    """
    挿入
    ランダムに選んだ 1 つの都市を取り出してその位置を詰め、同じくランダムに選んだ１つの都市の所に挿入し、それ以降をずらす方式。
    """
    size = len(individual)  # 個体の大きさ
    # 変異を行う 2 点を決定する
    p1 = np.random.randint(0, size - 1)
    p2 = np.random.randint(p1 + 1, size)
    # p2 の位置にある遺伝子を p1 の位置に挿入
    individual.insert(p1, individual.pop(p2))

    return individual,
