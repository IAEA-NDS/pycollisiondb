"""
Unit tests for the search keywords of PyCollisionDB
"""

import unittest
from pycollisiondb.pycollisiondb import (
    PyCollision,
    PyCollisionDBKeywordError,
    PyCollisionDBPlotError,
)


class PyCollisionDBTest(unittest.TestCase):
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

        pks_consistent_datatypes = (102737, 102739)

        # Should not raise the PyCollisionDBPlotError exception.
        pycoll._get_plot_metadata(pks_consistent_datatypes)

        pks_inconsistent_datatypes = (102737, 102738)
        self.assertRaises(
            PyCollisionDBPlotError,
            pycoll.plot_datasets,
            None,
            pks_inconsistent_datatypes,
        )
        with self.assertRaises(PyCollisionDBPlotError) as exc:
            pycoll.plot_datasets(None, pks_inconsistent_datatypes)
        self.assertEqual(
            str(exc.exception), "Data types not all the same in requested plot."
        )

        pks_inconsistent_frames = (102739, 102740)
        self.assertRaises(
            PyCollisionDBPlotError, pycoll.plot_datasets, None, pks_inconsistent_frames
        )

        pks_inconsistent_columns = (102739, 102741)
        self.assertRaises(
            PyCollisionDBPlotError, pycoll.plot_datasets, None, pks_inconsistent_columns
        )
