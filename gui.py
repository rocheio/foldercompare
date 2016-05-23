"""Lightweight cross-platform graphic interface for folder compare program."""

import getpass
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import foldercompare

class FolderComparisonGUI(tk.Frame):
    """The graphic interface for the application."""

    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.root = root

        # tkinter app variables -- .get() returns False until .set() otherwise
        self.folder1 = tk.StringVar()
        self.folder2 = tk.StringVar()
        self.folder_output = tk.StringVar()
        self.filename = tk.StringVar()
        self.output_as_text = tk.BooleanVar()
        self.output_as_text.set(1)
        self.output_as_csv = tk.BooleanVar()
        self.output_as_csv.set(1)

        self.set_design_options()
        self.create_widgets()
        self.set_action_options()

    def set_design_options(self):
        """Configure widget design options before placing them in GUI."""

        self.root.title("Folder Comparison Tool")
        self.root.minsize(300, 200)
        self.button_options = {
            'fill': tk.constants.BOTH,
            'padx': 5,
            'pady': 5,
        }

    def create_widgets(self):
        """Create widgets on GUI launch."""

        tk.Label(
            self, text='Folder Comparison Tool', font=16,
            ).pack()

        tk.Button(
            self, text='Select Folder 1',
            command=lambda: self.set_directory(self.folder1),
            ).pack(**self.button_options)

        tk.Label(
            self, textvariable=self.folder1, fg="blue",
            ).pack()

        tk.Button(
            self, text='Select Folder 2',
            command=lambda: self.set_directory(self.folder2),
            ).pack(**self.button_options)

        tk.Label(
            self, textvariable=self.folder2, fg="blue",
            ).pack()

        tk.Button(
            self, text='Select Output Folder',
            command=lambda: self.set_directory(self.folder_output),
            ).pack(**self.button_options)

        tk.Label(
            self, textvariable=self.folder_output, fg="blue",
            ).pack()

        tk.Label(
            self, text="Choose a name for output file(s)",
            ).pack()

        tk.Entry(
            self, textvariable=self.filename
            ).pack()

        tk.Label(
            self, text='Select type(s) of output:'
            ).pack()

        tk.Checkbutton(
            self, text='.txt', variable=self.output_as_text,
            ).pack()

        tk.Checkbutton(
            self, text='.csv', variable=self.output_as_csv,
            ).pack()

        tk.Button(
            self, text='Run', command=self.validate_and_run,
            ).pack(**self.button_options)

    def set_action_options(self):
        """Configure widget action options after placing them in GUI."""

        self.directory_options = {
            'initialdir': r'C:\Users\{}\Desktop'.format(getpass.getuser()),
            'mustexist': False,
            'parent': self.root,
            'title': 'Choose a directory',
        }

    def set_directory(self, variable):
        """Return a selected directory name.

        ARGS:
            variable (tk.Variable): The tkinter variable to save selection as.
        """

        selection = filedialog.askdirectory(**self.directory_options)
        variable.set(selection)

    def validate_and_run(self):
        """Run the folder comparison program with user selected data."""

        # Validate user inputs savid in tkinter variables
        folder1_is_valid = os.path.exists(self.folder1.get())
        folder2_is_valid = os.path.exists(self.folder2.get())
        folder_output_is_valid = os.path.exists(self.folder_output.get())
        output_name_valid = self.filename.get()
        output_type_selected = (self.output_as_text.get() or
                                self.output_as_csv.get())

        # Show error if validation failed
        if not folder1_is_valid:
            messagebox.showerror("Error", "Must select Folder 1")
        elif not folder2_is_valid:
            messagebox.showerror("Error", "Must select Folder 2")
        elif not folder_output_is_valid:
            messagebox.showerror("Error", "Must select Output Folder")
        elif not output_name_valid:
            messagebox.showerror(
                "Error", "Must enter a filename for output (excluding path)"
                )
        elif not output_type_selected:
            messagebox.showerror("Error", "Must select type(s) of output")
        else:
            # Determine name for output file(s)
            folder = self.folder_output.get()
            filename = self.filename.get().split('.')[0]
            output_filename = os.path.join(folder, filename)

            # Determine output type(s) from checkboxes
            if self.output_as_text.get() and self.output_as_csv.get():
                output_type = 'both'
            elif self.output_as_text.get():
                output_type = 'txt'
            elif self.output_as_csv.get():
                output_type = 'csv'

            # Run the folder compare program
            try:
                foldercompare.compare(self.folder1.get(), self.folder2.get(),
                                      output_filename, output_type=output_type)
            except Exception:
                messagebox.showerror(
                    "Error", "An error has occured, please try again."
                    )
            else:
                messagebox.showinfo("Success", "Folder comparison complete")


if __name__ == '__main__':
    # Start the app in dev mode
    ROOT = tk.Tk()
    FolderComparisonGUI(ROOT).pack()
    ROOT.mainloop()
