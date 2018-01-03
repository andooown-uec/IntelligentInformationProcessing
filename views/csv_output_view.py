# -*- coding: utf-8 -*-

from .abstract_view import AbstractView


class CSVOutputView(AbstractView):
    """
    CSV 出力を管理するクラス
    """


    def __init__(self, statistics):
        """
        コンストラクタ
        :param statistics: 統計情報
        """
        self._stats = statistics    # 統計情報
        # ヘッダを表示
        print('Gen', 'Min', 'Max', 'Ave', 'Std', sep=',')


    def update(self):
        """出力を更新する関数"""
        print(self._stats['gen'], self._stats['min'], self._stats['max'], self._stats['ave'], self._stats['std'], sep=',')


    def finalize(self):
       pass
