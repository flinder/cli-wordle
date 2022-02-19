import pytest
from wordle import Wordle

solution = 'burns'
w = Wordle(solution=solution)


def test_check_submission_finds_no_matches():
    submission = 'light'
    response = w.check_submission(submission=submission)
    expected_response = [w.MISMATCH] * 5
    assert response == expected_response


def test_check_submission_finds_single_match():
    submission = 'rocky'
    response = w.check_submission(submission=submission)
    expected_response = [w.MATCH] + [w.MISMATCH] * 4
    assert response == expected_response


def test_check_submission_finds_multiple_matches():
    submission = 'shard'
    response = w.check_submission(submission=submission)
    expected_response = [w.MATCH, w.MISMATCH, w.MISMATCH, w.MATCH, w.MISMATCH]
    assert response == expected_response


def test_check_submission_finds_exact_match():
    submission = 'loves'
    response = w.check_submission(submission=submission)
    expected_response = [w.MISMATCH] * 4 + [w.EXACT_MATCH]
    assert response == expected_response


def test_check_submission_finds_exact_and_normal_matches():
    submission = 'runes'
    response = w.check_submission(submission=submission)
    expected_response = [w.MATCH, w.EXACT_MATCH, w.MATCH, w.MISMATCH, w.EXACT_MATCH]
    assert response == expected_response


def test_check_submission_fails_on_too_long_submission():
    submission = 'longest'
    with pytest.raises(AssertionError) as e_info:
        w.check_submission(submission)

