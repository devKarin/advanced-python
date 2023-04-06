import unittest

from square_kkikas.src.square_kkikas.calculator import Calculator


class CalculatorTest(unittest.TestCase):
    """
    CalculatorTest class.

    A class for test cases testing outputs of Calculator functions.
    """

    def test_sum_simple_integers(self):
        """
        Test whether the sum is calculated correctly in case of arguments being simple integers.
        """
        calculator = Calculator(2, 5)
        self.assertEqual(calculator.calculate_sum(), 7, "Should be 7")
    
    def test_sum_floats(self):
        """
        Test whether the sum is calculated correctly when using floats.
        """
        calculator = Calculator(2.2, 5.7)
        self.assertEqual(calculator.calculate_sum(), 7.9, "Should be 7.7")


if __name__ == "__main__":
    unittest.main()
