"""
Unit tests for the search keywords of PyCollisionDB
"""

import unittest
from pycollisiondb.pycollisiondb import PyCollision, PyCollisionDBKeywordError

import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

logger2 = logging.getLogger("pycollisiondb")
logger2.setLevel(logging.DEBUG)
logger2.addHandler(ch)


class PyCollisionDBTest(unittest.TestCase):
    # def test_query_keyword_validation(self):
    #    logger.debug("RUNNING A TEST!")
    #    pycoll = PyCollision()
    #    pycoll = PyCollision.get_datasets(query={"pks": [89433]})
    #    print(pycoll.datasets[89433].metadata["reaction"])

    #   self.assertRaises(PyCollisionDBKeywordError, pycoll.query, notakey=1)
    #   self.assertRaises(PyCollisionDBKeywordError, pycoll.query, pk=1, pks=[3, 4])

    def test_change_units(self):
        pycoll = PyCollision.get_datasets(
            archive_uuid="1e32c5d7-edb9-4a4d-81db-52d8c41836b6", DATA_DIR="tests"
        )
        self.assertEqual(len(pycoll.datasets), 3)

        ds = pycoll.datasets[103104]
        ycol = ds.metadata["columns"][1]
        self.assertEqual(ycol["name"], "sigma")
        self.assertEqual(ycol["units"], "cm2")
        ds.convert_units("sigma", "a02")
        self.assertAlmostEqual(ds.y[0], 0.5785125)
        self.assertAlmostEqual(ds.unc_lo[0], 0.057137037)
        self.assertEqual(ycol["units"], "a02")

        xcol = ds.metadata["columns"][0]
        self.assertEqual(xcol["name"], "E")
        self.assertEqual(xcol["units"], "eV.u-1")
        ds.convert_units("E", "keV.u-1")
        self.assertAlmostEqual(ds.x[0], 9.4)
        self.assertEqual(xcol["units"], "keV.u-1")


# class PyCollisionDBReactionTextTest(unittest.TestCase):
#    def test_reaction_text_ordering(self):
#        logger.debug("RUNNING A TEST!")
#        pycoll = PyCollision.get_datasets(
#            query={"reaction_texts": ["H+ + H 1s -> H+ + H+ + e-"]},
#            DB_URL='http://127.0.0.1:8282')
#        self.assertEqual(len(pycoll.datasets), 4)
#        self.assertEqual(sorted(list(pycoll.datasets.keys())),
#                         [102737, 103103, 103104, 107356])
