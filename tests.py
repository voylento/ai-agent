import unittest
import tempfile
import os
from pathlib import Path

from functions.functions import (
        run_python_file,
    )

class TestWriteFile(unittest.TestCase):
    
    def test_file_mainpy(self):
        """Test that passing "" as file_path equates returns error"""

        result = run_python_file("calculator", "main.py")
        print(result)


    def test_file_testspy(self):

        result = run_python_file("calculator", "tests.py")
        print(result)


    def test_file_outside_workingdir(self):

        result = run_python_file("calculator", "../main.py")
        print(result)

    def test_file_nonexistant(self):

        result = run_python_file("calculator", "nonexistent.py")
        print(result)

if __name__ == '__main__':
    unittest.main()
