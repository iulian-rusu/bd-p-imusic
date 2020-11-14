import tkinter as tk
import abc


class BasePage(tk.Frame, metaclass=abc.ABCMeta):
    """
        Base abstract class for all GUI pages.
        Sets the frame dimensions and adds the frame to the master grid.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.config(height=self.winfo_height(), width=self.winfo_width())
        self.config(height=self.winfo_height(), width=self.winfo_width())

    def show(self, wnd_title: str, aboveThis=None):
        self.winfo_toplevel().title(wnd_title)
        super().tkraise(aboveThis)

    @staticmethod
    def font(size: str, style: str = '') -> str:
        return f'{"{Sawasdee}"} {size} {"{"}{style}{"}"}'

    @abc.abstractmethod
    def build_gui(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_wnd_title() -> str:
        pass
