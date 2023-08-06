# -*- coding: utf-8 -*-
import math ,time ,os #line:2
import numpy as np #line:3
import numpy .random as nr #line:4
from copy import deepcopy #line:5
import matplotlib .pyplot as plt #line:6
from joblib import Parallel ,delayed #line:7
import hashlib #line:8
md5_s =['6c11f117a84c860c4044f8a1a45a0e67','cb51d4bbfdf4cc67e8bec57bc57e21c8','28f9afcaa52714aa964e215b7247a691','57f92316a9e611dd97c1528694ff6f9f','fd3dbb083970d4ba54ff6d067ab0c320','57c3d88ebf6777016c1429d25f283052','5f12a9899da112ee22a9a3ca7286b75b','9c84d4d198be8a5ef0dd96a8df934a80','df9c3ded3fe362c4c513a2bb3b28383f','12536e9b1dad1aabd97139327a115cc4','2a282b5b4649959c8a37c38e333789ad','0946a6c2e833058ced3d4798ba7ed903','432b8b1a39018c5b423f618c825a170c','46332f4160a17a9cb13fe5a559a66004','53630aba1c1685f49a216d70eb6bb7e0','acd9e269de3dcf51a4090cc907ae6ca9','affe60d5c024c79e77e7723bbca9608d','985b95f3aa925b05f3ac50561bab5dc2','2b7b9589e306a4419a7b259a1a7f1127','f9ac39e0da75c423a92003125f573429','0a988276a12594b79f9d79457371a1ad','ff4808135d6784b9a849f650cf579a46','91f88b573ccf4e2cc31da287baaff287','660440c7e709d6d3cd86293bd8ef1368','d552702c3e333e8c8e0d766c9b2c2b1c','31cd4b4c4b6964a1d4b1f78e8d2b213e','03a6a04c30c6d5b2041671c39eeec57e','503b8c8889c87da762be47d452d9fe12','146aec80f4ccdd435a2aaf7339e598e8','a02c5ad1046ed530f5e96c317300f312']#line:43
class vcopt :#line:62
    def __init__ (O00O0OO0O00O00000 ):#line:63
        pass #line:64
    def __del__ (OOO0O0OOOO0O0000O ):#line:65
        pass #line:66
    def setting_1 (OOO000OO0OOOOOOOO ,OOOOO00000OOOOOO0 ,O0O000000000OOOO0 ,O0OO000O00O00O000 ,O0OO0OO0O0O0OOO00 ,O0OO00OOOOOO0O00O ,O0OO0OOOOO000O0O0 ,O000OOOOO000OOOO0 ,OO0O00O0OO00OOOOO ):#line:70
        OOO000OO0OOOOOOOO .para_range =OOOOO00000OOOOOO0 #line:71
        OOO000OO0OOOOOOOO .para_num =len (OOOOO00000OOOOOO0 )#line:72
        OOO000OO0OOOOOOOO .score_func =O0O000000000OOOO0 #line:73
        OOO000OO0OOOOOOOO .aim =float (O0OO000O00O00O000 )#line:74
        OOO000OO0OOOOOOOO .show_pool_func =O0OO0OO0O0O0OOO00 #line:75
        if OOO000OO0OOOOOOOO .show_pool_func ==None :pass #line:77
        elif OOO000OO0OOOOOOOO .show_pool_func in ['bar','print','plot']:pass #line:78
        elif callable (OOO000OO0OOOOOOOO .show_pool_func ):pass #line:79
        elif type (O0OO0OO0O0O0OOO00 )==str :#line:80
            if len (O0OO0OO0O0O0OOO00 )==0 or O0OO0OO0O0O0OOO00 [-1 ]!='/':#line:81
                OOO000OO0OOOOOOOO .show_pool_func ='bar'#line:82
        if type (O0OO00OOOOOO0O00O )in [int ,float ]:#line:84
            OOO000OO0OOOOOOOO .seed =int (O0OO00OOOOOO0O00O )#line:85
        else :#line:86
            OOO000OO0OOOOOOOO .seed =None #line:87
        nr .seed (OOO000OO0OOOOOOOO .seed )#line:88
        OO00OOO00OOO000OO =1577804400.0 #line:89
        if type (O0OO0OOOOO000O0O0 )in [int ,float ]:#line:91
            OOO000OO0OOOOOOOO .pool_num =int (O0OO0OOOOO000O0O0 )#line:92
            if OOO000OO0OOOOOOOO .pool_num %2 !=0 :#line:94
                OOO000OO0OOOOOOOO .pool_num +=1 #line:95
        else :#line:96
            OOO000OO0OOOOOOOO .pool_num =None #line:97
        if type (O000OOOOO000OOOO0 )in [int ,float ]:#line:99
            OOO000OO0OOOOOOOO .max_gen =int (O000OOOOO000OOOO0 )#line:100
        else :#line:101
            OOO000OO0OOOOOOOO .max_gen =None #line:102
        OOO000OO0OOOOOOOO .core_num =9 -8 #line:105
        if type (OO0O00O0OO00OOOOO )in [int ,float ]:#line:106
            O00OO00OO000OOOO0 =hashlib .md5 (str (O0OO00OOOOOO0O00O ).encode ()).hexdigest ()#line:108
            if O00OO00OO000OOOO0 in md5_s and time .time ()<OO00OOO00OOO000OO :#line:109
                OOO000OO0OOOOOOOO .core_num =int (OO0O00O0OO00OOOOO )#line:110
        OOO000OO0OOOOOOOO .start =time .time ()#line:111
    def setting_2 (OO0O00OO0O0OO00O0 ,O00OOOOOOOOO0000O ,OO00O0OO00OOO0000 ,O0000O0000000OO0O ):#line:115
        if OO0O00OO0O0OO00O0 .pool_num is None :#line:117
            OO0O00OO0O0OO00O0 .pool_num =O00OOOOOOOOO0000O #line:118
        OO0O00OO0O0OO00O0 .parent_num =OO00O0OO00OOO0000 #line:119
        OO0O00OO0O0OO00O0 .child_num =O0000O0000000OO0O #line:120
        OO0O00OO0O0OO00O0 .family_num =OO00O0OO00OOO0000 +O0000O0000000OO0O #line:121
        if OO0O00OO0O0OO00O0 .max_gen is None :#line:123
            OO0O00OO0O0OO00O0 .max_n =1000000 #line:124
        else :#line:125
            OO0O00OO0O0OO00O0 .max_n =OO0O00OO0O0OO00O0 .max_gen //OO0O00OO0O0OO00O0 .pool_num +1 #line:126
    def setting_3 (O0O0OOO0000OO0OO0 ,OOO00O0000O0O0OOO ):#line:130
        O0O0OOO0000OO0OO0 .pool ,O0O0OOO0000OO0OO0 .pool_score =np .zeros ((O0O0OOO0000OO0OO0 .pool_num ,O0O0OOO0000OO0OO0 .para_num ),dtype =OOO00O0000O0O0OOO ),np .zeros (O0O0OOO0000OO0OO0 .pool_num )#line:131
        O0O0OOO0000OO0OO0 .parent ,O0O0OOO0000OO0OO0 .parent_score =np .zeros ((O0O0OOO0000OO0OO0 .parent_num ,O0O0OOO0000OO0OO0 .para_num ),dtype =OOO00O0000O0O0OOO ),np .zeros (O0O0OOO0000OO0OO0 .parent_num )#line:132
        O0O0OOO0000OO0OO0 .child ,O0O0OOO0000OO0OO0 .child_score =np .zeros ((O0O0OOO0000OO0OO0 .child_num ,O0O0OOO0000OO0OO0 .para_num ),dtype =OOO00O0000O0O0OOO ),np .zeros (O0O0OOO0000OO0OO0 .child_num )#line:133
        O0O0OOO0000OO0OO0 .family ,O0O0OOO0000OO0OO0 .family_score =np .zeros ((O0O0OOO0000OO0OO0 .family_num ,O0O0OOO0000OO0OO0 .para_num ),dtype =OOO00O0000O0O0OOO ),np .zeros (O0O0OOO0000OO0OO0 .family_num )#line:134
    def print_info (O0O0O000OO000OO00 ):#line:138
        if O0O0O000OO000OO00 .show_pool_func is not None :#line:139
            print ('___________________ info ___________________')#line:140
            print ('para_range : n={}'.format (O0O0O000OO000OO00 .para_num ))#line:141
            print ('score_func : {}'.format (type (O0O0O000OO000OO00 .score_func )))#line:142
            print ('aim : {}'.format (O0O0O000OO000OO00 .aim ))#line:143
            print ('show_pool_func : \'{}\''.format (O0O0O000OO000OO00 .show_pool_func ))#line:145
            print ('seed : {}'.format (O0O0O000OO000OO00 .seed ))#line:146
            print ('pool_num : {}'.format (O0O0O000OO000OO00 .pool_num ))#line:147
            print ('max_gen : {}'.format (O0O0O000OO000OO00 .max_gen ))#line:148
            if O0O0O000OO000OO00 .core_num ==1 :#line:149
                print ('core_num : {} (*vcopt, vc-grendel)'.format (O0O0O000OO000OO00 .core_num ))#line:150
            else :#line:151
                print ('core_num : {} (vcopt, *vc-grendel)'.format (O0O0O000OO000OO00 .core_num ))#line:152
            print ('___________________ start __________________')#line:153
    def score_pool_multi (OOOOOO00OO0OOOO00 ,O00OO0OO0O00O00OO ):#line:157
        O0O000O0O00OO000O =OOOOOO00OO0OOOO00 .para_range [OOOOOO00OO0OOOO00 .pool [O00OO0OO0O00O00OO ]]#line:158
        OOOOOO00OO0OOOO00 .pool_score [O00OO0OO0O00O00OO ]=OOOOOO00OO0OOOO00 .score_func (O0O000O0O00OO000O )#line:159
        OOOOOO00OO0OOOO00 .aaa +=1 #line:160
        if OOOOOO00OO0OOOO00 .show_pool_func !=None :#line:161
            O0O0OOO00000O0000 ='\rScoring first gen {}/{}        '.format (O00OO0OO0O00O00OO +1 ,OOOOOO00OO0OOOO00 .pool_num )#line:162
            print (O0O0OOO00000O0000 ,end ='')#line:163
    def score_pool (OOOOO0O000OO00OO0 ):#line:164
        OOOOO0O000OO00OO0 .aaa =0 #line:165
        Parallel (n_jobs =OOOOO0O000OO00OO0 .core_num ,require ='sharedmem')([delayed (OOOOO0O000OO00OO0 .score_pool_multi )(O0OO0OOO000O00000 )for O0OO0OOO000O00000 in range (OOOOO0O000OO00OO0 .pool_num )])#line:166
        if OOOOO0O000OO00OO0 .show_pool_func !=None :#line:167
            OOOO0O00OO0000O00 ='\rScoring first gen {}/{}        '.format (OOOOO0O000OO00OO0 .pool_num ,OOOOO0O000OO00OO0 .pool_num )#line:168
            print (OOOO0O00OO0000O00 )#line:169
    def score_pool_dc_multi (OO00O00OO0OOO00O0 ,O000OO0000O0O0OOO ):#line:180
        O0O0OOOOOO0OO0OO0 =[]#line:181
        for OOO000O000OOO000O in range (OO00O00OO0OOO00O0 .para_num ):#line:182
            O0O0OOOOOO0OO0OO0 .append (OO00O00OO0OOO00O0 .para_range [OOO000O000OOO000O ][OO00O00OO0OOO00O0 .pool [O000OO0000O0O0OOO ,OOO000O000OOO000O ]])#line:183
        O0O0OOOOOO0OO0OO0 =np .array (O0O0OOOOOO0OO0OO0 )#line:184
        OO00O00OO0OOO00O0 .pool_score [O000OO0000O0O0OOO ]=OO00O00OO0OOO00O0 .score_func (O0O0OOOOOO0OO0OO0 )#line:185
        OO00O00OO0OOO00O0 .aaa +=1 #line:186
        if OO00O00OO0OOO00O0 .show_pool_func !=None :#line:187
            O0O000O00OOOOO000 ='\rScoring first gen {}/{}        '.format (O000OO0000O0O0OOO +1 ,OO00O00OO0OOO00O0 .pool_num )#line:188
            print (O0O000O00OOOOO000 ,end ='')#line:189
    def score_pool_dc (O000O000O00O0O00O ):#line:190
        O000O000O00O0O00O .aaa =0 #line:191
        Parallel (n_jobs =O000O000O00O0O00O .core_num ,require ='sharedmem')([delayed (O000O000O00O0O00O .score_pool_dc_multi )(O0O0OO0O0000O0OO0 )for O0O0OO0O0000O0OO0 in range (O000O000O00O0O00O .pool_num )])#line:192
        if O000O000O00O0O00O .show_pool_func !=None :#line:193
            O0O00OO00O0O00000 ='\rScoring first gen {}/{}        '.format (O000O000O00O0O00O .pool_num ,O000O000O00O0O00O .pool_num )#line:194
            print (O0O00OO00O0O00000 )#line:195
    def score_pool_rc_multi (O0OO0O00O000O00O0 ,OO00OO0000O0000O0 ):#line:209
        O0O0O0OO0000O000O =O0OO0O00O000O00O0 .pool [OO00OO0000O0000O0 ]*(O0OO0O00O000O00O0 .para_range [:,1 ]-O0OO0O00O000O00O0 .para_range [:,0 ])+O0OO0O00O000O00O0 .para_range [:,0 ]#line:210
        O0OO0O00O000O00O0 .pool_score [OO00OO0000O0000O0 ]=O0OO0O00O000O00O0 .score_func (O0O0O0OO0000O000O )#line:211
        O0OO0O00O000O00O0 .aaa +=1 #line:212
        if O0OO0O00O000O00O0 .show_pool_func !=None :#line:213
            OOOOOO00OOOOO00OO ='\rScoring first gen {}/{}        '.format (OO00OO0000O0000O0 +1 ,O0OO0O00O000O00O0 .pool_num )#line:214
            print (OOOOOO00OOOOO00OO ,end ='')#line:215
    def score_pool_rc (O00OOO0OO000O0O0O ):#line:216
        O00OOO0OO000O0O0O .aaa =0 #line:217
        Parallel (n_jobs =O00OOO0OO000O0O0O .core_num ,require ='sharedmem')([delayed (O00OOO0OO000O0O0O .score_pool_rc_multi )(O00OO000OO000O0OO )for O00OO000OO000O0OO in range (O00OOO0OO000O0O0O .pool_num )])#line:218
        if O00OOO0OO000O0O0O .show_pool_func !=None :#line:219
            O0OO00000OO00OOOO ='\rScoring first gen {}/{}        '.format (O00OOO0OO000O0O0O .pool_num ,O00OOO0OO000O0O0O .pool_num )#line:220
            print (O0OO00000OO00OOOO )#line:221
    def save_best_mean (O000O0000O0OOOOO0 ):#line:255
        O000O0000O0OOOOO0 .best_index =np .argmin (np .abs (O000O0000O0OOOOO0 .aim -O000O0000O0OOOOO0 .pool_score ))#line:257
        O000O0000O0OOOOO0 .pool_best =deepcopy (O000O0000O0OOOOO0 .pool [O000O0000O0OOOOO0 .best_index ])#line:259
        O000O0000O0OOOOO0 .score_best =deepcopy (O000O0000O0OOOOO0 .pool_score [O000O0000O0OOOOO0 .best_index ])#line:260
        O000O0000O0OOOOO0 .score_mean =np .mean (O000O0000O0OOOOO0 .pool_score )#line:263
        O000O0000O0OOOOO0 .gap_mean =np .mean (np .abs (O000O0000O0OOOOO0 .aim -O000O0000O0OOOOO0 .pool_score ))#line:264
        O000O0000O0OOOOO0 .score_mean_save =deepcopy (O000O0000O0OOOOO0 .score_mean )#line:266
        O000O0000O0OOOOO0 .gap_mean_save =deepcopy (O000O0000O0OOOOO0 .gap_mean )#line:267
    def make_parent (O00OO0OOOOO00O000 ,OOOOO0O00O000O000 ):#line:271
        O00OO0OOOOO00O000 .pool_select =OOOOO0O00O000O000 #line:272
        O00OO0OOOOO00O000 .parent =O00OO0OOOOO00O000 .pool [O00OO0OOOOO00O000 .pool_select ]#line:273
        O00OO0OOOOO00O000 .parent_score =O00OO0OOOOO00O000 .pool_score [O00OO0OOOOO00O000 .pool_select ]#line:274
    def make_family (OO0O00O00OOO00OO0 ):#line:278
        OO0O00O00OOO00OO0 .family =np .vstack ((OO0O00O00OOO00OO0 .child ,OO0O00O00OOO00OO0 .parent ))#line:279
        OO0O00O00OOO00OO0 .family_score =np .hstack ((OO0O00O00OOO00OO0 .child_score ,OO0O00O00OOO00OO0 .parent_score ))#line:280
    def JGG (OOOOOO0O0O00O0OO0 ):#line:284
        OOOOOO0O0O00O0OO0 .family_select =np .argpartition (np .abs (OOOOOO0O0O00O0OO0 .aim -OOOOOO0O0O00O0OO0 .family_score ),OOOOOO0O0O00O0OO0 .parent_num )[:OOOOOO0O0O00O0OO0 .parent_num ]#line:287
        OOOOOO0O0O00O0OO0 .pool [OOOOOO0O0O00O0OO0 .pool_select ]=OOOOOO0O0O00O0OO0 .family [OOOOOO0O0O00O0OO0 .family_select ]#line:289
        OOOOOO0O0O00O0OO0 .pool_score [OOOOOO0O0O00O0OO0 .pool_select ]=OOOOOO0O0O00O0OO0 .family_score [OOOOOO0O0O00O0OO0 .family_select ]#line:290
    def end_check (O000O0O00OOOOO00O ):#line:294
        O000O0O00OOOOO00O .best_index =np .argmin (np .abs (O000O0O00OOOOO00O .aim -O000O0O00OOOOO00O .pool_score ))#line:296
        O000O0O00OOOOO00O .score_best =deepcopy (O000O0O00OOOOO00O .pool_score [O000O0O00OOOOO00O .best_index ])#line:297
        O000O0O00OOOOO00O .gap_mean =np .mean (np .abs (O000O0O00OOOOO00O .aim -O000O0O00OOOOO00O .pool_score ))#line:299
        if O000O0O00OOOOO00O .score_best ==O000O0O00OOOOO00O .aim :#line:301
            return 10 #line:302
        if O000O0O00OOOOO00O .gap_mean >=O000O0O00OOOOO00O .gap_mean_save :#line:304
            return 1 #line:305
        return 0 #line:306
    def make_info (O0O0OOO0OOO0O0000 ,OOOOO0000O0000OOO ):#line:324
        O0O0OO0O00OO00OOO ={'gen':OOOOO0000O0000OOO ,'best_index':O0O0OOO0OOO0O0000 .best_index ,'best_score':round (O0O0OOO0OOO0O0000 .score_best ,4 ),'mean_score':round (O0O0OOO0OOO0O0000 .score_mean ,4 ),'mean_gap':round (O0O0OOO0OOO0O0000 .gap_mean ,4 ),'time':round (time .time ()-O0O0OOO0OOO0O0000 .start ,1 )}#line:329
        return O0O0OO0O00OO00OOO #line:330
    def show_pool (O0000O00OOOOOOO0O ,OO00000OO000000O0 ):#line:334
        O0000OOOO0OO0O0OO =O0000O00OOOOOOO0O .make_info (OO00000OO000000O0 )#line:335
        O0000O00OOOOOOO0O .show_pool_func (O0000O00OOOOOOO0O .para_range [O0000O00OOOOOOO0O .pool ],**O0000OOOO0OO0O0OO )#line:336
    def show_pool_dc (O0O0OO00OO0O0OOO0 ,OO00O00000OOO0000 ):#line:337
        O0OO0O0OO0OOO0O0O =O0O0OO00OO0O0OOO0 .make_info (OO00O00000OOO0000 )#line:338
        OO00OOOO0O0O0O0OO =[]#line:339
        for OOO000O0O0OOO0O0O in range (O0O0OO00OO0O0OOO0 .pool_num ):#line:340
            OO0O0OOO00OOO000O =[]#line:341
            for OOO0OOO00OO00OOOO in range (O0O0OO00OO0O0OOO0 .para_num ):#line:342
                OO0O0OOO00OOO000O .append (O0O0OO00OO0O0OOO0 .para_range [OOO0OOO00OO00OOOO ][O0O0OO00OO0O0OOO0 .pool [OOO000O0O0OOO0O0O ,OOO0OOO00OO00OOOO ]])#line:343
            OO00OOOO0O0O0O0OO .append (OO0O0OOO00OOO000O )#line:344
        OO00OOOO0O0O0O0OO =np .array (OO00OOOO0O0O0O0OO )#line:345
        O0O0OO00OO0O0OOO0 .show_pool_func (OO00OOOO0O0O0O0OO ,**O0OO0O0OO0OOO0O0O )#line:346
    def show_pool_rc (OOOOOOOO0O000O0OO ,OO0000OO0OO00OOO0 ):#line:347
        OO00O0O000O00OO0O =OOOOOOOO0O000O0OO .make_info (OO0000OO0OO00OOO0 )#line:348
        O0OO0OO000OOO00O0 =np .array (list (map (lambda OO0O0O0O0OOO0000O :OOOOOOOO0O000O0OO .pool [OO0O0O0O0OOO0000O ]*(OOOOOOOO0O000O0OO .para_range [:,1 ]-OOOOOOOO0O000O0OO .para_range [:,0 ])+OOOOOOOO0O000O0OO .para_range [:,0 ],range (OOOOOOOO0O000O0OO .pool_num ))))#line:351
        OOOOOOOO0O000O0OO .show_pool_func (O0OO0OO000OOO00O0 ,**OO00O0O000O00OO0O )#line:352
    def make_round (O0O000O00OO0O0OOO ):#line:356
        O00OO0O000OOO0000 =round (O0O000O00OO0O0OOO .score_best ,4 )#line:357
        O0000O0000O0OOO0O =round (O0O000O00OO0O0OOO .score_mean ,4 )#line:358
        OO0OOOO0O000O0OOO =round (O0O000O00OO0O0OOO .gap_mean ,4 )#line:359
        O00O0O0000O0OOOOO =round (time .time ()-O0O000O00OO0O0OOO .start ,1 )#line:360
        return O00OO0O000OOO0000 ,O0000O0000O0OOO0O ,OO0OOOO0O000O0OOO ,O00O0O0000O0OOOOO #line:361
    def show_pool_bar (OOOO0O0OOO0O0OOOO ,OO00OO000OO00OO0O ):#line:366
        O0O0OO0000O00O0O0 =round (OOOO0O0OOO0O0OOOO .score_best ,4 )#line:368
        OO0O000O00OO00000 =min (abs (OOOO0O0OOO0O0OOOO .aim -OOOO0O0OOO0O0OOOO .init_score_range [0 ]),abs (OOOO0O0OOO0O0OOOO .aim -OOOO0O0OOO0O0OOOO .init_score_range [1 ]))#line:370
        O0OOOOOOOOO0OOO0O =abs (OOOO0O0OOO0O0OOOO .aim -OOOO0O0OOO0O0OOOO .score_best )#line:371
        OO00O00OOO00000OO =min (abs (OOOO0O0OOO0O0OOOO .aim -OOOO0O0OOO0O0OOOO .gap_mean ),OO0O000O00OO00000 )#line:372
        if OO0O000O00OO00000 ==0 :#line:374
            OO0O000O00OO00000 =0.001 #line:375
        OOOOOO00OO0000O00 =int (O0OOOOOOOOO0OOO0O /OO0O000O00OO00000 *40 )#line:376
        OOO0OO000O00O0O00 =int ((OO00O00OOO00000OO -O0OOOOOOOOO0OOO0O )/OO0O000O00OO00000 *40 )#line:377
        OO0O00O00OO0O00O0 =40 -OOOOOO00OO0000O00 -OOO0OO000O00O0O00 #line:378
        OO000OO0O000000O0 ='\r|{}+{}<{}| gen={}, best_score={}'.format (' '*OOOOOO00OO0000O00 ,' '*OOO0OO000O00O0O00 ,' '*OO0O00O00OO0O00O0 ,OO00OO000OO00OO0O ,O0O0OO0000O00O0O0 )#line:380
        print (OO000OO0O000000O0 ,end ='')#line:381
        if OO00OO000OO00OO0O ==0 :#line:383
            time .sleep (0.2 )#line:384
    def show_pool_print (OO00O0O0O0OOOO00O ,OOO00OO0000O000O0 ):#line:386
        O0O00OO0O0O00OO0O ,OOOOOOOO000O0000O ,O0O0OO00O00OO0OOO ,O0O0O0OO00O000000 =OO00O0O0O0OOOO00O .make_round ()#line:387
        print ('gen={}, best_score={}, mean_score={}, mean_gap={}, time={}'.format (OOO00OO0000O000O0 ,O0O00OO0O0O00OO0O ,OOOOOOOO000O0000O ,O0O0OO00O00OO0OOO ,O0O0O0OO00O000000 ))#line:388
    def show_pool_plot (O0O00OOOOOOO0OOOO ,OOOO0OOO000OO000O ):#line:391
        O00O0O0000O0O0OOO ,O0OO00000OO0O00O0 ,OO000OO0OOO000000 ,O000OOO0OO0OO0OO0 =O0O00OOOOOOO0OOOO .make_round ()#line:392
        plt .bar (range (len (O0O00OOOOOOO0OOOO .pool_score [:100 ])),O0O00OOOOOOO0OOOO .pool_score [:100 ])#line:394
        plt .ylim ([min (O0O00OOOOOOO0OOOO .aim ,O0O00OOOOOOO0OOOO .init_score_range [0 ]),max (O0O00OOOOOOO0OOOO .aim ,O0O00OOOOOOO0OOOO .init_score_range [1 ])])#line:395
        plt .title ('gen={}{}best_score={}{}mean_score={}{}mean_gap={}{}time={}'.format (OOOO0OOO000OO000O ,'\n',O00O0O0000O0O0OOO ,'\n',O0OO00000OO0O00O0 ,'\n',OO000OO0OOO000000 ,'\n',O000OOO0OO0OO0OO0 ),loc ='left')#line:396
        plt .show ();plt .close ();print ()#line:397
    def show_pool_save (OOO0O00O0OOO000O0 ,O00OOO00OO00O0O0O ):#line:400
        OOO0O00O0OOO000O0 .show_pool_bar (O00OOO00OO00O0O0O )#line:402
        OO00O000OOOOO00OO ,O0000OOOOOOO00000 ,O0OO00OOO00O0O000 ,O00000O0OOO00OO0O =OOO0O00O0OOO000O0 .make_round ()#line:404
        plt .bar (range (len (OOO0O00O0OOO000O0 .pool_score [:100 ])),OOO0O00O0OOO000O0 .pool_score [:100 ])#line:406
        plt .ylim ([min (OOO0O00O0OOO000O0 .aim ,OOO0O00O0OOO000O0 .init_score_range [0 ]),max (OOO0O00O0OOO000O0 .aim ,OOO0O00O0OOO000O0 .init_score_range [1 ])])#line:407
        plt .title ('gen={}{}best_score={}{}mean_score={}{}mean_gap={}{}time={}'.format (O00OOO00OO00O0O0O ,'\n',OO00O000OOOOO00OO ,'\n',O0000OOOOOOO00000 ,'\n',O0OO00OOO00O0O000 ,'\n',O00000O0OOO00OO0O ),loc ='left')#line:408
        plt .subplots_adjust (left =0.1 ,right =0.95 ,bottom =0.1 ,top =0.70 )#line:409
        plt .savefig (OOO0O00O0OOO000O0 .show_pool_func +'round_{}.png'.format (str (O00OOO00OO00O0O0O ).zfill (4 )));plt .close ()#line:410
    def opt2 (O00O000O00000000O ,O000000O0O000OO0O ,O00O0OOO000O000O0 ,O0O0O00OO0O00OOO0 ,show_para_func =None ,seed =None ,step_max =float ('inf')):#line:416
        O000000O0O000OO0O ,O00OO0OOOOO0OOO0O =np .array (O000000O0O000OO0O ),O00O0OOO000O000O0 (O000000O0O000OO0O )#line:418
        O0O0OO00O000O0000 ={}#line:419
        if seed !='pass':nr .seed (seed )#line:420
        O00O000O00O00OOOO =0 #line:421
        if show_para_func !=None :#line:423
            O0O0OO00O000O0000 .update ({'step_num':O00O000O00O00OOOO ,'score':round (O00OO0OOOOO0OOO0O ,3 )})#line:424
            show_para_func (O000000O0O000OO0O ,**O0O0OO00O000O0000 )#line:425
        while 1 :#line:427
            O0OO0O00OOOO0OOOO =False #line:428
            if O00O000O00O00OOOO >=step_max :#line:429
                break #line:431
            O000O0000O0O00O00 =np .arange (0 ,len (O000000O0O000OO0O )-1 )#line:433
            nr .shuffle (O000O0000O0O00O00 )#line:434
            for OOO0OO000000000OO in O000O0000O0O00O00 :#line:435
                if O0OO0O00OOOO0OOOO ==True :break #line:437
                OO00O0000O00OO0OO =np .arange (OOO0OO000000000OO +1 ,len (O000000O0O000OO0O ))#line:439
                nr .shuffle (OO00O0000O00OO0OO )#line:440
                for O0000O00O00000O00 in OO00O0000O00OO0OO :#line:441
                    if O0OO0O00OOOO0OOOO ==True :break #line:443
                    OO0O00000OO0O0000 =np .hstack ((O000000O0O000OO0O [:OOO0OO000000000OO ],O000000O0O000OO0O [OOO0OO000000000OO :O0000O00O00000O00 +1 ][::-1 ],O000000O0O000OO0O [O0000O00O00000O00 +1 :]))#line:446
                    OO0O0OOOO00O00O00 =O00O0OOO000O000O0 (OO0O00000OO0O0000 )#line:447
                    if np .abs (O0O0O00OO0O00OOO0 -OO0O0OOOO00O00O00 )<np .abs (O0O0O00OO0O00OOO0 -O00OO0OOOOO0OOO0O ):#line:450
                        O000000O0O000OO0O ,O00OO0OOOOO0OOO0O =OO0O00000OO0O0000 ,OO0O0OOOO00O00O00 #line:451
                        O00O000O00O00OOOO +=1 #line:452
                        if show_para_func !=None :#line:453
                            O0O0OO00O000O0000 .update ({'step_num':O00O000O00O00OOOO ,'score':round (O00OO0OOOOO0OOO0O ,3 )})#line:454
                            show_para_func (O000000O0O000OO0O ,**O0O0OO00O000O0000 )#line:455
                        O0OO0O00OOOO0OOOO =True #line:456
            if O0OO0O00OOOO0OOOO ==False :#line:457
                break #line:459
        return O000000O0O000OO0O ,O00OO0OOOOO0OOO0O #line:460
    def opt2_tspGA (OOO00OO00O00000O0 ,O00OO0O0OOOO00O0O ,OOO00OO00OOO0O0OO ,step_max =float ('inf')):#line:464
        O00OO0O0OOOO00O0O ,OOO00OO00OOO0O0OO =O00OO0O0OOOO00O0O ,OOO00OO00OOO0O0OO #line:466
        OO0OO000000OOOO00 =0 #line:467
        while 1 :#line:469
            OOOOO0OOOOO00O0OO =False #line:470
            if OO0OO000000OOOO00 >=step_max :#line:471
                break #line:472
            O000O0O000OO0O00O =np .arange (0 ,OOO00OO00O00000O0 .para_num -1 )#line:474
            nr .shuffle (O000O0O000OO0O00O )#line:476
            for OOO0O0O0OO0000O00 in O000O0O000OO0O00O :#line:477
                if OOOOO0OOOOO00O0OO ==True :break #line:479
                OO0O00O0OOO0OOO0O =np .arange (OOO0O0O0OO0000O00 +1 ,OOO00OO00O00000O0 .para_num )#line:481
                nr .shuffle (OO0O00O0OOO0OOO0O )#line:482
                for OO0000OOOO0O0OO0O in OO0O00O0OOO0OOO0O :#line:483
                    if OOOOO0OOOOO00O0OO ==True :break #line:485
                    O0OO00OOOO0O00OO0 =np .hstack ((O00OO0O0OOOO00O0O [:OOO0O0O0OO0000O00 ],O00OO0O0OOOO00O0O [OOO0O0O0OO0000O00 :OO0000OOOO0O0OO0O +1 ][::-1 ],O00OO0O0OOOO00O0O [OO0000OOOO0O0OO0O +1 :]))#line:488
                    OO00OOOOOOOOO0OO0 =OOO00OO00O00000O0 .score_func (OOO00OO00O00000O0 .para_range [O0OO00OOOO0O00OO0 ])#line:489
                    if np .abs (OOO00OO00O00000O0 .aim -OO00OOOOOOOOO0OO0 )<np .abs (OOO00OO00O00000O0 .aim -OOO00OO00OOO0O0OO ):#line:492
                        O00OO0O0OOOO00O0O ,OOO00OO00OOO0O0OO =O0OO00OOOO0O00OO0 ,OO00OOOOOOOOO0OO0 #line:493
                        OO0OO000000OOOO00 +=1 #line:494
                        OOOOO0OOOOO00O0OO =True #line:495
            if OOOOO0OOOOO00O0OO ==False :#line:496
                break #line:498
        return O00OO0O0OOOO00O0O ,OOO00OO00OOO0O0OO #line:499
    def tspGA_multi (OOOOO00OO00OOO0O0 ,OO00O00O0OOOOOO00 ):#line:528
        OOOO00OOOOOO0O000 =OOOOO00OO00OOO0O0 .pool [OO00O00O0OOOOOO00 ]#line:530
        O0000000OOO0OOO00 =OOOOO00OO00OOO0O0 .pool_score [OO00O00O0OOOOOO00 ]#line:531
        O0OOOO0O0000O0000 =np .ones ((OOOOO00OO00OOO0O0 .child_num ,OOOOO00OO00OOO0O0 .para_num ),dtype =int )#line:532
        O00O0O00000O0O0O0 =np .zeros (OOOOO00OO00OOO0O0 .child_num )#line:533
        O0O000O0O0O000OOO =np .hstack ((OOOO00OOOOOO0O000 [:,-2 :].reshape (OOOOO00OO00OOO0O0 .parent_num ,2 ),OOOO00OOOOOO0O000 ,OOOO00OOOOOO0O000 [:,:2 ].reshape (OOOOO00OO00OOO0O0 .parent_num ,2 )))#line:538
        for O0O0O000OO00OO0OO in range (OOOOO00OO00OOO0O0 .child_num ):#line:541
            OOOO00O0OO0OO000O =OOOO00OOOOOO0O000 [nr .randint (OOOOO00OO00OOO0O0 .parent_num ),0 ]#line:543
            if nr .rand ()<(1.0 /OOOOO00OO00OOO0O0 .para_num ):#line:544
                OOOO00O0OO0OO000O =nr .choice (OOOOO00OO00OOO0O0 .para_index )#line:545
            O0OOOO0O0000O0000 [O0O0O000OO00OO0OO ,0 ]=OOOO00O0OO0OO000O #line:546
            for OO000O00000OOO0O0 in range (1 ,OOOOO00OO00OOO0O0 .para_num ):#line:548
                O0OOO0000O000O00O =np .zeros ((OOOOO00OO00OOO0O0 .parent_num ,OOOOO00OO00OOO0O0 .para_num +4 ),dtype =bool )#line:550
                OOO00OOOO0OOO00O0 =np .zeros ((OOOOO00OO00OOO0O0 .parent_num ,OOOOO00OO00OOO0O0 .para_num +4 ),dtype =bool )#line:551
                O0OOO0000O000O00O [:,1 :-3 ]+=(OOOOO00OO00OOO0O0 .parent ==OOOO00O0OO0OO000O )#line:553
                O0OOO0000O000O00O [:,3 :-1 ]+=(OOOOO00OO00OOO0O0 .parent ==OOOO00O0OO0OO000O )#line:554
                OOO00OOOO0OOO00O0 [:,0 :-4 ]+=(OOOOO00OO00OOO0O0 .parent ==OOOO00O0OO0OO000O )#line:555
                OOO00OOOO0OOO00O0 [:,4 :]+=(OOOOO00OO00OOO0O0 .parent ==OOOO00O0OO0OO000O )#line:556
                O0OOOO0O00O00OOO0 =np .ones (OOOOO00OO00OOO0O0 .para_num )*(1.0 /OOOOO00OO00OOO0O0 .para_num )#line:559
                for OO0OO00OOO0O0000O in O0O000O0O0O000OOO [O0OOO0000O000O00O ]:#line:560
                    O0OOOO0O00O00OOO0 [np .where (OOOOO00OO00OOO0O0 .para_index ==OO0OO00OOO0O0000O )[0 ]]+=1.0 /OOOOO00OO00OOO0O0 .parent_num #line:561
                for OO0OO00OOO0O0000O in O0O000O0O0O000OOO [OOO00OOOO0OOO00O0 ]:#line:562
                    O0OOOO0O00O00OOO0 [np .where (OOOOO00OO00OOO0O0 .para_index ==OO0OO00OOO0O0000O )[0 ]]+=0.1 /OOOOO00OO00OOO0O0 .parent_num #line:563
                for OO0OO00OOO0O0000O in O0OOOO0O0000O0000 [O0O0O000OO00OO0OO ,0 :OO000O00000OOO0O0 ]:#line:566
                    O0OOOO0O00O00OOO0 [np .where (OOOOO00OO00OOO0O0 .para_index ==OO0OO00OOO0O0000O )[0 ]]=0.0 #line:567
                O0OOOO0O00O00OOO0 *=1.0 /np .sum (O0OOOO0O00O00OOO0 )#line:570
                OOOO00O0OO0OO000O =nr .choice (OOOOO00OO00OOO0O0 .para_index ,p =O0OOOO0O00O00OOO0 )#line:571
                O0OOOO0O0000O0000 [O0O0O000OO00OO0OO ,OO000O00000OOO0O0 ]=OOOO00O0OO0OO000O #line:573
        for O0O0O000OO00OO0OO in range (OOOOO00OO00OOO0O0 .child_num ):#line:577
            O000000OOOOOOOOOO =OOOOO00OO00OOO0O0 .para_range [O0OOOO0O0000O0000 [O0O0O000OO00OO0OO ]]#line:578
            O00O0O00000O0O0O0 [O0O0O000OO00OO0OO ]=OOOOO00OO00OOO0O0 .score_func (O000000OOOOOOOOOO )#line:579
        O0O00OO0O0OO00O00 =np .vstack ((O0OOOO0O0000O0000 ,OOOO00OOOOOO0O000 ))#line:581
        OO0O0O0OOO0OOOOOO =np .hstack ((O00O0O00000O0O0O0 ,O0000000OOO0OOO00 ))#line:582
        for O0O0O000OO00OO0OO in range (OOOOO00OO00OOO0O0 .family_num ):#line:584
            O0O00OO0O0OO00O00 [O0O0O000OO00OO0OO ],OO0O0O0OOO0OOOOOO [O0O0O000OO00OO0OO ]=OOOOO00OO00OOO0O0 .opt2_tspGA (O0O00OO0O0OO00O00 [O0O0O000OO00OO0OO ],OO0O0O0OOO0OOOOOO [O0O0O000OO00OO0OO ],step_max =OOOOO00OO00OOO0O0 .opt2_num )#line:585
        OO0OO0O0O0OOO000O =np .argpartition (np .abs (OOOOO00OO00OOO0O0 .aim -OO0O0O0OOO0OOOOOO ),OOOOO00OO00OOO0O0 .parent_num )[:OOOOO00OO00OOO0O0 .parent_num ]#line:587
        OOOOO00OO00OOO0O0 .pool [OO00O00O0OOOOOO00 ]=O0O00OO0O0OO00O00 [OO0OO0O0O0OOO000O ]#line:588
        OOOOO00OO00OOO0O0 .pool_score [OO00O00O0OOOOOO00 ]=OO0O0O0OOO0OOOOOO [OO0OO0O0O0OOO000O ]#line:589
    def tspGA (OO000OOOO0OO0OOO0 ,O00O0000000O00O00 ,O0OOO00OO0000OOOO ,O0000OOOOOO00OOOO ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:591
        O00O0000000O00O00 =np .array (O00O0000000O00O00 )#line:596
        OO000OOOO0OO0OOO0 .setting_1 (O00O0000000O00O00 ,O0OOO00OO0000OOOO ,O0000OOOOOO00OOOO ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:599
        OO000OOOO0OO0OOO0 .setting_2 (OO000OOOO0OO0OOO0 .para_num *10 ,2 ,4 )#line:600
        OO000OOOO0OO0OOO0 .setting_3 (int )#line:601
        OO000OOOO0OO0OOO0 .print_info ()#line:602
        OO000OOOO0OO0OOO0 .para_index =np .arange (OO000OOOO0OO0OOO0 .para_num )#line:605
        OO000OOOO0OO0OOO0 .opt2_num =1 #line:606
        for O00O000OO0O000O0O in range (OO000OOOO0OO0OOO0 .pool_num ):#line:609
            OO000OOOO0OO0OOO0 .pool [O00O000OO0O000O0O ]=deepcopy (OO000OOOO0OO0OOO0 .para_index )#line:610
            nr .shuffle (OO000OOOO0OO0OOO0 .pool [O00O000OO0O000O0O ])#line:611
        OO000OOOO0OO0OOO0 .score_pool ()#line:614
        for O00O000OO0O000O0O in range (OO000OOOO0OO0OOO0 .pool_num ):#line:617
            OO000OOOO0OO0OOO0 .pool [O00O000OO0O000O0O ],OO000OOOO0OO0OOO0 .pool_score [O00O000OO0O000O0O ]=OO000OOOO0OO0OOO0 .opt2_tspGA (OO000OOOO0OO0OOO0 .pool [O00O000OO0O000O0O ],OO000OOOO0OO0OOO0 .pool_score [O00O000OO0O000O0O ],step_max =OO000OOOO0OO0OOO0 .opt2_num )#line:618
            if OO000OOOO0OO0OOO0 .show_pool_func !=None :#line:619
                OOO00O0O000OO0O0O ='\rMini 2-opting first gen {}/{}        '.format (O00O000OO0O000O0O +1 ,OO000OOOO0OO0OOO0 .pool_num )#line:620
                print (OOO00O0O000OO0O0O ,end ='')#line:621
        if OO000OOOO0OO0OOO0 .show_pool_func !=None :print ()#line:622
        OO000OOOO0OO0OOO0 .save_best_mean ()#line:625
        OO000OOOO0OO0OOO0 .init_score_range =(np .min (OO000OOOO0OO0OOO0 .pool_score ),np .max (OO000OOOO0OO0OOO0 .pool_score ))#line:627
        OO000OOOO0OO0OOO0 .init_gap_mean =deepcopy (OO000OOOO0OO0OOO0 .gap_mean )#line:628
        if OO000OOOO0OO0OOO0 .show_pool_func ==None :pass #line:631
        elif OO000OOOO0OO0OOO0 .show_pool_func =='bar':OO000OOOO0OO0OOO0 .show_pool_bar (0 )#line:632
        elif OO000OOOO0OO0OOO0 .show_pool_func =='print':OO000OOOO0OO0OOO0 .show_pool_print (0 )#line:633
        elif OO000OOOO0OO0OOO0 .show_pool_func =='plot':OO000OOOO0OO0OOO0 .show_pool_plot (0 )#line:634
        elif callable (OO000OOOO0OO0OOO0 .show_pool_func ):OO000OOOO0OO0OOO0 .show_pool (0 )#line:635
        elif type (show_pool_func )==str :#line:636
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:637
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:638
                OO000OOOO0OO0OOO0 .show_pool_save (0 )#line:639
        OO0OOOO0OOOO0OO00 =0 #line:642
        for O0000O00OOO0OOOO0 in range (1 ,OO000OOOO0OO0OOO0 .max_n +1 ):#line:643
            OOOOOO000O0O00OOO =np .arange (OO000OOOO0OO0OOO0 .pool_num )#line:648
            nr .shuffle (OOOOOO000O0O00OOO )#line:649
            OOOOOO000O0O00OOO =OOOOOO000O0O00OOO .reshape ((OO000OOOO0OO0OOO0 .pool_num //OO000OOOO0OO0OOO0 .parent_num ),OO000OOOO0OO0OOO0 .parent_num )#line:650
            Parallel (n_jobs =OO000OOOO0OO0OOO0 .core_num ,require ='sharedmem')([delayed (OO000OOOO0OO0OOO0 .tspGA_multi )(O0O00OO0OO000O0O0 )for O0O00OO0OO000O0O0 in OOOOOO000O0O00OOO ])#line:653
            OO0OOOO0OOOO0OO00 +=OO000OOOO0OO0OOO0 .end_check ()#line:710
            OO000OOOO0OO0OOO0 .save_best_mean ()#line:713
            if OO000OOOO0OO0OOO0 .show_pool_func ==None :pass #line:716
            elif OO000OOOO0OO0OOO0 .show_pool_func =='bar':OO000OOOO0OO0OOO0 .show_pool_bar (O0000O00OOO0OOOO0 *OO000OOOO0OO0OOO0 .pool_num )#line:717
            elif OO000OOOO0OO0OOO0 .show_pool_func =='print':OO000OOOO0OO0OOO0 .show_pool_print (O0000O00OOO0OOOO0 *OO000OOOO0OO0OOO0 .pool_num )#line:718
            elif OO000OOOO0OO0OOO0 .show_pool_func =='plot':OO000OOOO0OO0OOO0 .show_pool_plot (O0000O00OOO0OOOO0 *OO000OOOO0OO0OOO0 .pool_num )#line:719
            elif callable (OO000OOOO0OO0OOO0 .show_pool_func ):OO000OOOO0OO0OOO0 .show_pool (O0000O00OOO0OOOO0 *OO000OOOO0OO0OOO0 .pool_num )#line:720
            elif type (show_pool_func )==str :#line:721
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:722
                    OO000OOOO0OO0OOO0 .show_pool_save (O0000O00OOO0OOOO0 )#line:723
            if OO0OOOO0OOOO0OO00 >=1 :#line:726
                break #line:727
        OOO0OO000O000OO00 =OO000OOOO0OO0OOO0 .para_range [OO000OOOO0OO0OOO0 .pool_best ]#line:730
        if OO000OOOO0OO0OOO0 .show_pool_func =='bar':print ()#line:733
        elif type (show_pool_func )==str :#line:734
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:735
                print ()#line:736
        if OO000OOOO0OO0OOO0 .show_pool_func !=None :#line:739
            print ('__________________ results _________________')#line:740
            print ('para : {}'.format (OOO0OO000O000OO00 ))#line:741
            print ('score : {}'.format (OO000OOOO0OO0OOO0 .score_best ))#line:742
            print ('____________________ end ___________________')#line:743
        return OOO0OO000O000OO00 ,OO000OOOO0OO0OOO0 .score_best #line:745
    def dcGA_multi (O0OO000O0OOO0OO0O ,OO00O0OO00000OOO0 ):#line:773
        O0O0O00O0OO000OO0 =O0OO000O0OOO0OO0O .pool [OO00O0OO00000OOO0 ]#line:775
        O0000O00000O0O0OO =O0OO000O0OOO0OO0O .pool_score [OO00O0OO00000OOO0 ]#line:776
        O0O0OO0O0OOOOOO0O =np .zeros ((O0OO000O0OOO0OO0O .child_num ,O0OO000O0OOO0OO0O .para_num ),dtype =int )#line:777
        OOOOO0O0O00OO00O0 =np .zeros (O0OO000O0OOO0OO0O .child_num )#line:778
        if O0OO000O0OOO0OO0O .para_num >=3 :#line:781
            OO0OOO00O0OOO000O =nr .choice (range (1 ,O0OO000O0OOO0OO0O .para_num ),2 ,replace =False )#line:785
            if OO0OOO00O0OOO000O [0 ]>OO0OOO00O0OOO000O [1 ]:#line:786
                OO0OOO00O0OOO000O [0 ],OO0OOO00O0OOO000O [1 ]=OO0OOO00O0OOO000O [1 ],OO0OOO00O0OOO000O [0 ]#line:787
            for O00O0O0O0OOOO0000 in range (len (O0OO000O0OOO0OO0O .choice )):#line:789
                O0O0OO0O0OOOOOO0O [O00O0O0O0OOOO0000 ]=np .hstack ((O0O0O00O0OO000OO0 [O0OO000O0OOO0OO0O .choice [O00O0O0O0OOOO0000 ,0 ],:OO0OOO00O0OOO000O [0 ]],O0O0O00O0OO000OO0 [O0OO000O0OOO0OO0O .choice [O00O0O0O0OOOO0000 ,1 ],OO0OOO00O0OOO000O [0 ]:OO0OOO00O0OOO000O [1 ]],O0O0O00O0OO000OO0 [O0OO000O0OOO0OO0O .choice [O00O0O0O0OOOO0000 ,2 ],OO0OOO00O0OOO000O [1 ]:]))#line:792
            for O00O0O0O0OOOO0000 in [2 ,3 ]:#line:797
                O00OOOO00OO00OOOO =nr .randint (0 ,2 ,O0OO000O0OOO0OO0O .para_num )#line:798
                O0O0OO0O0OOOOOO0O [O00O0O0O0OOOO0000 ][O00OOOO00OO00OOOO ==0 ]=O0O0O00O0OO000OO0 [0 ][O00OOOO00OO00OOOO ==0 ]#line:799
                O0O0OO0O0OOOOOO0O [O00O0O0O0OOOO0000 ][O00OOOO00OO00OOOO ==1 ]=O0O0O00O0OO000OO0 [1 ][O00OOOO00OO00OOOO ==1 ]#line:800
            for O00000OO00OO0OO00 in O0O0OO0O0OOOOOO0O :#line:804
                for OO0OOOO0O0O0OOO0O in range (O0OO000O0OOO0OO0O .para_num ):#line:805
                    if nr .rand ()<(1.0 /O0OO000O0OOO0OO0O .para_num ):#line:806
                        O00000OO00OO0OO00 [OO0OOOO0O0O0OOO0O ]=nr .choice (O0OO000O0OOO0OO0O .para_index [OO0OOOO0O0O0OOO0O ])#line:807
        elif O0OO000O0OOO0OO0O .para_num ==2 :#line:811
            O0O0OO0O0OOOOOO0O [:2 ]=np .array ([[O0O0O00O0OO000OO0 [0 ,0 ],O0O0O00O0OO000OO0 [1 ,1 ]],[O0O0O00O0OO000OO0 [0 ,1 ],O0O0O00O0OO000OO0 [1 ,0 ]]])#line:813
            for O00O0O0O0OOOO0000 in range (2 ,O0OO000O0OOO0OO0O .child_num ):#line:815
                for OO0OOOO0O0O0OOO0O in range (2 ):#line:816
                    O0O0OO0O0OOOOOO0O [O00O0O0O0OOOO0000 ,OO0OOOO0O0O0OOO0O ]=nr .choice (O0OO000O0OOO0OO0O .para_index [OO0OOOO0O0O0OOO0O ])#line:817
        elif O0OO000O0OOO0OO0O .para_num ==1 :#line:819
            for O00O0O0O0OOOO0000 in range (O0OO000O0OOO0OO0O .child_num ):#line:821
                O0O0OO0O0OOOOOO0O [O00O0O0O0OOOO0000 ]=nr .choice (O0OO000O0OOO0OO0O .para_index [0 ])#line:822
        for O00O0O0O0OOOO0000 in range (O0OO000O0OOO0OO0O .child_num ):#line:826
            O00OOOO0O0OOO0000 =[]#line:827
            for OO0OOOO0O0O0OOO0O in range (O0OO000O0OOO0OO0O .para_num ):#line:828
                O00OOOO0O0OOO0000 .append (O0OO000O0OOO0OO0O .para_range [OO0OOOO0O0O0OOO0O ][O0O0OO0O0OOOOOO0O [O00O0O0O0OOOO0000 ,OO0OOOO0O0O0OOO0O ]])#line:829
            O00OOOO0O0OOO0000 =np .array (O00OOOO0O0OOO0000 )#line:830
            OOOOO0O0O00OO00O0 [O00O0O0O0OOOO0000 ]=O0OO000O0OOO0OO0O .score_func (O00OOOO0O0OOO0000 )#line:831
        OO0O0O0OOOOOOO000 =np .vstack ((O0O0OO0O0OOOOOO0O ,O0O0O00O0OO000OO0 ))#line:833
        O00OOOO00OO00O000 =np .hstack ((OOOOO0O0O00OO00O0 ,O0000O00000O0O0OO ))#line:834
        O0OO000OO00O00OO0 =np .argpartition (np .abs (O0OO000O0OOO0OO0O .aim -O00OOOO00OO00O000 ),O0OO000O0OOO0OO0O .parent_num )[:O0OO000O0OOO0OO0O .parent_num ]#line:836
        O0OO000O0OOO0OO0O .pool [OO00O0OO00000OOO0 ]=OO0O0O0OOOOOOO000 [O0OO000OO00O00OO0 ]#line:837
        O0OO000O0OOO0OO0O .pool_score [OO00O0OO00000OOO0 ]=O00OOOO00OO00O000 [O0OO000OO00O00OO0 ]#line:838
    def dcGA (OOO00O0OOOO0O0000 ,OOOOOOO0000O0O0OO ,OO00OO0OOOOO0OOOO ,OOO00OOO0OOO0OOO0 ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:841
        if type (OOOOOOO0000O0O0OO )==list :#line:846
            if isinstance (OOOOOOO0000O0O0OO [0 ],list )==False :#line:847
                OOOOOOO0000O0O0OO =[OOOOOOO0000O0O0OO ]#line:848
        if type (OOOOOOO0000O0O0OO )==np .ndarray :#line:849
            if OOOOOOO0000O0O0OO .ndim ==1 :#line:850
                OOOOOOO0000O0O0OO =OOOOOOO0000O0O0OO .reshape (1 ,len (OOOOOOO0000O0O0OO ))#line:851
        OOO00O0OOOO0O0000 .setting_1 (OOOOOOO0000O0O0OO ,OO00OO0OOOOO0OOOO ,OOO00OOO0OOO0OOO0 ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:854
        OOO00O0OOOO0O0000 .setting_2 (OOO00O0OOOO0O0000 .para_num *10 ,2 ,4 )#line:855
        OOO00O0OOOO0O0000 .setting_3 (int )#line:856
        OOO00O0OOOO0O0000 .print_info ()#line:857
        OOO00O0OOOO0O0000 .para_index =[]#line:860
        for OOO000OOO0000O0O0 in range (OOO00O0OOOO0O0000 .para_num ):#line:861
            OOO00O0OOOO0O0000 .para_index .append (np .arange (len (OOO00O0OOOO0O0000 .para_range [OOO000OOO0000O0O0 ])))#line:862
        OOO00O0OOOO0O0000 .choice =np .array ([[0 ,1 ,0 ],[1 ,0 ,1 ]],dtype =int )#line:863
        for OOO000OOO0000O0O0 in range (OOO00O0OOOO0O0000 .pool_num ):#line:866
            for O0O0O0OO0O00O0O0O in range (OOO00O0OOOO0O0000 .para_num ):#line:867
                OOO00O0OOOO0O0000 .pool [OOO000OOO0000O0O0 ,O0O0O0OO0O00O0O0O ]=nr .choice (OOO00O0OOOO0O0000 .para_index [O0O0O0OO0O00O0O0O ])#line:868
        OOO00O0OOOO0O0000 .score_pool_dc ()#line:871
        OOO00O0OOOO0O0000 .save_best_mean ()#line:872
        OOO00O0OOOO0O0000 .init_score_range =(np .min (OOO00O0OOOO0O0000 .pool_score ),np .max (OOO00O0OOOO0O0000 .pool_score ))#line:874
        OOO00O0OOOO0O0000 .init_gap_mean =deepcopy (OOO00O0OOOO0O0000 .gap_mean )#line:875
        if OOO00O0OOOO0O0000 .show_pool_func ==None :pass #line:878
        elif OOO00O0OOOO0O0000 .show_pool_func =='bar':OOO00O0OOOO0O0000 .show_pool_bar (0 )#line:879
        elif OOO00O0OOOO0O0000 .show_pool_func =='print':OOO00O0OOOO0O0000 .show_pool_print (0 )#line:880
        elif OOO00O0OOOO0O0000 .show_pool_func =='plot':OOO00O0OOOO0O0000 .show_pool_plot (0 )#line:881
        elif callable (OOO00O0OOOO0O0000 .show_pool_func ):OOO00O0OOOO0O0000 .show_pool (0 )#line:882
        elif type (show_pool_func )==str :#line:883
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:884
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:885
                OOO00O0OOOO0O0000 .show_pool_save (0 )#line:886
        OO000OOO0O0OO000O =0 #line:889
        for O000O0O0O0000OOO0 in range (1 ,OOO00O0OOOO0O0000 .max_n +1 ):#line:890
            OOOO0O0O0000O000O =np .arange (OOO00O0OOOO0O0000 .pool_num )#line:893
            nr .shuffle (OOOO0O0O0000O000O )#line:894
            OOOO0O0O0000O000O =OOOO0O0O0000O000O .reshape ((OOO00O0OOOO0O0000 .pool_num //OOO00O0OOOO0O0000 .parent_num ),OOO00O0OOOO0O0000 .parent_num )#line:895
            Parallel (n_jobs =OOO00O0OOOO0O0000 .core_num ,require ='sharedmem')([delayed (OOO00O0OOOO0O0000 .dcGA_multi )(OOOO00O0O0O0OO00O )for OOOO00O0O0O0OO00O in OOOO0O0O0000O000O ])#line:898
            OO000OOO0O0OO000O +=OOO00O0OOOO0O0000 .end_check ()#line:954
            OOO00O0OOOO0O0000 .save_best_mean ()#line:957
            if OOO00O0OOOO0O0000 .show_pool_func ==None :pass #line:960
            elif OOO00O0OOOO0O0000 .show_pool_func =='bar':OOO00O0OOOO0O0000 .show_pool_bar (O000O0O0O0000OOO0 *OOO00O0OOOO0O0000 .pool_num )#line:961
            elif OOO00O0OOOO0O0000 .show_pool_func =='print':OOO00O0OOOO0O0000 .show_pool_print (O000O0O0O0000OOO0 *OOO00O0OOOO0O0000 .pool_num )#line:962
            elif OOO00O0OOOO0O0000 .show_pool_func =='plot':OOO00O0OOOO0O0000 .show_pool_plot (O000O0O0O0000OOO0 *OOO00O0OOOO0O0000 .pool_num )#line:963
            elif callable (OOO00O0OOOO0O0000 .show_pool_func ):OOO00O0OOOO0O0000 .show_pool (O000O0O0O0000OOO0 *OOO00O0OOOO0O0000 .pool_num )#line:964
            elif type (show_pool_func )==str :#line:965
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:966
                    OOO00O0OOOO0O0000 .show_pool_save (O000O0O0O0000OOO0 )#line:967
            if OO000OOO0O0OO000O >=1 :#line:970
                break #line:971
        O0O000OO0OOO0O00O =[]#line:974
        for O0O0O0OO0O00O0O0O in range (OOO00O0OOOO0O0000 .para_num ):#line:975
            O0O000OO0OOO0O00O .append (OOO00O0OOOO0O0000 .para_range [O0O0O0OO0O00O0O0O ][OOO00O0OOOO0O0000 .pool [OOO00O0OOOO0O0000 .best_index ,O0O0O0OO0O00O0O0O ]])#line:976
        O0O000OO0OOO0O00O =np .array (O0O000OO0OOO0O00O )#line:977
        if OOO00O0OOOO0O0000 .show_pool_func =='bar':print ()#line:980
        elif type (show_pool_func )==str :#line:981
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:982
                print ()#line:983
        if OOO00O0OOOO0O0000 .show_pool_func !=None :#line:986
            print ('__________________ results _________________')#line:987
            print ('para : {}'.format (O0O000OO0OOO0O00O ))#line:988
            print ('score : {}'.format (OOO00O0OOOO0O0000 .score_best ))#line:989
            print ('____________________ end ___________________')#line:990
        return O0O000OO0OOO0O00O ,OOO00O0OOOO0O0000 .score_best #line:992
    def setGA_multi (O0OO000O0000OO000 ,OO0OO00OO000O00OO ):#line:1022
        OOO00O0OOO00O0O00 =O0OO000O0000OO000 .pool [OO0OO00OO000O00OO ]#line:1024
        O000O00O0O0O0OOO0 =O0OO000O0000OO000 .pool_score [OO0OO00OO000O00OO ]#line:1025
        O00O0OO0O0O000OOO =np .zeros ((O0OO000O0000OO000 .child_num ,O0OO000O0000OO000 .para_num ),dtype =int )#line:1026
        OOOO0OO0OO0O00000 =np .zeros (O0OO000O0000OO000 .child_num )#line:1027
        O00O00OOOO0OO000O =set (OOO00O0OOO00O0O00 [0 ])&set (OOO00O0OOO00O0O00 [1 ])#line:1032
        O0O0OO0OOOOO0O000 =set (O0OO000O0000OO000 .para_index )-O00O00OOOO0OO000O #line:1034
        for OO0O0OO00O00OOOO0 in range (len (O00O0OO0O0O000OOO )):#line:1036
            O0OOO0O0000O00O00 =nr .choice (np .array (list (O0O0OO0OOOOO0O000 )),O0OO000O0000OO000 .set_num -len (O00O00OOOO0OO000O ),replace =False )#line:1037
            O00O0OO0O0O000OOO [OO0O0OO00O00OOOO0 ]=np .hstack ((np .array (list (O00O00OOOO0OO000O )),O0OOO0O0000O00O00 ))#line:1039
        for O00O0000OOOO00000 in O00O0OO0O0O000OOO [2 :]:#line:1046
            for OO0O0OO0O0O00O0O0 in range (O0OO000O0000OO000 .set_num ):#line:1047
                if nr .rand ()<(1.0 /O0OO000O0000OO000 .set_num ):#line:1048
                    OO0O0O0OO0000OOO0 =nr .choice (O0OO000O0000OO000 .para_index )#line:1049
                    if OO0O0O0OO0000OOO0 not in O00O0000OOOO00000 :#line:1050
                        O00O0000OOOO00000 [OO0O0OO0O0O00O0O0 ]=OO0O0O0OO0000OOO0 #line:1051
        for OO0O0OO00O00OOOO0 in range (O0OO000O0000OO000 .child_num ):#line:1056
            O00OOO0O0OO000000 =O0OO000O0000OO000 .para_range [O00O0OO0O0O000OOO [OO0O0OO00O00OOOO0 ]]#line:1057
            OOOO0OO0OO0O00000 [OO0O0OO00O00OOOO0 ]=O0OO000O0000OO000 .score_func (O00OOO0O0OO000000 )#line:1058
        O0OOO000OO00O0000 =np .vstack ((O00O0OO0O0O000OOO ,OOO00O0OOO00O0O00 ))#line:1060
        OOO00OOO0O00O000O =np .hstack ((OOOO0OO0OO0O00000 ,O000O00O0O0O0OOO0 ))#line:1061
        O00OO0OOO00OO0O0O =np .argpartition (np .abs (O0OO000O0000OO000 .aim -OOO00OOO0O00O000O ),O0OO000O0000OO000 .parent_num )[:O0OO000O0000OO000 .parent_num ]#line:1063
        O0OO000O0000OO000 .pool [OO0OO00OO000O00OO ]=O0OOO000OO00O0000 [O00OO0OOO00OO0O0O ]#line:1064
        O0OO000O0000OO000 .pool_score [OO0OO00OO000O00OO ]=OOO00OOO0O00O000O [O00OO0OOO00OO0O0O ]#line:1065
    def setGA (OOOOOO000000OOO00 ,OOOO0OOOOO0O0OO00 ,O00000OOOO00O0O0O ,O000OOOOO0000O00O ,O00OO00O00O00OOOO ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:1067
        OOOO0OOOOO0O0OO00 =np .array (OOOO0OOOOO0O0OO00 )#line:1072
        OOOOOO000000OOO00 .setting_1 (OOOO0OOOOO0O0OO00 ,O000OOOOO0000O00O ,O00OO00O00O00OOOO ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:1075
        OOOOOO000000OOO00 .set_num =O00000OOOO00O0O0O #line:1076
        OOOOOO000000OOO00 .para_num =OOOOOO000000OOO00 .set_num #line:1077
        OOOOOO000000OOO00 .setting_2 (OOOOOO000000OOO00 .para_num *10 ,2 ,4 )#line:1078
        OOOOOO000000OOO00 .setting_3 (int )#line:1079
        OOOOOO000000OOO00 .print_info ()#line:1080
        OOOOOO000000OOO00 .para_index =np .arange (len (OOOOOO000000OOO00 .para_range ))#line:1083
        for OOOO00OO00OO00O00 in range (OOOOOO000000OOO00 .pool_num ):#line:1086
            OOOOOO000000OOO00 .pool [OOOO00OO00OO00O00 ]=nr .choice (OOOOOO000000OOO00 .para_index ,OOOOOO000000OOO00 .set_num ,replace =False )#line:1087
        OOOOOO000000OOO00 .score_pool ()#line:1091
        OOOOOO000000OOO00 .save_best_mean ()#line:1092
        OOOOOO000000OOO00 .init_score_range =(np .min (OOOOOO000000OOO00 .pool_score ),np .max (OOOOOO000000OOO00 .pool_score ))#line:1094
        OOOOOO000000OOO00 .init_gap_mean =deepcopy (OOOOOO000000OOO00 .gap_mean )#line:1095
        if OOOOOO000000OOO00 .show_pool_func ==None :pass #line:1098
        elif OOOOOO000000OOO00 .show_pool_func =='bar':OOOOOO000000OOO00 .show_pool_bar (0 )#line:1099
        elif OOOOOO000000OOO00 .show_pool_func =='print':OOOOOO000000OOO00 .show_pool_print (0 )#line:1100
        elif OOOOOO000000OOO00 .show_pool_func =='plot':OOOOOO000000OOO00 .show_pool_plot (0 )#line:1101
        elif callable (OOOOOO000000OOO00 .show_pool_func ):OOOOOO000000OOO00 .show_pool (0 )#line:1102
        elif type (show_pool_func )==str :#line:1103
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1104
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:1105
                OOOOOO000000OOO00 .show_pool_save (0 )#line:1106
        OO0O00O0O0O00O00O =0 #line:1109
        for OO0000O000000000O in range (1 ,OOOOOO000000OOO00 .max_n +1 ):#line:1110
            O00O0OOO00O0OOO0O =np .arange (OOOOOO000000OOO00 .pool_num )#line:1113
            nr .shuffle (O00O0OOO00O0OOO0O )#line:1114
            O00O0OOO00O0OOO0O =O00O0OOO00O0OOO0O .reshape ((OOOOOO000000OOO00 .pool_num //OOOOOO000000OOO00 .parent_num ),OOOOOO000000OOO00 .parent_num )#line:1115
            Parallel (n_jobs =OOOOOO000000OOO00 .core_num ,require ='sharedmem')([delayed (OOOOOO000000OOO00 .setGA_multi )(O000O0OO0O00OOO0O )for O000O0OO0O00OOO0O in O00O0OOO00O0OOO0O ])#line:1118
            OO0O00O0O0O00O00O +=OOOOOO000000OOO00 .end_check ()#line:1154
            OOOOOO000000OOO00 .save_best_mean ()#line:1157
            if OOOOOO000000OOO00 .show_pool_func ==None :pass #line:1160
            elif OOOOOO000000OOO00 .show_pool_func =='bar':OOOOOO000000OOO00 .show_pool_bar (OO0000O000000000O *OOOOOO000000OOO00 .pool_num )#line:1161
            elif OOOOOO000000OOO00 .show_pool_func =='print':OOOOOO000000OOO00 .show_pool_print (OO0000O000000000O *OOOOOO000000OOO00 .pool_num )#line:1162
            elif OOOOOO000000OOO00 .show_pool_func =='plot':OOOOOO000000OOO00 .show_pool_plot (OO0000O000000000O *OOOOOO000000OOO00 .pool_num )#line:1163
            elif callable (OOOOOO000000OOO00 .show_pool_func ):OOOOOO000000OOO00 .show_pool (OO0000O000000000O *OOOOOO000000OOO00 .pool_num )#line:1164
            elif type (show_pool_func )==str :#line:1165
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1166
                    OOOOOO000000OOO00 .show_pool_save (OO0000O000000000O )#line:1167
            if OO0O00O0O0O00O00O >=1 :#line:1170
                break #line:1171
        O00O0OO0OO0O0OO00 =OOOOOO000000OOO00 .para_range [OOOOOO000000OOO00 .pool_best ]#line:1174
        if OOOOOO000000OOO00 .show_pool_func =='bar':print ()#line:1177
        elif type (show_pool_func )==str :#line:1178
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1179
                print ()#line:1180
        if OOOOOO000000OOO00 .show_pool_func !=None :#line:1183
            print ('__________________ results _________________')#line:1184
            print ('para : {}'.format (O00O0OO0OO0O0OO00 ))#line:1185
            print ('score : {}'.format (OOOOOO000000OOO00 .score_best ))#line:1186
            print ('____________________ end ___________________')#line:1187
        return O00O0OO0OO0O0OO00 ,OOOOOO000000OOO00 .score_best #line:1189
    def rcGA_multi (O0OOOO0OO0O00OOOO ,O0OO00O0O0O0OO000 ):#line:1217
        O0OOOO0000OOO00OO =O0OOOO0OO0O00OOOO .pool [O0OO00O0O0O0OO000 ]#line:1219
        O0OO0O00000OOO00O =O0OOOO0OO0O00OOOO .pool_score [O0OO00O0O0O0OO000 ]#line:1220
        O0OO0OOOO0O00000O =np .ones ((O0OOOO0OO0O00OOOO .child_num ,O0OOOO0OO0O00OOOO .para_num ),dtype =float )*2.0 #line:1221
        OO000OOOO00O00OOO =np .zeros (O0OOOO0OO0O00OOOO .child_num )#line:1222
        OOO0O0O0OO000OOOO =np .mean (O0OOOO0000OOO00OO ,axis =0 )#line:1227
        for O00OO0O00OO00OOOO in range (O0OOOO0OO0O00OOOO .child_num ):#line:1230
            for OO0OO0OO0000OOOOO in range (O0OOOO0OO0O00OOOO .para_num ):#line:1231
                O0OO0OOOO0O00000O [O00OO0O00OO00OOOO ,OO0OO0OO0000OOOOO ]=OOO0O0O0OO000OOOO [OO0OO0OO0000OOOOO ]#line:1233
                for OOO000OOOOOOO00OO in range (O0OOOO0OO0O00OOOO .parent_num ):#line:1235
                    O0OO0OOOO0O00000O [O00OO0O00OO00OOOO ,OO0OO0OO0000OOOOO ]+=nr .normal (0 ,O0OOOO0OO0O00OOOO .sd )*(O0OOOO0000OOO00OO [OOO000OOOOOOO00OO ][OO0OO0OO0000OOOOO ]-OOO0O0O0OO000OOOO [OO0OO0OO0000OOOOO ])#line:1236
        O0OO0OOOO0O00000O =np .clip (O0OO0OOOO0O00000O ,0.0 ,1.0 )#line:1238
        for O00OO0O00OO00OOOO in range (O0OOOO0OO0O00OOOO .child_num ):#line:1242
            OO00OOO00O0OOOOO0 =O0OO0OOOO0O00000O [O00OO0O00OO00OOOO ]*(O0OOOO0OO0O00OOOO .para_range [:,1 ]-O0OOOO0OO0O00OOOO .para_range [:,0 ])+O0OOOO0OO0O00OOOO .para_range [:,0 ]#line:1243
            OO000OOOO00O00OOO [O00OO0O00OO00OOOO ]=O0OOOO0OO0O00OOOO .score_func (OO00OOO00O0OOOOO0 )#line:1244
        OOO00000O0O0O0O0O =np .vstack ((O0OO0OOOO0O00000O ,O0OOOO0000OOO00OO ))#line:1246
        O0OO0OO00OOOO000O =np .hstack ((OO000OOOO00O00OOO ,O0OO0O00000OOO00O ))#line:1247
        O000O00000OOO00O0 =np .argpartition (np .abs (O0OOOO0OO0O00OOOO .aim -O0OO0OO00OOOO000O ),O0OOOO0OO0O00OOOO .parent_num )[:O0OOOO0OO0O00OOOO .parent_num ]#line:1249
        O0OOOO0OO0O00OOOO .pool [O0OO00O0O0O0OO000 ]=OOO00000O0O0O0O0O [O000O00000OOO00O0 ]#line:1250
        O0OOOO0OO0O00OOOO .pool_score [O0OO00O0O0O0OO000 ]=O0OO0OO00OOOO000O [O000O00000OOO00O0 ]#line:1251
    def rcGA (OO0O0OO00000O0O00 ,OO00000OO0OOOO0O0 ,OOOOO0O0OO0000O0O ,O00OOO00000O00OO0 ,show_pool_func ='bar',seed =None ,pool_num =None ,max_gen =None ,core_num =1 ):#line:1254
        OO00000OO0OOOO0O0 =np .array (OO00000OO0OOOO0O0 )#line:1259
        if OO00000OO0OOOO0O0 .ndim ==1 :#line:1260
            OO00000OO0OOOO0O0 =OO00000OO0OOOO0O0 .reshape (1 ,2 )#line:1261
        OO0O0OO00000O0O00 .setting_1 (OO00000OO0OOOO0O0 ,OOOOO0O0OO0000O0O ,O00OOO00000O00OO0 ,show_pool_func ,seed ,pool_num ,max_gen ,core_num )#line:1264
        OO0O0OO00000O0O00 .setting_2 (OO0O0OO00000O0O00 .para_num *10 ,2 ,4 )#line:1265
        OO0O0OO00000O0O00 .setting_3 (float )#line:1266
        OO0O0OO00000O0O00 .print_info ()#line:1267
        OO0O0OO00000O0O00 .sd =1.2 /math .sqrt (OO0O0OO00000O0O00 .parent_num )#line:1270
        if OO0O0OO00000O0O00 .para_num ==1 :#line:1275
            O0OOOO0OO00O0OOO0 =np .tile (np .array ([0.5 ]),(OO0O0OO00000O0O00 .pool_num //OO0O0OO00000O0O00 .para_num )+1 )#line:1276
        else :#line:1277
            O0OOOO0OO00O0OOO0 =np .tile (np .arange (0.0 ,1.000001 ,1.0 /(OO0O0OO00000O0O00 .para_num -1 )),(OO0O0OO00000O0O00 .pool_num //OO0O0OO00000O0O00 .para_num )+1 )#line:1278
        for OO000OO0O000O000O in range (OO0O0OO00000O0O00 .para_num ):#line:1281
            OO0O0OO00000O0O00 .pool [:,OO000OO0O000O000O ]=nr .permutation (O0OOOO0OO00O0OOO0 [:OO0O0OO00000O0O00 .pool_num ])#line:1282
        if OO0O0OO00000O0O00 .para_num ==1 :#line:1285
            OO0O0OO00000O0O00 .pool +=nr .rand (OO0O0OO00000O0O00 .pool_num ,OO0O0OO00000O0O00 .para_num )*1.0 -0.5 #line:1286
        else :#line:1287
            OO0O0OO00000O0O00 .pool +=nr .rand (OO0O0OO00000O0O00 .pool_num ,OO0O0OO00000O0O00 .para_num )*(2.0 /(3 *OO0O0OO00000O0O00 .para_num -3 ))-(1.0 /(3 *OO0O0OO00000O0O00 .para_num -3 ))#line:1288
        OO0O0OO00000O0O00 .pool =np .clip (OO0O0OO00000O0O00 .pool ,0.0 ,1.0 )#line:1291
        def O00O000OO00OO00OO (OO00OO0OOOO0O0OOO ):#line:1294
            O0OOOO000OOOO00O0 =np .expand_dims (OO0O0OO00000O0O00 .pool ,axis =1 )-np .expand_dims (OO0O0OO00000O0O00 .pool ,axis =0 )#line:1295
            O0OOOO000OOOO00O0 =np .sqrt (np .sum (O0OOOO000OOOO00O0 **2 ,axis =-1 ))#line:1296
            O0OOOO000OOOO00O0 =np .sum (O0OOOO000OOOO00O0 ,axis =-1 )/OO0O0OO00000O0O00 .pool_num #line:1297
            return O0OOOO000OOOO00O0 #line:1298
        if OO0O0OO00000O0O00 .pool_num <=5 *10 :#line:1301
            O0OOO0OOOO00O0O00 =200 #line:1302
        elif OO0O0OO00000O0O00 .pool_num <=10 *10 :#line:1303
            O0OOO0OOOO00O0O00 =150 #line:1304
        elif OO0O0OO00000O0O00 .pool_num <=15 *10 :#line:1305
            O0OOO0OOOO00O0O00 =70 #line:1306
        elif OO0O0OO00000O0O00 .pool_num <=20 *10 :#line:1307
            O0OOO0OOOO00O0O00 =30 #line:1308
        elif OO0O0OO00000O0O00 .pool_num <=30 *10 :#line:1309
            O0OOO0OOOO00O0O00 =12 #line:1310
        else :#line:1311
            O0OOO0OOOO00O0O00 =0 #line:1312
        O000O00000O0O0OO0 =False #line:1313
        for O00000O00OO0000O0 in range (O0OOO0OOOO00O0O00 ):#line:1314
            O0OO0OOO000O00OO0 =O00O000OO00OO00OO (OO0O0OO00000O0O00 .pool )#line:1315
            OOO000000OOO000OO =np .argmin (O0OO0OOO000O00OO0 )#line:1316
            OO0O0OO00000O0O00 .pool [OOO000000OOO000OO ]=nr .rand (OO0O0OO00000O0O00 .para_num )#line:1318
            O0OO0000OOO00OOOO =O00O000OO00OO00OO (OO0O0OO00000O0O00 .pool )#line:1319
            O00000O0OOO0000O0 =0 #line:1321
            while np .sum (O0OO0000OOO00OOOO )<np .sum (O0OO0OOO000O00OO0 ):#line:1322
                OO0O0OO00000O0O00 .pool [OOO000000OOO000OO ]=nr .rand (OO0O0OO00000O0O00 .para_num )#line:1324
                O0OO0000OOO00OOOO =O00O000OO00OO00OO (OO0O0OO00000O0O00 .pool )#line:1325
                O00000O0OOO0000O0 +=1 #line:1326
                if O00000O0OOO0000O0 ==O0OOO0OOOO00O0O00 :#line:1327
                    O000O00000O0O0OO0 =True #line:1329
                    break #line:1330
            if O000O00000O0O0OO0 ==True :#line:1331
                break #line:1332
        OO0O0OO00000O0O00 .score_pool_rc ()#line:1337
        OO0O0OO00000O0O00 .save_best_mean ()#line:1338
        OO0O0OO00000O0O00 .init_score_range =(np .min (OO0O0OO00000O0O00 .pool_score ),np .max (OO0O0OO00000O0O00 .pool_score ))#line:1340
        OO0O0OO00000O0O00 .init_gap_mean =deepcopy (OO0O0OO00000O0O00 .gap_mean )#line:1341
        if OO0O0OO00000O0O00 .show_pool_func ==None :pass #line:1344
        elif OO0O0OO00000O0O00 .show_pool_func =='bar':OO0O0OO00000O0O00 .show_pool_bar (0 )#line:1345
        elif OO0O0OO00000O0O00 .show_pool_func =='print':OO0O0OO00000O0O00 .show_pool_print (0 )#line:1346
        elif OO0O0OO00000O0O00 .show_pool_func =='plot':OO0O0OO00000O0O00 .show_pool_plot (0 )#line:1347
        elif callable (OO0O0OO00000O0O00 .show_pool_func ):OO0O0OO00000O0O00 .show_pool_rc (0 )#line:1348
        elif type (show_pool_func )==str :#line:1349
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1350
                if not os .path .exists (show_pool_func ):os .mkdir (show_pool_func )#line:1351
                OO0O0OO00000O0O00 .show_pool_save (0 )#line:1352
        O00000O0OOO0000O0 =0 #line:1355
        for OO000OOO0O0OO0O0O in range (1 ,OO0O0OO00000O0O00 .max_n +1 ):#line:1356
            OO0OO0O0000OOO0OO =np .arange (OO0O0OO00000O0O00 .pool_num )#line:1359
            nr .shuffle (OO0OO0O0000OOO0OO )#line:1360
            OO0OO0O0000OOO0OO =OO0OO0O0000OOO0OO .reshape ((OO0O0OO00000O0O00 .pool_num //OO0O0OO00000O0O00 .parent_num ),OO0O0OO00000O0O00 .parent_num )#line:1361
            Parallel (n_jobs =OO0O0OO00000O0O00 .core_num ,require ='sharedmem')([delayed (OO0O0OO00000O0O00 .rcGA_multi )(O0O00000O0OO0OOOO )for O0O00000O0OO0OOOO in OO0OO0O0000OOO0OO ])#line:1364
            OO0O0OO00000O0O00 .sd =max (OO0O0OO00000O0O00 .sd *0.995 ,0.9 /math .sqrt (OO0O0OO00000O0O00 .parent_num ))#line:1394
            if np .max (np .std (OO0O0OO00000O0O00 .pool ,axis =0 ))<0.03 :#line:1397
                O00000O0OOO0000O0 +=1 #line:1398
            OO0O0OO00000O0O00 .save_best_mean ()#line:1401
            if OO0O0OO00000O0O00 .show_pool_func ==None :pass #line:1404
            elif OO0O0OO00000O0O00 .show_pool_func =='bar':OO0O0OO00000O0O00 .show_pool_bar (OO000OOO0O0OO0O0O *OO0O0OO00000O0O00 .pool_num )#line:1405
            elif OO0O0OO00000O0O00 .show_pool_func =='print':OO0O0OO00000O0O00 .show_pool_print (OO000OOO0O0OO0O0O *OO0O0OO00000O0O00 .pool_num )#line:1406
            elif OO0O0OO00000O0O00 .show_pool_func =='plot':OO0O0OO00000O0O00 .show_pool_plot (OO000OOO0O0OO0O0O *OO0O0OO00000O0O00 .pool_num )#line:1407
            elif callable (OO0O0OO00000O0O00 .show_pool_func ):OO0O0OO00000O0O00 .show_pool_rc (OO000OOO0O0OO0O0O *OO0O0OO00000O0O00 .pool_num )#line:1408
            elif type (show_pool_func )==str :#line:1409
                if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1410
                    OO0O0OO00000O0O00 .show_pool_save (OO000OOO0O0OO0O0O )#line:1411
            if O00000O0OOO0000O0 >=1 :#line:1414
                break #line:1415
        O00OO000O0O000O0O =OO0O0OO00000O0O00 .pool_best *(OO0O0OO00000O0O00 .para_range [:,1 ]-OO0O0OO00000O0O00 .para_range [:,0 ])+OO0O0OO00000O0O00 .para_range [:,0 ]#line:1418
        if OO0O0OO00000O0O00 .show_pool_func =='bar':print ()#line:1421
        elif type (show_pool_func )==str :#line:1422
            if len (show_pool_func )>0 and show_pool_func [-1 ]=='/':#line:1423
                print ()#line:1424
        if OO0O0OO00000O0O00 .show_pool_func !=None :#line:1427
            print ('__________________ results _________________')#line:1428
            print ('para : {}'.format (O00OO000O0O000O0O ))#line:1429
            print ('score : {}'.format (OO0O0OO00000O0O00 .score_best ))#line:1430
            print ('____________________ end ___________________')#line:1431
        return O00OO000O0O000O0O ,OO0O0OO00000O0O00 .score_best #line:1433
if __name__ =='__main__':#line:1443
    pass #line:1444
