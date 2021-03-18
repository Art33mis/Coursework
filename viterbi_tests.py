""" This file contains tests for convolutional coder and Viterbi decoder """

import unittest
import viterbi_dec


class MyTestCase(unittest.TestCase):
    """ Main test which check correctness of work Viterbi decoder """
    def test_total(self, string="11 01 10 10 10"):
        self.assertEqual(viterbi_dec.coder("11111")[:-1], string)
        test_str = string
        for i in range(len(test_str)):
            if test_str[i] == '0':
                test_str = test_str[:i] + "1" + test_str[i + 1:]
            if test_str[i] == '1':
                test_str = test_str[:i] + "0" + test_str[i + 1:]
            self.assertEqual(viterbi_dec.decoder(test_str), "11111")
            test_str = string


if __name__ == '__main__':
    unittest.main()
