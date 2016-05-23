# foldercompare

A Windows application that compares the content of two folders with a simple GUI. Outputs a very simple report to a text file, a CSV file, or both.

A quick tool I made at work to help another department. Uses the Python standard library package [`filecmp`][filecmp] to do the comparison and [`tkinter`][tkinter] to build the GUI. [PyInstaller][pyinstaller] was used to package the script into an executable.

### Building the .exe

1. Install [Python 3][python]
2. Clone this repo
3. Install requirements using `pip install -r requirements.txt`
4. Run tests using `python -m unittest tests/test_foldercompare.py`
5. Build the program using the script `./build_exe.sh`
6. The standalone program is now located at `./dist/foldercompare.exe`


[filecmp]: https://docs.python.org/3.5/library/filecmp.html
[pyinstaller]: http://www.pyinstaller.org/
[python]: https://www.python.org/downloads/
[tkinter]: https://docs.python.org/3.5/library/tkinter.html
