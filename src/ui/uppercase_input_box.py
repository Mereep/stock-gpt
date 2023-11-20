from tkinter import simpledialog
import tkinter as tk


def uppercase_input_box(prompt):
    def to_uppercase(*args):
        value = entry_var.get()
        entry_var.set(value.upper())

    root = tk.Tk()
    root.withdraw()

    entry_var = tk.StringVar()
    entry_var.trace("w", to_uppercase)

    result = simpledialog.askstring(prompt, entry_var, parent=root)

    if result:
        return result.upper()
    else:
        return None
