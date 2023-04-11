"""
Main test module for square sum calculator with user interface.


"""

import unittest
from square_kkikas.tests.test_calculator import CalculatorTest


class ApplicationTest(unittest.TestCase):
    """
    ApplicationTest class.

    A class for test cases testing main application functions.
    """

    def test_first(self):
        """
        Test for user interface.
        """
        print("first test run")
        self.assertEqual(0, 0, "Should be 0")


if __name__ == "__main__":
    # Add tests into one suite and run test cases sequentially.
    suite = unittest.TestSuite()
    suite.addTest(CalculatorTest("Test square calculator module"))
    suite.addTest(ApplicationTest("Test Gui."))
    unittest.TextTestRunner().run(suite)
