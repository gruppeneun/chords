from chords.chord import Chord
from dataset.readData import ReadData
import json
import re
import os

directory = './chord_sequences'
if not os.path.exists(directory):
    os.makedirs(directory)

# define the object to read in the chords for the tunes
data_obj = ReadData()
data_obj.read_tunes()

# use simplified basic chords - or full chords?
basic_chords = False

if basic_chords:
    data, names = data_obj.rootAndDegreesSimplified()
    file_name = './chord_sequences/chords_relative_basic.txt'
else:
    data, names = data_obj.rootAndDegrees()
    file_name = './chord_sequences/chords_relative_full.txt'

filename_tunes = os.path.join(directory, 'tune_names.txt')
filename_mode = os.path.join(directory, 'tune_mode.txt')

# read the (musical) key and mode for each tune
default_keys = json.load(open('dataset/keys.json'))

##
# index the name of the tunes to be able to match them to the generated chord sequences
name_dict = {}
i = 0
for key in default_keys.keys():
    name_dict[i] = key
    i += 1

# index the modality of the tunes to be able to match them to the generated chord sequences
mode_dict = {}
i = 0
for key in default_keys.keys():
    mode_dict[i] = default_keys[key]['mode']
    i += 1

###
# Generate Chord sequences

sequences = []
modes = []
for i in range(len(data)):
    tune = data[i]
    seq = []
    # transpose a major tune to C major, and a minor tune to A minor
    key = 3 if mode_dict[i] == 'major' else 0
    for chord in tune:
        formatted_chord = Chord(chord).toSymbol(key=key, keyLess=False, includeRoot=True, includeBass=False)
        # delete all the chord extensions (+b9), (+#9), (+b11), (+#11), (+b13), (+#13)
        formatted_chord = re.sub('\(\+[b#]?[0-9]+\)', '', formatted_chord)
        # replace mM9 chord by mM7 because it occurs only once
        formatted_chord = re.sub('mM9$', 'mM7', formatted_chord)
        # replace all maug chords; they occur only once minor-augmented =
        seq += [formatted_chord]
        # print("Bar {}: {}".format(chord['measure'], formatted_chord))
    sequences += [seq]
    modes.append(mode_dict[i])

###
# Generate file with tune names

file = open(filename_tunes, 'w')  # write to file
for tune in names:
    file.write(f'{tune}\n')
file.close()  # close file

###
# for each tune, remove all chords occurring multiple times in a sequence

file = open(file_name, 'w')  # write to file
for tune in sequences:
    last_chord = None
    for chord in tune:
        if chord != last_chord:
            file.write(f'{chord} ')
            last_chord = chord
    file.write(f'\n')
file.close()

###
# Generate file with modality

file = open(filename_mode, 'w')  # write to file
for mode in modes:
    file.write(f'{mode}\n')
file.close()  # close file
