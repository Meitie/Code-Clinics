import re, datetime

def valid_date(start_date):
    """
    Checks if the start date is the correct format (using regex):
    :return: True if valid
    :return: False if invalid
    """
    if (re.findall(r"\d\d\d\d-\d\d-\d\d", start_date)):
        return True
    else:
        return False


def valid_time(start_time):
    """
    Checks if the start time is the correct format (using regex):
    :return: True if valid
    :return: False if invalid
    """
    if re.findall(r"^\d\d:\d\d$", start_time):
        return True
    else:
        return False


def validate_params(command_params):
    """
    Checks if the it is valid or not.
    seperates the date and time into variabels.
    runs if they are valid or not, if both are true returns the date and time
    else returns false
    """
    if command_params == []:
        print("invalid request, plese try again")
        return "", ""
    if len(command_params) != 2:
        print("invalid request, plese try again")
        return "", ""

    date = command_params[0]
    time = command_params[1]
    
    if valid_date(date) == True and valid_time(time) == True:
        return date, time
    else:
        print("invalid request, plese try again")
        return "", ""

    return "", ""


def meeting_setups(command_params, user_name):
    """
    If there are commands then assign them the values of "summary" and "description".
    Else 'summary' is the username and 'description' is "Open for anything"
    """
    if command_params:
        summary = command_params[0]
        description = command_params[1]
        return summary, description
    else:
        summary = user_name
        description = "Open for anything"
        return summary, description


def clearing_dates(table_data):
    """
    Grab the whole table data, and strip it to just the list of dates.
    returns just the list of the start dates. 
    """
    available_dates = table_data[0]
    available_dates.pop(available_dates.index(""))
    return available_dates


def validated_slot(table_data, date, time):
    """
    Check if the date and the time are in the start times and dates.
    If they are then make the variable "time_in" and "date_in" for True.
    Else they will be False.
    if "time_in" and "date_in" are true return "True".
    else return false.
    """
    start_times = ['08:00', '08:30', '10:00', '11:30', '13:00', '14:30', '16:00', '17:30']
    available_dates = clearing_dates(table_data)
    time_in = False
    date_in = False
    for i in start_times:
        if time == str(i):
            time_in = True
            break

    for i in available_dates:
        if date == str(i):
            date_in = True
            break

    if time_in == True and date_in == True:
        return True
    else:
        return False


def user_pre_slotted(cc_events, user_name):
    """
    Makes a Creators and Start_times list, append all the creators
    and date times. as well as splitting them all  on the "@".
    Slots = the dateTime for each of the creators.
    returns slots
    """
    creators = list()
    start_times = list()
    for i in range(len(cc_events)):
        creators.append(cc_events[i]['creator']['email'])
        start_times.append(cc_events[i]['start']['dateTime'])

    creator_names = list()
    for i in range(len(creators)):
        name = creators[i]
        name = name.split('@')
        creator_names.append(name[0])

    slots = [cc_events[num]['start']['dateTime'] for num, user in enumerate(creator_names) if creator_names[num] == user_name]
    return slots


def already_booked(slots, date, time):
    """
    Converts the date and time into the correct format.
    for each item in the slots list, it checks if there is already a matching times.
    If there is change the value of "conflicted_times"
    if "conflicted_times" not an empty string then return False
    else return True
    """
    date_time = f'{date}T{time}:00+02:00'
    conflicted_times = ''
    for i in slots:
        if date_time == i:
            conflicted_times = i
            break
    
    if conflicted_times != '':
        return False
    else:
        return True


def make_datetime_from_string(string):
    """
    Creates a dattime object form a given string, in the right format.
    :return: a datetime in the correct format.
    """
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S%z")


def freebusy_check(service, date, time, user_name):
    """
    checks the format for timeMin and timeMax as well as the timezones.
    then checks the id for both calendars.
    returns the eventsResults.
    """
    event = {
        "timeMin": (make_datetime_from_string(f'{date}T{time}:00+0200')).isoformat(),
        "timeMax": (make_datetime_from_string(f'{date}T{time}:00+0200')+datetime.timedelta(minutes = 90)).isoformat(),
        "timeZone": 'Africa/Johannesburg',
        "items": [
            {
                "id": user_name + '@student.wethinkcode.co.za'
            },
            {
                'id': 'teamtwotesting@gmail.com'
            }
        ]
    }

    eventsResult = service.freebusy().query(body=event).execute()
    return eventsResult


