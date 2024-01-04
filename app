#!/usr/bin/env python3
import datetime, sys, json, os, re
from api_calls import serives_maker, event_maker
from user_logging import login, logout
from clinician import create, cancel, update
from patient import book, leave
from clinic_calendars import patient_calendar, clinician_calendar, delete_calendar, update_calendar_slot, leave_calendar

def valid_action():
    """
    Returns a list of every valid action that the users can run.
    """
    return ["create", "cancel", "update", "join", "leave", "login","logout",'help'\
        ,'create_calendar','join_calendar','delete_calendar','update_calendar','leave_calendar']


def valid_command(action):
    """
    This function checks to make sure that the action from the user is valid and correct
    """
    if action in valid_action():
        return True
    else:
        return False


def call_calendar(events, calendar,service,user_name):
    """
    This function calls the calendar if the user has meetings in it \
        to print and generate it
    """
    try:
        calendar.generate_table(8,events, fetch_calendar(service),user_name)
        calendar.table_data = []
    except:
        print("You have no meetings in your calendar")


def handle_command(command, command_params, service, user_name):
    '''
    Creating conditions that will take the users input, then performing the requested action.
    '''

    if command == "help":
        help_func()
        return

    if command == "create":
        print("Attempting to create event(s)...")
        us_events = event_maker.get_user_events(service, 7)
        cc_events = event_maker.get_code_clinic_events(service, 7) 
        clinician_calendar.generate_table(8, us_events, user_name)
        create.insert_event(command_params, service, user_name, clinician_calendar.table_data, clinician_calendar.full_time_list, cc_events, us_events)
        return

    elif command == "cancel":
        print("Attempting to delete your event...")
        events = event_maker.get_user_events(service, 7)
        cancel.delete_event(command_params, service, user_name, events)
        return

    elif command == "update":
        print("Attempting to update your event...")
        events = event_maker.get_user_events(service, 7)
        update.update_event(service, command_params, events, user_name)
        return

    elif command == 'join_calendar':
        events = event_maker.get_user_events(service, 7)
        try:
            patient_calendar.generate_table(8,events, fetch_calendar(service),user_name)
            patient_calendar.table_data = []
        except:
            print("You have no meetings in your calendar")

    elif command == 'delete_calendar':
        events = event_maker.get_user_events(service, 7)
        try:
            delete_calendar.generate_table(8,fetch_calendar(service),user_name)
            delete_calendar.table_data = []
        except:
            print("You have no meetings in your calendar")

    elif command == 'create_calendar':
        events = event_maker.get_user_events(service, 7)
        try:
            clinician_calendar.print_table(8, events,user_name)
        except:
            print('You have no meetings in your calendar')

    elif command == 'leave_calendar':
        events = event_maker.get_user_events(service, 7)
        try:
            leave_calendar.generate_table(8, fetch_calendar(service),user_name)
        except:
            print('You have no meetings in your calendar')

    
    elif command == 'update_calendar':
        events = event_maker.get_user_events(service, 7)
        try:
            update_calendar_slot.generate_table(8, fetch_calendar(service),user_name)
        except:
            print('You have no meetings in your calendar')


    elif command == "join":
        print("Attempting to join the event...")
        cc_events = event_maker.get_code_clinic_events(service, 7)
        book.insert_patient(service, command_params, user_name, cc_events)
        return

    elif command == "leave":
        print("Attempting to leave the event...")
        cc_events = event_maker.get_code_clinic_events(service, 7)
        leave.delete_event(service, command_params[0], user_name)
       
    return


def arguments():
    """
    Grabs all the system arguments that the users passed in and removes the name
    of the file that was run only keeping the passed args.
    """
    arg = sys.argv
    arg = arg[1:]
    return arg


def fetch_calendar(service):
    """
    Fetches the 2 different calendars, 'code-clinics' and 'users'
    returns the 'code-clinics' calendar.
    """
    tttevent = event_maker.get_code_clinic_events(service, 7)
    primaryevent = event_maker.get_user_events(service, 7)

    return tttevent
   

def help_func():
    """
    Prints out the Help for the users to see what they can do, depending on their role
    """
    helped = """
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
   <./app "create_calendar">
   join_calendar         See a preview of the booking calendar, and the available slots     \
   <./app "join_calendar"> 
   delete_calendar       See all the slots you can delete                                   \
   <./app "delete_calendar">
   update_calendar       See all the events you can update                                  \
   <./app "update_calendar">
   leave_calendar        See all the events you can leave                                   \
   <./app "leave_calendar">
   """
    print(helped)
    return helped


def argument_validator(action):
    """
    Recievs the action from the user as a parameter, and then it splits them\
        valids that it is a valid argument and the parameters are valid
    :returns: command (being the valid action to take), lower case
    :returns: all the params for the argument, lower case
    """
    command = ""
    params = ""

    if not action:
        return "zz", ""

    if action[0] in valid_action():
        command = action[0]

    if not command == "":
        action.pop(action.index(command))
        params = list(map(lambda x: x.lower(), action))
    elif command in valid_action() and params == "":
        print("no valid parameteres found, plese try again")
        help_func()
        return "", ""
    else:
        print("no valid action found, please try again")
        help_func()
        return "", ""
    return command.lower(), params


def main():
    """
    This is the main function where everything is first called and processed
    """

    action = arguments()
    command, command_params = argument_validator(action)
    if command == "" and command_params == "":
        return
    if command == 'logout':
        print(("\033[1;32mLogging out\033[0m"))
        logout.logout()
        sys.exit()
    if command == 'login':
        user_name = login.log_in_checker()[0]
    user_name = login.log_in_checker()[0]
    service = serives_maker.creating_service()
    handle_command(command, command_params, service, user_name)


if __name__ == '__main__':
    main()
