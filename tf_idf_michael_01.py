#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 10:25:42 2021

@author: michael
"""


import pandas as pd
import numpy as np
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

###
#
# size of the ngrams
N_ngram = 3

# filename definitions
directory = './chord_sequences'
tune_names_path = os.path.join(directory, 'tune_names.txt')
path_to_file = os.path.join(directory, 'chords_relative_full.txt')

###
# read data

with open(tune_names_path, encoding="utf8", errors="replace") as f:
    tune_names = f.read().splitlines()
for line in tune_names[:20]:
    print(line)


with open(path_to_file) as f:
    lines = f.read().splitlines()

for i in range(len(lines)):
    lines[i] = lines[i].strip()
    if i < 10:
        print(lines[i])

##
# Convert the raw text into arrays of tunes, containing an array of chords
tunes = []
chords_total = 0
for tune in lines:
    tunes.append(tune.strip().split(' '))
    chords_total += len(tune)

print(type(tunes))

# irgendwie habe ich die tunes nicht in TF-IDF zu laufen gebracht. Habe eine manuelle List erstellt um weiterarbeiten zu können.

tunes_manuell = ['CM7 Ebmdim Dm7 G7 CM7 Ebmdim Dm7 G7 C7 F7 Bb7 Eb7 G7 CM7 Ebmdim Dm7 G7 CM7 Ebmdim Dm7 G7 Gm7 C7 FM7 Fm7 D7 Dm7 G7 CM7', 
                 'CM7 Am7 Dm7 G7 CM7 Am7 Dm7 G7 Gm7 C7 FM7 E7 A7 D7 Dm7 G7 D7 G7 C6 F#m7b5 B7 Em7 C#m7b5 F#m7b5 B7 Em7 A7 D7 GM7 Em7 Am7 D7 G7 C#dim7 Dm7 G7 CM7 Am7 Dm7 G7 CM7 Am7 Dm7 G7 Gm7 C7 FM7 E7 A7 D7 G7 C6 Dm7 G7', 
                 'C Em F Em Dm7 C E7 Am G# Dm7 G7 C Caug FM7 G7 C Em F Em Dm7 C E7 Am G# Dm7 G7 C F C G7 C G7 C Am G Am G Am C#dim7 Dm7 C#mdim Dm7 G7 C Em F Em Dm7 C E7 Am G# Dm7 G7 C Em7b5 A7 Dm7 G7 C F6 C', 
                 "Dm7 G7 CM7 Am7 Dm7 G7 CM7 Am7 Dm7 G7 C6 Am7 D7 G7 Dm7 G7 CM7 Am7 Dm7 G7 Em7b5 A7 Dm7 Fm6 CM7 Am7 Dm7 G7 C6 Am7 Dm7 G7",
                 'Dm7 G7 CM7 Dm7 G7 CM7 Bm7 E7 Am7 D7 GM7 Am7 D7 Dm7 G7 C G7 EM7 FM7 A7 Dm7 Fm6 Eaug7 CM7 Am7 Dm7 G7 CM7',
                 'FM7 Fm6 CM7 A7 D7 G7 C C7 C G7 C Dm Em C G# C G7 C G7 C Dm Em C G# C G7 C C7 FM7 Fm6 CM7 A7 D7 G7 C C7',
                 'CM7 A7 Dm7 G7 Em7 A7 Dm7 G7 Gm7 C7 F7 Bb7 Em7 A7 Dm7 G7 Dm7 G7 C6 E7 A7 D7 G7 CM7 A7 Dm7 G7 Em7 A7 Dm7 G7 Gm7 C7 F7 Bb7 Dm7 G7 C6',
                 'C7 F7 C7 F7 C7 Dm7 G7 C7 G7',
                 'CM7 A7 Dm7 G7 Em7 A7 Dm7 G7 Gm7 C7 F7 Bb7 Em7 A7 Dm7 G7 Dm7 G7 C6 E7 A7 D7 G7 CM7 A7 Dm7 G7 Em7 A7 Dm7 G7 Gm7 C7 F7 Bb7 Dm7 G7 C6',
                 'C6 C#dim7 Dm6 Ebdim7 Em7 Am7 Dm7 G7 C6 Ebdim7 Dm7 G7 Em7 A7 D7 G7 C6 C#dim7 Dm6 Ebdim7 Em7 Am7 Dm7 G7 C6 C7 FM7 F#m7b5 B7 Em7 A7 Dm7 G7 C6 Dm7 G7']
print(tunes_manuell)
print(type(tunes_manuell))

# bag of Words Model

# get bag of words features in sparse format
cv = CountVectorizer(min_df=0., max_df=1.)  
cv_matrix = cv.fit_transform(tunes_manuell)
print(cv_matrix)

cv_matrix = cv_matrix.toarray()


# get all unique words in the corpus
vocab = cv.get_feature_names()
pd.DataFrame(cv_matrix, columns = vocab)

# Bag of N-Grams Model, Vorbereitung für TF-IDF.
bv = CountVectorizer(ngram_range=(2,2))
bv_matrix = bv.fit_transform(tunes_manuell)

bv_matrix = bv_matrix.toarray()
vocab = bv.get_feature_names()

tf_idf_bag = pd.DataFrame(bv_matrix, columns=vocab)
print(tf_idf_bag)

# # Using TF-IDF Transformer

tt = TfidfTransformer(norm='l2', use_idf=True)
tt_matrix = tt.fit_transform(cv_matrix)

tt_matrix = tt_matrix.toarray()
vocab = cv.get_feature_names()

tf_idf1 = pd.DataFrame(np.round(tt_matrix, 2), columns=vocab)



# # Using TF-IDF Vectorizer

tv = TfidfVectorizer(min_df = 0., max_df = 1., norm = 'l2', use_idf = True)
tv_matrix = tv.fit_transform(tunes_manuell)
tv_matrix = tv_matrix.toarray()

vocab = tv.get_feature_names()
tf_idf2 = pd.DataFrame(np.round(tv_matrix, 2), columns = vocab)
print(tf_idf2)