import image_processing
import db_interface
import json
from datetime import datetime
import pytz


def add_employee_to_db(employee_id,  file_stream, name, manager, store_id, entry_time, working_hour, number):
    encodings = image_processing.get_encodings(file_stream)

    if len(encodings) == 0:
        print('NOT A FACE IMAGE')
        return json.dumps({'employeeAddition': False, 'employeeId': -1})


    employee_id = db_interface.add_employee_in_db(employee_id, encodings, name, manager, store_id, number, entry_time, working_hour)

    return json.dumps({'employeeAddition': True, 'employeeId': employee_id})

def identify_employee(file_stream):
    encodings = image_processing.get_encodings(file_stream)

    if len(encodings) == 0:
        return -1, False

    employee_id, found = db_interface.find_employee_in_db(encodings)

    return employee_id, found

def employee_sign_in(file_stream, time_stamp):

    employee_id, found = identify_employee(file_stream)

    if found:

        time_stamp = float(time_stamp) / 1000.0
        time_stamp = datetime.fromtimestamp(time_stamp, tz=pytz.utc)
        tz = pytz.timezone('Asia/Kolkata')
        time_stamp = time_stamp.astimezone(tz)

        db_interface.employee_sign_in(employee_id, time_stamp)
        return json.dumps({'identificationSuccesful': 'Success', 
                         'employeeName': 'RandomStringForNow'})
    else:
        return json.dumps({'identificationSuccesful': 'Failure',
'employeeName': 'RandomStringForNow'})


def employee_sign_out(file_stream, time_stamp):

    employee_id, found = identify_employee(file_stream)

    if found:
        time_stamp = float(time_stamp) / 1000.0
        time_stamp = datetime.fromtimestamp(time_stamp, tz=pytz.utc)
        tz = pytz.timezone('Asia/Kolkata')
        time_stamp = time_stamp.astimezone(tz)

        db_interface.employee_sign_out(employee_id, time_stamp)
        return json.dumps({'identificationSuccesful': 'Success',
'employeeName': 'RandomStringForNow'})
    else:
        return json.dumps({'identificationSuccesful': 'Failure',
'employeeName': 'RandomStringForNow'})
