# Smith-Waterman algorithm
# https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm

import numpy as np
import pandas as pd
import os
from tqdm import tqdm

# read test tunes
tunesPath = 'chord_sequences/chords_relative_full.txt'
with open(tunesPath, 'r') as file:
    tunes = file.readlines()
# split tunes into lists of chords
tunes = [line.split(' ') for line in [line.replace(' \n', '') for line in tunes]]

# read test tune names
tuneNamesPath = 'chord_sequences/tune_names.txt'
with open(tuneNamesPath, 'r') as file:
    names = file.readlines()
# split tunes into lists of chords
names = [line.replace('.xml', '') for line in [line.replace('\n', '') for line in names]]


# tunes to be compared
ind1 = 0
ind2 = 2
t1 = tunes[ind1]
t1_name = names[ind1]
t2 = tunes[ind2]
t2_name = names[ind2]

def SmithWaterman(t1, t1_name,
                  t2, t2_name,
                  sm_m = 3,
                  sm_p = -3,
                  gap_p = -2
                  ):
    '''
    Alignes the chords of two tunes using the Smith-Waterman algoritm
    https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm
    
    Parameters
    ----------
    t1 : list
        List of chords for tune 1.
    t1_name : str
        Name of tune 1.
    t2 : list
        List of chords for tune 1.
    t2_name : str
        Name of tune 2.
    sm_m : int, optional
        Score for matching chords. The default is 3.
    sm_p : int, optional
        Penalty for substitution. The default is -3.
    gap_p : int, optional
        Penalty for gap. The default is -2.

    Returns
    -------
    pandas DataFrame

    '''
    # initialize matrix
    mat = np.zeros((len(t2)+1, len(t1)+1), dtype=int)
    
    # compute matrix entries
    # start at 1 because of 0 padding in first row and column
    for i in range(1, len(t2)+1): # go through rows
        for j in range(1, len(t1)+1): # go through columns
            # matching chords?
            if t1[j-1] == t2[i-1]:
                sub = sm_m
            else:
                sub = sm_p
            mat[i,j] = max([
                   mat[i-1,j-1] + sub, # diagonal
                   mat[i-1,j] + gap_p, # top
                   mat[i,j-1] + gap_p, # left
                   0
                ])
    
    # check if any matches at all
    if mat.max() == 0:
        rel_score = 0
        ali_disp = ''
        full_disp = ''
        ali_len = 0
        ali_nrmatch = 0
        ali_nrgaps = 0
        ali_nrsub = 0
        ali_lm = 0
        ali_lg = 0
    else:
        # find indices of maximum values
        max_ind = np.where(mat == mat.max())
        
        scores = []
        traces = []
        
        # generate alignment traces from maximum positions
        for i in range(len(max_ind[0])):
            curr = mat[max_ind[0][i], max_ind[1][i]]
            score = curr
            ind_i = [max_ind[0][i]]
            ind_j = [max_ind[1][i]]
            while curr != 0:
                tmp = np.array([[0, mat[ind_i[0], ind_j[0]-1]],
                                [mat[ind_i[0]-1, ind_j[0]], mat[ind_i[0]-1, ind_j[0]-1]]],
                               dtype=int)
                curr = tmp.max()
                if curr != 0:
                    score += curr
                    tmp_max_ind = np.where(tmp == tmp.max())
                    ind_i.insert(0, ind_i[0] - tmp_max_ind[0][0])
                    ind_j.insert(0, ind_j[0] - tmp_max_ind[1][0])
            scores.append(score)
            traces.append([ind_i, ind_j])
            
        # take longest alignment
        trace = traces[np.argmax(scores)]
        
        # calculate some alignment scores:
        # score normalized to maximum possible score
        max_score = 0
        for i in range(1, min(len(t1), len(t2))+1):
            max_score += i*3
        rel_score = max(scores) / max_score
        # length of alignment region
        ali_len = len(trace[0])
        # longest match, gap, number of gaps, number of substitutions, number of matches
        ali_nrmatch = 1 # always starts with match
        ali_nrgaps = 0
        ali_nrsub = 0
        curr_m = 1 # counter for current match length
        curr_g = 0 # counter for current gap length
        ali_lm = 1 # lognest stretch of matches
        ali_lg = 0 # longest gap
        curr = 'm' # currently in match region
        for i in range(1, len(trace[0])):
            if trace[1][i] == trace[1][i-1] or trace[0][i] == trace[0][i-1]:
                curr_m = 0 # set current match length zero
                if curr == 'g': # if currently in gap
                    curr_g += 1
                    ali_lg = max(ali_lg, curr_g)
                else: # start gap
                    curr = 'g'
                    curr_m = 0
                    curr_g = 1
                    ali_nrgaps += 1
            elif t1[trace[1][i]-1] == t2[trace[0][i]-1]:
                ali_nrmatch += 1
                if curr == 'm': # if currently in match region
                    curr_m += 1
                    ali_lm = max(ali_lm, curr_m)
                else: # start match
                    curr = 'm'
                    curr_g = 0
                    curr_m = 1
            else:
                curr = 's'
                ali_nrsub += 1
        
        # create strings to print alginment
        t1_ali = t1[trace[1][0]-1]
        t2_ali = t2[trace[0][0]-1]
        
        g_ali = '|' + ' '*(len(t1[trace[1][0]-1])-1)
        for i in range(1, len(trace[1])):
            if trace[1][i] == trace[1][i-1]:
                t1_ali = t1_ali + ' ' + '-'*len(t2[trace[0][i]-1])
                g_ali = g_ali + ' '*(len(t2[trace[0][i]-1])+1)
                t2_ali = t2_ali + ' ' + t2[trace[0][i]-1]
            elif trace[0][i] == trace[0][i-1]:
                t2_ali = t2_ali + ' ' + '-'*len(t1[trace[1][i]-1])
                g_ali = g_ali + ' '*(len(t1[trace[1][i]-1])+1)
                t1_ali = t1_ali + ' ' + t1[trace[1][i]-1]
            else:
                d1 = len(t2[trace[0][i]-1]) - len(t1[trace[1][i]-1])
                t1_ali = t1_ali + ' ' + t1[trace[1][i]-1] + ' '*d1
                d2 = len(t1[trace[1][i]-1]) - len(t2[trace[0][i]-1])
                t2_ali = t2_ali + ' ' + t2[trace[0][i]-1] + ' '*d2
                if t1[trace[1][i]-1] == t2[trace[0][i]-1]:
                    g_ali = g_ali + ' |' + ' '*(len(t1[trace[1][i]-1])-1)
                else:
                    g_ali = g_ali + ' X' + ' '*(len(t1[trace[1][i]-1])-1)
        
        ali_disp = t1_ali + '\n' + g_ali + '\n' + t2_ali
        
        # add sequences in front of alignment
        if trace[1][0]-1 == 0:
            t1_pre = ''
        else:
            t1_pre = t1[0]
        for t in t1[1:trace[1][0]-1]:
            t1_pre = t1_pre + ' ' + t
        t1_pre = t1_pre + ' '
        
        if trace[0][0]-1 == 0:
            t2_pre = ''
        else:
            t2_pre = t2[0]
        for t in t2[1:trace[0][0]-1]:
            t2_pre = t2_pre + ' ' + t
        t2_pre = t2_pre + ' '
        
        if len(t1_pre) > len(t2_pre):
            t2_pre = ' '*(len(t1_pre)-len(t2_pre)) + t2_pre
            g_ali = ' '*len(t1_pre) + g_ali
        elif len(t1_pre) < len(t2_pre):
            t1_pre = ' '*(len(t2_pre)-len(t1_pre)) + t1_pre
            g_ali = ' '*len(t2_pre) + g_ali
            
        # add sequences after alignment
        if trace[1][-1]-1 == len(t1)-1:
            t1_post = ''
        else:
            t1_post = ' ' + t1[trace[1][-1]]
        for t in t1[trace[1][-1]+1:len(t1)]:
            t1_post = t1_post + ' ' + t
        
        if trace[0][-1]-1 == len(t2)-1:
            t2_post = ''
        else:
            t2_post =  ' ' + t2[trace[0][-1]]
        for t in t2[trace[0][-1]+1:len(t2)]:
            t2_post = t2_post + ' ' + t
            
        full_disp = (t1_pre + t1_ali + t1_post) + '\n' + g_ali + '\n' + (t2_pre + t2_ali + t2_post)
    
    return pd.DataFrame({
                'tune1_name' : t1_name,
                'tune1' : [t1],
                'tune2_name' : t2_name,
                'tune2' : [t2],
                'alignment_score' : rel_score,
                'alignment_length' : ali_len,
                'nr_matches' : ali_nrmatch,
                'nr_gaps' : ali_nrgaps,
                'nr_substitutions' : ali_nrsub,
                'longest_match_region' : ali_lm,
                'longest_gap_region' : ali_lg,
                'alignment_str' : ali_disp,
                'full_str' : full_disp
        })

res = []
for i in range(len(tunes)-1):
    for j in range(i+1, len(tunes)):
        print(names[i] + ' vs. ' + names[j])
        res.append(SmithWaterman(tunes[i], names[i], tunes[j], names[j],
                                 sm_m = 3, sm_p = -3, gap_p = -2))
res = pd.concat(res)

directory = './calculations'
if not os.path.exists(directory):
    os.makedirs(directory)
res.to_csv(directory+'/smith_waterman.zip')
