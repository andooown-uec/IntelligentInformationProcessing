# -*- coding: utf-8 -*-

import numpy as np
import random
from deap import base, creator, tools
import matplotlib.pyplot as plt
import argparse
from position_manager import PositionManager
from gene_order_converter import GeneOrderConverter

positions = None    # 巡回する位置を管理するオブジェクト
converter = None    # 遺伝子と巡回する順番のコンバータ
current_distance = 0    # 現在の移動距離
current_gene = None     # 現在の遺伝子
line_plot = None    # 巡回ルート表示用のオブジェクト


def evaluate_gene(gene):
    """遺伝子の評価関数。移動距離の合計を返す"""
    # 遺伝子を巡回順番のリストに変換
    order = converter.convert_to_order(gene)
    # 合計の移動距離を計算
    total = positions.calc_moving_distance(order)

    return total,


def create_gene(length):
    """遺伝子を生成する関数"""
    return converter.convert_to_gene(list(np.random.permutation(length)))


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
    order = converter.convert_to_order(current_gene)
    # 経路を更新
    pos = positions.positions[order]
    line_plot.set_xdata(pos[:, 0])
    line_plot.set_ydata(pos[:, 1])


if __name__ == '__main__':
    # argparser
    parser = argparse.ArgumentParser()
    # 位置引数の設定
    parser.add_argument('pos_cnt',   help='Nuber of positions',                  type=int)
    parser.add_argument('gen_cnt',   help='Number of generations',               type=int)
    parser.add_argument('pop_cnt',   help='Number of genes in each generations', type=int)
    parser.add_argument('crossover', help='Rate of crossover (0 ~ 1)',           type=float)
    parser.add_argument('mutation',  help='Rate of mutation (0 ~ 1)',            type=float)
    # オプショナル引数を設定
    parser.add_argument('--seed', help='Seed value', type=int)
    # 引数をパース
    args = parser.parse_args()
    # 定数を設定
    POSITIONS_COUNT = args.pos_cnt  # 巡回する地点の数
    GENERATION_COUNT = args.gen_cnt # 計算する世代の数
    GENES_COUNT = args.pop_cnt      # 一世代あたりの遺伝子の数
    CROSSOVER_RATE = args.crossover # 交叉率
    MUTATION_RATE = args.mutation   # 突然変異率

    # 乱数のシード値を設定
    if args.seed:
        random.seed(args.seed)
        np.random.seed(args.seed)

    # 巡回する地点を管理するオブジェクトを作成
    positions = PositionManager(POSITIONS_COUNT)
    # コンバータを作成
    converter = GeneOrderConverter(POSITIONS_COUNT)

    # creator の設定
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Gene", list, fitness=creator.FitnessMax)
    # toolbox の設定
    toolbox = base.Toolbox()
    toolbox.register("create_gene", create_gene, POSITIONS_COUNT)
    toolbox.register("gene", tools.initIterate, creator.Gene, toolbox.create_gene)
    toolbox.register("population", tools.initRepeat, list, toolbox.gene)
    toolbox.register("evaluate", evaluate_gene)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_gene, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # 世代を生成
    pop = toolbox.population(n=GENES_COUNT)

    print("Start of evolution")

    # 初期世代の各個体の適応度を計算
    fitnesses = list(map(toolbox.evaluate, pop))
    for gene, fit in zip(pop, fitnesses):
        gene.fitness.values = fit
    # 現在の最短経路を更新
    current_gene = tools.selBest(pop, 1)[0]

    print("  Evaluated {0} individuals".format(len(pop)))

    # インタラクティブモードを有効化
    plt.ion()
    # グラフを作成
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(1, 1, 1)
    # 経路をプロット
    line_plot, = ax.plot(positions.positions[:, 0], positions.positions[:, 1], color='blue', linewidth=3, zorder=1)
    update_figure(line_plot)
    # 各地点をプロット
    ax.scatter(positions.positions[:, 0], positions.positions[:, 1], color='cyan', zorder=2)
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
        invalid_gene = [gene for gene in offspring if not gene.fitness.valid]
        # 適応度を再計算
        fitnesses = map(toolbox.evaluate, invalid_gene)
        for ind, fit in zip(invalid_gene, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated {0} individuals".format(len(invalid_gene)))

        # 世代を更新
        pop[:] = offspring
        # 適応度を取得
        fits = [gene.fitness.values[0] for gene in pop]

        dist = min(fits)
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x * x for x in fits])
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min {0}".format(dist))
        print("  Max {0}".format(max(fits)))
        print("  Avg {0}".format(mean))
        print("  Std {0}".format(std))

        # 現在の距離と最良の遺伝子を更新
        current_distance = dist
        current_gene = tools.selBest(pop, 1)[0]
        # グラフを更新
        update_figure(line_plot)
        plt.draw()
        plt.pause(0.01)

    print("-- End of (successful) evolution --")

    print("Best order: {0}".format(converter.convert_to_order(current_gene)))
    print("Moving distance: {0}".format(current_gene.fitness.values[0]))
