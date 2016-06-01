# Build the standalone .exe file using pyinstaller
pyinstaller --onefile --windowed --name foldercompare.exe -y ./gui.py

# Move the created .exe into the top-level folder
mv ./dist/foldercompare.exe .

# Remove the folders left over from building
rm -rf ./build
rm -rf ./dist
rm -rf ./foldercompare.exe.spec
