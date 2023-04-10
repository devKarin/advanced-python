"""
Test module for Calculator module.

Available classes:
class CalculatorTest(unittest.TestCase):
    A class for test cases testing outputs of Calculator functions.

Available functions within CalculatorTest class:
test_sum_simple_integers(self):
    Tests calculate_sum() function with simple integers.
test_sum_floats(self):
    Tests calculate_sum() function with floats.
test_sum_negative_integers(self):
    Tests calculate_sum() function with simple negative integers.
test_sum_negative_floats(self):
    Tests calculate_sum() function with negative floats.
test_sum_mixed_signs(self):
    Tests calculate_sum() function with both positive and negative numbers
    at the same time.
test_sum_big_positive_integers(self):
    Tests calculate_sum() function with big positive integers.
test_sum_big_negative_integers(self):
    Tests calculate_sum() function with big negative integers.
test_sum_big_positive_floats(self):
    Tests calculate_sum() function with big positive floating point nummbers.
test_sum_small_positive_floats(self):
    Tests calculate_sum() function with small positive floating point
    nummbers.
test_sum_big_negative_floats(self):
    Tests calculate_sum() function with big negative floating point
    nummbers.
test_sum_small_negative_floats(self):
    Tests calculate_sum() function with small negative floating point
    nummbers.
test_sum_big_positive_integer_small_negative_float(self):
    Tests calculate_sum() function with both big positive integers and small
    negative floatin point numbers at the same time.
test_sum_zeros(self):
    Tests calculate_sum() function with zeros as arguments.
test_sum_one_zero_other_floats(self):
    Tests calculate_sum() function with zeros and floating point
    numbers at the same time.
test_sum_strings(self):
    Tests calculate_sum() function with strings as arguments.
test_sum_empty(self):
    Tests calculate_sum() function with missing arguments or no arguments.
test_square_positive_integer(self):
    Tests calculate_square_of_sum() function with positive integers passed
    to the calculator instance.
test_square_negative_integer(self):
    Tests calculate_square_of_sum() function with negative integers passed
    to the calculator instance.
test_square_positive_float(self):
    Tests calculate_square_of_sum() function with positive floating point
    numbers passed to the calculator instance.
test_square_negative_float(self):
    Tests calculate_square_of_sum() function with negative floating point
    numbers passed to the calculator instance.
test_square_big_positive_integer(self):
    Tests calculate_square_of_sum() function with big positive integers
    passed to the calculator instance.
test_square_big_negative_integer(self):
    Tests calculate_square_of_sum() function with big negative integers
    passed to the calculator instance.
test_square_big_positive_float(self):
    Tests calculate_square_of_sum() function with big positive floating point
    numbers passed to the calculator instance.
test_square_big_negative_float(self):
    Tests calculate_square_of_sum() function with big negative floating point
    numbers passed to the calculator instance.
test_square_small_positive_float(self):
    Tests calculate_square_of_sum() function with small positive floating point
    numbers passed to the calculator instance.
test_square_small_negative_float(self):
    Tests calculate_square_of_sum() function with small negative floating point
    numbers passed to the calculator instance.
test_square_zero(self):
    Tests calculate_square_of_sum() function with zeros as arguments
    passed to the calculator instance.
test_square_empty(self):
    Tests calculate_square_of_sum() function with no arguments
    passed to the calculator instance.

"""

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
        calculator = Calculator(1, 2, 35)
        self.assertEqual(calculator.calculate_sum(), 38, "Should be 38")
        calculator = Calculator(201, 5, 23, 6987)
        self.assertEqual(calculator.calculate_sum(), 7216, "Should be 7216")

    def test_sum_floats(self):
        """
        Test whether the sum is calculated correctly in case arguments being floats.
        """

        calculator = Calculator(2.2, 5.7)
        self.assertEqual(calculator.calculate_sum(), 7.9, "Should be 7.9")
        calculator = Calculator(5.685, 1.45656, 7.151)
        self.assertEqual(calculator.calculate_sum(),
                         14.29256, "Should be 14.29256")
        calculator = Calculator(2.765321, 54846.7, 8.453435, 48486.0)
        self.assertEqual(calculator.calculate_sum(),
                         103343.918756, "Should be 103343.918756")
        calculator = Calculator(0.2, 0.71, 8.15, 0.815, 5.02)
        self.assertEqual(calculator.calculate_sum(),
                         14.895, "Should be 14.895")

    def test_sum_negative_integers(self):
        """
        Test whether the sum is calculated correctly in case arguments being negative integers.
        """

        calculator = Calculator(-5, -6)
        self.assertEqual(calculator.calculate_sum(), -11, "Should be -11")
        calculator = Calculator(-286, -3, -15214)
        self.assertEqual(calculator.calculate_sum(), -
                         15503, "Should be -15503")
        calculator = Calculator(-8, -9, -4, -2)
        self.assertEqual(calculator.calculate_sum(), -23, "Should be -23")

    def test_sum_negative_floats(self):
        """
        Test whether the sum is calculated correctly in case arguments being negative floats.
        """

        calculator = Calculator(-1.55, -6.78)
        self.assertEqual(calculator.calculate_sum(), -8.33, "Should be -8.33")
        calculator = Calculator(-0.505, -6.078, -15.57985)
        self.assertEqual(calculator.calculate_sum(), -
                         22.16285, "Should be -22.16285")
        calculator = Calculator(-5.55, -6.666, -0.777, -0.808)
        self.assertEqual(calculator.calculate_sum(), -
                         13.801, "Should be -13.801")
        calculator = Calculator(-0.5, -0.05, -0.005, -0.0005)
        self.assertEqual(calculator.calculate_sum(), -
                         0.5555, "Should be -0.5555")

    def test_sum_mixed_signs(self):
        """
        Test whether the sum is calculated correctly in case arguments have
        different signs.
        """

        calculator = Calculator(-7, 3.12)
        self.assertEqual(calculator.calculate_sum(), -3.88, "Should be -3.88")
        calculator = Calculator(-0.72, 3, 125.86, -856.0203)
        self.assertEqual(calculator.calculate_sum(), -
                         727.8803, "Should be -727.8803")
        calculator = Calculator(-2, 3, -3, 2)
        self.assertEqual(calculator.calculate_sum(), 0, "Should be 0")

    def test_sum_big_positive_integers(self):
        """
        Test whether the sum is calculated correctly in case arguments being big positive integers.
        """

        calculator = Calculator(4546786413130, 123458484764131)
        self.assertEqual(calculator.calculate_sum(),
                         128005271177261, "Should be 128005271177261")
        calculator = Calculator(54564848113377, 111111111111, 454545458686)
        self.assertEqual(calculator.calculate_sum(),
                         55130504683174, "Should be 55130504683174")

    def test_sum_big_negative_integers(self):
        """
        Test whether the sum is calculated correctly in case arguments being big negative integers.
        """

        calculator = Calculator(-546513144416, -1515153111303)
        self.assertEqual(calculator.calculate_sum(), -
                         2061666255719, "Should be -2061666255719")
        calculator = Calculator(-545451, -51565123, -54855694)
        self.assertEqual(calculator.calculate_sum(), -
                         106966268, "Should be -106966268")

    def test_sum_big_positive_floats(self):
        """
        Test whether the sum is calculated correctly in case arguments being big positive floats.
        """

        calculator = Calculator(469138434.16, 15951231113.03)
        self.assertEqual(calculator.calculate_sum(),
                         16420369547.19, "Should be 16420369547.19")
        calculator = Calculator(
            945151212511.5455, 448258742369.2555, 125423215214.58419)
        self.assertEqual(calculator.calculate_sum(),
                         1518833170095.38519, "Should be 1518833170095.38519")

    def test_sum_small_positive_floats(self):
        """
        Test whether the sum is calculated correctly in case arguments being small positive floats.
        """

        calculator = Calculator(0.000000004691, 0.00000000000000003)
        self.assertEqual(calculator.calculate_sum(),
                         0.00000000469100003, "Should be 0.00000000469100003")
        calculator = Calculator(0.00000000911119, 0.000000004, 0.000001254)
        self.assertEqual(calculator.calculate_sum(),
                         0.00000126711119, "Should be 0.00000126711119")

    def test_sum_big_negative_floats(self):
        """
        Test whether the sum is calculated correctly in case arguments being big negative floats.
        """

        calculator = Calculator(-46913338434.11, -3551231113.0351)
        self.assertEqual(calculator.calculate_sum(), -
                         50464569547.1451, "Should be -50464569547.1451")
        calculator = Calculator(-9412851512.571125, -
                                148258322369.2175, -1211123211214.00411)
        self.assertEqual(calculator.calculate_sum(), -
                         1368794385095.792735, "Should be -1368794385095.792735")

    def test_sum_small_negative_floats(self):
        """
        Test whether the sum is calculated correctly in case arguments being small negative floats.
        """

        calculator = Calculator(-0.00000000000046913311, -0.0000003550351)
        self.assertEqual(calculator.calculate_sum(
        ), -0.00000035503556913311, "Should be -0.00000035503556913311")
        calculator = Calculator(-0.0000000009, -
                                0.000000000000000014, -0.000000000000012111)
        self.assertEqual(calculator.calculate_sum(), -
                         0.000000000900012125, "Should be -0.000000000900012125")

    def test_sum_big_positive_integer_small_negative_float(self):
        """
        Test whether the sum is calculated correctly in case of one argument
        is a big positive integer and
        one argument is a small negative float.
        """

        calculator = Calculator(54564848113377, -0.00000000000046913311)
        self.assertEqual(calculator.calculate_sum(),
                         54564848113376.999999999999530867,
                         "Should be 54564848113376.999999999999530867")
        calculator = Calculator(
            1518833170095, -0.000000000000000014, -0.000000000000012111, 125423215214)
        self.assertEqual(calculator.calculate_sum(),
                         1644256385308.999999999999987875,
                         "Should be 1644256385308.999999999999987875")

    def test_sum_zeros(self):
        """
        Test whether the sum is calculated correctly in case arguments being zeros.
        """

        calculator = Calculator(0, 0)
        self.assertEqual(calculator.calculate_sum(), 0, "Should be 0")
        calculator = Calculator(0, 0, 0, 0, 0)
        self.assertEqual(calculator.calculate_sum(), 0, "Should be 0")

    def test_sum_one_zero_other_floats(self):
        """
        Test whether the sum is calculated correctly in case one argument
        is zero, others are floats.
        """

        calculator = Calculator(0, 0.5679)
        self.assertEqual(calculator.calculate_sum(),
                         0.5679, "Should be 0.5679")
        calculator = Calculator(0.00575, 0, 7.0, 1.85, 9.4789)
        self.assertEqual(calculator.calculate_sum(),
                         18.33465, "Should be 18.33465")

    def test_sum_strings(self):
        """
        Test whether the sum is calculated correctly in case of arguments being strings.
        """

        calculator = Calculator("0", "8")
        self.assertEqual(calculator.calculate_sum(), 8, "Should be 8")
        calculator = Calculator("fizz", "buzz", "bar")
        self.assertEqual(calculator.calculate_sum(), 0, "Should be 0")
        calculator = Calculator("5,3", "1.7", "0 1")
        self.assertEqual(calculator.calculate_sum(), 8, "Should be 8")

    def test_sum_empty(self):
        """
        Test whether the sum is calculated correctly in case of arguments being empty.
        """

        calculator = Calculator(0, )
        self.assertEqual(calculator.calculate_sum(), 0, "Should be 0")
        calculator = Calculator(0.05750, 7, )
        self.assertEqual(calculator.calculate_sum(),
                         7.05750, "Should be 7.05750")
        calculator = Calculator()
        self.assertEqual(calculator.calculate_sum(), 0, "Should be 0")

    def test_square_positive_integer(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being positive integers.
        """

        calculator = Calculator(1, 0)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         1, "Should be 1")
        calculator = Calculator(9, 4, 10, 2)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         625, "Should be 625")
        calculator = Calculator(2, 3)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         25, "Should be 25")

    def test_square_negative_integer(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being negative integers.
        """

        calculator = Calculator(-1, 0)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         1, "Should be 1")
        calculator = Calculator(-1, -4, -2, -3)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         100, "Should be 100")
        calculator = Calculator(-4, -2)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         36, "Should be 36")

    def test_square_positive_float(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments being positive floats.
        """

        calculator = Calculator(0.1, 0.02)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.144, "Should be 0.144")
        calculator = Calculator(0.2, 0.02, 0.02, 0.01)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.625, "Should be 0.625")

    def test_square_negative_float(self):
        """
        Test whether the square of sum is calculated correctly in case
        of arguments of the calculator being negative floats.
        """

        calculator = Calculator(-0.11, -0.09)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.4, "Should be 0.4")
        calculator = Calculator(-0.222478, -2.02, -8.5911, -0.000401)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         117.375100972441, "Should be 117.375100972441")

    def test_square_big_positive_integer(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being big positive integers.
        """
        calculator = Calculator(446461548, 0)
        self.assertEqual(calculator.calculate_sum(),
                         199327913842556304, "Should be 199327913842556304")
        calculator = Calculator(
            4545151, 65542, 1254)
        self.assertEqual(calculator.calculate_sum(),
                         21270055130809, "Should be 21270055130809")

    def test_square_big_negative_integer(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being big negative integers.
        """
        calculator = Calculator(-422431541, -98412, -123456)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         178635904139321281, "Should be 178635904139321281")

    def test_square_big_positive_float(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being big positive floats.
        """
        calculator = Calculator(123456789.11, 258741.09011)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         15305532412694329.4566440121,
                         "Should be 15305532412694329.4566440121")
        calculator = Calculator(222.478, 200.02, 85000.911, 401.000001)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         7365829180.370929818001, "Should be 7365829180.370929818001")

    def test_square_big_negative_float(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being big negative floats.
        """
        calculator = Calculator(-123456789.11, -258741.09011)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         15305532412694329.4566440121,
                         "Should be 15305532412694329.4566440121")
        calculator = Calculator(-222.478, -200.02, -85000.911, -401.000001)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         7365829180.370929818001, "Should be 7365829180.370929818001")

    def test_square_small_positive_float(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being small positive floats.
        """
        calculator = Calculator(0.00012345678911, 0.0000000251)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.0000000152477769381743365921,
                         "Should be 0.0000000152477769381743365921")
        calculator = Calculator(0.0000000000222,
                                0.0000002002,
                                0.0000085,
                                0.0000004)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.00000000008281404408937284,
                         "Should be 0.00000000008281404408937284")

    def test_square_small_negative_float(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being small negative floats.
        """
        calculator = Calculator(-0.00012345678911, -0.0000000251)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.0000000152477769381743365921,
                         "Should be 0.0000000152477769381743365921")
        calculator = Calculator(-0.0000000000222,
                                -0.0000002002,
                                -0.0000085,
                                -0.0000004)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0.00000000008281404408937284,
                         "Should be 0.00000000008281404408937284")

    def test_square_zero(self):
        """
        Test whether the square of sum is calculated correctly in case of
        arguments of the calculator being zeros.
        """
        calculator = Calculator(0, 0, 0, 0)
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0, "Should be 0")

    def test_square_empty(self):
        """
        Test whether the square of sum is calculated correctly in case of arguments
        of the calculator being missing.
        """

        calculator = Calculator()
        self.assertEqual(calculator.calculate_square_of_sum(),
                         0, "Should be 0")


if __name__ == "__main__":
    unittest.main()
