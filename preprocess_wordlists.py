import os
import re
import requests
import numpy as np
from wordle import Wordle

WORD_LIST_URLS = {
    'en_US': 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt',
    'de_DE': 'https://raw.githubusercontent.com/dys2p/wordlists-de/main/de-7776-v1.txt'
}


def de_special_chars(word):
    special_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss'}
    for char, replacement in special_chars.items():
        word = re.sub(char, replacement, word)
    return word


def preprocess_word_list(word_list_url: str, output_file: str, language: str) -> None:

    word_list = requests.get(word_list_url).content.decode('utf-8').split('\n')
    out = set()
    for line in word_list:
        line = line.strip('\r\n')
        word = de_special_chars(line.lower()) if language == 'de_DE' else line.lower()
        if word and len(word) == Wordle.WORD_LENGTH and word.isalpha():
            out.add(word)

    print(f'Parsed {len(out)} words for {language}')
    with open(output_file, 'w') as outfile:
        out = sorted(list(out))
        for word in out:
            outfile.write(word + '\n')


if __name__ == '__main__':

    for lang, url in WORD_LIST_URLS.items():
        print(f'Processing {lang}')
        preprocess_word_list(word_list_url=url,
                             output_file=os.path.join('../data/', lang + '.txt'),
                             language=lang)