def do_you_have_meetings(service, date, time, user_name):
    """
    Grabs the events from freebusy_check
    seperates the 2 calendars based on the events.
    Check if the patients calendar is empty in the alotted time.
    If patient['busy'] == []: return true
    else they have an event and return false
    """
    events = freebusy_check(service, date, time, user_name)
    two_cals = events['calendars']
    patient, clinic = two_cals[user_name+'@student.wethinkcode.co.za'], two_cals['teamtwotesting@gmail.com']

    if patient['busy'] == []:
        return True
    else:
        return False
    return False


def insertion_of_event(service, event, date, time):
    """
    Try to insert the events into the calendar.
    If it succeeds then says "The events have been created"
    Else prints "A Spooky thing happend"
    """
    try:
        service.events().insert(calendarId='teamtwotesting@gmail.com', body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True).execute()
        return print(f"The event(s) have been created at {time} on the {date}")
    except:
        print("A spooky thing happened. Please try again.")


def valid_date_checker(date, time):
    """
    checks the valid date and time, and makes sure that they are valid.
    as well as proper datetime.
    If if is valid then returns starttime, endtime, valid_slot.
    Else returns "Please enter a valid date and time"
    """
    date = date.split("-")
    time = time.split(":")
    year, month, day = date[0], date[1], date[2]
    hour, minute = time[0], time[1]
    valid_check = False

    while not valid_check:
        try:
            valid_slot = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
            valid_check = True
        except:
            print("Please enter a valid date and time")

    starttime = f'{year}-{month}-{day}T{hour}:{minute}:00+02:00'
    endtime = str(valid_slot + datetime.timedelta(minutes=30)).split(" ")
    endtime = f'{endtime[0]}T{endtime[1]}+02:00'

    return starttime, endtime, valid_slot


def create_event(date, time, summary, description, user_name, service):
    """
    Gets the valid times, dates and summarys.
    Creates the valid event to submit to the service for the calendar.
    Checks if the timeslot is the 1 event slot, if it is create one.
    Else if it is the 90 min slot, create 3x30min slots.
    """
    starttime, endtime, valid_slot = valid_date_checker(date, time)
    
    event = {
        'summary': summary,
        'location': '',
        'description': description,
        'start': {
            'dateTime': starttime,
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': endtime,
            'timeZone': 'Africa/Johannesburg',
        },
        "hangoutLink": "https://meet.google.com/snz-hfvt-zuo?pli=1&authuser=0",
        'attendees': [
            {'email': f'{user_name}@student.wethinkcode.co.za'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'anyoneCanAddSelf': True,
    }

    if time == '08:00' or time == '17:30':
        insertion_of_event(service, event, date, time)
    else:
        for i in range(3):
            starttime = str(valid_slot + datetime.timedelta(minutes=(i) * 30)).split(" ")
            endtime = str(valid_slot + datetime.timedelta(minutes=(i + 1) * 30)).split(" ")
            event["start"]["dateTime"] = f'{starttime[0]}T{starttime[1]}+02:00'
            event["end"]["dateTime"] = f'{endtime[0]}T{endtime[1]}+02:00'
            insertion_of_event(service, event, starttime[0], starttime[1])
    return 


def insert_event(command_params, service, user_name, table_data, full_time_list, cc_events, us_events):
    """
    Seperates the command params into the slots they need if valid.
    1. checks if they are valid slot. if False return.
    2. checks if they user already has this slot. if False return.
    3. checks if the user already has a meeting in their calendar. if False return.
    4. if you passed all other checks, then create the event.
    """
    date, time = validate_params(command_params[:2])
    summary, description = meeting_setups(command_params[2:], user_name)

    if validated_slot(table_data, date, time) == False:
        print("Invalid time slot, please stick to the allotted times, please check the calendar.")
        return

    slots = user_pre_slotted(cc_events, user_name)
    if already_booked(slots, date, time) == False:
        print(f"You have already a time booked on '{date}' at '{time}'.")
        return

    if do_you_have_meetings(service, date, time, user_name) == False:
        print("You already have a meeting at this time in your calendar.")
        return
    
    create_event(date, time, summary, description, user_name, service)
