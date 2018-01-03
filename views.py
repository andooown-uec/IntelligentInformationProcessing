# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt


class AbstractView(metaclass=ABCMeta):
    """
    表示を管理する基底クラス
    """


    @abstractmethod
    def update(self):
        """表示を更新する関数"""
        pass


    @abstractmethod
    def finalize(self):
        """最後の処理を行う関数"""
        pass

