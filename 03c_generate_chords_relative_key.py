from chords.chord import Chord
from dataset.readData import ReadData
import json
import re
import os

config = json.load(open('config.json'))

directory = config['config']['output_directory']
if not os.path.exists(directory):
    os.makedirs(directory)

subdir = os.path.join(directory, 'chords')
if not os.path.exists(subdir):
    os.makedirs(subdir)

##
# define the object to read in the chords for the tunes
data_obj = ReadData()
data_obj.read_tunes()

# use simplified basic chords - or full chords?
method = 'relative_key'
if config['config']['use_basic_chords']:
    data, names = data_obj.rootAndDegreesSimplified()
    fn = f"{config['config']['input']}_chords-basic_{method}.txt"
    file_name = os.path.join(subdir, fn)
else:
    data, names = data_obj.rootAndDegrees()
    fn = f"{config['config']['input']}_chords-full_{method}.txt"
    file_name = os.path.join(subdir, fn)


filename_tunes = os.path.join(subdir, f"{config['config']['input']}_tune_names.txt")
filename_mode = os.path.join(subdir, f"{config['config']['input']}_tune_mode.txt")
filename_composer = os.path.join(subdir, f"{config['config']['input']}_composer.txt")



##
# read the meta information with key mode, composer, sections
meta_info = json.load(open('dataset/meta_info.json'))

# index the meta_info of the tunes to be able to match them to the generated chord sequences
meta_dict = {}
i = 0
for tune in meta_info.keys():
    meta_dict[i] = meta_info[tune]
    i += 1


###
# Generate Chord sequences

sequences = []
modes = []
composers = []
for i in range(len(data)):
    tune = data[i]
    seq = []
    # transpose a major tune to C major, and a minor tune to A minor
    key = 3 if meta_dict[i]['default_key']['mode'] == 'major' else 0
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
    modes.append(meta_dict[i]['default_key']['mode'])
    composers.append(meta_dict[i]['composer'])

###
# Generate file with tune names
file = open(filename_tunes, 'w')  # write to file
for tune in names:
    file.write(f'{tune}\n')
file.close()  # close file

###
# for each tune, remove all chords occurring multiple times in a sequence

file = open(file_name, 'w')  # write to file

if config['config']['reduce_consecutive_chords']:
    for tune in sequences:
        last_chord = None
        for chord in tune:
            if chord != last_chord:
                file.write(f'{chord} ')
                last_chord = chord
        file.write(f'\n')
else:
    for tune in sequences:
        last_chord = None
        for chord in tune:
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

###
# Generate file with composer

file = open(filename_composer, 'w')  # write to file
for composer in composers:
    file.write(f'{composer}\n')
file.close()  # close file
