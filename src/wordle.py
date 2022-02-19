import sys
from argparse import ArgumentParser
import os
import numpy as np
import enchant
from termcolor import colored


class Wordle:
    EXACT_MATCH = 'green'
    MATCH = 'yellow'
    MISMATCH = 'white'
    SUPPORTED_LANGUAGES = ['en_US', 'de_DE']
    DATA_DIR = 'data/'
    MAX_TRIES = 5
    WORD_LENGTH = 5
    CMDS = {'solve': '!solve', 'quit': '!quit'}

    def __init__(self, language: str = 'en_US', seed: int = None, solution: str = None) -> None:
        assert language in self.SUPPORTED_LANGUAGES
        self.language = language
        self.dictionary = enchant.Dict(language)
        self.solution = solution
        self.language = language
        self.solved = False

        with open(os.path.join(self.DATA_DIR, self.language + '_reviewed.txt')) as infile:
            self.word_list = [word.strip('\n') for word in infile.readlines()]

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
        assert len(word) == self.WORD_LENGTH, f'Word must have {self.WORD_LENGTH} letters.'

    def _assert_correct_spelling(self, word: str) -> None:
        assert self.dictionary.check(word) or self.dictionary.check(word.capitalize()), \
            f'{word} not found in {self.language} dictionary'

    def _validate_input(self, word: str):
        self._assert_correct_word_length(word)
        self._assert_correct_spelling(word)

    def check_submission(self, submission: str) -> list[str]:
        self._validate_input(submission)

        response = [self.MISMATCH] * self.WORD_LENGTH
        for index, (lsub, lsol) in enumerate(zip(submission, self.solution)):
            if lsub == lsol:
                response[index] = self.EXACT_MATCH
                continue
            if lsub in self.solution:
                response[index] = self.MATCH

        if response == [self.EXACT_MATCH] * self.WORD_LENGTH:
            self.solved = True

        return response

    def play(self):
        print('*'*50)
        print('WORDLE')
        print('*'*50)
        print(f'Selected language: {self.language}, number of tries: {self.MAX_TRIES}.')
        print(f'Game random seed: {self.seed}')
        print('\n')
        tries = 0
        while not self.solved and tries <= self.MAX_TRIES:
            _input = input(f'Type a {self.WORD_LENGTH} letter word> ')
            if _input == self.CMDS['solve']:
                break
            if _input == self.CMDS['quit']:
                sys.exit()
            try:
                coding = self.check_submission(_input)
                print_colored_response(_input, coding)
            except AssertionError as e:
                print(e)
                continue
            tries += 1

        if not w.solved:
            print(f'\nwomp womp womp... the solution was {self.solution}')
        else:
            print(f'Congrats, you did it! In {tries} tries.')


def print_colored_response(submission: str, coding: list[str]) -> None:
    text = ''
    for letter, color in zip(submission, coding):
        if color == Wordle.MISMATCH:
            text = text + colored(letter, 'white', 'on_grey')
        else:
            text = text + colored(letter, 'grey', f'on_{color}')
    print(text)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--language', type=str, choices=['en_US', 'de_DE'], default='en_US')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--solution', type=str)
    #parser.add_argument('--hard', action='store_true', required=False)

    args = parser.parse_args()

    w = Wordle(language=args.language, seed=args.seed, solution=args.solution)
    w.play()
