# -*- coding: utf-8 -*-

from .abstract_view import AbstractView
from .views_util import sort_order_by_zeroindex


class VerboseView(AbstractView):
    """
    進捗表示出力を管理するクラス
    """


    def __init__(self, positions_count, generation_count, individual_count, crossover_rate, mutation_rate, statistics, hof, opt_dist=None, opt_order=None):
        """
        コンストラクタ
        :param positions_count: 巡回する地点の数
        :param generation_count: 世代数
        :param individual_count: 世代あたりの個体の数
        :param crossover_rate: 交叉率
        :param mutation_rate: 突然変異率
        :param statistics: 統計情報
        :param hof: 殿堂入り個体を保存するオブジェクト
        """
        self._stats = statistics    # 統計情報
        self._hof = hof     # 殿堂入り個体を保存するオブジェクト
        self._opt_distance = opt_dist   # 最適な距離
        self._opt_order = opt_order     # 最適な巡回順
        # 情報を表示
        print('Positions: {}'.format(positions_count))
        print('Generations: {}'.format(generation_count))
        print('Individual: {} / generation'.format(individual_count))
        print('Crossover rate: {}'.format(crossover_rate))
        print('Mutation rate: {}'.format(mutation_rate), end='\n\n')
        # ヘッダを表示
        print('{0:<5} {1:<12} {2:<12} {3:<12} {4:<12}'.format('Gen', 'Min', 'Max', 'Ave', 'Std'))
        print('=' * 58)


    def update(self):
        """出力を更新する関数"""
        print(
            str(self._stats['gen']).ljust(5),
            '{:.4f}'.format(self._stats['min']).rjust(12),
            '{:.4f}'.format(self._stats['max']).rjust(12),
            '{:.4f}'.format(self._stats['ave']).rjust(12),
            '{:.4f}'.format(self._stats['std']).rjust(12))


    def finalize(self):
        """最終結果を出力する関数"""
        # 結果を表示
        if self._opt_distance and self._opt_order:
            error_rate = (self._hof.items[0].fitness.values[0] - self._opt_distance) / self._opt_distance   # 誤差率
            print("\nBest order:\n  {}".format(sort_order_by_zeroindex(self._hof.items[0])))
            print("Optimal order:\n  {}".format(sort_order_by_zeroindex(self._opt_order)))
            print("Moving distance: {0:.4f} (Error: {1:.2%})".format(self._hof.items[0].fitness.values[0], error_rate))
            print("Optimal distance: {:.4f}".format(self._opt_distance))
        else:
            print("\nBest order:\n  {}".format(sort_order_by_zeroindex(self._hof.items[0])))
            print("Moving distance: {:.4f}".format(self._hof.items[0].fitness.values[0]))
