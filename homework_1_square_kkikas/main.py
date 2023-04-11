"""
Main module for square of sum calculator.

Main module which chooses and starts user interface for
square of sum calculator.

"""
# Uncomment following line to use terminal-based user interface.
# from square_kkikas.calculator import Calculator

# Comment following line out to use terminal-based user interface.
from gui.gui import Gui


# Comment following function out to use terminal-based user interface.
def graphical_user_interface():
    """
    Graphical user interface.

    Starts the graphical user interface.
    """

    root = Gui()
    root.create_set_of_inputs()
    root.create_calculator_button()
    root.create_close_button()
    root.window.mainloop()


# Uncomment following function to use terminal-based user interface.
# def terminal_user_interface():
#     """
#     Terminal-based user interface.
#
#     Starts the terminal-based user interface.
#     """
#
#     print("Square of sum calculator\n")
#     raw_input_a = input("Insert argument a: ")
#     raw_input_b = input("Insert argument b: ")
#
#     calculator = Calculator(raw_input_a, raw_input_b)
#     output = calculator.calculate_square_of_sum()
#     print(f"(a + b)\u00B2 = {output}\n")
#     print("The output is rounded to the precision of 10 decimal points")
#     print("To quit, press Ctrl + C\n")
#     terminal_user_interface()


# Comment following line out to use terminal-based user interface.
graphical_user_interface()
# Uncomment following line to use terminal-based user interface.
# terminal_user_interface()


if __name__ == "__main__":
    pass
