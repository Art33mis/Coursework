""" This file contains tests for convolutional coder and Viterbi decoder """

import unittest
import statistical_dec
import numpy as np


class MyTestCase(unittest.TestCase):
    """ Main test which check correctness of work Viterbi decoder """
    def test_total(self):
        inform_b = np.random.randint(2, size=5)
        ch = statistical_dec.channel(statistical_dec.coder(inform_b))
        d = statistical_dec.decoder(ch)
        np.testing.assert_array_equal(d[:-2], np.array(inform_b))



if __name__ == '__main__':
    unittest.main()
