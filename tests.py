from unittest import TestCase

from timetp import tokenizer


class TestTokenizer(TestCase):
    def test_first_letter_isalpha_syntax_error(self):
        with self.assertRaises(SyntaxError):
            tokenizer('d4')

        with self.assertRaises(SyntaxError):
            tokenizer('4dw')

    def test_number_without_letter(self):
        with self.assertRaises(SyntaxError):
            tokenizer('4')

        with self.assertRaises(SyntaxError):
            tokenizer('4d5')

    def test_bad_letters(self):
        with self.assertRaises(SyntaxError):
            tokenizer("4y")

        with self.assertRaises(SyntaxError):
            tokenizer('4d5g')

    def test_one_pair(self):
        time = '4d'
        result = tokenizer(time)
        self.assertEqual(result, [(4, 'd')])

    def test_many_pairs(self):
        time = '4d5w12h54m11s'
        result = tokenizer(time)
        self.assertEqual(
            result,
            [(4, 'd'), (5, 'w'), (12, 'h'), (54, 'm'), (11, 's')]
        )
