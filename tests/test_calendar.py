import unittest
from unittest.mock import patch
import io
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS + "/")
import clinic_calendars.calendar as c
import datetime


class Test_Quickstart(unittest.TestCase):

    def test_list_week(self):
        result = c.creating_list_of_week(8,datetime.date.today())
        self.assertEqual(len(result),8)


    def test_empty_strings(self):
        result = c.generate_list_of_empty_strings(3)
        self.assertEqual(result,['','','',''])
    


if __name__ == '__main__':
    unittest.main()

