import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, lambdify


class FunctionPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("Function Plotter")

        self.create_widgets()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

    def create_widgets(self):
        ttk.Label(self.master, text="Function:").grid(row=0, column=0, padx=10, pady=5)
        self.expression_entry = ttk.Entry(self.master)
        self.expression_entry.grid(row=0, column=1, padx=10, pady=5)
        self.expression_entry.insert(0, "x**2")

        self.x_min_label = ttk.Label(self.master, text="X Min:")
        self.x_min_label.grid(row=1, column=0, padx=10, pady=5)
        self.x_min_entry = ttk.Entry(self.master)
        self.x_min_entry.grid(row=1, column=1, padx=10, pady=5)
        self.x_min_entry.insert(0, "-10")

        self.x_max_label = ttk.Label(self.master, text="X Max:")
        self.x_max_label.grid(row=2, column=0, padx=10, pady=5)
        self.x_max_entry = ttk.Entry(self.master)
        self.x_max_entry.grid(row=2, column=1, padx=10, pady=5)
        self.x_max_entry.insert(0, "10")

        self.color_label = ttk.Label(self.master, text="Color:")
        self.color_label.grid(row=3, column=0, padx=10, pady=5)
        self.color_combobox = ttk.Combobox(self.master, values=["blue", "red", "green", "yellow", "orange"])
        self.color_combobox.grid(row=3, column=1, padx=10, pady=5)
        self.color_combobox.set("blue")

        self.units_label = ttk.Label(self.master, text="Units:")
        self.units_label.grid(row=4, column=0, padx=10, pady=5)
        self.units_combobox = ttk.Combobox(self.master, values=["rad", "deg"])
        self.units_combobox.grid(row=4, column=1, padx=10, pady=5)
        self.units_combobox.set("deg")

        self.save_button = ttk.Button(self.master, text="Save as PNG", command=self.save_graph)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

        ttk.Button(self.master, text="Save as PNG", command=self.save_graph).grid(row=5, column=0, columnspan=2,
                                                                                  pady=10)
        ttk.Button(self.master, text="Plot Function", command=self.plot).grid(row=6, column=0, columnspan=2, pady=10)

    def plot(self):
        try:
            x = symbols('x')
            expression = self.expression_entry.get()
            func = lambdify(x, expression, 'numpy')

            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
            color = self.color_combobox.get()
            units = self.units_combobox.get()

            if units == "deg":
                x_min = np.deg2rad(x_min)
                x_max = np.deg2rad(x_max)

            x_values = np.linspace(x_min, x_max, 400)
            y_values = func(x_values)

            self.ax.clear()
            self.ax.plot(x_values, y_values, label=f"$y = {expression}$", color=color)
            self.ax.grid()
            self.ax.legend()

            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Invalid values. Error: {str(e)}")

    def save_graph(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if filename:
                self.figure.savefig(filename)
                messagebox.showinfo("Success", "Graph saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save. Error: {str(e)}")


def main():
    root = tk.Tk()
    app = FunctionPlotter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
