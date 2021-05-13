import os

directory = './chord_sequences'
path_to_file = os.path.join(directory, 'chords_full_all_keys.txt')

with open(path_to_file) as f:
    tunes = f.read().splitlines()

# split the chords per tune into lists
for i in range(len(tunes)):
    # remove the space at the end of each tune
    tunes[i] = tunes[i].strip()
    if i < 5:
        print(tunes[i])
    # split the chords per tune into a list
    tunes[i] = tunes[i].split(' ')

# create a list of all unique chords
flat_list = [chord for tune in tunes for chord in tune]
all_chords = list(set(flat_list))

print(f'Number of unique chords: {len(all_chords)}\n')

###
path_to_file = os.path.join(directory, 'chords_relative_full.txt')

with open(path_to_file) as f:
    tunes = f.read().splitlines()

# split the chords per tune into lists
for i in range(len(tunes)):
    # remove the space at the end of each tune
    tunes[i] = tunes[i].strip()
    if i < 5:
        print(tunes[i])
    # split the chords per tune into a list
    tunes[i] = tunes[i].split(' ')

# create a list of all unique chords
flat_list = [chord for tune in tunes for chord in tune]
all_chords = list(set(flat_list))

print(f'Number of unique chords: {len(all_chords)}\n')
