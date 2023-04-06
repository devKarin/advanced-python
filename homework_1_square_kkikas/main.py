from gui.gui import Gui

root = Gui()
root.create_set_of_inputs()
root.create_calculator_button()
root.create_close_button()
root.window.mainloop()

if __name__ == "__main__":
    print("Square application started.")