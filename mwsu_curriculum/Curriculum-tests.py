import unittest
import pytest
from .curriculumlib import load_syllabi
from .curriculumlib import hours_per_semester
from .curriculumlib import courses_per_semester
from .curriculumlib import parse_course
from .curriculumlib import load_assignments

def standardTest():
    pass

#Testing load_syllabi

def testLSIsNotNone():
    assert load_syllabi() is not None

#Testing hours_per_semester

def testHPSIsNotNone():
    assert hours_per_semester() is not None

#Testing courses_per_semester

def testCPSIsNotNone():
    assert courses_per_semester() is not None

# Testing parse_course

def testPCIsNotNone():
    assert parse_course() is not None

#Testing load_assignments

def testLAIsNotNone():
    assert load_assignments() is not None


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
