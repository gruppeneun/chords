from chords.chord import Chord
from chords.ngrams.buildNGrams import NGrams
from dataset.readData import ReadData
import re
import tqdm
import os
import json

config = json.load(open('config.json'))

N_ngram = config['config']['N_ngrams']

directory = config['config']['output_directory']
if not os.path.exists(directory):
    os.makedirs(directory)

subdir = os.path.join(directory, f"ngrams{N_ngram}")
if not os.path.exists(subdir):
    os.makedirs(subdir)

##
# define the object to read in the chords for the tunes
data_obj = ReadData()
data_obj.read_tunes()

# use simplified basic chords - or full chords?
method = f"all_key"
if config['config']['use_basic_chords']:
    data, names = data_obj.rootAndDegreesSimplified()
    fn = f"{config['config']['input']}_chords-basic_{method}.txt"
    file_name = os.path.join(subdir, fn)

else:
    data, names = data_obj.rootAndDegrees()
    fn = f"{config['config']['input']}_chords-full_{method}.txt"
    file_name = os.path.join(subdir, fn)

filename_tunes = os.path.join(subdir, f"{config['config']['input']}_tune_names_{method}.txt")


tune_names = []
for tune in names:
    tune_name = re.sub(r'\.xml', "", tune)
    tune_names += [tune_name]

##
# read the (musical) key and mode for each tune
default_keys = json.load(open('dataset/keys.json'))


###
# Generate Chord sequences

sequences_all = []
tune_names_all = []
for key in tqdm.tqdm(range(0, 12)):
    for i in range(len(data)):
        tune = data[i]
        seq = []
        for chord in tune:
            formatted_chord = Chord(chord).toSymbol(key=key, includeRoot=True, includeBass=False)
            # delete all the chord extensions (+b9), (+#9), (+b11), (+#11), (+b13), (+#13)
            formatted_chord = re.sub('\(\+[b#]?[0-9]+\)', '', formatted_chord)
            # replace mM9 chord by mM7 because it occurs only once
            formatted_chord = re.sub('mM9$', 'mM7', formatted_chord)
            # replace all maug chords; they occur only once minor-augmented =
            seq += [formatted_chord]
            # print("Bar {}: {}".format(chord['measure'], formatted_chord))
        sequences_all += [seq]
        tune_names_all.append(tune_names[i])

##
#
# for each tune, remove all chords occurring multiple times in a sequence
seq_unique = []
tune_unique_chords = []

if config['config']['reduce_consecutive_chords']:
    for tune in tqdm.tqdm(sequences_all):
        tune_unique_chords = []
        last_chord = None
        for chord in tune:
            if chord != last_chord:
                tune_unique_chords.append(chord)
                last_chord = chord
        seq_unique.append(tune_unique_chords)
else:
    seq_unique = sequences_all

##
#
# build n-grams for each tune
print('Building n-grams...')
ngrams = NGrams(seq_unique)
nn = ngrams.build(n=N_ngram)
print('Done.')

##
# Replace spaces between chords by underscores
seq_patterns = []
tune_chords = []
for tune in nn:
    tune_chords = []
    for chord in tune:
        tune_chords.append(chord.replace(" ", "-"))
    seq_patterns.append(tune_chords)



###
# Generate file with tune names

file = open(filename_tunes, 'w')  # write to file
for tune in tune_names_all:
    file.write(f'{tune}\n')
file.close()  # close file

###
# for each tune, remove all chords occurring multiple times in a sequence

file = open(file_name, 'w')  # write to file
for tune in seq_patterns:
    for chord in tune:
        file.write(f'{chord} ')
    file.write(f'\n')
file.close()

