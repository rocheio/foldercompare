"""Test the foldercompare.py module."""

import filecmp
import os
import unittest

import foldercompare

class TestCompare(unittest.TestCase):
    """Test the compare function with known inputs and expected outputs.

    Serves as a regression and integration test for the entire module.
    """

    def setUp(self):
        """Set test input data and expected control outputs."""

        self.folder1 = r'.\tests\control_data_1\Data Folder'
        self.folder2 = r'.\tests\control_data_2\Data Folder'
        self.resultfile = r'.\tests\results'
        self.controlresults = r'.\tests\control_results'

    def test_create_txt(self):
        """Can create a single TXT file, identical to the control."""

        foldercompare.compare(self.folder1, self.folder2,
                              self.resultfile, output_type='txt')

        result = filecmp.cmp(self.resultfile + '.txt',
                             self.controlresults + '.txt',
                             shallow=False)
        self.assertTrue(result)

    def test_create_csv(self):
        """Can create a single CSV file, identical to the control."""

        foldercompare.compare(self.folder1, self.folder2,
                              self.resultfile, output_type='csv')

        result = filecmp.cmp(self.resultfile + '.csv',
                             self.controlresults + '.csv',
                             shallow=False)
        self.assertTrue(result)

    def test_create_both(self):
        """Can create both files at once, identical to the control."""

        foldercompare.compare(self.folder1, self.folder2,
                              self.resultfile, output_type='both')

        result = filecmp.cmp(self.resultfile + '.txt',
                             self.controlresults + '.txt',
                             shallow=False)
        self.assertTrue(result)

        result = filecmp.cmp(self.resultfile + '.csv',
                             self.controlresults + '.csv',
                             shallow=False)
        self.assertTrue(result)

    def test_compare_bad_mode(self):
        """Can not provide an unsupported comparison mode."""

        with self.assertRaises(ValueError):
            foldercompare.compare(self.folder1, self.folder2,
                                  self.resultfile, output_type='badparam')

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
