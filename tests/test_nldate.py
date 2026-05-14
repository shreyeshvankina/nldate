import pytest
from datetime import date
from nldate import parse


@pytest.fixture
def base_date():
    return date(2024, 5, 10)


def test_today(base_date):
    assert parse("today", today=base_date) == date(2024, 5, 10)


def test_tomorrow(base_date):
    assert parse("tomorrow", today=base_date) == date(2024, 5, 11)


def test_yesterday(base_date):
    assert parse("yesterday", today=base_date) == date(2024, 5, 9)


def test_next_weekday(base_date):
    assert parse("next Tuesday", today=base_date) == date(2024, 5, 14)


def test_last_weekday(base_date):
    assert parse("last Monday", today=base_date) == date(2024, 5, 6)


def test_in_x_days(base_date):
    assert parse("in 3 days", today=base_date) == date(2024, 5, 13)


def test_x_days_ago(base_date):
    assert parse("4 days ago", today=base_date) == date(2024, 5, 6)


def test_exact_date():
    assert parse("December 1st, 2025") == date(2025, 12, 1)


def test_complex_before_exact():
    assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)


def test_complex_after_relative(base_date):
    assert parse("1 year and 2 months after yesterday", today=base_date) == date(
        2025, 7, 9
    )


def test_case_insensitivity(base_date):
    assert parse("NEXT tUeSdAy", today=base_date) == date(2024, 5, 14)
