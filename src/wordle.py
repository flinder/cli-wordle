import sys
from argparse import ArgumentParser
import os
import pickle
import numpy as np
import enchant
from termcolor import colored


class Wordle:
    EXACT_MATCH = 'green'
    MATCH = 'yellow'
    MISMATCH = 'white'
    SUPPORTED_LANGUAGES = ['en_US', 'de_DE']
    SUPPORTED_LENGTHS = [3, 4, 5, 6, 7]
    DATA_DIR = 'data/'

    def __init__(self, word_length: int = 5, language: str = 'en_US', seed: int = None, solution: str = None) -> None:
        assert language in self.SUPPORTED_LANGUAGES
        assert word_length in self.SUPPORTED_LENGTHS
        self.language = language
        self.word_length = word_length
        self.dictionary = enchant.Dict(language)

        self.solution = solution
        self.language = language
        self.solved = False

        with open(os.path.join(self.DATA_DIR, self.language + '.pkl'), 'rb') as infile:
            word_lists = pickle.load(infile)
            self.word_list = word_lists[self.word_length]

        self.solution = solution
        if solution is None:
            self.seed = seed
            if seed is None:
                self.seed = np.random.randint(100000, 999999)
            np.random.seed(self.seed)
            self.solution = np.random.choice(self.word_list, 1)[0]
        else:
            self._validate_input(solution)

    def _assert_correct_word_length(self, word: str) -> None:
        assert len(word) == self.word_length, f'Word must be of length {self.word_length}'

    def _assert_correct_spelling(self, word: str) -> None:
        assert self.dictionary.check(word) or self.dictionary.check(word.capitalize()), \
            f'{word} not found in {self.language} dictionary'

    def _validate_input(self, word: str):
        self._assert_correct_word_length(word)
        self._assert_correct_spelling(word)

    def check_submission(self, submission: str) -> list[int]:
        self._validate_input(submission)

        response = [self.MISMATCH] * self.word_length
        for index, (lsub, lsol) in enumerate(zip(submission, self.solution)):
            if lsub == lsol:
                response[index] = self.EXACT_MATCH
                continue
            if lsub in self.solution:
                response[index] = self.MATCH

        if response == [self.EXACT_MATCH] * self.word_length:
            self.solved = True

        return response

    def play(self):
        print(f'Game random seed: {self.seed}')
        tries = 0
        while not self.solved:
            _input = input(f'{self.word_length} letters> ')
            if _input == '!solve':
                break
            if _input == '!quit':
                sys.exit()
            tries += 1
            try:
                coding = self.check_submission(_input)
                print_colored_response(_input, coding)
            except AssertionError as e:
                print(e)

        if not w.solved:
            print(f'womp womp womp... the solution is {self.solution}')
        else:
            print(f'Congrats, you did it! In {tries} tries.')


def print_colored_response(submission: str, coding: list[int]) -> None:
    text = ''
    for letter, color in zip(submission, coding):
        if color == Wordle.MISMATCH:
            text = text + colored(letter, 'white', 'on_grey')
        else:
            text = text + colored(letter, 'grey', f'on_{color}')
    print(text)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--word_length', type=int, choices=[3, 4, 5, 6, 7], default=5, required=True)
    parser.add_argument('--language', type=str, choices=['en_US', 'de_DE'], default='en_US', required=True)
    parser.add_argument('--seed', type=int, required=False)
    parser.add_argument('--solution', type=str, required=False)
    parser.add_argument('--hard', action='store_true', required=False)

    w = Wordle(language='en_US')
    w.play()
