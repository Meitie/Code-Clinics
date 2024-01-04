import unittest
from unittest.mock import patch
import io
import sys
import os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS + "/")
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader 
spec = spec_from_loader("app", SourceFileLoader("app", USER_PATHS + '/app'))
app = module_from_spec(spec)
spec.loader.exec_module(app)
sys.modules['app'] = app
import app


class Test_Quickstart(unittest.TestCase):

    text = io.StringIO()
    sys.stdout = text

    def test_valid_action(self):
        result = app.valid_action()
        self.assertEqual(result,["create", "cancel", "update", "join", "leave","logout",'help','create_calendar','join_calendar','delete_calendar','update_calendar','leave_calendar'])


    def test_valid_command(self):
        result1 = app.valid_command('create')
        result2 = app.valid_command('cancel')
        result3 = app.valid_command('create_calendar')
        result4 = app.valid_command('hello')
        self.assertEqual(result1,True)
        self.assertEqual(result2,True)
        self.assertEqual(result3,True)
        self.assertEqual(result4,False)


    def test_arguments(self):
        pass


    def test_help_func(self):
        result = app.help_func()
        self.assertEqual(result,"""
   These are the code-clinics commands that can be used in various situations:\n\
   Please copy and paste the code in '<>' to call the functions:\n\
   \nlogging in and out:\n\
   login                     logs the user in automatically when a command is entered       \
   <./app login "username">
   logout                    logs you out of the code clinics calendar                      \
   <./app logout>
   \nVolunteering commands:\n\
   create                    Create a slot (of 3x30 minutes), to host a code-clinic         \
   <./app create "date" "time" "summary" "description">
   update                    Update an existing slots description/summary                   \
   <./app update "id" "summary" "description">
   delete                    Deletes an individual users sessions of code clinics           \
   <./app delete "id">
   \nBooking commands:\n\
   join                      Join a code clinic slot (of 1x30 minutes) with a host          \
   <./app join "id_of_session" "description">
   leave                     Leave a session that you are apart of                          \
   <./app leave "id_of_session">
   \nCalendar commands:\n\
   voluntee_calendar     See a preview of the volunteering calendar, and the available slots\
   <./app "create_calendar_slot">
   join_calendar         See a preview of the booking calendar, and the available slots     \
   <./app "join_calendar_slot"> 
   delete_calendar       See all the slots you can delete                                   \
   <./app "delete_calendar_slot">
   update_calendar       See all the events you can update                                  \
   <./app "update_calendar_slot">
   leave_calendar        See all the events you can leave                                   \
   <./app "leave_calendar_slot">
   """)

    def test_argument_validator(self):
        result1 = app.argument_validator(['create_calendar'])
        result2 = app.argument_validator(['join hbsadfbahsjbd'])
        self.assertEqual(result1,('create_calendar', []))
        self.assertEqual(result2,('',''))


if __name__ == '__main__':
    unittest.main()
