from chords.ngrams.buildNGrams import NGrams
import tqdm
import pandas as pd
import pickle
import os

###
#
# size of the ngrams
N_ngram = 3

# filename definitions
directory = './chord_sequences'
tune_names_path = os.path.join(directory, 'tune_names.txt')
path_to_file = os.path.join(directory, 'chords_relative_full.txt')

# outputfiles
outputfile_progressions = 'progressions_inv.pickle'
outputfile_ngrams = 'ngrams.csv'
outputfile_top_ngrams = 'ngrams_top.csv'
outputfile_score = 'ngrams_score.csv'

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

##
# build a count table for chords

# build a set of unique chords
chords_unique = list(set(' '.join(lines).strip().split(' ')))
print(
    f'Found {len(tunes)} tunes with a total number of {chords_total} chords in the dataset, with {len(chords_unique)} unique chords.')

# build a TF dictionary for the chords
chords_count = {}
for chord in chords_unique:
    cnt = 0
    for tune in tunes:
        cnt += tune.count(chord)
    chords_count[chord] = cnt / chords_total

##
# build n-grams for each tune
ngrams = NGrams(tunes)
nn = ngrams.build(n=N_ngram)
# print(nn)

# calculate total number of ngrams, build a set of unique ngrams
ngrams_array = [ngram for tune in nn for ngram in tune]
ngrams_total = len(ngrams_array)
ngrams_unique = set(ngrams_array)
print(f'Found {ngrams_total} ngrams, with {len(ngrams_unique)} unique ngrams.')

# build a TF dictionary for the ngrams
ngrams_count = {}
ngrams_tf = []
ngrams_vector = []
for ngram in tqdm.tqdm(ngrams_unique):
    cnt = 0
    for tune in nn:
        cnt += tune.count(ngram)
    ngrams_count[ngram] = cnt / ngrams_total

    ngrams_vector.append(ngram)
    ngrams_tf.append(ngrams_count[ngram])
    # print(f'{ngram}: {ngrams_count[ngram]}')

df_ngrams = pd.DataFrame(list(zip(ngrams_vector, ngrams_tf)),
                         columns=['ngram', 'tf'])

##
#
infile = open(os.path.join(directory, outputfile_progressions), 'rb')
progressions_inv = pickle.load(infile)
infile.close()

# [progressions_inv[v] for v in row if progressions_inv.get(v)]
df_ngrams['prog'] = df_ngrams.ngram.apply(lambda row: progressions_inv.get(row) if row in progressions_inv else '')

##
# write to disk
df_ngrams.sort_values('tf', ascending=False, inplace=True)
df_ngrams.to_csv(os.path.join(directory, outputfile_ngrams),
                 index=False,
                 sep=';',
                 encoding='utf-8',
                 errors='replace')

##
#
ngrams = []
tunes = []
for row in tqdm.tqdm(df_ngrams.head(2000).itertuples()):
    i = 0
    for i in range(len(nn)):
        if nn[i].count(row.ngram) > 0:
            tunes.append(tune_names[i])
            ngrams.append(row.ngram)

df_top_ngrams = pd.DataFrame(list(zip(ngrams, tunes)),
                             columns=['ngram', 'tune'])

df_top_ngrams.to_csv(os.path.join(directory, outputfile_top_ngrams),
                     index=False,
                     sep=';',
                     encoding='utf-8',
                     errors='replace')

