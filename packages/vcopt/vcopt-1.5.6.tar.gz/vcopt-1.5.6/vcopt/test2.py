# -*- coding: utf-8 -*-
from joblib import Parallel, delayed
from multiprocessing import Pool, cpu_count
import numpy as np
import numpy.random as nr

import test_multi as mmm





result = mmm.foo().goo()

print(result)

'''
#iteration
iteration = np.arange(100)
nr.shuffle(iteration)
iteration = iteration.reshape(50, 2)


def process(i, j):
    return i * 2
    #return [{'id': j, 'sum': sum(range(i*j))} for j in range(100)]

result = Parallel(n_jobs=2)([delayed(process)(n, m) for n, m in iteration])

print(result)
'''
'''
def process2(i):
    return i * 2


if __name__ == "__main__":
    __spec__ = 'ModuleSpec(name=\'builtins\', loader=<class \'_frozen_importlib.BuiltinImporter\'>)'
    with Pool(2) as pool:
        results = pool.map(process2, range(10))
    
    print(results)'''