from chords.chord import Chord
from dataset.readData import ReadData
import re
import pickle

directory = './chord_sequences'
outputfile_progressions = 'progressions_inv.pickle'
data_obj = ReadData()
data_obj.read_progressions()

# data, names = data_obj.rootAndDegreesBasic()
data, names = data_obj.rootAndDegrees()

###
# Generate Chord sequences

sequences = []
progressions = {}
for index in range(len(data)):
    sequences = []
    for key in range(0, 12):
        seq = []
        for chord in data[index]:
            formatted_chord = Chord(chord).toSymbol(key=key, includeRoot=True, includeBass=False)
            # delete all the chord extensions (+b9), (+#9), (+b11), (+#11), (+b13), (+#13)
            formatted_chord = re.sub('\(\+[b#]?[0-9]+\)', '', formatted_chord)
            # replace mM9 chord by mM7 because it occurs only once
            formatted_chord = re.sub('mM9$', 'mM7', formatted_chord)
            # replace all maug chords; they occur only once minor-augmented =
            seq += [formatted_chord]
            # print("Bar {}: {}".format(chord['measure'], formatted_chord))
        sequences += [seq]
    progressions[names[index]] = sequences

###
# create inverse dictionary with common chord progressions

progressions_inv = {}
for key, value in progressions.items():
    for chord_prog in value:
        chord_prog_text = ' '.join(chord_prog)
        if chord_prog_text not in progressions_inv:
            progressions_inv[chord_prog_text] = key
        else:
            print('warning: duplicate names for common chord progressions')

outfile = open(outputfile_progressions, 'wb')
pickle.dump(progressions_inv, outfile)
outfile.close()
