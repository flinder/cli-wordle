import pytest
from wordle import Wordle

mismatch = Wordle.MISMATCH
exact_match = Wordle.EXACT_MATCH
match = Wordle.MATCH

test_data = [
    # No match
    ('en_US', 'burns', 'light', [mismatch] * 5),
    ('de_DE', 'kranz', 'beute', [mismatch] * 5),
    # Single match
    ('en_US', 'burns', 'rocky', [match] + [mismatch] * 4),
    ('de_DE', 'kranz', 'zelte', [match] + [mismatch] * 4),
    # Multiple matches
    ('en_US', 'burns', 'shard', [match, mismatch, mismatch, match, mismatch]),
    ('de_DE', 'kranz', 'ringe', [match, mismatch, match, mismatch, mismatch]),
    # Exact match
    ('en_US', 'burns', 'loves', [mismatch, mismatch, mismatch, mismatch, exact_match]),
    ('de_DE', 'kranz', 'kelle', [exact_match, mismatch, mismatch, mismatch, mismatch]),
    # Exact match and match
    ('en_US', 'burns', 'runes', [match, exact_match, match, mismatch, exact_match]),
    ('de_DE', 'kranz', 'erben', [mismatch, exact_match, mismatch, mismatch, match]),
]


@pytest.mark.parametrize("language, solution, submission, expected_response", test_data)
def test_check_submission(language, solution, submission, expected_response):
    w = Wordle(solution=solution, language=language)
    response = w.check_submission(submission=submission)
    assert response == expected_response


def test_check_submission_fails_on_too_long_submission():
    w = Wordle()
    submission = 'longest'
    with pytest.raises(AssertionError) as e_info:
        w.check_submission(submission)


init_test_data = [
    ('en_US', None, 'hello'),
    ('de_DE', None, 'hallo'),
    ('en_US', 0, None),
    ('de_DE', 0, None),
]


@pytest.mark.parametrize('language, seed, solution', init_test_data)
def test_wordle_initializes(language, seed, solution):
    w = Wordle(language=language, seed=seed, solution=solution)