# -*- coding: utf-8 -*-

import numpy as np


class PositionManager:
    def __init__(self, pos_count):
        """コンストラクタ"""
        self.count = pos_count
        # 巡回する地点の座標を作成
        self.positions = np.random.randint(-200, 201, size=(self.count, 2))
        # 座標軸ごとの各点の距離を計算
        xs, ys = [self.positions[:, i] for i in [0, 1]]
        dx = xs - xs.reshape((self.count, 1))
        dy = ys - ys.reshape((self.count, 1))
        # 各点ごとの距離を計算
        self.distances = np.sqrt(dx ** 2 + dy ** 2)


    def calc_moving_distance(self, order):
        """巡回順から移動距離を計算する関数"""
        total = self.distances[order[0], order[-1]]
        for i, j in zip(order[:-1], order[1:]):
            total += self.distances[order[i], order[j]]

        return total
