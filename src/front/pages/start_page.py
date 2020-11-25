import tkinter as tk
import tkinter.ttk as ttk
import logging
from abc import ABC
import datetime

from src.back.user import User
from src.front.pages.base_page import BasePage
from src.front.utils import CustomButton


class StartPage(BasePage, ABC):
    """
    The starting page of the application.
    Contains a log-in form, as well as a registration form for new users.
    """

    def __init__(self, *args, **kwargs):
        BasePage.__init__(self, *args, **kwargs)
        self.build_gui()
        self.entries += [
            self.username_entry, self.password_entry, self.username_reg_entry, self.password_reg_entry,
            self.password_conf_entry, self.email_entry, self.first_name_entry, self.last_name_entry,
            self.card_nr_entry, self.card_type_spinbox, self.exp_y_spinbox, self.exp_m_spinbox, self.exp_d_spinbox,
        ]

    def on_log_in(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not self.master.log_in_user(username, password):
            self.login_btn.display_message('invalid', delay=1)

    def on_register(self):
        self.register_routine()

    def register_routine(self):
        try:
            # check passwords
            password = self.password_reg_entry.get().strip()
            password_conf = self.password_conf_entry.get().strip()
            if len(password) < User.MIN_PASS_LEN:
                raise ValueError(f'password must be at least {User.MIN_PASS_LEN} characters')
            if len(password) > User.MAX_PASS_LEN:
                raise ValueError(f'password must be at most {User.MAX_PASS_LEN} characters')
            if password != password_conf:
                raise ValueError('passwords don\'t match')
            # get other user data
            username = self.username_reg_entry.get().strip()
            first_name = self.first_name_entry.get().title().strip()
            last_name = self.last_name_entry.get().title().strip()
            email = self.email_entry.get().strip()
            # email is optional - check if it is specified
            if len(email) == 0:
                email = User.NO_EMAIL_MSG
            # check card number
            card_nr = self.card_nr_entry.get().strip()
            if not (len(card_nr) == 16 and card_nr.isalnum()):
                raise ValueError('card number must be 16 digits long')
            # check if all date spinboxes are specified
            exp_d = self.exp_d_spinbox.get()
            exp_m = self.exp_m_spinbox.get()
            exp_y = self.exp_y_spinbox.get()
            if len(exp_d) * len(exp_m) * len(exp_y) == 0:
                raise ValueError('incomplete date')
            # convert date to desired format
            expiration_date = f'{exp_d}-{exp_m}-{exp_y}'
            expiration_date = datetime.datetime.strptime(expiration_date, '%d-%m-%Y').strftime('%d %b %Y')
            # initial account balance is always 0
            account_balance = '0'
            card_type = self.card_type_spinbox.get()
            user_to_register = User(username, first_name, last_name, password, email, card_nr, expiration_date,
                                    account_balance, card_type)
            if user_to_register.has_empty_fields():
                raise ValueError('not all input fields completed')
            # try to load user data into database
            if not self.master.register_user(user_to_register):
                raise ValueError('unable to insert user into database')
        except ValueError as err:
            logging.error(f'Failed to register new user: {err}')
            self.reg_btn.display_message('error', delay=1)

    def build_gui(self):
        # log-in frame
        self.login_frame = tk.Frame(self)
        self.login_frame.config(background='#d3d3d3', height=self.winfo_height(), padx='50', width='600')
        self.login_frame.grid(column='1', row='0')
        filler_top = tk.Frame(self.login_frame)
        filler_top.grid(pady='120', columnspan='2')
        filler_bot = tk.Frame(self.login_frame)
        filler_bot.grid(row='4', pady='120', columnspan='2')
        # username and password fields and labels
        self.username_lbl = tk.Label(self.login_frame)
        self.username_lbl.config(background='#d3d3d3', font=BasePage.LIGHT_FONT, text='username:')
        self.username_lbl.grid(row='1', padx='15', pady='20', sticky='e')
        self.username_entry = tk.Entry(self.login_frame, font=BasePage.LIGHT_FONT)
        self.username_entry.config(relief='flat')
        self.username_entry.grid(column='1', padx='20', pady='20', row='1')
        self.username_entry.bind('<Return>', lambda event: self.on_log_in())
        self.password_lbl = tk.Label(self.login_frame)
        self.password_lbl.config(background='#d3d3d3', font=BasePage.LIGHT_FONT, text='password:')
        self.password_lbl.grid(padx='15', pady='20', row='2', sticky='e')
        self.password_entry = tk.Entry(self.login_frame, show='*', font=BasePage.LIGHT_FONT)
        self.password_entry.config(relief='flat')
        self.password_entry.grid(column='1', padx='20', pady='20', row='2')
        self.password_entry.bind('<Return>', lambda event: self.on_log_in())
        # 'log-in' button
        self.login_btn = CustomButton(self.login_frame)
        self.login_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.LIGHT_FONT,
                              relief='flat')
        self.login_btn.config(text='log in', width='10')
        self.login_btn.grid(column='0', columnspan='2', padx='5', pady='10', ipadx='5', ipady='3', row='3')
        self.login_btn.configure(command=self.on_log_in)

        # application info frame
        self.info_frame = tk.Frame(self, background='#c3c3c3')
        filler_top = tk.Frame(self.info_frame)
        filler_top.grid(pady='130', columnspan='2')
        filler_bot = tk.Frame(self.info_frame)
        filler_bot.grid(row='3', pady='136', columnspan='2')
        self.info_frame.config(height=self.winfo_height(), padx='30', width='400')
        self.info_frame.grid(column='0', row='0')
        self.app_info_msg = tk.Message(self.info_frame)
        self.app_info_msg.config(font='{Bahnschrift Light} 16 {bold}', takefocus=False,
                                 text='Welcome to iMusic.\nPlease log in to your account.',
                                 width='300', background='#c3c3c3')
        self.app_info_msg.grid(padx='50', row='1', sticky='w')
        self.description_msg = tk.Message(self.info_frame)
        self.description_msg.config(font='{Bahnschrift Light} 14 {}', takefocus=False,
                                    text='Browse and buy music from one of the largest databases in the world. ',
                                    width='300', background='#c3c3c3')
        self.description_msg.grid(column='0', padx='50', row='2', sticky='w')
        # registration frame
        self.register_frame = tk.Frame(self)
        self.register_frame.config(height='800', padx='70', width='400')
        self.register_frame.grid(column='2', pady='30', row='0')
        self.register_msg = tk.Message(self.register_frame)
        self.register_msg.config(font='{Bahnschrift Light} 16 {bold}', text='Don\'t have an account yet?\nRegister '
                                                                            'now for free!', width='350')
        self.register_msg.grid(columnspan='2', padx='5', pady='4')
        self.username_reg_lbl = tk.Label(self.register_frame)
        self.username_reg_lbl.config(font=BasePage.LIGHT_FONT, text='username:')
        self.username_reg_lbl.grid(padx='10', pady='5', row='1', sticky='e')
        self.first_name_lbl = tk.Label(self.register_frame)
        self.first_name_lbl.config(font=BasePage.LIGHT_FONT, text='first name:')
        self.first_name_lbl.grid(padx='10', pady='5', row='2', sticky='e')
        self.last_name_lbl = tk.Label(self.register_frame)
        self.last_name_lbl.config(font=BasePage.LIGHT_FONT, text='last name:')
        self.last_name_lbl.grid(padx='10', pady='5', row='3', sticky='e')
        self.password_reg_lbl = tk.Label(self.register_frame)
        self.password_reg_lbl.config(font=BasePage.LIGHT_FONT, text='password:')
        self.password_reg_lbl.grid(padx='10', pady='5', row='4', sticky='e')
        self.password_conf_lbl = tk.Label(self.register_frame)
        self.password_conf_lbl.config(font=BasePage.LIGHT_FONT, text='confirm password:')
        self.password_conf_lbl.grid(padx='10', pady='5', row='5', sticky='e')
        self.email_lbl = tk.Label(self.register_frame)
        self.email_lbl.config(font=BasePage.LIGHT_FONT, text='email:')
        self.email_lbl.grid(padx='10', pady='5', row='6', sticky='e')
        self.card_nr_lbl = tk.Label(self.register_frame)
        self.card_nr_lbl.config(font=BasePage.LIGHT_FONT, text='card number:')
        self.card_nr_lbl.grid(padx='10', pady='5', row='7', sticky='e')
        self.exp_date_lbl = tk.Label(self.register_frame)
        self.exp_date_lbl.config(font=BasePage.LIGHT_FONT, text='expiration date:')
        self.exp_date_lbl.grid(padx='10', pady='5', row='9', sticky='e')
        self.card_type_lbl = tk.Label(self.register_frame)
        self.card_type_lbl.config(font=BasePage.LIGHT_FONT, text='type:')
        self.card_type_lbl.grid(padx='10', pady='5', row='8', sticky='e')
        self.username_reg_entry = tk.Entry(self.register_frame, font=BasePage.LIGHT_FONT)
        self.username_reg_entry.config(relief='flat')
        self.username_reg_entry.grid(column='1', row='1')
        self.first_name_entry = tk.Entry(self.register_frame, font=BasePage.LIGHT_FONT)
        self.first_name_entry.config(relief='flat')
        self.first_name_entry.grid(column='1', row='2')
        self.last_name_entry = tk.Entry(self.register_frame, font=BasePage.LIGHT_FONT)
        self.last_name_entry.config(relief='flat')
        self.last_name_entry.grid(column='1', row='3')
        self.password_reg_entry = tk.Entry(self.register_frame, show='*', font=BasePage.LIGHT_FONT)
        self.password_reg_entry.config(relief='flat')
        self.password_reg_entry.grid(column='1', row='4')
        self.password_conf_entry = tk.Entry(self.register_frame, show='*', font=BasePage.LIGHT_FONT)
        self.password_conf_entry.config(relief='flat')
        self.password_conf_entry.grid(column='1', row='5')
        self.email_entry = tk.Entry(self.register_frame, font=BasePage.LIGHT_FONT)
        self.email_entry.config(relief='flat')
        self.email_entry.grid(column='1', row='6')
        self.card_nr_entry = tk.Entry(self.register_frame, font=BasePage.LIGHT_FONT)
        self.card_nr_entry.config(relief='flat')
        self.card_nr_entry.grid(column='1', row='7')
        self.card_type_spinbox = tk.Spinbox(self.register_frame)
        self.card_type_spinbox.config(font=BasePage.LIGHT_FONT, relief='flat', values='credit debit',
                                      width='10', state='readonly')
        self.card_type_spinbox.grid(column='1', row='8')
        self.exp_date_frame = ttk.Frame(self.register_frame)
        self.exp_y_spinbox = tk.Spinbox(self.exp_date_frame)
        year = tk.StringVar()
        self.exp_y_spinbox.config(font=BasePage.LIGHT_FONT, from_='2020', to='2099', increment='1',
                                  relief='flat', state='readonly')
        self.exp_y_spinbox.config(textvariable=year, width='5')
        self.exp_y_spinbox.grid(column='1', padx='5', row='0')
        self.exp_m_spinbox = tk.Spinbox(self.exp_date_frame)
        month = tk.StringVar()
        self.exp_m_spinbox.config(font=BasePage.LIGHT_FONT, from_='1', to='12', increment='1', relief='flat')
        self.exp_m_spinbox.config(textvariable=month, width='5', state='readonly')
        self.exp_m_spinbox.grid(column='1', padx='5', row='1')
        self.exp_d_spinbox = tk.Spinbox(self.exp_date_frame)
        day = tk.StringVar()
        self.exp_d_spinbox.config(font=BasePage.LIGHT_FONT, from_='1', to='31', increment='1', relief='flat')
        self.exp_d_spinbox.config(textvariable=day, width='5', state='readonly')
        self.exp_d_spinbox.grid(column='1', padx='5', row='2')
        self.year_lbl = tk.Label(self.exp_date_frame)
        self.year_lbl.config(font=BasePage.LIGHT_FONT, text='year:')
        self.year_lbl.grid(column='0', row='0', sticky='e')
        self.month_lbl = tk.Label(self.exp_date_frame)
        self.month_lbl.config(font=BasePage.LIGHT_FONT, text='month:')
        self.month_lbl.grid(column='0', row='1', sticky='e')
        self.day_lbl = tk.Label(self.exp_date_frame)
        self.day_lbl.config(font=BasePage.LIGHT_FONT, text='day:')
        self.day_lbl.grid(column='0', row='2', sticky='e')
        self.exp_date_frame.config(height='200', width='400')
        self.exp_date_frame.grid(column='1', padx='5', pady='5', row='9')
        # 'register' button
        self.reg_btn = CustomButton(self.register_frame)
        self.reg_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.LIGHT_FONT,
                            relief='flat')
        self.reg_btn.config(text='register', width='10')
        self.reg_btn.configure(command=self.on_register)
        self.reg_btn.grid(column='0', columnspan='2', padx='5', pady='20', ipadx='5', ipady='3', row='10')
