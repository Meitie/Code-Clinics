def deleted(service, eventsID):
    """
    Trys to execute the service call to delete the event off the 'code-clinics' calenar.
    If it success print "Your event has been deleted"
    else prints "That is not an existing event"
    """
    try:
        service.events().delete(calendarId='teamtwotesting@gmail.com',
                                   eventId=eventsID).execute()
        print("Your event has been deleted")
    except:
        print("That is not an existing event")


def delete_event(delete_id ,service, user_name, events):
    """
    Converts the "delete_id" list into a string.
    checks each item that has the same ID as the delete id from the events.
    1. if the creator is the same as the person logged in.
    2. if the id is the same as the one we want to delete.
    If both are true: run the deleted function and return.
    else: Show the errors that are related.
    """
    delete_id = ''.join(delete_id)
    canllelation = [item for item in events if item["id"] == delete_id]
    if (canllelation[0]["creator"]['email']) == (user_name + '@student.wethinkcode.co.za'):
        if (canllelation[0]["id"]) == delete_id:
            deleted(service, delete_id)
            return
        else:
            print("The ID's do not match, please try again.")
    else:
        print("This is not your slot, please choose your own slot.")