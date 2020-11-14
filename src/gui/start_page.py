import tkinter as tk
import tkinter.ttk as ttk
import logging
from abc import ABC

from src.gui.base_page import BasePage


class StartPage(BasePage, ABC):
    """
        The starting page of the application.
        Contains a log-in form, as well as a registration form for new users.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_gui()

    def on_log_in(self):
        logging.info("User logged in")
        self.master.show_page('home')

    def on_register(self):
        logging.info("New user registered")
        self.master.show_page('home')

    @staticmethod
    def get_wnd_title() -> str:
        return 'Welcome to iMusic'

    def build_gui(self):
        # log-in frame
        self.login_frame = tk.Frame(self)
        self.login_frame.config(background='#d3d3d3', height=self.winfo_height(), padx='100', width='600')
        self.login_frame.grid(column='1', pady='350', row='0')
        self.username_lbl = tk.Label(self.login_frame)
        self.username_lbl.config(background='#d3d3d3', font=BasePage.font('12'), text='username:')
        self.username_lbl.grid(padx='15', pady='20', sticky='e')
        self.username_entry = tk.Entry(self.login_frame, font=BasePage.font('12'))
        self.username_entry.config(relief='flat')
        self.username_entry.grid(column='1', padx='20', pady='20', row='0')
        self.password_lbl = tk.Label(self.login_frame)
        self.password_lbl.config(background='#d3d3d3', font=BasePage.font('12'), text='password:')
        self.password_lbl.grid(padx='15', pady='20', row='1', sticky='e')
        self.password_entry = tk.Entry(self.login_frame, show=".", font=BasePage.font('12', 'bold'))
        self.password_entry.config(relief='flat')
        self.password_entry.grid(column='1', padx='20', pady='20', row='1')
        # log-in button
        self.login_btn = tk.Button(self.login_frame)
        self.login_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.font('12'), relief='flat')
        self.login_btn.config(text='log in')
        self.login_btn.grid(column='0', columnspan='2', padx='5', pady='10', row='2')
        self.login_btn.configure(command=self.on_log_in)
        # application info frame
        self.info_frame = tk.Frame(self)
        self.info_frame.config(height=self.winfo_height(), padx='100', width='400')
        self.info_frame.grid(column='0', pady='100', row='0')
        self.app_info_msg = tk.Message(self.info_frame)
        self.app_info_msg.config(font=BasePage.font('16', 'bold'), takefocus=False,
                                 text='Welcome to iMusic.\nPlease log into your account or register a new one.',
                                 width='300')
        self.app_info_msg.grid(padx='50')
        self.description_msg = tk.Message(self.info_frame)
        self.description_msg.config(font=BasePage.font('14'), takefocus=False,
                                    text='Browse and buy music from one of the largest databases in the world. ',
                                    width='300')
        self.description_msg.grid(column='0', padx='50', row='1')
        # registration frame
        self.register_frame = tk.Frame(self)
        self.register_frame.config(height='800', padx='100', width='400')
        self.register_frame.grid(column='2', pady='100', row='0')
        self.register_msg = tk.Message(self.register_frame)
        self.register_msg.config(font=BasePage.font('16', 'bold'), text='Don\'t have an account yet?\nRegister now for '
                                                                        'free!', width='350')
        self.register_msg.grid(columnspan='2', padx='5', pady='5')
        self.username_reg_lbl = tk.Label(self.register_frame)
        self.username_reg_lbl.config(font=BasePage.font('12'), text='username:')
        self.username_reg_lbl.grid(padx='10', pady='5', row='1', sticky='e')
        self.first_name_lbl = tk.Label(self.register_frame)
        self.first_name_lbl.config(font=BasePage.font('12'), text='first name:')
        self.first_name_lbl.grid(padx='10', pady='5', row='2', sticky='e')
        self.last_name_lbl = tk.Label(self.register_frame)
        self.last_name_lbl.config(font=BasePage.font('12'), text='last name:')
        self.last_name_lbl.grid(padx='10', pady='5', row='3', sticky='e')
        self.password_reg_lbl = tk.Label(self.register_frame)
        self.password_reg_lbl.config(font=BasePage.font('12'), text='password:')
        self.password_reg_lbl.grid(padx='10', pady='5', row='4', sticky='e')
        self.password_conf_lbl = tk.Label(self.register_frame)
        self.password_conf_lbl.config(font=BasePage.font('12'), text='confirm password:')
        self.password_conf_lbl.grid(padx='10', pady='5', row='5', sticky='e')
        self.email_lbl = tk.Label(self.register_frame)
        self.email_lbl.config(font=BasePage.font('12'), text='email:')
        self.email_lbl.grid(padx='10', pady='5', row='6', sticky='e')
        self.card_nr_lbl = tk.Label(self.register_frame)
        self.card_nr_lbl.config(font=BasePage.font('12'), text='card number:')
        self.card_nr_lbl.grid(padx='10', pady='5', row='7', sticky='e')
        self.exp_date_lbl = tk.Label(self.register_frame)
        self.exp_date_lbl.config(font=BasePage.font('12'), text='expiration date:')
        self.exp_date_lbl.grid(padx='10', pady='5', row='9', sticky='e')
        self.card_type_lbl = tk.Label(self.register_frame)
        self.card_type_lbl.config(font=BasePage.font('12'), text='type:')
        self.card_type_lbl.grid(padx='10', pady='5', row='8', sticky='e')
        self.username_reg_entry = tk.Entry(self.register_frame, font=BasePage.font('12'))
        self.username_reg_entry.config(relief='flat')
        self.username_reg_entry.grid(column='1', row='1')
        self.first_name_entry = tk.Entry(self.register_frame, font=BasePage.font('12'))
        self.first_name_entry.config(relief='flat')
        self.first_name_entry.grid(column='1', row='2')
        self.last_name_entry = tk.Entry(self.register_frame, font=BasePage.font('12'))
        self.last_name_entry.config(relief='flat')
        self.last_name_entry.grid(column='1', row='3')
        self.password_reg_entry = tk.Entry(self.register_frame, show=".", font=BasePage.font('12', 'bold'))
        self.password_reg_entry.config(relief='flat')
        self.password_reg_entry.grid(column='1', row='4')
        self.password_conf_entry = tk.Entry(self.register_frame, show=".", font=BasePage.font('12', 'bold'))
        self.password_conf_entry.config(relief='flat')
        self.password_conf_entry.grid(column='1', row='5')
        self.email_entry = tk.Entry(self.register_frame, font=BasePage.font('12'))
        self.email_entry.config(relief='flat')
        self.email_entry.grid(column='1', row='6')
        self.card_nr_entry = tk.Entry(self.register_frame, font=BasePage.font('12'))
        self.card_nr_entry.config(relief='flat')
        self.card_nr_entry.grid(column='1', row='7')
        self.card_type_spinbox = tk.Spinbox(self.register_frame)
        self.card_type_spinbox.config(font=BasePage.font('12'), relief='flat', values='credit debit', width='10')
        self.card_type_spinbox.grid(column='1', row='8')
        self.exp_date_frame = ttk.Frame(self.register_frame)
        self.exp_y_spinbox = tk.Spinbox(self.exp_date_frame)
        year = tk.StringVar()
        self.exp_y_spinbox.config(font=BasePage.font('12'), from_='2020', to='2099', increment='1', relief='flat')
        self.exp_y_spinbox.config(textvariable=year, width='5')
        self.exp_y_spinbox.grid(column='1', padx='5', row='0')
        self.exp_m_spinbox = tk.Spinbox(self.exp_date_frame)
        month = tk.StringVar()
        self.exp_m_spinbox.config(font=BasePage.font('12'), from_='1', to='12', increment='1', relief='flat')
        self.exp_m_spinbox.config(textvariable=month, width='5')
        self.exp_m_spinbox.grid(column='1', padx='5', row='1')
        self.exp_d_spinbox = tk.Spinbox(self.exp_date_frame)
        day = tk.StringVar()
        self.exp_d_spinbox.config(font=BasePage.font('12'), from_='1', to='31', increment='1', relief='flat')
        self.exp_d_spinbox.config(textvariable=day, width='5')
        self.exp_d_spinbox.grid(column='1', padx='5', row='2')
        self.year_lbl = tk.Label(self.exp_date_frame)
        self.year_lbl.config(font=BasePage.font('12'), text='year:')
        self.year_lbl.grid(column='0', row='0', sticky='e')
        self.month_lbl = tk.Label(self.exp_date_frame)
        self.month_lbl.config(font=BasePage.font('12'), text='month:')
        self.month_lbl.grid(column='0', row='1', sticky='e')
        self.day_lbl = tk.Label(self.exp_date_frame)
        self.day_lbl.config(font=BasePage.font('12'), text='day:')
        self.day_lbl.grid(column='0', row='2', sticky='e')
        self.exp_date_frame.config(height='200', width='400')
        self.exp_date_frame.grid(column='1', padx='5', pady='5', row='9')
        # register button
        self.reg_btn = tk.Button(self.register_frame)
        self.reg_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.font('12'), relief='flat')
        self.reg_btn.config(text='register')
        self.reg_btn.configure(command=self.on_register)
        self.reg_btn.grid(column='0', columnspan='2', padx='5', pady='10', row='10')
