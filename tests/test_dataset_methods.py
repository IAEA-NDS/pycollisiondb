"""
Unit tests for various methods of the PyCollDataSet class.
"""

import unittest
from pycollisiondb.pycollisiondb import PyCollision
from pycollisiondb.pycoll_ds import PyCollDataSet


class PyCollisionValidationTest(unittest.TestCase):
    def test_print_values(self):
        pycoll = PyCollision.get_datasets(
            archive_uuid="9e6a467b-d531-4241-85f9-a86fdcdb9d68", DATA_DIR="tests"
        )
        lines = pycoll.datasets[102737].print_values()
        lines = lines.split("\n")
        self.assertEqual(lines[0], "E / eV.u-1 sigma / cm2")
        self.assertEqual(lines[3], "9000.0 1.235e-17")
