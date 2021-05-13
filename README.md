# Analysis of Chord Sequences of Jazz Standards

## Installation
`pip install -r requirements.txt`

## Input Data

* `01_parseAllFiles.py`: parses the xml input files from iReal Pro and encodes them into a json file with root, bass and degrees for each chord (relative values, numbers only)
* `02_read_common_chord_progressions.py`: trial to encode common chord progressions for later mapping with n-grams; creates a pickle file with a dictionary as output.
* `03a_generate_chords_all_keys.py`: encode the relative values from step 01 into the chord names. Select either simplified (basic) chords or full chords.
  * each tune is encoded in all 12 keys -> resulting in 12 * 1334 = 16008 rows.
* `03b_generate_chords_default_key.py`: encode each tune in its default key. Results in 1334 rows.
* `03c_generate_chords_relative_key.py`: encode the major tunes in C major, and the minor tunes in A minor. Results in 1334 rows.
* `read_chords.py`: Example how to read and split the generated chords into lists

Notes:
* All consequtive duplicate chords are removed in step 3.
* All alterations #9, #11, #13 and b9, b11, b13 are removed.

Recommendation:
* in `01_parseAllFiles.py`, use the /test/ directory to create a small test set
* use `03c_generate_chords_relative_key.py` to start working



## Possible Approaches
### TF-IDF with single Chords
First calculate the TF-IDF for each tune, then calculate a distance metric to determine similarity between tunes.

* Calculate TF-IDF. Result is a matrix with n unique chords and m tunes.
  * Example: https://stackabuse.com/python-for-nlp-creating-tf-idf-model-from-scratch/
* Then try Jaccard metric or Cosine Similarity to calculate similarity of tunes
  * Example: https://iq.opengenus.org/document-similarity-tf-idf/

### TF-IDF with N-Grams as Inputs
Again calculate the TF-IDF for each tune, but this time use N-Grams as inputs instead of single chords. Then calculate a distance metric to determine similarity between tunes.

### Word Embeddings, vec2word
Might not work because it does not respect the chord sequence, but still worth a try.

### Whatever other ideas
Whatever else could be interesting to try.


