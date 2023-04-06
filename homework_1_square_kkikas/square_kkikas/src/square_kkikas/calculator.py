import math


class Calculator:
    """
    Calculator class.

    Calculate sum of the arguments.
    """
    power = 2

    def __init__(self, arg_a, arg_b) -> float:
        """
        Initialize the Calculator class.

        Calculator has two input arguments and two calculated properties.
        """
        self.arg_a = arg_a
        self.arg_b = arg_b
        self.sum_of_args = 0
        self.square_of_sum = 0
    
    def validate_arguments(self):
        """
        Check whether the arguments are correct type and convert them if needed.

        Arguments other than type of integer or float are converted into floats with the value of 0.
        Floats and integers are converted into floats
        """
        if not (isinstance(self.arg_a, float) or isinstance(self.arg_a, int)):
            self.arg_a = float(0)
        else:
            self.arg_a = float(self.arg_a)
        if not (isinstance(self.arg_b, float) or isinstance(self.arg_b, int)):
            self.arg_b = float(0)
        else:
            self.arg_b = float(self.arg_b)
        
    def calculate_sum(self):
        self.validate_arguments()
        self.sum_of_args = sum((self.arg_a, self.arg_b))
        return self.sum_of_args
    
    def calculate_square_of_sum(self):
        self.calculate_sum()
        self.square_of_sum = math.pow(self.sum_of_args, self.power)
        return self.square_of_sum


if __name__ == "__main__":
    calculator1 = Calculator(1, 8)
    calculator2 = Calculator(1.1, 8.8)
    print(calculator1.calculate_sum())
    print(calculator2.calculate_sum())
    print(calculator1.calculate_square_of_sum())
    print(calculator2.calculate_square_of_sum())
