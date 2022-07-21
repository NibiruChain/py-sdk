import unittest
from collections import namedtuple

from nibiru.exceptions import ConvertError, InvalidArgumentError
from nibiru.utils import float_to_sdkdec, sdkdec_to_float


class TestDecimals(unittest.TestCase):
    def test_to_dec(self):
        tc = namedtuple('testcase', 'name arg exp fail')
        tests = [
            tc('empty string', '', '', True),
            # valid numbers
            tc('number 0', 0, '0' + '0' * 18, False),
            tc('number 10', 10, '10' + '0' * 18, False),
            tc('number 123', 123, '123' + '0' * 18, False),
            tc('neg. number 123', -123, '-123' + '0' * 18, False),
            # with fractional
            tc('missing mantisse', 0.3, '03' + '0' * 17, False),
            tc('number 0.5', 0.5, '05' + '0' * 17, False),
            tc('number 13.235', 13.235, '13235' + '0' * 15, False),
            tc('neg. number 13.235', -13.235, '-13235' + '0' * 15, False),
            tc('number 1574.00005', 1574.00005, '157400005' + '0' * 13, False),
        ]

        for tt in tests:
            with self.subTest(tt.name):
                try:
                    res = float_to_sdkdec(tt.arg)
                    self.assertEqual(tt.exp, res)
                    self.assertFalse(tt.fail)
                except (InvalidArgumentError, ConvertError):
                    self.assertTrue(tt.fail)

    def test_from_dec(self):
        tc = namedtuple('testcase', 'name arg exp fail')
        tests = [
            tc('number with \'.\'', '.3', '', True),
            tc('number with \'.\'', '5.3', '', True),
            tc('invalid number', 'hello', '', True),
            # valid numbers
            tc('empty string', '', 0, False),
            tc('empty string', None, 0, False),
            tc('number 0', '0' * 5, 0, False),
            tc('number 0', '0' * 22, 0, False),
            tc('number 10', '10' + '0' * 18, 10, False),
            tc('neg. number 10', '-10' + '0' * 18, -10, False),
            tc('number 123', '123' + '0' * 18, 123, False),
            # with fractional
            tc('number 0.5', '05' + '0' * 17, 0.5, False),
            tc('fractional only 0.00596', '596' + '0' * 13, 0.00596, False),
            tc('number 13.5', '135' + '0' * 17, 13.5, False),
            tc('neg. number 13.5', '-135' + '0' * 17, -13.5, False),
            tc('number 1574.00005', '157400005' + '0' * 13, 1574.00005, False),
        ]

        for tt in tests:
            with self.subTest(tt.name):
                try:
                    res = sdkdec_to_float(tt.arg)
                    self.assertEqual(tt.exp, res)
                except (InvalidArgumentError, ConvertError):
                    self.assertTrue(tt.fail)


if __name__ == '__main__':
    unittest.main()
