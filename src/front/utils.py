import threading
import time
import tkinter as tk


def config_after_delay(delay: float, *components, **kwargs, ):
    def wrapped():
        time.sleep(delay)
        for component in components:
            component.config(**kwargs)
    threading.Thread(target=wrapped).start()


class CustomButton(tk.Button):
    """
    Custom tk.Button that changes background when hovered.
    Adapted from https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change.
    """

    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.bind("<Enter>", lambda event: self.on_enter())
        self.bind("<Leave>", lambda event: self.on_leave())
        self.default_bg = self["background"]

    def on_enter(self):
        if self['state'] == 'normal':
            self.default_bg = self["background"]
            self['background'] = self['activebackground']

    def on_leave(self):
        if self['state'] == 'normal':
            self['background'] = self.default_bg

    def config(self, *args, **kwargs):
        if 'background' in kwargs.keys():
            self.default_bg = kwargs['background']
        tk.Button.config(self, *args, **kwargs)

    def display_message(self, msg: str, delay: float, background='#ff9b9b', final_state='normal'):
        normal_msg = self['text']
        prev_bg = self.default_bg
        self.config(text=msg, background=background, state='disabled')
        config_after_delay(delay, self, text=normal_msg, background=prev_bg, state=final_state)
