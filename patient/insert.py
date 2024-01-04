import datetime

def already_booked(slots, attendees, user_name):
    """
    Creates a flag to check if the attendees is already there.
    if the email is equal to the logged in email, set flag to true.
    If the flag is True return False
    Else return True
    """
    already_joined = False
    for i in attendees:
        if i["email"] == user_name+'@student.wethinkcode.co.za':
            already_joined = True

    if already_joined == True:
        return False
    else:
        return True


def fully_booked(slots, attendees, user_name):
    """
    Checks if the list of attendees is already at the max of two or not.
    if it is 2 or more returns False
    else Returns True
    """
    if len(attendees) >= 2:
        return False
    else:
        return True


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


def current_events(service, calander_id):
    """
    Grabs and returns the current events from the 'code-clinics' calendar.
    returns it as an event.
    """
    event = service.events().get(calendarId='teamtwotesting@gmail.com', eventId=calander_id).execute()
    return event


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


def insert_patient(service, command_params, user_name, cc_events):
    """
    Creates all variables that will be used, for the params, and the date/time.
    Checks if the user already has slots. If false return.
    Checks if the slot is already fully booked. if False return.
    Adds the user to the event.
    checks if you already have meetings or not.
    trys to update the calendar slot, if it succeeds prints "You have successfully joined"
    If failed prints "No event with that name was found".
    """
    event = current_events(service, command_params[0])
    begin = event['start']["dateTime"]
    begin = begin.split("T")
    date = begin[0]
    time = begin[1][:5]

    slots = user_pre_slotted(cc_events, user_name)
    if already_booked(slots, event["attendees"], user_name) == False:
        print(f"You have already joined a slot on '{date}' at '{time}'.")
        return

    if fully_booked(slots, event["attendees"], user_name) == False:
        print(f"Sorry this event is fully booked.")
        return

    event['attendees'].append({'email': f'{user_name}@student.wethinkcode.co.za'})

    if do_you_have_meetings(service, date, time, user_name) == False:
        print("You already have a meeting at this time in your calendar.")
        return
    
    try:
        service.events().update(calendarId='teamtwotesting@gmail.com', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("You have successfully joined the meeting")
    except:
        print("No event with that name was found")

    return