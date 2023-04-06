import unittest
from square_kkikas.tests.test_calculator import CalculatorTest

class ApplicationTest(unittest.TestCase):
    """
    CApplicationTest class.

    A class for test cases testing main application functions.
    """
    def test_first(self):
        print("first test run")


if __name__ == "__main__":
    # Add tests into one suite and run test cases sequentially.
    suite = unittest.TestSuite()
    suite.addTest(CalculatorTest("Test square calculator module"))
    suite.addTest(ApplicationTest("Test Gui."))
    unittest.TextTestRunner().run(suite)
