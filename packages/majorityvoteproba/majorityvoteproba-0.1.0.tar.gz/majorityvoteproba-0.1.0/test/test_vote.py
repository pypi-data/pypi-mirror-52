import unittest
from majorityvoteproba import majority_vote_proba
import numpy as np
# import numpy.testing as npt   # assert_almost_equal


class Test_Vote(unittest.TestCase):

    def test1(self):
        x = np.array([[0.49, 0.6, 0.6]])
        y, vote, cnt = majority_vote_proba(x)
        self.assertEquals(y, 0.5666666666666667)  # .5+.2/3
        self.assertEquals(vote, 1)
        self.assertEquals(cnt, 2)

    def test2(self):
        x = np.array([[0.4, 0.4, 0.5]])
        y, vote, cnt = majority_vote_proba(x)
        self.assertEquals(y, 0.43333333333333335)  # .5-.2/3
        self.assertEquals(vote, 0)
        self.assertEquals(cnt, 1)


# run
if __name__ == '__main__':
    unittest.main()
