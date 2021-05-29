import os
import json
from chords.parseFile import parseFile

##
# read config file
config = json.load(open('config.json'))

# directory with the input xml chord files
xmldirectory = config['xmldirectory'][config['config']['input']]

##
#
files = os.listdir(xmldirectory)

# json object that will be saved into file
out = {}
composers = {}
keys = {}
for file in files:
    print(file)
    out[file], key, mode, composer = parseFile(xmldirectory + file)
    composers[file] = composer
    keys[file] = {'key': key,
                  'mode': mode}

f = open("dataset/chords.json", "w")
f.write(json.dumps(out, indent=2))
f.close()

f = open("dataset/composers.json", "w")
f.write(json.dumps(composers, indent=2))
f.close()

f = open("dataset/keys.json", "w")
f.write(json.dumps(keys, indent=2))
f.close()
