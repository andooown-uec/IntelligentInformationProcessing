# -*- coding: utf-8 -*-

import numpy as np

pos_list = []   # 巡回する地点のリスト
pos = []        # 巡回する地点の座標


def encode_gene(order):
    """各地点を巡回する順番を遺伝子に変換する関数"""
    # 巡回する地点のリストをコピー
    cp_list = pos_list.copy()
    # 遺伝子を生成
    gene = []
    for o in order:
        # 位置を検索
        index = cp_list.index(o)
        # 遺伝子に追加し、地点のリストから削除
        gene.append(index)
        cp_list.pop(index)

    return gene


def decode_gene(gene):
    """遺伝子を各地点を巡回する順番に変換する関数"""
    # 巡回する地点のリストをコピー
    cp_list = pos_list.copy()
    # 遺伝子を生成
    order = []
    for g in gene:
        # 遺伝子から位置を検索し、地点のリストに追加
        order.append(cp_list.pop(g))

    return order


if __name__ == '__main__':
    pos_count = 32  # 巡回する地点の数

    # 巡回する地点のリストを作成
    pos_list = list(range(pos_count))
    # 巡回する地点の座標を作成
    pos = np.random.randint(-200, 201, size=(pos_count, 2))

    # 座標軸ごとの各点の距離を計算
    xs, ys = [pos[:, i] for i in [0, 1]]
    dx = xs - xs.reshape((pos_count, 1))
    dy = ys - ys.reshape((pos_count, 1))
    # 各点ごとの距離を計算
    diffs = np.sqrt(dx ** 2 + dy ** 2)
