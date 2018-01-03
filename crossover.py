# -*- coding: utf-8 -*-

import numpy as np
import itertools


def get_function_by_shortname(name):
    """省略名から該当する関数オブジェクトを取得する関数"""
    crossovers = {
        'cx': cycle_crossover,
        'ox': ordered_crossover,
        'pmx': partially_mapped_crossover,
        'erx': edge_recombination_crossover
    }

    return crossovers[name]


def cycle_crossover(ind1, ind2):
    """循環交叉"""
    size = len(ind1)    # 個体の大きさ
    old1, old2 = ind1.copy(), ind2.copy()   # 親
    # 子孫を初期化
    ind1[:], ind2[:] = [-1] * size, [-1] * size
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


def ordered_crossover(ind1, ind2):
    """順序交叉"""
    size = len(ind1)  # 個体の大きさ
    old1, old2 = ind1.copy(), ind2.copy()  # 親
    # 子孫を初期化
    ind1[:], ind2[:] = [-1] * size, [-1] * size
    # 切断点を決定する
    p1 = np.random.randint(0, size - 1)
    p2 = np.random.randint(p1 + 1, size)
    # 切断点間はそのままコピー
    ind1[p1:p2], ind2[p1:p2] = old1[p1:p2], old2[p1:p2]
    # 第 2 切断点を先頭に並べ替え
    old1 = old1[p2:] + old1[:p1] + old1[p1:p2]
    old2 = old2[p2:] + old2[:p1] + old2[p1:p2]
    # 他方の子と衝突するものを除く
    old1 = list(filter(lambda x: x not in ind2, old1))
    old2 = list(filter(lambda x: x not in ind1, old2))
    # 残りを継承
    ind1[:p1], ind2[:p1] = old2[size - p2:], old1[size - p2:]
    ind1[p2:], ind2[p2:] = old2[:size - p2], old1[:size - p2]

    return ind1, ind2


def partially_mapped_crossover(ind1, ind2):
    """部分写像交叉"""
    size = len(ind1)  # 個体の大きさ
    old1, old2 = ind1.copy(), ind2.copy()  # 親
    # 子孫を初期化
    ind1[:], ind2[:] = [-1] * size, [-1] * size
    # 切断点を決定する
    p1, p2 = np.random.randint(0, size), np.random.randint(0, size)
    if p1 == p2:
        p2 = (p2 + 1) % size
    p1, p2 = min(p1, p2), max(p1, p2)
    # 切断点間は他方の親のコピー
    ind1[p1:p2], ind2[p1:p2] = old2[p1:p2], old1[p1:p2]
    # 残りは衝突を起こさないものはそのまま、起こすものは切断点間の入れ替えを参照してコピー
    for i in itertools.chain(range(p1), range(p2, size)):
        if old1[i] not in ind1:
            ind1[i] = old1[i]
        else:
            num = old1[i]
            while num in ind1:
                num = ind2[ind1.index(num)]
            ind1[i] = num
        if old2[i] not in ind2:
            ind2[i] = old2[i]
        else:
            num = old2[i]
            while num in ind2:
                num = ind1[ind2.index(num)]
            ind2[i] = num

    return ind1, ind2


def edge_recombination_crossover(ind1, ind2):
    """辺再組合せ交叉"""
    size = len(ind1)  # 個体の大きさ
    # 近傍リストを作成
    neighbors = [set() for _ in range(size)]
    for p in range(size):
        # 近傍の都市をリストに追加
        index1, index2 = ind1.index(p), ind2.index(p)
        neighbors[p].add(ind1[(index1 - 1) % size])
        neighbors[p].add(ind1[(index1 + 1) % size])
        neighbors[p].add(ind2[(index2 - 1) % size])
        neighbors[p].add(ind2[(index2 + 1) % size])
    # 探索
    build_edge_recombination(list(map(lambda s: s.copy(), neighbors)), ind1, size)
    build_edge_recombination(list(map(lambda s: s.copy(), neighbors)), ind2, size)

    return ind1, ind2


def build_edge_recombination(neighbors, ind, size):
    """近傍リストから遺伝子を再構築する関数"""
    # 探索開始点を決定する
    point = np.random.randint(0, size)
    # 探索
    for i in range(size - 1):
        # 遺伝子に追加
        ind[i] = point
        # 現在の地点を近傍リストから削除
        for p in range(size):
            if point in neighbors[p]:
                neighbors[p].remove(point)
        # 次の探索点を決定する
        if len(neighbors[point]) < 1:
            # 現在の地点の近傍リストが空のとき、まだ回っていない地点から選択
            point = np.random.choice(list(filter(lambda x: x not in ind[:i + 1], range(size))))
        else:
            # 現在の地点の近傍とその地点が持つ近傍の数を取得
            ns = list(map(lambda n: (n, len(neighbors[n])), neighbors[point]))
            # 最小の近傍数を取得
            min_n = min(ns, key=lambda n: n[1])[1]
            # 最小の近傍を持つ地点から 1 つを選択する
            ns = list(map(lambda nn: nn[0], filter(lambda n: n[1] == min_n, ns)))
            point = np.random.choice(ns)
    # 末尾を追加
    ind[-1] = point
