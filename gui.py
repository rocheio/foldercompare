"""Lightweight cross-platform graphic interface for folder compare program."""

import getpass
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import foldercompare

class FolderComparisonGUI(tk.Frame):
    """The graphic interface for the application."""

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.data = {}
        self.set_design_options()
        self.create_widgets()
        self.set_action_options()

    def set_design_options(self):
        """Configure widget design options before placing them in GUI."""

        self.root.title("Folder Comparison")
        self.root.minsize(300, 200)
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
            self, text='Folder 1',
            command= lambda: self.set_directory('folder1'),
            ).pack(**self.button_options)

        tk.Button(
            self, text='Folder 2',
            command= lambda: self.set_directory('folder2'),
            ).pack(**self.button_options)

        tk.Label(
            self, text='Select folder for output:'
            ).pack()

        tk.Button(
            self, text='Output Folder',
            command= lambda: self.set_directory('folder_output'),
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

        tk.Button(
            self, text='Run', command=self.run_program
            ).pack(**self.button_options)

    def set_action_options(self):
        """Configure widget action options after placing them in GUI."""

        self.directory_options = {
            'initialdir': r'C:\Users\{}\Desktop'.format(getpass.getuser()),
            'mustexist': False,
            'parent': self.root,
            'title': 'Choose a directory',
        }

    def set_directory(self, key=None):
        """Return a selected directory name."""

        response = filedialog.askdirectory(**self.directory_options)
        self.data[key] = response

    def run_program(self):
        """Run the folder comparison program with user selected data."""

        if 'folder1' not in self.data:
            messagebox.showerror("Error", "Must select Folder 1")
        elif 'folder2' not in self.data:
            messagebox.showerror("Error", "Must select Folder 2")
        elif 'folder_output' not in self.data:
            messagebox.showerror("Error", "Must select Output Folder")
        else:
            try:
                foldercompare.compare(
                    self.data['folder1'],
                    self.data['folder2'],
                    self.data['folder_output'] + '/results',
                    output_type='both')
            except Exception:
                messagebox.showerror("Error", "An error has occured")
            else:
                messagebox.showinfo("Success", "Folder comparison complete")


if __name__ == '__main__':
    # Start the app in dev mode
    ROOT = tk.Tk()
    FolderComparisonGUI(ROOT).pack()
    ROOT.mainloop()
