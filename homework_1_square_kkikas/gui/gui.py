import tkinter
from square_kkikas.src.square_kkikas.calculator import Calculator


class Gui:
    placeholder_text = ""

    def __init__(self):
        self.window = tkinter.Tk()
        self.title = self.window.title("Square calculator")
        self.arg_a = tkinter.Entry(self.window, width=5, bg="#87CEFA")
        self.arg_b = tkinter.Entry(self.window, width=5, bg="#87CEFA")
        self.output = tkinter.Message(self.window, fg="#87CEFA", bg="#00008B", text=f"({arg1 or 0} + {arg2 or 0})2 = {result or 0}", width=120)
        self.calculator_button = tkinter.Button(self.window, text="Calculate (a + b)2", bg="lightblue", fg="#00008B", command=self.clicked)
        self.close_button = tkinter.Button(self.window, text="Close", bg="#FFC0CB", fg="#0000CD", command=self.window.quit)

        self.window.config(bg="#B0C4DE")
        self.window.resizable(width=True, height=True)

    def create_set_of_inputs(self):
        tkinter.Label(self.window, text="a", bg="#B0C4DE").grid(column=0, row=0, padx=15, pady=5)
        self.arg_a.grid(column=1, row=0, padx=15, pady=5)
        self.arg_a.focus()

        tkinter.Label(self.window, text="b", bg="#B0C4DE").grid(column=2, row=0, padx=15, pady=5)
        self.arg_b.grid(column=3, row=0, padx=15, pady=5)

    def create_calculator_button(self):
        self.calculator_button.grid(column=4, row=0, padx=15, pady=5)

    def create_close_button(self):
        self.close_button.grid(column=0, columnspan=7, row=1, padx=15, pady=5)

    def clicked(self):
        arg1 = self.arg_a.get()
        arg2 = self.arg_b.get()

        calculator = Calculator(arg1, arg2)
        result = calculator.calculate_square_of_sum()
        # output = tkinter.Message(self.window, fg="#87CEFA", bg="#00008B", text=f"({arg1 or 0} + {arg2 or 0})2 = {result}", width=120)
        self.output.grid(column=5, row=0, padx=15, pady=5)
        self.arg_a.delete(0, tkinter.END)
        self.arg_b.delete(0, tkinter.END)
        self.arg_a.focus()


if __name__ == "__main__":
    print("Calculator window")
