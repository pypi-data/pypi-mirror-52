import unittest
import numpy as np
import numpy.testing as npt
from onepara import onepara


class Test_onepara_func(unittest.TestCase):

    def test1(self):
        R0 = np.array(
            [[1.00000000, -0.94814754, 0.09932496],
             [-0.94814754, 1.00000000, -0.33933036],
             [0.09932496, -0.33933036, 1.00000000]])

        R1 = np.array(
            [[1.00000000, 0.60394902, 0.60394902],
             [0.60394902, 1.00000000, 0.60394902],
             [0.60394902, 0.60394902, 1.00000000]])

        Rfit = onepara(R0)

        npt.assert_allclose(Rfit, R1)


# run
if __name__ == '__main__':
    unittest.main()
