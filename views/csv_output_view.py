# -*- coding: utf-8 -*-

from .abstract_view import AbstractView
from .views_util import sort_order_by_zeroindex


class CSVOutputView(AbstractView):
    """
    CSV 出力を管理するクラス
    """


    def __init__(self, filename, statistics, hof):
        """
        コンストラクタ
        :param statistics: 統計情報
        """
        self._filename = filename   # ファイル名
        self._stats = statistics    # 統計情報
        self._hof = hof             # 殿堂入り個体を保存するオブジェクト
        self._current_hof = []      # 現在の殿堂入り個体
        # ヘッダを表示
        with open(self._filename, 'w') as f:
            f.write('Generation,Min,Max,Average,Standard deviation,Hall of Fame\n')


    def update(self):
        """出力を更新する関数"""
        with open(self._filename, 'a') as f:
            f.write(','.join(map(str, [self._stats['gen'], self._stats['min'], self._stats['max'], self._stats['ave'], self._stats['std']])))
            if self._hof.items[0] != self._current_hof:
                # 殿堂入り個体が更新されたときのみその個体を表示する
                self._current_hof = self._hof.items[0]
                f.write(',' + '-'.join(map(str, sort_order_by_zeroindex(self._current_hof))))
            f.write('\n')


    def finalize(self):
       pass
