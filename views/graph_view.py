# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from .abstract_view import AbstractView


class GraphView(AbstractView):
    """
    グラフ表示を管理するクラス
    """
    _fitness_hist = []  # 適応度の履歴


    def __init__(self, positions, position_min, position_max, generation_count, hof):
        """
        コンストラクタ
        :param positions: 巡回する地点のリスト
        :param position_min: 巡回する地点の座標の最小値
        :param position_max: 巡回する地点の座標の最大値
        :param generation_count: 実行する世代数
        :param init_fitness: 最初の適応度
        """
        self._pos = positions   # 巡回する地点のリスト
        self._hof = hof         # 殿堂入り個体を保存するオブジェクト

        # インタラクティブモードを有効化
        plt.ion()

        # グラフを作成
        fig = plt.figure(figsize=(3, 5))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        # 経路用のグラフを作成
        self._order_plot, = ax1.plot(self._pos[:, 0], self._pos[:, 1], color='blue', linewidth=3, zorder=1)
        # 各地点をプロット
        ax1.scatter(self._pos[:, 0], self._pos[:, 1], color='cyan', zorder=2)
        # グラフの範囲を指定
        rng = position_max - position_min
        rng_min, rng_max = position_min - rng * 0.1, position_max + rng * 0.1
        ax1.set_xlim(rng_min, rng_max)
        ax1.set_ylim(rng_min, rng_max)

        # 進捗表示用のグラフを作成
        self._fitness_plot, = ax2.plot([0], [self._hof.items[0].fitness.values[0]], color='blue')
        # グラフの範囲を指定
        ax2.set_xlim(0, generation_count)
        ax2.set_ylim(0, self._hof.items[0].fitness.values[0] * 1.2)


    def update(self):
        """グラフを更新する関数"""
        # 経路を更新
        pos = self._pos[self._hof.items[0] + [self._hof.items[0][0]]]
        self._order_plot.set_xdata(pos[:, 0])
        self._order_plot.set_ydata(pos[:, 1])

        # 適応度を履歴に追加
        self._fitness_hist.append(self._hof.items[0].fitness.values[0])
        # 距離を更新
        self._fitness_plot.set_xdata(range(len(self._fitness_hist)))
        self._fitness_plot.set_ydata(self._fitness_hist)

        # グラフを更新
        plt.draw()
        plt.pause(0.01)


    def finalize(self):
        pass
