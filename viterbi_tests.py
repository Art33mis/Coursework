""" This file contains tests for convolutional coder and Viterbi decoder """

import unittest
import viterbi_dec


class MyTestCase(unittest.TestCase):
    """ Main test which check correctness of work Viterbi decoder """
    def test_total(self, string="11 01 10 10 10"):
        self.assertEqual(viterbi_dec.coder("11111")[:-1], string)
        test_str = string
        for char in test_str:
            if char == '0':
                char = '1'
            else:
                char = "0"
            self.assertEqual(viterbi_dec.decoder(test_str), "11111")


if __name__ == '__main__':
    unittest.main()
