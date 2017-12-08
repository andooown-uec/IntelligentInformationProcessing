# -*- coding: utf-8 -*-

import numpy as np
import random
from deap import base, creator, tools
import matplotlib.pyplot as plt

CROSSOVER_RATE = 0.5    # 交叉率
MUTATION_RATE = 0.2     # 個体突然変異率
GENERATION_COUNT = 100  # 世代数

pos_list = []   # 巡回する地点のリスト
pos = []        # 巡回する地点の座標
pos_diffs = []  # 巡回する地点間の距離
current_distance = 0    # 現在の移動距離
current_gene = None     # 現在の遺伝子
line_plot = None    # 巡回ルート表示用のオブジェクト


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


def evaluate_gene(gene):
    """遺伝子の評価関数。移動距離の合計を返す"""
    # 遺伝子を巡回順番のリストに変換
    order = decode_gene(gene)
    # 合計の移動距離を計算
    total = 0   # 移動距離
    for i in range(len(order) - 1):
        total += pos_diffs[order[i], order[i + 1]]

    return total,


def create_gene(length):
    """遺伝子を生成する関数"""
    return encode_gene(list(np.random.permutation(length)))


def mutate_gene(gene, indpb):
    """遺伝子の突然変異を行う関数"""
    size = len(gene)
    for i in range(size):
        if np.random.rand() < indpb:
            gene[i] = np.random.randint(size - i)

    return gene,


def update_figure(line_plot):
    """グラフを更新する関数"""
    # 遺伝子を巡回順に変換
    order = decode_gene(current_gene)
    # 経路を更新
    line_plot.set_xdata([pos[o, 0] for o in order])
    line_plot.set_ydata([pos[o, 1] for o in order])


if __name__ == '__main__':
    pos_count = 32  # 巡回する地点の数

    # シード値を設定
    np.random.seed(64)
    random.seed(64)

    # 巡回する地点のリストを作成
    pos_list = list(range(pos_count))
    # 巡回する地点の座標を作成
    pos = np.random.randint(-200, 201, size=(pos_count, 2))

    # 座標軸ごとの各点の距離を計算
    xs, ys = [pos[:, i] for i in [0, 1]]
    dx = xs - xs.reshape((pos_count, 1))
    dy = ys - ys.reshape((pos_count, 1))
    # 各点ごとの距離を計算
    pos_diffs = np.sqrt(dx ** 2 + dy ** 2)

    # creator の設定
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    # toolbox の設定
    toolbox = base.Toolbox()
    toolbox.register("create_gene", create_gene, pos_count)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.create_gene)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_gene)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_gene, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # 世代を生成
    pop = toolbox.population(n=300)

    print("Start of evolution")

    # 初期世代の各個体の適応度を計算
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # 現在の最短経路を更新
    current_gene = tools.selBest(pop, 1)[0]

    print("  Evaluated {0} individuals".format(len(pop)))

    # インタラクティブモードを有効化
    plt.ion()
    # グラフを作成
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(1, 1, 1)
    # 経路をプロット
    line_plot, = ax.plot(pos[:, 0], pos[:, 1], color='blue', linewidth=3, zorder=1)
    update_figure(line_plot)
    # 各地点をプロット
    ax.scatter(pos[:, 0], pos[:, 1], color='cyan', zorder=2)
    # グラフの範囲を指定
    ax.set_xlim(-250, 250)
    ax.set_ylim(-250, 250)
    # グラフを表示
    plt.draw()
    plt.pause(0.01)

    # 学習
    for g in range(GENERATION_COUNT):
        print("-- Generation {0} --".format(g))

        # 個体を選択し、そのクローンを作成
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # 交叉
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if np.random.rand() < CROSSOVER_RATE:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # 突然変異
        for mutant in offspring:
            if np.random.rand() < MUTATION_RATE:
                toolbox.mutate(mutant)
                del mutant.fitness.values


        # 交叉や突然変異で適応度がリセットされた個体を抽出
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        # 適応度を再計算
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated {0} individuals".format(len(invalid_ind)))

        # 世代を更新
        pop[:] = offspring
        # 適応度を取得
        fits = [ind.fitness.values[0] for ind in pop]

        dist = min(fits)
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x * x for x in fits])
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min {0}".format(dist))
        print("  Max {0}".format(max(fits)))
        print("  Avg {0}".format(mean))
        print("  Std {0}".format(std))

        # 現在の距離と経路を更新
        current_distance = dist
        current_gene = tools.selBest(pop, 1)[0]
        # グラフを更新
        update_figure(line_plot)
        plt.draw()
        plt.pause(0.01)

    print("-- End of (successful) evolution --")

    # 最良の個体を取得
    best_ind = tools.selBest(pop, 1)[0]
    
    print("Best order: {0}".format(decode_gene(best_ind)))
    print("Moving distance: {0}".format(best_ind.fitness.values[0]))
