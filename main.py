# -*- coding: utf-8 -*-

import numpy as np

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
