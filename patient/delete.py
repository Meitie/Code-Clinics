def current_events(service, calander_id):
    """
    Grabs all the events from the current calendar with the associated ID.
    returns the found event
    """
    event = service.events().get(calendarId='teamtwotesting@gmail.com', eventId=calander_id).execute()

    return event


def leaving(service, event):
    """
    Trys to execute the service call to delete the event off the 'code-clinics' calenar.
    If it success print "Your have left the meeting"
    else prints "No event with that name was found."
    """
    try:
        service.events().update(calendarId='teamtwotesting@gmail.com', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("You have left the meeting.")
    except:
        print("No event with that name was found.")


def delete_event(service, params, user_name):
    """
    Creates the event, as well as a counter flag.
    Checks for each attendee in the event to find if the logged in user is one of them.
    if they are increase the flag "count"
    if count not 0 (mean you were found).
    Find the index where you are the attendee and pop off the list, and run leaving.
    else Print out the error statements. 
    """
    event = current_events(service, params)
    count = 0
    for i in event['attendees']:
        if i['email'] != user_name+'@student.wethinkcode.co.za':
            count += 1
            continue

    if count != 0:
        if (event["id"]) == params:
            event['attendees'].pop(count)
            leaving(service, event)
        else:
            print("The ID's do not match, please try again.")
    else:
        print("This is not your slot, please choose your own slot.")