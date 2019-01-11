# -*- coding: utf-8 -*-

import sys
sys.path.append('../pyplane/')

import core.PyPlaneHelpers as pph
import unittest


class CoreTests(unittest.TestCase):

    def test_check_if_latex(self):

        res = pph.check_if_latex()

        # this assumes that latex and dvipng are installed on the
        # testing machine
        expected_res = True

        self.assertEqual(res, expected_res)


def main():
    unittest.main()

if __name__ == '__main__':
    main()