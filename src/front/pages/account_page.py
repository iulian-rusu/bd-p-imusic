import logging
import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC

from src.back.input_processing import sanitize
from src.back.transaction_processing import Transaction
from src.front.pages.base_page import BasePage
from src.front.table_views.table_view import TableView
from src.front.utils import CustomButton
from src.front.table_views.transaction_view import TransactionView


class AccountPage(BasePage, ABC):
    """
    The user account page of the application.
    Contains the user's personal information and all purhcased music albums.
    """

    def __init__(self, *args, **kwargs):
        BasePage.__init__(self, *args, **kwargs)
        self.build_gui()
        # group entries by responsibilities
        self.personal_entries = [self.username_entry, self.first_name_entry, self.last_name_entry, self.email_entry,
                                 self.old_pass_entry, self.new_pass_entry, self.new_pass_conf_entry]
        self.payment_entries = [self.amount_entry, self.verif_entry]
        self.entries += self.personal_entries
        self.entries += self.payment_entries
        self.entries += [self.card_nr_entry, self.card_type_entry, self.exp_date_entry]
        # remember widgets that are toggled by button presses
        self.personal_toggled_lbls = [
            self.password_lbl, self.old_password_lbl, self.new_password_lbl, self.new_password_conf_lbl,
            self.old_password_lbl]
        self.payment_toggled_lbls = [
            self.add_funds_lbl, self.amount_lbl, self.verif_lbl, self.validate_btn]
        self.is_editing_personal_info = False
        self.selected_transaction = None
        self.current_view_btn = None

    def reset(self):
        super().reset()
        # hide widgets that need to be toggled
        for label in self.personal_toggled_lbls:
            label.config(state='disabled')
        for label in self.payment_toggled_lbls:
            label.config(state='disabled')
        self.load_account_data()
        for entry in self.entries:
            entry.config(state='readonly')
        self.account_balance_lbl.config(text=f"balance: ${self.master.user.account_balace / 100.0}")
        self.on_personal_info_view()

    def on_home(self):
        self.master.show_page('home')

    def on_my_albums_view(self):
        self.set_current_view(self.my_albums_btn)

    def on_personal_info_view(self):
        self.set_current_view(self.account_info_btn)

    def on_log_out(self):
        self.master.user = None
        self.master.show_page('start')

    def on_refund(self):
        if not self.selected_transaction:
            return
        if self.master.refund_transaction(self.selected_transaction.tr_id, self.selected_transaction.amount):
            self.account_balance_lbl.config(text=f"balance: ${self.master.user.account_balace / 100.0}")
            self.transaction_view.delete_selected_row()
            self.selected_transaction = None
            self.refund_btn.config(state='disabled', background='#59c872')
        else:
            self.refund_btn.display_message('error', delay=0.5, final_state='disabled')

    def on_album_select(self, event):
        if self.refund_btn['text'] != 'refund album':
            return
        transaction_data = self.transaction_view.get_selected_transaction_data(event)
        if transaction_data:
            self.selected_transaction = Transaction.TransactionData(*transaction_data)
            self.refund_btn.config(state='normal')
        else:
            self.refund_btn.config(state='disabled')

    def on_add_funds(self):
        for label in self.payment_toggled_lbls:
            label.config(state='normal')
        for entry in self.payment_entries:
            entry.config(state='normal')

    def on_validate(self):
        try:
            amount = self.amount_entry.get().strip()
            verif = self.verif_entry.get().strip()
            # verification code not actually implemented, just a placeholder mechanism
            if not verif.isnumeric():
                raise ValueError("varification code must be numeric")
            # update funds in database
            if self.master.add_user_funds(amount):
                self.validate_btn.display_message('success', delay=0.5, background='#59c872', final_state='disabled')
                self.account_balance_lbl.config(text=f"balance: ${self.master.user.account_balace / 100.0}")
            else:
                raise ValueError('databases error')
        except (ValueError, OverflowError) as err:
            logging.error(f"Failed to add funds to account: {err}")
            self.validate_btn.display_message('error', delay=0.5, final_state='disabled')
        for label in self.payment_toggled_lbls:
            label.config(state='disabled')
        for entry in self.payment_entries:
            entry.delete(0, 'end')
            entry.config(state='disabled')

    def on_personal_info_edit(self):
        if not self.is_editing_personal_info:
            self.is_editing_personal_info = True
            for entry in self.personal_entries:
                entry.config(state='normal')
            for label in self.personal_toggled_lbls:
                label.config(state='normal')
        else:
            self.is_editing_personal_info = False
            self.save_personal_info()

    def set_current_view(self, new_btn: CustomButton):
        if self.current_view_btn:
            self.current_view_btn.config(font=BasePage.LIGHT_FONT, background='#d1d1d1')
        new_btn.config(font=BasePage.UNDERLINED_BOLD_FONT, background='#c1c1c1')
        self.current_view_btn = new_btn
        current_view = self.views[self.current_view_btn]
        if isinstance(current_view, TableView):
            self.refund_btn.tkraise()
            username_key = sanitize(self.master.user.username)
            current_view.load_searched_rows(username_key, connection=self.master.db_connection)
        else:
            self.add_funds_btn.tkraise()
        current_view.tkraise()

    def save_personal_info(self):
        user = self.master.user
        # get user input data
        username, first_name, last_name, email, old_pass, new_pass, new_pass_conf \
            = [e.get().strip() for e in self.personal_entries]
        first_name = first_name.title()
        last_name = last_name.title()
        email = email.lower()
        try:
            if len(old_pass):
                # attempt to change user password
                if not user.match_password(old_pass):
                    raise ValueError("old password incorrect")
                if len(new_pass) < user.MIN_PASS_LEN or new_pass != new_pass_conf:
                    raise ValueError("new passwords don't match")
            elif len(new_pass):
                raise ValueError("old password required to change password")
            # update in database
            if self.master.update_user(username, first_name, last_name, email, new_pass):
                logging.info("Successfully updated user data")
            else:
                raise RuntimeError('database could not update data')
        except (ValueError, RuntimeError) as err:
            logging.error(f"Failed to edit personal data: {err}")
            self.edit_personal_info_btn.display_message('error', delay=0.5)
        self.reset()

    def load_account_data(self):
        user = self.master.user
        self.username_entry.insert(0, user.username)
        self.first_name_entry.insert(0, user.first_name)
        self.last_name_entry.insert(0, user.last_name)
        self.email_entry.insert(0, user.email)
        self.card_nr_entry.insert(0, user.card_nr)
        self.card_type_entry.insert(0, user.card_type)
        self.exp_date_entry.insert(0, user.expiration_date)

    def build_gui(self):
        # top menu
        self.top_menu_frame = tk.Frame(self)
        # 'log out' button
        self.log_out_btn = CustomButton(self.top_menu_frame)
        self.log_out_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.LIGHT_FONT,
                                relief='flat')
        self.log_out_btn.config(text='log out', command=self.on_log_out)
        self.log_out_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                               width='200', x='0', y='0')
        # 'add funds' button
        self.add_funds_btn = CustomButton(self.top_menu_frame)
        self.add_funds_btn.config(activebackground='#39a852', background='#59c872',
                                  font=BasePage.LIGHT_FONT, relief='flat')
        self.add_funds_btn.config(text='add funds', command=self.on_add_funds)
        self.add_funds_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.85714', rely='0.0',
                                 width='200', x='0', y='0')
        # 'refund' button
        self.refund_btn = CustomButton(self.top_menu_frame)
        self.refund_btn.config(activebackground='#39a852', background='#59c872',
                               font=BasePage.LIGHT_FONT, relief='flat')
        self.refund_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.85714', rely='0.0',
                              width='200', x='0', y='0')
        self.refund_btn.config(text='refund album', state='disabled', command=self.on_refund)
        # 'account balance' label
        self.account_balance_lbl = ttk.Label(self.top_menu_frame)
        self.account_balance_lbl.config(background='#d1d1d1', font=BasePage.LIGHT_FONT, foreground='#515151',
                                        text='balance: $0')
        self.account_balance_lbl.place(anchor='nw', height='40', relx='0.68', width='150', x='0', y='0')
        self.top_menu_frame.config(background='#d1d1d1', height='40', width='1400')
        self.top_menu_frame.grid()
        # bottom menu
        self.bottom_menu_frame = tk.Frame(self)
        # 'account info' button
        self.account_info_btn = CustomButton(self.bottom_menu_frame)
        self.account_info_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                     font=BasePage.LIGHT_FONT, relief='flat')
        self.account_info_btn.config(state='normal', text='account info', command=self.on_personal_info_view)
        self.account_info_btn.place(anchor='nw', height='40', relx='0.142857', width='600', x='0', y='0')
        # 'my albums' button
        self.my_albums_btn = CustomButton(self.bottom_menu_frame)
        self.my_albums_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                  font=BasePage.LIGHT_FONT, relief='flat')
        self.my_albums_btn.config(text='my albums', command=self.on_my_albums_view)
        self.my_albums_btn.place(anchor='nw', height='40', relx='0.57142857', width='600', x='0', y='0')
        # 'home' button
        self.home_btn = CustomButton(self.bottom_menu_frame)
        self.home_btn.config(activebackground='#9a9a9a', background='#b1b1b1',
                             font=BasePage.LIGHT_FONT, relief='flat')
        self.home_btn.config(text='home', command=self.on_home)
        self.home_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                            width='200', x='0', y='0')
        self.bottom_menu_frame.config(background='#c1c1c1', height='40', width='1400')
        self.bottom_menu_frame.grid(column='0', row='2')
        # content frame
        self.content_frame = tk.Frame(self)
        self.content_frame.config(height='591', width='1400')
        self.content_frame.grid(column='0', row='1')
        # transactions view
        self.transaction_view = TransactionView(master=self.content_frame)
        self.transaction_view.place(anchor='nw', height='591', width='1400', x='0', y='0')
        self.transaction_view.bind('<Button 1>', self.on_album_select)
        # account view
        self.account_info_frame = tk.Frame(self.content_frame)
        self.account_info_frame.config(width='1400', height='591')
        self.account_info_frame.grid()
        # build view dictionary
        self.views = {
            self.account_info_btn: self.account_info_frame,
            self.my_albums_btn: self.transaction_view
        }
        # personal info
        self.personal_info_frame = tk.LabelFrame(self.account_info_frame)
        self.label_frame = tk.Frame(self.personal_info_frame)
        self.username_lbl = tk.Label(self.label_frame)
        self.username_lbl.config(font=BasePage.LIGHT_FONT, text='username:')
        self.username_lbl.place(anchor='ne', relx='1.0', x='0', y='0')
        self.first_name_lbl = tk.Label(self.label_frame)
        self.first_name_lbl.config(font=BasePage.LIGHT_FONT, text='first name:')
        self.first_name_lbl.place(anchor='ne', relx='1.0', rely='0.1', x='0', y='0')
        self.last_name_lbl = tk.Label(self.label_frame)
        self.last_name_lbl.config(font=BasePage.LIGHT_FONT, text='last name:')
        self.last_name_lbl.place(anchor='ne', relx='1.0', rely='0.2', x='0', y='0')
        self.email_lbl = tk.Label(self.label_frame)
        self.email_lbl.config(font=BasePage.LIGHT_FONT, text='email:')
        self.email_lbl.place(anchor='ne', relx='1.0', rely='0.3', x='0', y='0')
        self.password_lbl = tk.Label(self.label_frame)
        self.password_lbl.config(font=BasePage.BOLD_FONT, state='normal', text='change your password')
        self.password_lbl.place(anchor='ne', relx='1', rely='0.4', x='0', y='0')
        self.old_password_lbl = tk.Label(self.label_frame)
        self.old_password_lbl.config(font=BasePage.LIGHT_FONT, text='old password:')
        self.old_password_lbl.place(anchor='ne', relx='1.0', rely='0.5', x='0', y='0')
        self.new_password_lbl = tk.Label(self.label_frame)
        self.new_password_lbl.config(font=BasePage.LIGHT_FONT, text='new password:')
        self.new_password_lbl.place(anchor='ne', relx='1.0', rely='0.6', x='0', y='0')
        self.new_password_conf_lbl = tk.Label(self.label_frame)
        self.new_password_conf_lbl.config(font=BasePage.LIGHT_FONT, text='confirm new password:')
        self.new_password_conf_lbl.place(anchor='ne', relx='1.0', rely='0.7', x='0', y='0')
        self.label_frame.config(height='200', width='200')
        self.label_frame.place(anchor='nw', height='450', relx='0.02', rely='0.05', width='200', x='0', y='0')
        self.entry_frame = tk.Frame(self.personal_info_frame)
        self.username_entry = tk.Entry(self.entry_frame)
        self.username_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.username_entry.place(anchor='nw', width='300', x='0', y='0')
        self.first_name_entry = tk.Entry(self.entry_frame)
        self.first_name_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.first_name_entry.place(anchor='nw', rely='0.1', width='300', x='0', y='0')
        self.last_name_entry = tk.Entry(self.entry_frame)
        self.last_name_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.last_name_entry.place(anchor='nw', rely='0.2', width='300', x='0', y='0')
        self.email_entry = tk.Entry(self.entry_frame)
        self.email_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.email_entry.place(anchor='nw', rely='0.3', width='300', x='0', y='0')
        self.old_pass_entry = tk.Entry(self.entry_frame)
        self.old_pass_entry.config(relief='flat', font=BasePage.LIGHT_FONT, show='*')
        self.old_pass_entry.place(anchor='nw', rely='0.5', width='300', x='0', y='0')
        self.new_pass_entry = tk.Entry(self.entry_frame)
        self.new_pass_entry.config(relief='flat', font=BasePage.LIGHT_FONT, show='*')
        self.new_pass_entry.place(anchor='nw', rely='0.6', width='300', x='0', y='0')
        self.new_pass_conf_entry = tk.Entry(self.entry_frame)
        self.new_pass_conf_entry.config(relief='flat', font=BasePage.LIGHT_FONT, show='*')
        self.new_pass_conf_entry.place(anchor='nw', rely='0.7', width='300', x='0', y='0')
        self.edit_personal_info_btn = CustomButton(self.entry_frame)
        self.edit_personal_info_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                           font=BasePage.LIGHT_FONT, relief='flat')
        self.edit_personal_info_btn.config(text='edit personal details', command=self.on_personal_info_edit)
        self.edit_personal_info_btn.place(anchor='nw', relx='0.15', rely='0.85', width='200', x='0', y='0')
        self.entry_frame.config(height='200', width='200')
        self.entry_frame.place(anchor='ne', height='450', relx='1.0', rely='0.05', width='350', x='0', y='0')
        self.personal_info_frame.config(borderwidth='2', font=BasePage.LIGHT_FONT, height='200',
                                        text='personal info')
        self.personal_info_frame.config(width='200')
        self.personal_info_frame.place(anchor='nw', height='500', relx='0.05', rely='0.07', width='600', x='0', y='0')
        # payment info
        self.payment_info_frame = tk.LabelFrame(self.account_info_frame)
        self.payment_label_frame = tk.Frame(self.payment_info_frame)
        self.card_nr_lbl = tk.Label(self.payment_label_frame)
        self.card_nr_lbl.config(font=BasePage.LIGHT_FONT, text='card number:')
        self.card_nr_lbl.place(anchor='ne', relx='1.0', x='0', y='0')
        self.exp_date_lbl = tk.Label(self.payment_label_frame)
        self.exp_date_lbl.config(font=BasePage.LIGHT_FONT, text='expiration date:')
        self.exp_date_lbl.place(anchor='ne', relx='1.0', rely='0.1', x='0', y='0')
        self.card_type_lbl = tk.Label(self.payment_label_frame)
        self.card_type_lbl.config(font=BasePage.LIGHT_FONT, text='card type:')
        self.card_type_lbl.place(anchor='ne', relx='1.0', rely='0.2', x='0', y='0')
        self.add_funds_lbl = tk.Label(self.payment_label_frame)
        self.add_funds_lbl.config(font=BasePage.BOLD_FONT, state='normal', text='add money to account')
        self.add_funds_lbl.place(anchor='ne', relx='1', rely='0.5', x='0', y='0')
        self.amount_lbl = tk.Label(self.payment_label_frame)
        self.amount_lbl.config(font=BasePage.LIGHT_FONT, text='USD amount:')
        self.amount_lbl.place(anchor='ne', relx='1.0', rely='0.6', x='0', y='0')
        self.verif_lbl = tk.Label(self.payment_label_frame)
        self.verif_lbl.config(font=BasePage.LIGHT_FONT, text='verification code:')
        self.verif_lbl.place(anchor='ne', relx='1.0', rely='0.7', x='0', y='0')
        self.payment_label_frame.config(height='200', width='200')
        self.payment_label_frame.place(anchor='nw', height='450', relx='0.02', rely='0.05', width='200', x='0', y='0')
        self.payment_entry_frame = tk.Frame(self.payment_info_frame)
        self.card_nr_entry = tk.Entry(self.payment_entry_frame)
        self.card_nr_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.card_nr_entry.place(anchor='nw', width='300', x='0', y='0')
        self.exp_date_entry = tk.Entry(self.payment_entry_frame)
        self.exp_date_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.exp_date_entry.place(anchor='nw', rely='0.1', width='300', x='0', y='0')
        self.card_type_entry = tk.Entry(self.payment_entry_frame)
        self.card_type_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.card_type_entry.place(anchor='nw', rely='0.2', width='300', x='0', y='0')
        self.amount_entry = tk.Entry(self.payment_entry_frame)
        self.amount_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.amount_entry.place(anchor='nw', rely='0.6', width='300', x='0', y='0')
        self.verif_entry = tk.Entry(self.payment_entry_frame)
        self.verif_entry.config(relief='flat', font=BasePage.LIGHT_FONT)
        self.verif_entry.place(anchor='nw', rely='0.7', width='300', x='0', y='0')
        self.validate_btn = CustomButton(self.payment_entry_frame)
        self.validate_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                 font=BasePage.LIGHT_FONT)
        self.validate_btn.config(justify='left', relief='flat', text='validate', command=self.on_validate)
        self.validate_btn.place(anchor='nw', relx='0.15', rely='0.85', width='200', x='0', y='0')
        self.payment_entry_frame.config(height='200', width='200')
        self.payment_entry_frame.place(anchor='ne', height='450', relx='1.0', rely='0.05', width='350', x='0', y='0')
        self.payment_info_frame.config(font=BasePage.LIGHT_FONT, height='200', text='payment info', width='200')
        self.payment_info_frame.place(anchor='nw', height='500', relx='0.52', rely='0.07', width='600', x='0', y='0')
