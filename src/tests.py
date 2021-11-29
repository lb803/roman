import os
import sys
import unittest


if sys.version_info[0] > 2:
    from io import StringIO
else:
    from StringIO import StringIO

import roman


TEST_MAP = ((0, 'N'), (1, 'I'), (3, 'III'), (4, 'IV'), (9, 'IX'), (14, 'XIV'),
            (19, 'XIX'), (24, 'XXIV'), (40, 'XL'), (49, 'XLIX'), (90, 'XC'),
            (99, 'XCIX'), (400, 'CD'), (490, 'CDXC'), (499, 'CDXCIX'),
            (900, 'CM'), (990, 'CMXC'), (998, 'CMXCVIII'), (999, 'CMXCIX'),
            (2013, 'MMXIII'))

if sys.version_info[0] > 2:
    _str = str
else:
    _str = unicode  # NOQA: F821


class TestRoman(unittest.TestCase):

    def test_toRoman(self):
        for num_arabic, num_roman in TEST_MAP:
            self.assertEqual(roman.toRoman(num_arabic), num_roman,
                             '%s should be %s' % (num_arabic, num_roman))

    def test_toRoman_errors(self):
        self.assertRaises(roman.OutOfRangeError, roman.toRoman, 100000)
        self.assertRaises(roman.NotIntegerError, roman.toRoman, '1')

    def test_fromRoman(self):
        for num_arabic, num_roman in TEST_MAP:
            self.assertEqual(roman.fromRoman(num_roman), num_arabic,
                             '%s should be %s' % (num_roman, num_arabic))

    def test_fromRoman_errors(self):
        self.assertRaises(
            roman.InvalidRomanNumeralError, roman.fromRoman, '')
        self.assertRaises(
            roman.InvalidRomanNumeralError, roman.fromRoman, 'Q12')

    def test_parse_args(self):
        sys.argv = ['roman', '10']
        args = roman.parse_args()
        self.assertFalse(args.reverse)
        self.assertEqual(args.number, '10')

    def test_main_toRoman(self):
        for num_arabic, num_roman in TEST_MAP:
            sys.argv = ['roman', _str(num_arabic)]
            sys.stdout = StringIO()
            ex_st = roman.main()
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, num_roman)
            self.assertEqual(ex_st, os.EX_OK)

    def test_main_fromRoman(self):
        for num_arabic, num_roman in TEST_MAP:
            sys.argv = ['roman', '--reverse', num_roman]
            sys.stdout = StringIO()
            ex_st = roman.main()
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, _str(num_arabic))
            self.assertEqual(ex_st, os.EX_OK)

    def test_main_fromRoman_caseInsensitive(self):
        for num_arabic, num_roman in TEST_MAP:
            sys.argv = ['roman', '--reverse', num_roman.lower()]
            sys.stdout = StringIO()
            ex_st = roman.main()
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, _str(num_arabic))
            self.assertEqual(ex_st, os.EX_OK)

    def test_main_isRoman(self):
        for num_arabic, num_roman in TEST_MAP:
            if num_arabic == 0:
                continue
            self.assertFalse(roman.isRoman(str(num_arabic)))
            self.assertTrue(roman.isRoman(str(num_roman)))

def test_suite():
    return unittest.makeSuite(TestRoman)
