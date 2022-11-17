"""
Unit tests for the validation of PyCollDataSet objects.
"""

import unittest
from pycollisiondb.pycollisiondb import PyCollision
from pycollisiondb.pycoll_ds import PyCollDataSet, PyCollDataSetValidationError


class PyCollisionValidationTest(unittest.TestCase):
    def test_query_keyword_validation(self):
        pycoll = PyCollision.get_datasets(
            archive_uuid="9e6a467b-d531-4241-85f9-a86fdcdb9d68", DATA_DIR="tests"
        )
        self.assertEqual(len(pycoll.datasets), 8)

        # pks: 102737 – 102742, 103103, 103104
        # 102737: OK
        # 102738: "data_type": "rate coefficient"
        # 102739: OK
        # 102740: "frame": "com"
        # 102741: "columns": ... "E" ... "units": "eV" (instead of eV.u-1)

        # Should be OK!
        pycoll.datasets[102737].validate(raise_exception=True)
        self.assertTrue(pycoll.validate())
        self.assertTrue(pycoll.datasets[102737].is_valid)

        pycoll.datasets[102738].x[4] = pycoll.datasets[102738].x[3]
        with self.assertRaises(PyCollDataSetValidationError) as exc:
            pycoll.datasets[102738].validate(raise_exception=True)
            self.assertEqual(str(exc.exception), "x-data not monotonic!")
        self.assertFalse(pycoll.datasets[102738].validate())
        self.assertEqual(
            pycoll.datasets[102738].validation_messages, ["x-data not monotonic!"]
        )
        self.assertFalse(pycoll.datasets[102738].is_valid)

        pycoll.datasets[102738].x[4] = pycoll.datasets[102738].x[2]
        with self.assertRaises(PyCollDataSetValidationError) as exc:
            pycoll.datasets[102738].validate(raise_exception=True)
            self.assertEqual(str(exc.exception), "x-data not monotonic!")

        pycoll.datasets[102739].y[4] = -0.1
        with self.assertRaises(PyCollDataSetValidationError) as exc:
            pycoll.datasets[102739].validate(raise_exception=True)
            self.assertEqual(str(exc.exception), "y-data not non-negative!")
        self.assertFalse(pycoll.datasets[102739].validate())
        self.assertEqual(
            pycoll.datasets[102739].validation_messages, ["y-data not non-negative!"]
        )
        self.assertFalse(pycoll.datasets[102739].is_valid)

        self.assertFalse(pycoll.validate())
