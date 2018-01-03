# -*- coding: utf-8 -*-

import numpy as np
import random
from deap import algorithms, base, creator, tools
import argparse
import json
import crossover, mutation
from views import GraphView, VerboseView, CSVOutputView


def load_positions(filename):
    """ファイルから巡回する地点の情報を取得する関数"""
    # ファイルを開く
    with open(filename, 'r') as f:
        # ファイルから座標を読み込む
        data = json.load(f)
        # 配列に格納
        pos = []
        for city in data['cities']:
            pos.append([city['x'], city['y']])
        pos = np.asarray(pos)
        # 座標の範囲を取得
        pos_min, pos_max = data['params']['min'], data['params']['max']

    return pos, pos_min, pos_max


def create_random_positions(count, pos_min, pos_max):
    """ランダムな地点を作成する関数"""
    # 巡回する地点の座標を作成
    pos = np.random.randint(pos_min, pos_max + 1, size=(count, 2))

    return pos


def calc_distances(pos):
    """地点の座標から距離マップを計算する関数"""
    # 座標軸ごとの各点の距離を計算
    xs, ys = [pos[:, i] for i in [0, 1]]
    dx = xs - xs.reshape((len(pos), 1))
    dy = ys - ys.reshape((len(pos), 1))
    # 各点ごとの距離を計算
    dist = np.sqrt(dx ** 2 + dy ** 2)

    return dist


def evaluate_individual(ind, distances):
    """遺伝子の評価関数。移動距離の合計を返す"""
    total = distances[ind[0], ind[-1]]
    for i, j in zip(ind[:-1], ind[1:]):
        total += distances[i, j]

    return total,


def create_individual(length):
    """遺伝子を生成する関数"""
    return list(np.random.permutation(length))


if __name__ == '__main__':
    # argparser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # 位置引数の設定
    parser.add_argument('pos_cnt',   help='Nuber of positions',                  type=int)
    parser.add_argument('gen_cnt',   help='Number of generations',               type=int)
    parser.add_argument('pop_cnt',   help='Number of genes in each generations', type=int)
    parser.add_argument('crossover', help='Method for crossover\n' \
                                        + '    cx: 循環交叉\n' \
                                        + '    ox: 順序交叉\n' \
                                        + '    pmx: 部分写像交叉\n' \
                                        + '    erx: 辺組替え交叉', choices=['cx', 'ox', 'pmx', 'erx'], type=str)
    parser.add_argument('crossover_rate', help='Rate of crossover (0 ~ 1)',           type=float)
    parser.add_argument('mutation',  help='Method for mutation\n' \
                                        + '    ins: 挿入\n' \
                                        + '    swp: 交換\n' \
                                        + '    inv: 逆位', choices=['ins', 'swp', 'inv'], type=str)
    parser.add_argument('mutation_rate',  help='Rate of individual mutation (0 ~ 1)', type=float)
    # オプショナル引数を設定
    parser.add_argument('--seed',       help='Seed value',        type=int)
    parser.add_argument('--verbose',    help='Verbose',           action='store_true')
    parser.add_argument('--csv',        help='Output csv',        action='store_true')
    parser.add_argument('--no-display', help="Don't show graphs", action='store_true')
    parser.add_argument('--data',       help='Cities data file',  action='store', nargs='?', const=None, default=None, type=str)
    # 引数をパース
    args = parser.parse_args()
    # 定数を設定
    POSITIONS_COUNT = args.pos_cnt  # 巡回する地点の数
    GENERATION_COUNT = args.gen_cnt # 計算する世代の数
    INDIVIDUAL_COUNT = args.pop_cnt # 一世代あたりの遺伝子の数
    CROSSOVER_RATE = args.crossover_rate    # 交叉率
    MUTATION_RATE = args.mutation_rate      # 突然変異率

    # 乱数のシード値を設定
    if args.seed:
        random.seed(args.seed)
        np.random.seed(args.seed)

    if args.data:
        # ファイルから巡回する地点の情報を取得
        positions, position_min, position_max = load_positions(args.data)
    else:
        # ランダムな地点を作成
        position_min, position_max = -1000, 1000
        positions = create_random_positions(POSITIONS_COUNT, position_min, position_max)
    # 地点間の距離を計算
    distances = calc_distances(positions)

    # creator の設定
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    # toolbox の設定
    toolbox = base.Toolbox()
    toolbox.register("create_individual", create_individual, len(positions))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_individual, distances=distances)
    toolbox.register("mate", crossover.get_function_by_shortname(args.crossover))
    toolbox.register("mutate", mutation.get_function_by_shortname(args.mutation))
    toolbox.register("select", tools.selTournament, tournsize=3)

    # 世代を生成
    pop = toolbox.population(n=INDIVIDUAL_COUNT)

    # 初期世代の各個体の適応度を計算
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # 殿堂入り個体を保存するオブジェクトを作成し、更新する
    hof = tools.HallOfFame(1)
    hof.update(pop)

    # コンソール出力用の View オブジェクトを作成する
    views = []
    if args.verbose:
        # 進捗出力
        stats = {}
        views.append(VerboseView(POSITIONS_COUNT, GENERATION_COUNT, INDIVIDUAL_COUNT, CROSSOVER_RATE, MUTATION_RATE, stats, hof))
    elif args.csv:
        # CSV 出力
        stats = {}
        views.append(CSVOutputView(stats))
    # グラフ表示用の View オブジェクトを作成する
    if not args.no_display:
        views.append(GraphView(positions, position_min, position_max, GENERATION_COUNT, hof))

    # 学習
    for g in range(1, GENERATION_COUNT + 1):
        # 個体を選択
        offspring = toolbox.select(pop, len(pop))

        # 交叉と突然変異
        offspring = algorithms.varAnd(offspring, toolbox, CROSSOVER_RATE, MUTATION_RATE)

        # 適応度がリセットされた個体の適応度を再計算
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # 殿堂入り個体を更新
        hof.update(offspring)

        # 世代を更新
        pop[:] = offspring

        # 情報を集計
        if 'stats' in locals():
            # 適応度を取得
            fits = [ind.fitness.values[0] for ind in pop]
            # 集計
            stats['gen'] = g
            stats['min'] = min(fits)
            stats['max'] = max(fits)
            stats['ave'] = sum(fits) / INDIVIDUAL_COUNT
            stats['std'] = abs(sum([x * x for x in fits]) / INDIVIDUAL_COUNT - stats['ave'] ** 2) ** 0.5
        # 表示を更新
        for v in views:
            v.update()

    # 結果を表示
    for v in views:
        v.finalize()
