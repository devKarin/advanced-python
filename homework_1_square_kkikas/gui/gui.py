"""
Graphical user interface module for Calculator package.

Provides graphical user interface built with tkinter for
calculating square of sum of two arguments.

"""

import tkinter
from square_kkikas.src.square_kkikas.calculator import Calculator


class Gui:
    """
    Graphical user interface built with tkinter for square sum calculator.
    """
    placeholder_text = ""

    def __init__(self):
        """
        Instantiate graphical user interface for the Calculator package.

        Graphical user interface has
        * a resizable window with title
        * two input fields
        * an output message field
        * a calculation button which fires the calculation function
        * a quit button which closes the program
        """
        self.window = tkinter.Tk()
        self.title = self.window.title("Square calculator")
        self.arg_a = tkinter.Entry(self.window, width=5, bg="#87CEFA")
        self.arg_b = tkinter.Entry(self.window, width=5, bg="#87CEFA")
        self.output = tkinter.Message(
            self.window, fg="#87CEFA", bg="#00008B", text="", width=120)
        self.calculator_button = tkinter.Button(self.window,
                                                text="Calculate (a + b)\u00B2",
                                                bg="lightblue",
                                                fg="#00008B",
                                                command=self.calculate)
        self.close_button = tkinter.Button(
            self.window, text="Close", bg="#FFC0CB", fg="#0000CD", command=self.window.quit)
        self.information = tkinter.Message(
            self.window, fg="#87CEFA", bg="#FFB6C1", text="The output is rounded to the precision of 10 decimal points", width=420)

        self.window.config(bg="#B0C4DE")
        self.window.resizable(width=True, height=True)

    def create_set_of_inputs(self):
        """
        Create fields for user input.

        Creates two input fields and their labels for user input.
        """
        tkinter.Label(self.window, text="a", bg="#B0C4DE").grid(
            column=0, row=0, padx=15, pady=5)
        self.arg_a.grid(column=1, row=0, padx=15, pady=5)
        self.arg_a.focus()

        tkinter.Label(self.window, text="b", bg="#B0C4DE").grid(
            column=2, row=0, padx=15, pady=5)
        self.arg_b.grid(column=3, row=0, padx=15, pady=5)

    def create_calculator_button(self):
        """
        Create calculator button.

        Creates calculator button which fires calculation function.
        """
        self.calculator_button.grid(column=4, row=0, padx=15, pady=5)

    def create_close_button(self):
        """
        Create quit button.

        Creates a button which closes the calculator program and the
        user interface.
        """
        self.close_button.grid(column=0, columnspan=7, row=1, padx=15, pady=5)

    def calculate(self):
        """
        Calculation function.

        Calculation function gets the user input and passes them to
        the calculator instance, calls the function which calculates
        the quare of sum of given arguments, configures the output message
        and outputs the result of calculation, clears the input fields
        and sets the focus to the first of them.
        """
        arg1 = self.arg_a.get()
        arg2 = self.arg_b.get()

        calculator = Calculator(arg1, arg2)
        result = calculator.calculate_square_of_sum()
        self.output.configure(
            text=f"({arg1 or 0} + {arg2 or 0})\u00B2 = {result}")
        self.output.grid(column=5, row=0, padx=15, pady=5)
        self.information.grid(column=0, columnspan=7, row=2, padx=15, pady=5)
        self.arg_a.delete(0, tkinter.END)
        self.arg_b.delete(0, tkinter.END)
        self.arg_a.focus()


if __name__ == "__main__":
    pass
