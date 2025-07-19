# Requires pandas: pip install pandas
import unittest
import pandas as pd
from src.data_processing import load_data
import os

class TestDataProcessing(unittest.TestCase):

    def test_load_data_success(self):
        file_path = 'Digital Recommendation Solution/sample_data.csv'
        data = load_data(file_path)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 4)

    def test_load_data_file_not_found(self):
        file_path = 'Digital Recommendation Solution/non_existent_file.csv'
        data = load_data(file_path)
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()