"""Test the foldercompare.py module."""

import filecmp
import os
import shutil
import unittest

import foldercompare

class TestRecursiveDircmpReport(unittest.TestCase):
    """Test the _recursive_dircmp function."""

    def setUp(self):
        """Create two folders for testing."""
        self.folder1 = os.path.join('tests', 'results1')
        self.folder2 = os.path.join('tests', 'results2')
        os.mkdir(self.folder1)
        os.mkdir(self.folder2)

    @unittest.skip('Fails half the time -- enough to avoid same_files feature')
    def test_dircmp_diff_files_accuracy(self):
        """Different files are identified as such using filecmp.dircmp()"""

        file1 = os.path.join(self.folder1, 'hello_world.txt')
        with open(file1, 'w') as file:
            file.write('foo')

        file2 = os.path.join(self.folder2, 'hello_world.txt')
        with open(file2, 'w') as file:
            file.write('bar')

        comparison = filecmp.dircmp(self.folder1, self.folder2)
        self.assertTrue(comparison.diff_files == ['hello_world.txt'])
        self.assertTrue(comparison.same_files == [])

    def test_file_in_both(self):
        """Classifies two identical files as the same."""

        file1 = os.path.join(self.folder1, 'hello_world.txt')
        with open(file1, 'w') as file:
            file.write('hello world')

        file2 = os.path.join(self.folder2, 'hello_world.txt')
        with open(file2, 'w') as file:
            file.write('hello world')

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        expected = {'both': ['./hello_world.txt'], 'right': [], 'left': []}
        self.assertEqual(report, expected)

    def test_file_only_in_left(self):
        """Classifies file only in one directory."""

        file1 = os.path.join(self.folder1, 'hello_world.txt')
        with open(file1, 'w') as file:
            file.write('hello world')

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        expected = {'left': ['./hello_world.txt'], 'right': [], 'both': []}
        self.assertEqual(report, expected)

    def test_subdirectory_only_in_left(self):
        """Classifies subdirectory with file only in left folder."""

        subdir1 = os.path.join(self.folder1, 'subdir')
        os.mkdir(subdir1)

        file1 = os.path.join(subdir1, 'hello_world.txt')
        with open(file1, 'w') as file:
            file.write('hello world')

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        expected = {'left': ['./subdir'], 'right': [], 'both': []}
        self.assertEqual(report, expected)

    def test_subdir_file_only_in_left(self):
        """Classifies file only in one subdirectory."""

        subdir1 = os.path.join(self.folder1, 'subdir')
        os.mkdir(subdir1)
        subdir2 = os.path.join(self.folder2, 'subdir')
        os.mkdir(subdir2)

        file1 = os.path.join(subdir1, 'hello_world.txt')
        with open(file1, 'w') as file:
            file.write('hello world')

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        expected = {'left': ['./subdir/hello_world.txt'], 'right': [], 'both': []}
        self.assertEqual(report, expected)

    def tearDown(self):
        """Delete test folders after each run."""
        shutil.rmtree(self.folder1)
        shutil.rmtree(self.folder2)


class TestCompareRegression(unittest.TestCase):
    """Test the compare function with known inputs and expected outputs."""

    def setUp(self):
        """Set test input data and expected control outputs."""

        self.folder1 = os.path.join('.', 'tests', 'control_data_1', 'Data Folder')
        self.folder2 = os.path.join('.', 'tests', 'control_data_2', 'Data Folder')
        self.resultfile = os.path.join('tests', 'results')
        self.controlresults = os.path.join('tests', 'control_results')

    def test_create_txt(self):
        """Can create a single TXT file, identical to the control."""

        foldercompare.compare(self.folder1, self.folder2,
                              self.resultfile, output_txt=True)

        result = filecmp.cmp(self.resultfile + '.txt',
                             self.controlresults + '.txt',
                             shallow=False)
        self.assertTrue(result)

    def test_create_csv(self):
        """Can create a single CSV file, identical to the control."""

        foldercompare.compare(self.folder1, self.folder2,
                              self.resultfile, output_csv=True)

        result = filecmp.cmp(self.resultfile + '.csv',
                             self.controlresults + '.csv',
                             shallow=False)
        self.assertTrue(result)

    def test_create_both(self):
        """Can create both files at once, identical to the control."""

        foldercompare.compare(self.folder1, self.folder2, self.resultfile,
                              output_txt=True, output_csv=True)

        result = filecmp.cmp(self.resultfile + '.txt',
                             self.controlresults + '.txt',
                             shallow=False)
        self.assertTrue(result)

        result = filecmp.cmp(self.resultfile + '.csv',
                             self.controlresults + '.csv',
                             shallow=False)
        self.assertTrue(result)

    def tearDown(self):
        """Delete test files after each run."""

        try:
            os.remove(self.resultfile + '.txt')
        except FileNotFoundError:
            pass

        try:
            os.remove(self.resultfile + '.csv')
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
