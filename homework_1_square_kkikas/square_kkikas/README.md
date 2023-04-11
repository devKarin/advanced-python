# `square-kkikas` calculator package for calculating square of sum for given arguments

This is a simple example package created for study purposes.<br>
This package contains a simple calculator, which calculates the sum of given arguments and square of that sum.<br>
This package was created with the help of Python packaging tutorial [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)<br>

## Structure
- `square_kkikas` is a starting point for the package directory which contains `src\square_kkikas` directory with the actual contents of that package and `tests` directory with unit tests to that package.<br>
- `square_kkikas\src\square_kkikas` is the core of this package containing `__init__.py` and `calculator.py` files.<br>
- `tests` directory contains `__init__.py` and `test_calculator.py` files. 

## Installation
To install the `square-kkikas` calculator package, run in your environment:<br>

```bash

pip install -i https://test.pypi.org/simple/ square-kkikas

```

## About the Calculator
`Calculator` class can be instantiated with any number of arguments with any type. Input arguments will be validated and converted into floating point numbers when possible. If it is not possible to convert the input into floating point number, its value is considered to be 0.0.<br>
`Calculator` accepts dot or comma for decimal point separator. Be aware that only the first comma or dot will be considered as a decimal separator and all the other commas and dots as well as spaces will be removed from input during the validation process.<br>
`Calculator` has two useful functions:
- `calculate_sum()` which takes no other arguments than the instance itself and which calculates and returns the sum of given arguments as a floating point number.
- `calculate_square_of_sum()` which takes no other arguments than the instance itself and which calculates and returns the square of the sum of given arguments as a floating point number. `calculate_square_of_sum()` uses the `calculate_sum()` function under the hood.

### Usage
To use the `Calculator`, import it, instantiate it and call either `calculate_sum()` or `calculate_sum()` function on the instance like so: <br>

```python

from square_kkikas.calculator import Calculator  # Import

calculator = Calculator(4, 5)  # Instantiate
square_of_sum = calculator.calculate_square_of_sum()  # Calculate square of sum. Returns 81.0 as a string.
sum = calculator.calculate_sum()  # Returns 9.0 as a floating point number.

```

In order to calculate the square of sum of given arguments there is no need to call `calculate_sum()` function first because the `calculate_square_of_sum()` function uses it under the hood anyway.<br>

### Change history
0.0.1 First version
0.0.2 Fix import in example given in README.md
0.0.3 Change `calculate_square_sum()` return type from str to float (without rounding). Rewrite tests regarding the change.