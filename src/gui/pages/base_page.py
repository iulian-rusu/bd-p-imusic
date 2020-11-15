import tkinter as tk
import abc


class BasePage(tk.Frame, metaclass=abc.ABCMeta):
    """
        Base abstract class for all GUI pages.
        Sets the frame dimensions and adds the frame to the master grid.
    """
    LIGHT_FONT = '{Bahnschrift Light} 12 {}'
    BOLD_FONT = '{Bahnschrift} 12 {}'
    UNDERLINED_BOLD_FONT = '{Bahnschrift} 12 {}'

    def __init__(self, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.grid(row=0, column=0, sticky="nsew")
        self.config(height=self.winfo_height(), width=self.winfo_width())
        self.config(height=self.winfo_height(), width=self.winfo_width())

    def show(self, aboveThis=None):
        self.winfo_toplevel().title(self.title)
        super().tkraise(aboveThis)

    @abc.abstractmethod
    def build_gui(self):
        pass
