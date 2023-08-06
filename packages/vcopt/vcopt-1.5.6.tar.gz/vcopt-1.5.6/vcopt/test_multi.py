# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as nr

from multiprocessing import Pool, cpu_count
from joblib import Parallel, delayed




class foo:
    def __init__(self):
        pass
    def __del__(self):
        pass
    
    def __spec__(self):
        pass
    
    def func(self, p):
        #self.a[p] *= 10
        return p * 10
    
    def goo(self):
        
        self.a = np.arange(10)
        
        self.func(5)
        
        print(self.a)
        
        self.a = Parallel(n_jobs=2, require='sharedmem', backend='threading')([delayed(self.func)(n) for n in range(10)])
        
        #with Pool(1) as pool:
        #    _ = pool.map(self.func, range(10))
        
        print(self.a)
        
        '''
        with Pool(1) as pool:
            result = pool.map(self.func, range(10))
        
        print(result)'''
        
        
        return self.a
        
        
        
    
    






if __name__ == '__main__':
    
    #__spec__ = 'ModuleSpec(name=\'builtins\', loader=<class \'_frozen_importlib.BuiltinImporter\'>)'
    
    
    pass


    
    
    
    '''
    __spec__ = 'ModuleSpec(name=\'builtins\', loader=<class \'_frozen_importlib.BuiltinImporter\'>)'
    with Pool() as pool:
        results = pool.map(parafunc, range(20))
    
    print (results)'''










