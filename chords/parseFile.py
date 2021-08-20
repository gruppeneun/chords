import xml.etree.ElementTree as ET
from dataset.xmlChildren import getChild, getChildren
from dataset.chordFromXML import ChordXML


def get_chords(measure, key):
    # each measure (beat) has multiple harmonies (chords)
    harmonies = getChildren(measure, "harmony")

    # parse the harmony tag with Chord().toJson and put it into the json file
    chords = []
    for harmony in harmonies:
        chord = ChordXML(harmony, key)  # chord.key is the default key of the tune, 0 = C!
        keynumber = chord.key
        chords += [chord.toJson()]
    # chords = [Chord(harmony, key).toJson() for harmony in harmonies]
    return chords, keynumber


def parseFile(file):
    # get the first child element with tag part, this is the song
    root = ET.parse(file).getroot()
    part1 = getChild(root, "part")

    identification = getChild(root, "identification")
    creator = getChild(identification, "creator")
    composer = creator.text

    # get the song key
    attribute = getChild(part1[0], "attributes")
    key = getChild(attribute, "key")
    keynumber = None
    mode = getChild(key, "mode").text

    out = {}
    sections = {}
    repeat_from = None
    ending1 = None
    measure_num_real = 0
    find_section = None

    # loop over all bars
    for measure in part1:
        measure_num_real += 1

        measure_num_xml = int(measure.attrib["number"])
        out[measure_num_real] = {}
        # print(f'Measure XML file: {measure_num_xml}, Real Measure: {measure_num_real}----- ')

        out[measure_num_real], keynumber = get_chords(measure=measure, key=key)

        for elem in measure.getchildren():

            # find section indicators A, B, C etc ('Rehearsal' xml tag)
            find_direction = elem.find('direction-type')
            if find_direction is not None:
                find_section = find_direction.find('rehearsal')
                if find_section is not None:
                    print(f"Bar {measure_num_real}, Section {find_section.text}")
                    sections[measure_num_real] = find_section.text

            # handle repetitions
            # print(f'    {elem}')
            # search for first or second endings
            find_ending = elem.find('ending')
            if find_ending is not None:
                if find_ending.attrib['type'] == 'start':
                    ending1 = measure_num_xml

            find_repeat = elem.find('repeat')
            if find_repeat is not None:
                if find_repeat.attrib['direction'] == 'forward':
                    repeat_from = measure_num_xml
                elif find_repeat.attrib['direction'] == 'backward':
                    if ending1 is None:
                        repeat_end = measure_num_xml + 1
                    else:
                        repeat_end = ending1
                    # print(f'looping over the bars {repeat_from} to {repeat_end}')

                    # by convention, if repeat forward sign is missing, repeat from start
                    if repeat_from is None:
                        repeat_from = 1

                    for i in range(repeat_from, repeat_end):
                        measure_num_real += 1
                        out[measure_num_real] = out[i]
                        if i in sections.keys():
                            print(f"Bar {measure_num_real}, Section {sections[i]}")
                            sections[measure_num_real] = sections[i]

                    find_section = None
                    repeat_from = None
                    ending1 = None

    return out, keynumber, mode, composer, sections, measure_num_real
