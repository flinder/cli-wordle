import os
import pickle
from wordle import Wordle

RAW_DATA_DIR = '../data/raw_wordlists'
PROCESSED_DATA_DIR = '../data/processed_word_lists'


def preprocess_word_list(input_file: str, output_file: str, word_lengths: list[int]) -> None:

    lens = set(word_lengths)
    out = {length: [] for length in word_lengths}
    # TODO: only words with [A-Za-z] no special characters

    with open(input_file) as infile:
        for line in infile:
            line = line.strip('\n')
            if (word_length := len(line)) in lens:
                out[word_length].append(line.lower())

    with open(output_file, 'wb') as outfile:
        pickle.dump(out, outfile)


if __name__ == '__main__':

    for language in Wordle.SUPPORTED_LANGUAGES:
        print(f'Processing {language}')
        preprocess_word_list(input_file=os.path.join(RAW_DATA_DIR, language + '.txt'),
                             output_file=os.path.join(PROCESSED_DATA_DIR, language + '.pkl'),
                             word_lengths=Wordle.SUPPORTED_LENGTHS)
