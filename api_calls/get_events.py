import datetime, json

def get_code_clinic_events(service, future_date):
    """
    Creates the calendar based on the days that will need to show up for the given days
    """
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    a_week = datetime.date.today() + datetime.timedelta(days=future_date)
    a_week = str(a_week) + 'T23:59:59.999999+02:00'
    # print(f'Getting the upcoming {future_date} days events of your calendar')
    events_result = service.events().list(calendarId='teamtwotesting@gmail.com', timeMin=now,
                                          timeMax=a_week, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    with open('.calendar_ttt.json', 'w+') as f:
        json.dump(events, f)
    return events


def get_user_events(service, future_date):
    """
    Creates the calendar based on the days that will need to show up for the given days
    """
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    a_week = datetime.date.today() + datetime.timedelta(days=future_date)
    a_week = str(a_week) + 'T23:59:59.999999+02:00'
    # print(f'Getting the upcoming {future_date} days events of your calendar')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=a_week, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    with open('.calendar.json', 'w+') as f:
        json.dump(events, f)
    return events