# -*- coding: utf-8 -*-

from .abstract_view import AbstractView


class CSVOutputView(AbstractView):
    """
    CSV 出力を管理するクラス
    """


    def __init__(self, filename, statistics):
        """
        コンストラクタ
        :param statistics: 統計情報
        """
        self._filename = filename   # ファイル名
        self._stats = statistics    # 統計情報
        # ヘッダを表示
        with open(self._filename, 'w') as f:
            f.write('Generation,Min,Max,Average,Standard deviation\n')


    def update(self):
        """出力を更新する関数"""
        with open(self._filename, 'a') as f:
            f.write(','.join(map(str, [self._stats['gen'], self._stats['min'], self._stats['max'], self._stats['ave'], self._stats['std']])) + '\n')


    def finalize(self):
       pass
