import json


class ReadData():
    def __init__(self):
        self.file_path = None
        self.data = None

    def read_tunes(self):
        self.file_path = './dataset/chords.json'

    def read_progressions(self):
        self.file_path = './dataset/chord_progressions/chord_progressions.json'

    def readData(self, modifier):
        """
        Reads the parsed json file and creates a list of dictionnaries. Each list element contains a list of the chords
        of one single tune.
        :param modifier: function pointer to the function who defines how to encode a chord:
                         one of rootAndDegrees(), rootAndDegreesBasic(),  rootAndDegreesOnly7()
        :return:
        """
        self.data = json.load(open(self.file_path))
        represent = lambda chord: {'root': chord['root'],
                                   'components': modifier(chord['degrees']),
                                   'bass': chord['bass'],
                                   'measure': chord['measure'],
                                   }
        # store the names of the dictionary keys
        names = list(self.data.keys())

        # store the chord sequences
        seqs = []
        # loop over all tunes
        for key in self.data.keys():
            song = self.data[key]
            seq = []
            for measureKey in song.keys():
                measure = song[measureKey]
                for chord in measure:
                    chord['measure'] = measureKey
                    seq += [represent(chord)]
            seqs += [seq]
        return seqs, names

    def rootAndDegrees(self):
        return self.readData(lambda x: x)

    def rootAndDegreesBasic(self):
        def modifier(degrees):
            no7 = degrees[:]
            if 1 in no7: no7.remove(1)
            if 2 in no7: no7.remove(2)
            if 3 not in no7 and 4 not in no7: no7 += [4]
            if 5 in no7: no7.remove(5)
            if 6 in no7: no7.remove(6)
            if 8 in no7: no7.remove(8)
            if 9 in no7: no7.remove(9)
            if 10 in no7: no7.remove(10)
            if 11 in no7: no7.remove(11)
            no7.sort()
            return no7

        return self.readData(modifier)

    def rootAndDegreesOnly7(self):
        def modifier(degrees):
            no7 = degrees[:]
            if 1 in no7: no7.remove(1)
            if 2 in no7: no7.remove(2)
            if 3 not in no7 and 4 not in no7: no7 += [4]
            if 3 in no7 and 4 in no7: no7.remove(3)
            if 5 in no7: no7.remove(5)
            if 6 in no7: no7.remove(6)
            if 8 in no7: no7.remove(8)
            if 9 in no7: no7.remove(9)
            no7.sort()
            return no7

        return self.readData(modifier)

