import unittest
from unittest.mock import patch
import io, os
import sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../'))
sys.path.insert(0, USER_PATHS + "/")
import clinician.insert as insert


class Test_Insert(unittest.TestCase):

    text = io.StringIO()
    sys.stdout = text

    def test_valid_date(self):
        self.assertTrue(insert.valid_date('2020-11-20'))
        self.assertFalse(insert.valid_date('2002020-123-200'))

    def test_valid_time(self):
        self.assertTrue(insert.valid_time('12:05'))
        self.assertFalse(insert.valid_time('132:102'))

    def test_validate_params(self):
        result1 = insert.validate_params([])
        result2 = insert.validate_params(['','',''])
        result3 = insert.validate_params(['2020-13-20','14:30'])
        self.assertEqual(result1,('',''))
        self.assertEqual(result2,('',''))
        self.assertEqual(result3,('2020-13-20','14:30'))
  
    def test_meetings_setups(self):
        result1 = insert.meeting_setups([],'John')
        result2 = insert.meeting_setups(['TR5','Help'],'John')
        self.assertEqual(result1,('John','Open for anything'))
        self.assertEqual(result2,('TR5','Help'))

    def test_clearing_dates(self):
        table_data = [["", "2020-12-11","2020-12-12","2020-12-13","2020-12-14"], ["8:30", "", "", "", "", ""]]
        output = ["2020-12-11","2020-12-12","2020-12-13","2020-12-14"]
        self.assertEqual(output, insert.clearing_dates(table_data))

    def test_valid_slot(self):
        table_data1 = [["", "2020-12-11","2020-12-12","2020-12-13","2020-12-14"], ["8:30", "", "", "", ""]]
        date1 = "2020-12-11"
        time1 = "08:00"
        table_data2 = [["", "2020-12-11","2020-12-12","2020-12-13","2020-12-14"], ["8:30", "", "", "", ""]]
        date2 = "2020-10-11"
        time2 = "07:00"
        self.assertEqual(True, insert.validated_slot(table_data1, date1, time1))
        self.assertEqual(False, insert.validated_slot(table_data2, date2, time2))

    def test_user_pre_slotted(self):
        cc_events = [{'kind': 'calendar#event', 'etag': '"3215770090430000"', 'id': 'ni5vqtiuhlrus1thgu0s512614', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bmk1dnF0aXVobHJ1czF0aGd1MHM1MTI2MTQgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T18:44:05.000Z', 'updated': '2020-12-13T18:44:05.241Z', 'summary': 'msegal', 'description': 'bob', 'creator': {'email': 'msegal@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-14T08:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-14T08:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'ni5vqtiuhlrus1thgu0s512614@google.com', 'sequence': 0, 'attendees': [{'email': 'msegal@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 10}]}}, {'kind': 'calendar#event', 'etag': '"3215769712086000"', 'id': 'utg8d7rhacjelm6pbip3k6s7b0', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=dXRnOGQ3cmhhY2plbG02cGJpcDNrNnM3YjAgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T18:40:55.000Z', 'updated': '2020-12-13T18:40:56.043Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'bthompso@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-15T08:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-15T09:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'utg8d7rhacjelm6pbip3k6s7b0@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215769713294000"', 'id': 'lcdglktnqvc0ah5rgg5kl50km4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=bGNkZ2xrdG5xdmMwYWg1cmdnNWtsNTBrbTQgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T18:40:56.000Z', 'updated': '2020-12-13T18:40:56.647Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'bthompso@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-15T09:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-15T09:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'lcdglktnqvc0ah5rgg5kl50km4@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215769714428000"', 'id': '3ad7on18b73b0db93802pai924', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=M2FkN29uMThiNzNiMGRiOTM4MDJwYWk5MjQgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T18:40:57.000Z', 'updated': '2020-12-13T18:40:57.214Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'bthompso@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-15T09:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-15T10:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '3ad7on18b73b0db93802pai924@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215688654247000"', 'id': 'drtn3tedh6bf2a5a6k2p3s0gi0', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ZHJ0bjN0ZWRoNmJmMmE1YTZrMnAzczBnaTAgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T07:25:26.000Z', 'updated': '2020-12-13T07:25:27.249Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'msegal@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-15T17:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-15T18:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'drtn3tedh6bf2a5a6k2p3s0gi0@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 10}]}}, {'kind': 'calendar#event', 'etag': '"3215709853168000"', 'id': 'u3g7t0amfcagajettrusfk7vek', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=dTNnN3QwYW1mY2FnYWpldHRydXNmazd2ZWsgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T10:22:06.000Z', 'updated': '2020-12-13T10:22:06.584Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'bthompso@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-17T11:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-17T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'u3g7t0amfcagajettrusfk7vek@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215709853996000"', 'id': 'olqegk5072cutpacmfodc31568', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=b2xxZWdrNTA3MmN1dHBhY21mb2RjMzE1NjggdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T10:22:06.000Z', 'updated': '2020-12-13T10:22:06.998Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'bthompso@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-17T12:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-17T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'olqegk5072cutpacmfodc31568@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215709855086000"', 'id': 'j3a2gq3lf6ku8sspcmctjlla7g', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=ajNhMmdxM2xmNmt1OHNzcGNtY3RqbGxhN2cgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T10:22:07.000Z', 'updated': '2020-12-13T10:22:07.543Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'bthompso@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-17T12:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-17T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'j3a2gq3lf6ku8sspcmctjlla7g@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': True}}, {'kind': 'calendar#event', 'etag': '"3215689156371000"', 'id': '8md0rm6hnogfhgiiepmfdj46a4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=OG1kMHJtNmhub2dmaGdpaWVwbWZkajQ2YTQgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T07:29:38.000Z', 'updated': '2020-12-13T07:29:38.227Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'msegal@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-19T13:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-19T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '8md0rm6hnogfhgiiepmfdj46a4@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 10}]}}, {'kind': 'calendar#event', 'etag': '"3215689157477000"', 'id': 'a0ppq0ldb2jejhs2khnjqhvopc', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=YTBwcHEwbGRiMmplamhzMmtobmpxaHZvcGMgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T07:29:38.000Z', 'updated': '2020-12-13T07:29:38.817Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'msegal@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-19T13:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-19T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': 'a0ppq0ldb2jejhs2khnjqhvopc@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 10}]}}, {'kind': 'calendar#event', 'etag': '"3215689158791000"', 'id': '6jnuq6o54v8bqucouj7s178fu4', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=NmpudXE2bzU0djhicXVjb3VqN3MxNzhmdTQgdGVhbXR3b3Rlc3RpbmdAbQ', 'created': '2020-12-13T07:29:39.000Z', 'updated': '2020-12-13T07:29:39.471Z', 'summary': 'bthompso', 'description': 'Open for anything', 'creator': {'email': 'msegal@student.wethinkcode.co.za'}, 'organizer': {'email': 'teamtwotesting@gmail.com', 'self': True}, 'start': {'dateTime': '2020-12-19T14:00:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'end': {'dateTime': '2020-12-19T14:30:00+02:00', 'timeZone': 'Africa/Johannesburg'}, 'iCalUID': '6jnuq6o54v8bqucouj7s178fu4@google.com', 'sequence': 0, 'attendees': [{'email': 'bthompso@student.wethinkcode.co.za', 'responseStatus': 'needsAction'}], 'anyoneCanAddSelf': True, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 10}]}}]
        output = ['2020-12-14T08:00:00+02:00', '2020-12-15T17:30:00+02:00', '2020-12-19T13:00:00+02:00', '2020-12-19T13:30:00+02:00', '2020-12-19T14:00:00+02:00']
        self.assertEqual(output, insert.user_pre_slotted(cc_events, "msegal"))
        self.assertNotEqual([], insert.user_pre_slotted(cc_events, "msegal"))

    def test_already_booked(self):
        slots = ['2020-12-14T08:00:00+02:00', '2020-12-15T17:30:00+02:00', '2020-12-19T13:00:00+02:00', '2020-12-19T13:30:00+02:00', '2020-12-19T14:00:00+02:00']
        self.assertFalse(insert.already_booked(slots, "2020-12-14", "08:00"))
        self.assertTrue(insert.already_booked(slots, "2020-10-14", "07:30"))

    


if __name__ == '__main__':
    unittest.main()
    
