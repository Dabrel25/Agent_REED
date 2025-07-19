import unittest
import io
import sys
from unittest.mock import patch

sys.path.append('Digital Recommendation Solution/src')
from main import main

class TestMain(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_prints_hello_world(self, stdout):
        main()
        self.assertEqual(stdout.getvalue().strip(), "Hello, world!")

if __name__ == '__main__':
    unittest.main()