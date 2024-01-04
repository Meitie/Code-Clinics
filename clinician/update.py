def current_events(service, calander_id):
    """
    Grabs the current events that are on the "code-clinics" calendar,
    and saves it to the event variable.
    :returns: event
    """
    event = service.events().get(calendarId='teamtwotesting@gmail.com', eventId=calander_id).execute()
    return event


def updaters(service, event):
    """
    Trys to execute the update via the service, if it was successfully run, then prints "You event has been updated"
    else "No event with that ID was found"
    """
    try:
        service.events().update(calendarId='teamtwotesting@gmail.com', eventId=event['id'], body=event, maxAttendees=2, sendUpdates='all', sendNotifications=True, alwaysIncludeEmail=True).execute()
        print("Your event has been updated")
    except:
        print("No event with that ID was found")


def update_event(service, params, events, user_name):
    """
    Grabs the current events, and and isolates the "summary" and the "description". 
    Checks if the params are there, if they are then it updates the parameters.
    Else the summary and description remains the same.
    1. Checks if the creator of the event is the current user.
    2. Checks if the id is the same as the parameter.
    if the previous checks are true = Runs the update function
    if the previous checks are false = Prints error message
    """
    event = current_events(service, params[0])

    summary = event["summary"]
    description = event["description"]
    if len(params) == 3:
        summary = params[1]
        description = params[2]
    else:
        print("Please add what you would like to change.")
        return
    event['summary'] = summary
    event['description'] = description

    if (event["creator"]['email']) == (user_name + '@student.wethinkcode.co.za'):
        if (event["id"]) == params[0]:
            updaters(service, event)
            return
        else:
            print("The ID's do not match, please try again.")
    else:
        print("This is not your slot, please choose your own slot.")


    return