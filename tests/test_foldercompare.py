"""Test the foldercompare.py module."""

import unittest
import foldercompare

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.folder1 = r'.\tests\control_data_1\Data Folder'
        self.folder2 = r'.\tests\control_data_2\Data Folder'
        self.resultfile = r'.\tests\results'

    def test_create_results(self):
        """Create results identical to the control."""

        foldercompare.compare(self.folder1, self.folder2,
                              self.resultfile, output_type='both')

if __name__ == '__main__':
    unittest.main()
