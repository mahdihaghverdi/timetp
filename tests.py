from datetime import timedelta
from unittest import TestCase

from timetp import tokenize, parse


class TestTokenizer(TestCase):
    def test_first_letter_isalpha_syntax_error(self):
        with self.assertRaises(SyntaxError):
            tokenize('d4')

        with self.assertRaises(SyntaxError):
            tokenize('4dw')

    def test_number_without_letter(self):
        with self.assertRaises(SyntaxError):
            tokenize('4')

        with self.assertRaises(SyntaxError):
            tokenize('4d5')

    def test_bad_letters(self):
        with self.assertRaises(SyntaxError):
            tokenize("4y")

        with self.assertRaises(SyntaxError):
            tokenize('4d5g')

    def test_one_pair(self):
        time = '4d'
        result = tokenize(time)
        self.assertEqual(result, [('days', 4)])

    def test_many_pairs(self):
        time = '4d5w12h54m11s'
        result = tokenize(time)
        self.assertEqual(
            result,
            [('days', 4), ('weeks', 5), ('hours', 12), ('minutes', 54), ('seconds', 11)]
        )


class TestParser(TestCase):
    def test_one_days(self):
        data = '4d'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(days=4))

    def test_many_days(self):
        data = '4d5d10d'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(days=4 + 5 + 10))

    def test_one_weeks(self):
        data = '5w'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(weeks=5))

    def test_many_days_many_weeks(self):
        data = '4d5w1d8w'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(days=4 + 1, weeks=5 + 8))

    def test_one_hours(self):
        data = '5h'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(hours=5))

    def test_many_days_weeks_hours(self):
        data = '2h4h4d5w11h1d8w'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(days=4 + 1, weeks=5 + 8, hours=2 + 4 + 11))

    def test_one_minutes(self):
        data = '5m'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(minutes=5))

    def test_many_days_weeks_hours_minutes(self):
        data = '2h4h43m4d90m5w11h1d5m8w'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(days=4 + 1, weeks=5 + 8, hours=2 + 4 + 11, minutes=5 + 90 + 43))

    def test_one_seconds(self):
        data = '5s'
        result = parse(tokenize(data))
        self.assertEqual(result, timedelta(seconds=5))

    def test_many_all(self):
        data = '110s2h4h43m4d90m5w11h1d68s5m8w98s'
        result = parse(tokenize(data))
        self.assertEqual(
            result, timedelta(
                days=4 + 1, weeks=5 + 8, hours=2 + 4 + 11, minutes=5 + 90 + 43, seconds=110 + 68 + 98
                )
            )
