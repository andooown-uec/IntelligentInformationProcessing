# -*- coding: utf-8 -*-

import numpy as np


def insert_mutation(individual):
    """
    挿入
    ランダムに選んだ 1 つの都市を取り出してその位置を詰め、同じくランダムに選んだ１つの都市の所に挿入し、それ以降をずらす方式。
    """
    size = len(individual)  # 個体の大きさ
    # 変異を行う 2 点を決定する
    p1, p2 = np.random.randint(0, size, size=2)
    if p1 == p2:
        p2 = (p2 + 1) % size
    if p1 > p2:
        p1, p2 = p2, p1
    # p2 の位置にある遺伝子を p1 の位置に挿入
    individual.insert(p1, individual.pop(p2))

    return individual,


def swap_mutation(individual):
    """
    交換
    ランダムに選んだ 2 つの遺伝子を入れ替える方式。
    """
    size = len(individual)  # 個体の大きさ
    # 変異を行う 2 点を決定する
    p1, p2 = np.random.randint(0, size, size=2)
    if p1 == p2:
        p2 = (p2 + 1) % size
    # 遺伝子を入れ替える
    individual[p1], individual[p2] = individual[p2], individual[p1]

    return individual,


def inversion_mutation(individual):
    """
    逆位
    ランダムに選んだ 2 点間の遺伝子を逆順に並べ替える方式。
    """
    size = len(individual)  # 個体の大きさ
    # 変異を行う 2 点を決定する
    p1, p2 = np.random.randint(0, size), np.random.randint(0, size)
    if p1 == p2:
        p2 = (p2 + 1) % size
    p1, p2 = min(p1, p2), max(p1, p2)
    # 2 点間の遺伝子を逆順に並べ替える
    individual[p1:p2] = list(reversed(individual[p1:p2]))

    return individual,
