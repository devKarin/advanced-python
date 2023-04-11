"""
Calculator module.

This module calculates sum and square of sum.

Available classes:
class Calculator:
    Performs calculations with given arguments.
    Calculator class has a class variable named power for power.

Available functions within Calculator class:
__init__(self, *args) -> None: 
    Initialises Calculator class.
    Every calculator has unknown amount of arguments.
validate_arguments(self) -> None:
    Converts arguments into float type.
    Removes spaces, converts commas into dots and removes duplicate dots.
    Strings are converted into floats with value of 0.
calculate_sum(self) -> float:
    Calculates sum of arguments passed to Calculator object.
calculate_square_of_sum(self) -> float:
    Calculates square of sum for arguments passed to Calculator object.

"""

import math
from decimal import Decimal


class Calculator:
    """
    Calculator class.

    Performs calculations with given arguments.
    """
    power = 2

    def __init__(self, *args) -> None:
        """
        Initialize the Calculator class.

        Calculator has two input arguments and two calculated properties.
        """
        self.args = args or (0, 0)

    def validate_arguments(self) -> None:
        """
        Convert arguments into floats.

        Arguments which can not be cast into floats will become zero-value
        floats, other arguments will be converted into floats.
        """

        valid_args = (list(self.args)).copy()

        # Clean the arguments.
        for index in range(len(self.args)):
            if isinstance(valid_args[index], str):
                valid_args[index] = (valid_args[index]).strip()
                valid_args[index] = (valid_args[index]).replace(",", ".")
                valid_args[index] = (valid_args[index]).replace(" ", "")
                if (valid_args[index]).count(".") > 1:
                    cleaned_string = (valid_args[index]).partition(".")
                    cleaned_string = list(cleaned_string)
                    cleaned_string[2] = (cleaned_string[2]).strip(".")
                    valid_args[index] = "".join(cleaned_string)

        # Convert arguments into floats.
        for index in range(len(self.args)):
            if isinstance(valid_args[index], str):
                split_string = (valid_args[index]).split(".")
                for part in split_string:
                    if not part.isdecimal():
                        valid_args[index] = float(0)
                        break
                else:
                    valid_args[index] = float(valid_args[index])
            else:
                valid_args[index] = float(valid_args[index])

        self.args = tuple(valid_args)

    def calculate_sum(self) -> float:
        """
        Calculate the sum of given arguments.

        Calls the validation function and then calculates the sum of
        given arguments.
        """
        self.validate_arguments()
        sum_of_args = sum(self.args)
        return sum_of_args

    def calculate_square_of_sum(self) -> str:
        """
        Calculate square of sum of given arguments.

        Calls the sum calculation function and then calculates the square
        of the sum.
        """
        sum_of_args = self.calculate_sum()
        square_of_sum = format(math.pow(Decimal.from_float(sum_of_args), self.power), '.10')
        return square_of_sum


if __name__ == "__main__":
    pass
