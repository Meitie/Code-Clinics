import json, datetime, sys, os
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS + "/")
from api_calls import serives_maker, event_maker


def user_name_func():
    '''
    Asking for the username, therfore it can connect to their email address
    '''
    user_name = input((f"Enter your WeThinkCode Student User_Name: "))
    return user_name


def log_in_checker():
    """
    Checks the user log in info:
    Checks if the expiry time in the user_info file has expired or not.
    Checks for the user roles and sets them up if they do not exist.
    """
    user_name = ''
    with open('.user_info.json', 'r+') as f:
        data = json.load(f)
    if data['expire'] == '':
        data['expire'] = datetime.datetime.now() + datetime.timedelta(hours=8)
        data['expire'] = data['expire'].strftime("%Y/%m/%d, %H:%M:%S")
        with open('.user_info.json', 'w+') as f:
            json.dump(data, f)
    elif datetime.datetime.strptime(data['expire'],'%Y/%m/%d, %H:%M:%S') > datetime.datetime.now():
        return data['user'],data['role']
    else:
        try:
            os.remove('token.pickle')
        except:
            pass
        data['user'] = ''
        data['role'] = ''
        data['expire'] = datetime.datetime.now() + datetime.timedelta(hours=8)
        data['expire'] = data['expire'].strftime("%Y/%m/%d, %H:%M:%S")
        with open('.user_info.json', 'w+') as f:
            json.dump(data, f)
    if data['user'] == '':
        user_name = user_name_func()
        serives_maker.creating_service()
        data['user'] = user_name
        with open('.user_info.json', 'w+') as f:
            json.dump(data, f)
    return data['user']
