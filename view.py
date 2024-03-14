import re
import tkinter as tk
from tkinter import ttk
from controller import Controller


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # create widgets
        # email label
        self.email_label = ttk.Label(self, text='Email:')
        self.email_label.grid(row=1, column=0)
        # email entry
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=30)
        self.email_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # password label
        self.password_email = ttk.Label(self, text='Password:')
        self.password_email.grid(row=2, column=0)
        # password entry
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, width=30)
        self.password_entry.grid(row=2, column=1)

        # save button
        self.save_button = ttk.Button(self, text='Save', command=self.save_button_clicked)
        self.save_button.grid(row=2, column=3, padx=10)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=3, column=1, sticky=tk.W)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def save_button_clicked(self):
        """
        Handle button click event
        :return:
        """
        if self.controller:
            try:
                msg = self.controller.save(self.email_var.get(), self.password_var.get())
                self.show_success(msg)
            except ValueError as error:
                self.show_error(error)

    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
        # self.email_entry['foreground'] = 'red'
        # self.email_entry.after(3000, self.email_entry.configure, {'foreground': 'black'})

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

        # reset the form
        # self.email_entry['foreground'] = 'black'
        self.email_var.set('')
        self.password_var.set('')

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label['text'] = ''


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Sign up')

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller()

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    App().mainloop()
