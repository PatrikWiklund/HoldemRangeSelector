import tkinter as tk

from range_selector import RangeSelector


# Just for testing the widget
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HoldemRangeSelector")
        self.rowconfigure(0, minsize=600, weight=1)
        self.columnconfigure(0, minsize=500, weight=1)
        range_selector_frame = RangeSelector(self, height=400, width=400)
        range_selector_frame.grid(row=0, column=0)


app = App()
app.mainloop()