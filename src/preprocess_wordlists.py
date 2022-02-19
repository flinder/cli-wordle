import os
import pickle
import re
import requests
from wordle import Wordle

WORD_LIST_URLS = {
    'en_US': 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt',
    'de_DE': 'https://raw.githubusercontent.com/davidak/wortliste/master/wortliste.txt'
}


def de_special_chars(word):
    special_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}
    for char, replacement in special_chars.items():
        word = re.sub(char, replacement, word)


def preprocess_word_list(word_list_url: str, output_file: str, word_lengths: list[int],
                         language: str) -> None:

    lens = set(word_lengths)
    out = {length: [] for length in word_lengths}

    word_list = requests.get(word_list_url).content.decode('utf-8').split('\n')
    for line in word_list:
        line = line.strip('\r\n')
        if (word_length := len(line)) in lens and line.isalpha():
            word = de_special_chars(line.lower()) if language == 'de_DE' else line.lower()
            out[word_length].append(word)

    print([f'{x}: {len(out[x])}' for x in out])
    with open(output_file, 'wb') as outfile:
        pickle.dump(out, outfile)


if __name__ == '__main__':

    for lang, url in WORD_LIST_URLS.items():
        print(f'Processing {lang}')
        preprocess_word_list(word_list_url=url,
                             output_file=os.path.join('../data/', lang + '.pkl'),
                             word_lengths=Wordle.SUPPORTED_LENGTHS,
                             language=lang)
