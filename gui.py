"""Lightweight cross-platform graphic interface for program."""

import getpass

import tkinter as tk
from tkinter import filedialog

class TkFileDialogExample(tk.Frame):
    """The design of the application."""

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.set_design_options()
        self.create_widgets()
        self.set_action_options()

    def set_design_options(self):
        """Configure widget design options before placing them in GUI."""

        self.button_options = {
            'fill': tk.constants.BOTH,
            'padx': 5,
            'pady': 5,
        }

    def create_widgets(self):
        """Create widgets on GUI launch."""

        tk.Label(
            self, text='Select folders to compare:'
            ).pack()

        tk.Button(
            self, text='Folder 1', command=self.askdirectory
            ).pack(**self.button_options)

        tk.Button(
            self, text='Folder 2', command=self.askdirectory
            ).pack(**self.button_options)

        tk.Label(
            self, text='Select folder for output:'
            ).pack()

        tk.Button(
            self, text='Output Folder', command=self.askdirectory
            ).pack(**self.button_options)

        tk.Label(
            self, text='Select method(s) of output:'
            ).pack()

        self.output_as_text = tk.IntVar()
        self.output_as_text.set(1)
        tk.Checkbutton(
            self, text='.txt', variable=self.output_as_text,
            ).pack()

        self.output_as_csv = tk.IntVar()
        self.output_as_csv.set(1)
        tk.Checkbutton(
            self, text='.csv', variable=self.output_as_csv,
            ).pack()


    def set_action_options(self):
        """Configure widget action options after placing them in GUI."""

        self.directory_options = {
            'initialdir': r'C:\Users\{}\Desktop'.format(getpass.getuser()),
            'mustexist': False,
            'parent': ROOT,
            'title': 'Choose a directory',
        }

    def askdirectory(self):
        """Return a selected directory name."""

        return filedialog.askdirectory(**self.directory_options)


if __name__ == '__main__':
    # Start the app in dev mode
    ROOT = tk.Tk()
    TkFileDialogExample(ROOT).pack()
    ROOT.mainloop()
