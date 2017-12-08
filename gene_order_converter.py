# -*- coding: utf-8 -*-

class GeneOrderConverter:
    def __init__(self, pos_count):
        """コンストラクタ"""
        # 巡回する地点のリストを作成
        self.pos_list = list(range(pos_count))


    def convert_to_gene(self, order):
        """各地点を巡回する順番を遺伝子に変換する関数"""
        # 巡回する地点のリストをコピー
        cp_list = self.pos_list.copy()
        # 遺伝子を生成
        gene = []
        for o in order:
            # 位置を検索
            index = cp_list.index(o)
            # 遺伝子に追加し、地点のリストから削除
            gene.append(index)
            cp_list.pop(index)

        return gene

    def convert_to_order(self, gene):
        """遺伝子を各地点を巡回する順番に変換する関数"""
        # 巡回する地点のリストをコピー
        cp_list = self.pos_list.copy()
        # 遺伝子を生成
        order = []
        for g in gene:
            # 遺伝子から位置を検索し、地点のリストに追加
            order.append(cp_list.pop(g))

        return order
