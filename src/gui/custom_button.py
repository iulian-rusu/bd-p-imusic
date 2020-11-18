import tkinter as tk


class CustomButton(tk.Button):
    """
    Custom tk.Button that changes background when hovered.
    Adapted from https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change.
    """
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.default_bg = self["background"]

    def on_enter(self, event):
        self.default_bg = self["background"]
        if self['state'] == 'normal':
            self['background'] = self['activebackground']

    def on_leave(self, event):
        if self['state'] == 'normal':
            self['background'] = self.default_bg

    def config(self, *args, **kwargs):
        if 'background' in kwargs.keys():
            self.default_bg = kwargs['background']
        tk.Button.config(self, *args, **kwargs)
