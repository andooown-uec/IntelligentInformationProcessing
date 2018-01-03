# -*- coding: utf-8 -*-


def sort_order_by_zeroindex(order):
    """巡回順を 0 を基準に並べ替える関数"""
    o = order.copy()
    index = o.index(0)
    size = len(o)
    # 0 の次がより小さくなるように並べる
    if o[(index - 1) % size] > o[(index + 1) % size]:
        o = [0] + o[(index + 1) % size:] + o[:index]
    else:
        o = [0] + list(reversed(o[(index + 1) % size:] + o[:index]))

    return o