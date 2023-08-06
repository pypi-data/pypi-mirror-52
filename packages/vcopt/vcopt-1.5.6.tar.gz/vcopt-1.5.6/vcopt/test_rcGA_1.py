# -*- coding: utf-8 -*-
import numpy as np
import time
import main as mmm

#二次関数（評価関数）
def niji_kansu(para):
    y = para**2
    time.sleep(0.001)
    return y

#パラメータ範囲（パラメータ１つだけでも2次元配列にする必要がある）
para_range = [-5, 5]
print(para_range)

#GAで最適化
para, score = mmm.vcopt().rcGA(para_range,
                               niji_kansu,
                               0.00,
                               show_pool_func='print',
                               pool_num=5000,
                               core_num=9)

#結果の表示
print(para)
print(score)