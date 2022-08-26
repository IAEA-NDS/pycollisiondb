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
    def test_query_keyword_validation(self):
        logger.debug("RUNNING A TEST!")
        pycoll = PyCollision()
        pycoll = PyCollision.get_datasets(query={"pks": [89433]})
        print(pycoll.datasets[89433].metadata["reaction"])

        self.assertRaises(PyCollisionDBKeywordError, pycoll.query, notakey=1)
        self.assertRaises(PyCollisionDBKeywordError, pycoll.query, pk=1, pks=[3, 4])
