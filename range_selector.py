import tkinter as tk

CARD_RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


class RangeSelector(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.selected_hands = []
        self.button_grid = [["" for i in range(13)] for j in range(13)]
        self.select_mode = True

        for i, card_one in enumerate(CARD_RANKS):
            for j, card_two in enumerate(CARD_RANKS):
                # The card with highest rank should be printed first
                # plus adding suit (s) or off-suit(o) and backgroundcolor
                if i < j:
                    hand = card_one + card_two + "o"
                    bg = "light pink"
                elif j == i:
                    hand = card_one + card_two
                    bg = "SpringGreen2"
                else:
                    hand = card_two + card_one + "s"
                    bg = "CadetBlue1"

                # Creating "virtual 1px image" to be able to resize button widgets
                img = tk.PhotoImage(width=1, height=1)
                button = ClickAndDragButton(
                    self,
                    text=hand,
                    bg=bg,
                    font=("Helvetica", 10),
                    image=img,
                    compound="c",
                    height=25,
                    width=25,
                )
                button.grid(row=j, column=i, sticky="nswe", pady=1, padx=1)
                # Need to create a reference to img else garbagecollector swollow it
                button.image = img
                button.original_bg = bg

                self.button_grid[j][i] = button

        self.bind_all("<Button-1>", self.mouse_down)
        self.bind_all("<ButtonRelease-1>", self.mouse_up)
        self.bind_all("<B1-Motion>", self.mouse_motion)

        # The click and drag functionality is inspired by "anonymoose" solution
        # https://stackoverflow.com/questions/46865046/tkinter-how-can-you-drag-across-buttons?answertab=active#tab-top

    def mouse_down(self, e):
        if e.widget["relief"] == "flat":
            self.select_mode = True
        else:
            self.select_mode = False
        self.update_containing_button(e)

    def mouse_up(self, e):
        for row in self.button_grid:
            for button in row:
                button.mouse_up()

    def mouse_motion(self, e):
        self.update_containing_button(e)

    def update_containing_button(self, e):
        for row in self.button_grid:
            for button in row:
                if self.winfo_containing(e.x_root, e.y_root) is button:
                    button.mouse_enter()


class ClickAndDragButton(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.already_changed = False

    def change(self):
        if (
            self.master.select_mode
            and not self.already_changed
            and self["relief"] == "flat"
        ):
            self.configure(bd=1, relief="raised", bg="yellow")
            self.master.selected_hands.append(self["text"])
            self.already_changed = True
        elif (
            not self.master.select_mode
            and not self.already_changed
            and self["relief"] == "raised"
        ):
            self.configure(relief="flat", bg=self.original_bg)
            self.master.selected_hands.remove(self["text"])
            self.already_changed = True

    def mouse_enter(self):
        if not self.already_changed:
            self.change()

    def mouse_up(self):
        self.already_changed = False