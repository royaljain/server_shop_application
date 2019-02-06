import image_processing
import db_interface
import json



def identify_employee(file_stream):
    encodings = image_processing.get_encodings(file_stream)
    found = db_interface.find_employee_in_db(encodings)

    if found:
        return json.dumps({'Identified': 'Success'})
    else:
        return json.dumps({'Identified': 'Failure'})      
