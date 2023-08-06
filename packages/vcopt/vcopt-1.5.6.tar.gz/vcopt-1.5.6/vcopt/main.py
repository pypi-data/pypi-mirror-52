# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as nr
import math, time, os
from copy import deepcopy
#from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
#from numba import jit
#np.set_printoptions(threshold=np.inf, precision=8, suppress=True, floatmode='maxprec')

class vcopt:
    def __init__(self):
        pass
    def __del__(self):
        pass
    #==========================================================================
    #setting 1
    #==========================================================================
    def setting_1(self, para_range, score_func, aim, show_pool_func, seed, pool_num, max_gen):
        self.para_range = para_range #そのままの形式で用いる
        self.para_num = len(para_range)
        self.score_func = score_func
        self.aim = float(aim)
        self.show_pool_func = show_pool_func #そのままの形式で用いる
        #規定以外であればNoneとする
        if self.show_pool_func == None: pass
        elif self.show_pool_func in ['bar', 'print', 'plot']: pass
        elif callable(self.show_pool_func) : pass
        elif type(show_pool_func) == str:
            if len(show_pool_func) == 0 or show_pool_func[-1] != '/':
                self.show_pool_func = 'bar'
        #intまたはNone
        if type(seed) in [int, float]:
            self.seed = int(seed)
        else:
            self.seed = None
        nr.seed(self.seed)
        #intまたはNone
        if type(pool_num) in [int, float]:
            self.pool_num = int(pool_num)
            #偶数にする
            if self.pool_num % 2 != 0:
                self.pool_num += 1
        else:
            self.pool_num = None
        #intまたはNone
        if type(max_gen) in [int, float]:
            self.max_gen = int(max_gen)
        else:
            self.max_gen = None
        self.start = time.time()
    #==========================================================================
    #setting 2
    #==========================================================================
    def setting_2(self, pool_num, parent_num, child_num):
        #self.pool_numがNoneであれば規定で上書き、intであればpass
        if self.pool_num is None:
            self.pool_num = pool_num
        self.parent_num = parent_num
        self.child_num = child_num
        self.family_num = parent_num + child_num
        #Noneであれば規定で上書き、intであれば使用
        if self.max_gen is None:
            self.max_n = 1000000
        else:
            self.max_n = self.max_gen // self.pool_num + 1
    #==========================================================================
    #setting 3
    #==========================================================================
    def setting_3(self, dtype):
        self.pool, self.pool_score = np.zeros((self.pool_num, self.para_num), dtype=dtype), np.zeros(self.pool_num)
        self.parent, self.parent_score = np.zeros((self.parent_num, self.para_num), dtype=dtype), np.zeros(self.parent_num)
        self.child, self.child_score = np.zeros((self.child_num, self.para_num), dtype=dtype), np.zeros(self.child_num)
        self.family, self.family_score = np.zeros((self.family_num, self.para_num), dtype=dtype), np.zeros(self.family_num)
    #==========================================================================
    #print info
    #==========================================================================
    def print_info(self):
        if self.show_pool_func is not None:
            print('___________________ info ___________________')
            print('para_range : n={}'.format(self.para_num))
            print('score_func : {}'.format(type(self.score_func)))
            print('aim : {}'.format(self.aim))
            
            print('show_pool_func : \'{}\''.format(self.show_pool_func))
            print('seed : {}'.format(self.seed))
            print('pool_num : {}'.format(self.pool_num))
            print('max_gen : {}'.format(self.max_gen))
            print('___________________ start __________________')
    #==========================================================================
    #score pool
    #==========================================================================
    def score_pool(self): #ndarray index to ndarray original #para_range==ndarray, para==[0, 1,...]int
        for i in range(self.pool_num):
            para = self.para_range[self.pool[i]]
            self.pool_score[i] = self.score_func(para)
            if self.show_pool_func != None:
                bar = '\rScoring first gen {}/{}        '.format(i + 1, self.pool_num)
                print(bar, end='')
        if self.show_pool_func is not None: print()

            
    def score_pool_dc(self): #list index to list original
        for i in range(self.pool_num):
            para = []
            for j in range(self.para_num):
                para.append(self.para_range[j][self.pool[i, j]])
            para = np.array(para)
            self.pool_score[i] = self.score_func(para)
            if self.show_pool_func != None:
                bar = '\rScoring first gen {}/{}        '.format(i + 1, self.pool_num)
                print(bar, end='')
        if self.show_pool_func is not None: print()
            
    def score_pool_rc(self): #para_range==ndarray, para==[0.0, 1.0]float
        for i in range(self.pool_num):
            para = self.pool[i] * (self.para_range[:, 1] - self.para_range[:, 0]) + self.para_range[:, 0]
            self.pool_score[i] = self.score_func(para)
            if self.show_pool_func != None:
                bar = '\rScoring first gen {}/{}        '.format(i + 1, self.pool_num)
                print(bar, end='')
        if self.show_pool_func is not None: print()
    #==========================================================================
    #score child
    #==========================================================================
    def score_child(self):        
        for i in range(self.child_num):
            para = self.para_range[self.child[i]]
            self.child_score[i] = self.score_func(para)
    
    def score_child_dc(self):        
        for i in range(self.child_num):
            para = []
            for j in range(self.para_num):
                para.append(self.para_range[j][self.child[i, j]])
            para = np.array(para)
            self.child_score[i] = self.score_func(para)
    
    def score_child_rc(self):        
        for i in range(self.child_num):
            para = self.child[i] * (self.para_range[:, 1] - self.para_range[:, 0]) + self.para_range[:, 0]
            self.child_score[i] = self.score_func(para)
    #==========================================================================
    #save best and mean
    #==========================================================================
    def save_best_mean(self):
        #best_index
        self.best_index = np.argmin(np.abs(self.aim - self.pool_score))
        #save best
        self.pool_best = deepcopy(self.pool[self.best_index])
        self.score_best = deepcopy(self.pool_score[self.best_index])
        
        #mean
        self.score_mean = np.mean(self.pool_score)
        self.gap_mean = np.mean(np.abs(self.aim - self.pool_score))
        #save mean
        self.score_mean_save = deepcopy(self.score_mean)
        self.gap_mean_save = deepcopy(self.gap_mean)
    #==========================================================================
    #make parent
    #==========================================================================
    def make_parent(self, it):
        self.pool_select = it
        self.parent = self.pool[self.pool_select]
        self.parent_score = self.pool_score[self.pool_select]
    #==========================================================================
    #make family
    #==========================================================================
    def make_family(self):
        self.family = np.vstack((self.child, self.parent))
        self.family_score = np.hstack((self.child_score, self.parent_score))
    #==========================================================================
    #JGG
    #==========================================================================
    def JGG(self):
        #np.argpartition(-array, K)[:K] returns max K index
        #np.argpartition(array, K)[:K] returns min K index
        self.family_select = np.argpartition(np.abs(self.aim - self.family_score), self.parent_num)[:self.parent_num]
        #return to pool
        self.pool[self.pool_select] = self.family[self.family_select]
        self.pool_score[self.pool_select] = self.family_score[self.family_select]
    #==========================================================================
    #end check
    #==========================================================================
    def end_check(self):
        #best
        self.best_index = np.argmin(np.abs(self.aim - self.pool_score))
        self.score_best = deepcopy(self.pool_score[self.best_index])
        #mean, gap
        self.gap_mean = np.mean(np.abs(self.aim - self.pool_score))
        #if reached aim
        if self.score_best == self.aim:
            return 10
        #if not updated
        if self.gap_mean >= self.gap_mean_save:
            return 1
        return 0
    '''
    def end_check_rc(self):
        #best
        self.best_index = np.argmin(np.abs(self.aim - self.pool_score))
        self.score_best = deepcopy(self.pool_score[self.best_index])
        #mean, gap
        self.gap_mean = np.mean(np.abs(self.aim - self.pool_score))
        #if reached aim
        if self.score_best == self.aim:
            return 10
        #if not updated
        if self.gap_mean >= self.gap_mean_save * 0.999:
            return 1
        return 0'''
    #==========================================================================
    #make info
    #==========================================================================
    def make_info(self, gen):
        info = {'gen':gen, 'best_index':self.best_index,\
                'best_score':round(self.score_best, 4),\
                'mean_score':round(self.score_mean, 4),\
                'mean_gap':round(self.gap_mean, 4),\
                'time':round(time.time() - self.start, 1)}
        return info
    #==========================================================================
    #show pool func
    #==========================================================================
    def show_pool(self, gen):
        info = self.make_info(gen)
        self.show_pool_func(self.para_range[self.pool], **info)
    def show_pool_dc(self, gen):
        info = self.make_info(gen)
        pool = []
        for i in range(self.pool_num):
            para = []
            for j in range(self.para_num):
                para.append(self.para_range[j][self.pool[i, j]])
            pool.append(para)
        pool = np.array(pool)
        self.show_pool_func(pool, **info)
    def show_pool_rc(self, gen):
        info = self.make_info(gen)
        pool = np.array(list(map(
                lambda i: self.pool[i] * (self.para_range[:, 1] - self.para_range[:, 0]) + self.para_range[:, 0],
                range(self.pool_num))))
        self.show_pool_func(pool, **info)
    #==========================================================================
    #make round
    #==========================================================================
    def make_round(self):
        best_score = round(self.score_best, 4)
        mean_score = round(self.score_mean, 4)
        mean_gap = round(self.gap_mean, 4)
        tim = round(time.time() - self.start, 1)
        return best_score, mean_score, mean_gap, tim
    #==========================================================================
    #show pool
    #==========================================================================
    #show pool bar
    def show_pool_bar(self, gen):
        #
        best_score = round(self.score_best, 4)
        #
        len_max = min(abs(self.aim - self.init_score_range[0]), abs(self.aim - self.init_score_range[1]))
        len_best = abs(self.aim - self.score_best)
        len_mean = min(abs(self.aim - self.gap_mean), len_max)
        #
        interval_0 = int(len_best / len_max * 40)
        interval_1 = int((len_mean - len_best) / len_max * 40)
        interval_2 = 40 - interval_0 - interval_1
        #
        bar = '\r|{}+{}<{}| gen={}, best_score={}'.format(' '*interval_0, ' '*interval_1, ' '*interval_2, gen, best_score)
        print(bar, end='')
        #print(bar)
        if gen == 0:
            time.sleep(0.2)
    
    def show_pool_print(self, gen):
        best_score, mean_score, mean_gap, tim = self.make_round()
        print('gen={}, best_score={}, mean_score={}, mean_gap={}, time={}'.format(gen, best_score, mean_score, mean_gap, tim))
        
    #show pool plot
    def show_pool_plot(self, gen):
        best_score, mean_score, mean_gap, tim = self.make_round()
        #プロット
        plt.bar(range(len(self.pool_score[:100])), self.pool_score[:100])
        plt.ylim([min(self.aim, self.init_score_range[0]), max(self.aim, self.init_score_range[1])])
        plt.title('gen={}{}best_score={}{}mean_score={}{}mean_gap={}{}time={}'.format(gen, '\n', best_score, '\n', mean_score, '\n', mean_gap, '\n', tim), loc='left')
        plt.show(); plt.close(); print()
        
    #show pool save
    def show_pool_save(self, gen):
        #
        self.show_pool_bar(gen)
        
        best_score, mean_score, mean_gap, tim = self.make_round()
        #プロット
        plt.bar(range(len(self.pool_score[:100])), self.pool_score[:100])
        plt.ylim([min(self.aim, self.init_score_range[0]), max(self.aim, self.init_score_range[1])])
        plt.title('gen={}{}best_score={}{}mean_score={}{}mean_gap={}{}time={}'.format(gen, '\n', best_score, '\n', mean_score, '\n', mean_gap, '\n', tim), loc='left')
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.70)
        plt.savefig(self.show_pool_func + 'round_{}.png'.format(str(gen).zfill(4))); plt.close()
        

    #==========================================================================
    #2-opt
    #==========================================================================
    def opt2(self, para, score_func, aim, show_para_func=None, seed=None, step_max=float('inf')):
        #
        para, score = np.array(para), score_func(para)
        kwargs = {}
        if seed != 'pass': nr.seed(seed)
        step = 0
        #
        if show_para_func != None:
            kwargs.update({'step_num':step, 'score':round(score, 3)})
            show_para_func(para, **kwargs)
        #opt
        while 1:
            update = False
            if step >= step_max:
                #print('stop')
                break
            
            i_set = np.arange(0, len(para)-1)
            nr.shuffle(i_set)
            for i in i_set:
                #continue check
                if update == True: break
                
                j_set = np.arange(i + 1, len(para))
                nr.shuffle(j_set)
                for j in j_set:
                    #continue check
                    if update == True: break
                    
                    #try
                    para_tmp = np.hstack((para[:i], para[i:j+1][::-1], para[j+1:]))
                    score_tmp = score_func(para_tmp)
                    
                    #check and update
                    if np.abs(aim - score_tmp) < np.abs(aim - score):
                        para, score = para_tmp, score_tmp
                        step += 1
                        if show_para_func != None:
                            kwargs.update({'step_num':step, 'score':round(score, 3)})
                            show_para_func(para, **kwargs)
                        update = True
            if update == False:
                #print('end')
                break
        return para, score
    #==========================================================================
    #2-opt for tspGA()
    #==========================================================================
    def opt2_tspGA(self, para, score, step_max=float('inf')):
        #
        para, score = para, score
        step = 0
        #opt
        while 1:
            update = False
            if step >= step_max:
                break
            
            i_set = np.arange(0, self.para_num - 1)
            #i_set = np.arange(0, self.para_num//4)
            nr.shuffle(i_set)
            for i in i_set:
                #continue check
                if update == True: break
                
                j_set = np.arange(i + 1, self.para_num)
                nr.shuffle(j_set)
                for j in j_set:
                    #continue check
                    if update == True: break
                    
                    #try
                    para_tmp = np.hstack((para[:i], para[i:j+1][::-1], para[j+1:]))
                    score_tmp = self.score_func(self.para_range[para_tmp])
                    
                    #check and update
                    if np.abs(self.aim - score_tmp) < np.abs(self.aim - score):
                        para, score = para_tmp, score_tmp
                        step += 1
                        update = True
            if update == False:
                #print('end')
                break
        return para, score



    #######################################################################################################################
    #######################################################################################################################
    def tspGA(self, para_range, score_func, aim, show_pool_func='bar', seed=None, pool_num=None, max_gen=None):
        
        #tspGA, para_range==ndarray, pool==[0, 1,...]int
        
        #pre
        para_range = np.array(para_range)
        
        #setting 1-3
        self.setting_1(para_range, score_func, aim, show_pool_func, seed, pool_num, max_gen)
        self.setting_2(self.para_num*10, 2, 4)
        self.setting_3(int)
        self.print_info()
        
        #specific
        self.para_index = np.arange(self.para_num) # para_indexはnumpy形式で用いる
        self.opt2_num = 1
        
        #gen 1 pool
        for i in range(self.pool_num):
            self.pool[i] = deepcopy(self.para_index)
            nr.shuffle(self.pool[i])
        
        #
        self.score_pool()  
        
        #mini 2-opt
        for i in range(self.pool_num):
            self.pool[i], self.pool_score[i] = self.opt2_tspGA(self.pool[i], self.pool_score[i], step_max=self.opt2_num)
            if self.show_pool_func != None:
                bar = '\rMini 2-opting first gen {}/{}        '.format(i + 1, self.pool_num)
                print(bar, end='')
        if self.show_pool_func != None: print()
        
        #       
        self.save_best_mean()
        
        self.init_score_range = (np.min(self.pool_score), np.max(self.pool_score))
        self.init_gap_mean = deepcopy(self.gap_mean)
        
        #show
        if self.show_pool_func == None: pass
        elif self.show_pool_func == 'bar': self.show_pool_bar(0)
        elif self.show_pool_func == 'print': self.show_pool_print(0)
        elif self.show_pool_func == 'plot': self.show_pool_plot(0)
        elif callable(self.show_pool_func) : self.show_pool(0) #関数であれば
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                if not os.path.exists(show_pool_func): os.mkdir(show_pool_func) #保存フォルダを作成
                self.show_pool_save(0)
        
        #gen 2-
        count = 0
        for n in range(1, self.max_n + 1):
            #
            #self.opt2_num = n // 10
            
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)
            
                #辺に着目したヒュリスティック操作
                #==============================================================
                #ex_parent
                self.ex_parent = np.hstack((self.parent[:, -2:].reshape(self.parent_num, 2), self.parent, self.parent[:, :2].reshape(self.parent_num, 2)))
                
                #child
                for i in range(self.child_num):
                    #first para
                    s = self.parent[nr.randint(self.parent_num), 0]
                    if nr.rand() < (1.0 / self.para_num):
                        s = nr.choice(self.para_index)
                    self.child[i, 0] = s
                    #following para
                    for j in range(1, self.para_num):
                        
                        mask_1 = np.zeros((self.parent_num, self.para_num + 4), dtype=bool)
                        mask_2 = np.zeros((self.parent_num, self.para_num + 4), dtype=bool)
                        
                        mask_1[:, 1:-3] += (self.parent == s)
                        mask_1[:, 3:-1] += (self.parent == s)
                        mask_2[:, 0:-4] += (self.parent == s)
                        mask_2[:, 4:] += (self.parent == s)
                        
                        #p
                        p = np.ones(self.para_num) * (1.0 / self.para_num)
                        for k in self.ex_parent[mask_1]:
                            p[np.where(self.para_index==k)[0]] += 1.0 / self.parent_num
                        for k in self.ex_parent[mask_2]:
                            p[np.where(self.para_index==k)[0]] += 0.1 / self.parent_num
                        
                        #mask passed para
                        for k in self.child[i, 0:j]:
                            p[np.where(self.para_index==k)[0]] = 0.0
                        #print(p)
                        #choice
                        p *= 1.0 / np.sum(p)
                        s = nr.choice(self.para_index, p=p)
                        #child
                        self.child[i, j] = s
                #==============================================================
                #
                self.score_child()
                self.make_family()
                
                #mini 2-opt
                for i in range(self.family_num):
                    self.family[i], self.family_score[i] = self.opt2_tspGA(self.family[i], self.family_score[i], step_max=self.opt2_num)
                
                self.JGG()
            
            #end check
            count += self.end_check()
            
            #
            self.save_best_mean()
            
            #show
            if self.show_pool_func == None: pass
            elif self.show_pool_func == 'bar': self.show_pool_bar(n * self.pool_num)
            elif self.show_pool_func == 'print': self.show_pool_print(n * self.pool_num)
            elif self.show_pool_func == 'plot': self.show_pool_plot(n * self.pool_num)
            elif callable(self.show_pool_func) : self.show_pool(n * self.pool_num) #関数であれば
            elif type(show_pool_func) == str:
                if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                    self.show_pool_save(n)
            
            #end
            if count >= 1:
                break
        
        #
        para = self.para_range[self.pool_best]
        
        #'bar'またはsaveなら改行
        if self.show_pool_func == 'bar': print()
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                print()
        
        #Noneでなければ出力
        if self.show_pool_func != None:
            print('__________________ results _________________')
            print('para : {}'.format(para))
            print('score : {}'.format(self.score_best))
            print('____________________ end ___________________')
        
        return para, self.score_best
    
    
    
    
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def dcGA(self, para_range, score_func, aim, show_pool_func=None, seed=None, pool_num=None, max_gen=None, cross=None):
        
        #dcGA, para_range==list, pool==[2, 1,...]int
        
        #pre
        if type(para_range) == list:
            if isinstance(para_range[0], list) == False:
                para_range = [para_range]
        if type(para_range) == np.ndarray:
            if para_range.ndim == 1:
                para_range = para_range.reshape(1, len(para_range))
        
        #setting 1-3
        self.setting_1(para_range, score_func, aim, show_pool_func, seed, pool_num, max_gen)
        self.setting_2(self.para_num*10, 2, 4)
        self.setting_3(int)
        self.print_info()
        
        #specific
        self.para_index = [] # para_indexはlist形式で用いる
        for i in range(self.para_num):
            self.para_index.append(np.arange(len(self.para_range[i])))
        self.choice = np.array([[0,1,0],[1,0,1]], dtype=int)
        
        #gen 1 pool
        for i in range(self.pool_num):
            for j in range(self.para_num):
                self.pool[i, j] = nr.choice(self.para_index[j])
        
        #
        self.score_pool_dc()
        self.save_best_mean()
        
        self.init_score_range = (np.min(self.pool_score), np.max(self.pool_score))
        self.init_gap_mean = deepcopy(self.gap_mean)
        
        #show
        if self.show_pool_func == None: pass
        elif self.show_pool_func == 'bar': self.show_pool_bar(0)
        elif self.show_pool_func == 'print': self.show_pool_print(0)
        elif self.show_pool_func == 'plot': self.show_pool_plot(0)
        elif callable(self.show_pool_func) : self.show_pool(0) #関数であれば
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                if not os.path.exists(show_pool_func): os.mkdir(show_pool_func) #保存フォルダを作成
                self.show_pool_save(0)
        
        #gen 2-
        count = 0
        for n in range(1, self.max_n + 1):
            #
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)
                
                #normal
                if self.para_num >= 3:
                    #2-point cross for child[:2]
                    #==============================================================
                    #cross point
                    cross_point = nr.choice(range(1, self.para_num), 2, replace=False)
                    if cross_point[0] > cross_point[1]:
                        cross_point[0], cross_point[1] = cross_point[1], cross_point[0]
                    #child
                    for i in range(len(self.choice)):
                        self.child[i] = np.hstack((self.parent[self.choice[i, 0], :cross_point[0]],
                                                   self.parent[self.choice[i, 1], cross_point[0]:cross_point[1]],
                                                   self.parent[self.choice[i, 2], cross_point[1]:]))
                    #==============================================================
                    #uniform cross for child[2:]
                    #==============================================================
                    #child
                    for i in [2, 3]:
                        mask = nr.randint(0, 2, self.para_num)
                        self.child[i][mask==0] = self.parent[0][mask==0]
                        self.child[i][mask==1] = self.parent[1][mask==1]
                    #==============================================================
                    #mutation
                    #==============================================================
                    for ch in self.child:
                        for j in range(self.para_num):
                            if nr.rand() < (1.0 / self.para_num):
                                ch[j] = nr.choice(self.para_index[j])
                    #==============================================================
                
                #if small dim, quick end
                elif self.para_num == 2:
                    #cross for child[:2]
                    self.child[:2] = np.array([[self.parent[0, 0], self.parent[1, 1]], [self.parent[0, 1], self.parent[1, 0]]])
                    #random for child[2:]
                    for i in range(2, self.child_num):
                        for j in range(2):
                            self.child[i, j] = nr.choice(self.para_index[j])
                
                elif self.para_num == 1:
                    #all random
                    for i in range(self.child_num):
                        self.child[i] = nr.choice(self.para_index[0])

                #
                self.score_child_dc()
                self.make_family()
                self.JGG()
            
            #end check
            count += self.end_check()
            
            #
            self.save_best_mean()
            
            #show
            if self.show_pool_func == None: pass
            elif self.show_pool_func == 'bar': self.show_pool_bar(n * self.pool_num)
            elif self.show_pool_func == 'print': self.show_pool_print(n * self.pool_num)
            elif self.show_pool_func == 'plot': self.show_pool_plot(n * self.pool_num)
            elif callable(self.show_pool_func) : self.show_pool(n * self.pool_num) #関数であれば
            elif type(show_pool_func) == str:
                if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                    self.show_pool_save(n)
            
            #end
            if count >= 1:
                break
        
        #
        para = []
        for j in range(self.para_num):
            para.append(self.para_range[j][self.pool[self.best_index, j]])
        para = np.array(para)
        
        #'bar'またはsaveなら改行
        if self.show_pool_func == 'bar': print()
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                print()
        
        #Noneでなければ出力
        if self.show_pool_func != None:
            print('__________________ results _________________')
            print('para : {}'.format(para))
            print('score : {}'.format(self.score_best))
            print('____________________ end ___________________')
        
        return para, self.score_best
        
        

    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def setGA(self, para_range, set_num, score_func, aim, show_pool_func=None, seed=None, pool_num=None, max_gen=None):
        
        #setGA, para_range==ndarray, pool==[o, 2,...]int set
        
        #pre
        para_range = np.array(para_range)
        
        #setting 1-3
        self.setting_1(para_range, score_func, aim, show_pool_func, seed, pool_num, max_gen)
        self.set_num = set_num
        self.para_num = self.set_num #update
        self.setting_2(self.para_num*10, 2, 4)
        self.setting_3(int)
        self.print_info()
        
        #specific
        self.para_index = np.arange(len(self.para_range)) # para_indexはnumpy形式で用いる
        
        #gen 1 pool
        for i in range(self.pool_num):
            self.pool[i] = nr.choice(self.para_index, self.set_num, replace=False)
            #self.pool[i] = np.sort(self.pool[i])
        
        #
        self.score_pool()
        self.save_best_mean()
        
        self.init_score_range = (np.min(self.pool_score), np.max(self.pool_score))
        self.init_gap_mean = deepcopy(self.gap_mean)
        
        #show
        if self.show_pool_func == None: pass
        elif self.show_pool_func == 'bar': self.show_pool_bar(0)
        elif self.show_pool_func == 'print': self.show_pool_print(0)
        elif self.show_pool_func == 'plot': self.show_pool_plot(0)
        elif callable(self.show_pool_func) : self.show_pool(0) #関数であれば
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                if not os.path.exists(show_pool_func): os.mkdir(show_pool_func) #保存フォルダを作成
                self.show_pool_save(0)

        #gen 2-
        count = 0
        for n in range(1, self.max_n + 1):
            #
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)            
            
                #subtour exchange cross
                #==============================================================
                #common part
                common_set = set(self.parent[0]) & set(self.parent[1])
                #uncommon part
                uncommon_set = set(self.para_index) - common_set
                #child
                for i in range(len(self.child)):
                    rand_part = nr.choice(np.array(list(uncommon_set)), self.set_num - len(common_set), replace=False)

                    self.child[i] = np.hstack((np.array(list(common_set)), rand_part))
                    #self.child[i, :len(common_part)] = np.array(list(common_part))
                    #self.child[i, len(common_part):] = rand_part
                    
                    #self.child[i] = np.sort(self.child[i])
                #mutation
                #==============================================================
                for ch in self.child[2:]:
                    for j in range(self.set_num):
                        if nr.rand() < (1.0 / self.set_num):
                            akak = nr.choice(self.para_index)
                            if akak not in ch:
                                ch[j] = akak
                #==============================================================
                #
                self.score_child()
                self.make_family()
                self.JGG()
                
            #end check
            count += self.end_check()
            
            #
            self.save_best_mean()
            
            #show
            if self.show_pool_func == None: pass
            elif self.show_pool_func == 'bar': self.show_pool_bar(n * self.pool_num)
            elif self.show_pool_func == 'print': self.show_pool_print(n * self.pool_num)
            elif self.show_pool_func == 'plot': self.show_pool_plot(n * self.pool_num)
            elif callable(self.show_pool_func) : self.show_pool(n * self.pool_num) #関数であれば
            elif type(show_pool_func) == str:
                if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                    self.show_pool_save(n)
            
            #end
            if count >= 1:
                break
        
        #
        para = self.para_range[self.pool_best]
        
        #'bar'またはsaveなら改行
        if self.show_pool_func == 'bar': print()
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                print()
        
        #Noneでなければ出力
        if self.show_pool_func != None:
            print('__________________ results _________________')
            print('para : {}'.format(para))
            print('score : {}'.format(self.score_best))
            print('____________________ end ___________________')
        
        return para, self.score_best

        
    #==============================================================#==============================================================
    #==============================================================#==============================================================
    def rcGA(self, para_range, score_func, aim, show_pool_func='bar', seed=None, pool_num=None, max_gen=None):
        
        #rcGA, para_range==ndarray, pool==[0.0, 1.0]float
        
        #pre
        para_range = np.array(para_range)
        if para_range.ndim == 1:
            para_range = para_range.reshape(1, 2)
        
        #setting 1-3
        self.setting_1(para_range, score_func, aim, show_pool_func, seed, pool_num, max_gen)
        self.setting_2(self.para_num*10, 2, 4)
        self.setting_3(float)
        self.print_info()
        
        #specific init sd
        self.sd = 1.2 / math.sqrt(self.parent_num)
        
        #gen 1 pool
        #==============================================================
        #point_choice for gen 1 pool [0.0, 1.0] x10
        if self.para_num == 1:
            point_choice = np.tile(np.array([0.5]), (self.pool_num // self.para_num) + 1)
        else:
            point_choice = np.tile(np.arange(0.0, 1.000001, 1.0/(self.para_num - 1)), (self.pool_num // self.para_num) + 1)
        
        #gen 1 pool
        for j in range(self.para_num):
            self.pool[:, j] = nr.permutation(point_choice[:self.pool_num])
        
        #perturbation
        if self.para_num == 1:
            self.pool += nr.rand(self.pool_num, self.para_num) * 1.0 - 0.5
        else:
            self.pool += nr.rand(self.pool_num, self.para_num) * (2.0/(3*self.para_num - 3)) - (1.0/(3*self.para_num - 3))
        
        #clip
        self.pool = np.clip(self.pool, 0.0, 1.0)
        
        #euclid distance
        def euclid(a):
            dists = np.expand_dims(self.pool, axis=1) - np.expand_dims(self.pool, axis=0)
            dists = np.sqrt(np.sum(dists ** 2, axis=-1))
            dists = np.sum(dists, axis=-1) / self.pool_num
            return dists
        
        #gen 1 pool distribution
        if self.pool_num <= 5*10:
            try_num = 200
        elif self.pool_num <= 10*10:
            try_num = 150
        elif self.pool_num <= 15*10:
            try_num = 70
        elif self.pool_num <= 20*10:
            try_num = 30
        elif self.pool_num <= 30*10:
            try_num = 12
        else:
            try_num = 0
        stop = False
        for i in range(try_num):
            dists_now = euclid(self.pool)
            select_id = np.argmin(dists_now)
            #re-born
            self.pool[select_id] = nr.rand(self.para_num)
            dists = euclid(self.pool)
            #改善するまで動かす
            count = 0
            while np.sum(dists) < np.sum(dists_now):
                #re-born
                self.pool[select_id] = nr.rand(self.para_num)
                dists = euclid(self.pool)
                count += 1
                if count == try_num:
                    #print('stop')
                    stop = True
                    break
            if stop == True:
                break
        #==============================================================
        

        #
        self.score_pool_rc()        
        self.save_best_mean()
        
        self.init_score_range = (np.min(self.pool_score), np.max(self.pool_score))
        self.init_gap_mean = deepcopy(self.gap_mean)
        
        #show
        if self.show_pool_func == None: pass
        elif self.show_pool_func == 'bar': self.show_pool_bar(0)
        elif self.show_pool_func == 'print': self.show_pool_print(0)
        elif self.show_pool_func == 'plot': self.show_pool_plot(0)
        elif callable(self.show_pool_func) : self.show_pool_rc(0) #関数であれば
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                if not os.path.exists(show_pool_func): os.mkdir(show_pool_func) #保存フォルダを作成
                self.show_pool_save(0)
        
        #gen 2-
        count = 0
        for n in range(1, self.max_n + 1):
            #
            #iteration
            iteration = np.arange(self.pool_num)
            nr.shuffle(iteration)
            iteration = iteration.reshape((self.pool_num//self.parent_num), self.parent_num)
            for it in iteration:
                #
                self.make_parent(it)
                
                #REX
                #==============================================================
                #parant average
                ave = np.mean(self.parent, axis=0)
                #child
                self.child[:, :] = 2.0
                for i in range(self.child_num):
                    for j in range(self.para_num):
                        #average
                        self.child[i, j] = ave[j]
                        #perturbation
                        for k in range(self.parent_num):
                            self.child[i, j] += nr.normal(0, self.sd) * (self.parent[k][j] - ave[j])
                #clip
                self.child = np.clip(self.child, 0.0, 1.0)
                #==============================================================
                #
                self.score_child_rc()
                self.make_family()
                self.JGG()
            
            #sd change
            #print(self.sd)
            self.sd = max(self.sd *0.995, 0.9 / math.sqrt(self.parent_num))
            
            #end check
            if np.max(np.std(self.pool, axis=0)) < 0.03:
                count += 1
            
            #
            self.save_best_mean()   
            
            #show
            if self.show_pool_func == None: pass
            elif self.show_pool_func == 'bar': self.show_pool_bar(n * self.pool_num)
            elif self.show_pool_func == 'print': self.show_pool_print(n * self.pool_num)
            elif self.show_pool_func == 'plot': self.show_pool_plot(n * self.pool_num)
            elif callable(self.show_pool_func) : self.show_pool_rc(n * self.pool_num) #関数であれば
            elif type(show_pool_func) == str:
                if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                    self.show_pool_save(n)
            
            #end
            if count >= 1:
                break
        
        #
        para = self.pool_best * (self.para_range[:, 1] - self.para_range[:, 0]) + self.para_range[:, 0]
        
        #'bar'またはsaveなら改行
        if self.show_pool_func == 'bar': print()
        elif type(show_pool_func) == str:
            if len(show_pool_func) > 0 and show_pool_func[-1] == '/':
                print()
        
        #Noneでなければ出力
        if self.show_pool_func != None:
            print('__________________ results _________________')
            print('para : {}'.format(para))
            print('score : {}'.format(self.score_best))
            print('____________________ end ___________________')
        
        return para, self.score_best
        
    
    






if __name__ == '__main__':
    pass


    
    
    
    '''
    __spec__ = 'ModuleSpec(name=\'builtins\', loader=<class \'_frozen_importlib.BuiltinImporter\'>)'
    with Pool() as pool:
        results = pool.map(parafunc, range(20))
    
    print (results)'''










