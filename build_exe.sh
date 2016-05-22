# Build the standalone .exe file using pyinstaller
# Places the file in the ./dist folder
pyinstaller --onefile --windowed --name foldercompare.exe -y ./gui.py
