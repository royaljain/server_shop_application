
import config
import psycopg2
import uuid

conn = psycopg2.connect(database=config.DATABASE, user = config.USER, 
    password = config.PASSWORD, host = config.HOST)



def add_consumer(string_encoding):

    cur = conn.cursor()
    consumer_id = str(uuid.uuid1()).replace("-","")
    cur.execute("INSERT INTO consumer_attributes VALUES (%s, NULL, 0, 0, 0, NULL)", (consumer_id,));
    cur.execute("INSERT INTO consumer_faces VALUES (%s, %s)", (consumer_id, string_encoding))
    cur.close()

    conn.commit()
    return consumer_id


def add_employee_in_db(employee_id, encodings, name, manager, store_id, number, entry_time, exit_time):


    cur = conn.cursor()
    string_encoding = list(encodings)

    entry_time = '{:02d}:00:00'.format(int(entry_time))
    exit_time = '{:02d}:00:00'.format(int(exit_time))
    cur.execute("INSERT INTO employee_attributes VALUES (%s, %s, %s, %s, %s, %s, 0, 0)", (employee_id, name, manager, store_id, entry_time, exit_time));

    cur.execute("INSERT INTO employee_faces VALUES (%s, %s)", (employee_id, string_encoding))

    cur.close()
    conn.commit()
    return employee_id




def find_employee_in_db(encoding):
    cur = conn.cursor()
    string_encoding = list(encoding)

    cur.execute("SELECT employeeId, distance(encodings, %s) FROM employee_faces ORDER BY distance(employee_faces.encodings, %s) LIMIT 1", (string_encoding, string_encoding))
    
    response = cur.fetchone()
    cur.close()

    if response is None:
        return -1, False

    else:
        employee_id, distance = response

        print('CLOSEST EMPLOYEE : ', employee_id, ' : ', str(distance))

        if employee_id is None or (distance < config.FACE_THRESHOLD):
            return employee_id, True

        else:
            return -1, False

def employee_sign_in(employee_id, time_stamp):
    pass

def employee_sign_out(employee_id, time_stamp):
    pass

def find_closest_face_in_db(encoding):

    cur = conn.cursor()
    string_encoding = list(encoding)

    cur.execute("SELECT ConsumerId, distance(encodings, %s) FROM consumer_faces ORDER BY distance(consumer_faces.encodings, %s) LIMIT 1", (string_encoding, string_encoding))
   
    response = cur.fetchone()

    if response is None:
        cur.close()
        return add_consumer(string_encoding), True

    else:
        consumer_id, distance = response

        if consumer_id is None or (distance > config.FACE_THRESHOLD):
            cur.close()
            return add_consumer(string_encoding), True

        else:
            cur.close()
            return consumer_id, False


def get_default_menu(store_id):

    cur = conn.cursor()
    cur.execute("SELECT *  FROM store_menu WHERE storeid = %s", (store_id,))
    #cur.execute(query)

    responses = cur.fetchall()

    cur.close()

    menu_and_pos = []

    for response in responses:

        tag = response[7]

        if tag is None:
            tag = ""

        menu_and_pos.append(({'dishId': response[1], 'dishName': response[2], 'dishDescription': response[3], 'dishImage': response[4], 'dishCategory': response[5], 'sellingPrice': response[6], 'tag': tag, 'rating': response[8]}, response[9]))


    menu = list(map(lambda x: x[0], sorted(menu_and_pos, key = lambda x: x[1])))
 
    return menu



def get_consumer_company(consumer_id):
    cur = conn.cursor()
    cur.execute("SELECT CompanyId  FROM consumer_attributes WHERE ConsumerId = %s", (consumer_id,))

    response = cur.fetchone()

    cur.close()

    return response


def get_store_discount(store_id):

    cur = conn.cursor()
    cur.execute("SELECT *  FROM store_discount WHERE StoreId = %s", (store_id,))

    responses = cur.fetchall()

    cur.close()

    discount_dictionary = {}

    for response in responses:
        discount_dictionary[response[0]] = response[2]

    return discount_dictionary


def get_consumer_discount(consumer_id):

    cur = conn.cursor()
    cur.execute("SELECT *  FROM consumer_discount WHERE ConsumerId = %s", (consumer_id,))

    responses = cur.fetchall()

    cur.close()

    discount_dictionary = {}

    for response in responses:
        discount_dictionary[response[0]] = response[2]

    return discount_dictionary


def get_company_discount(company_id):

    cur = conn.cursor()
    cur.execute("SELECT *  FROM company_discount WHERE Company_id = %s", (company_id,))

    response = cur.fetchone()

    if response is None:
        return 0

    cur.close()

    discount = response[0]

    return discount


def get_dish_count(consumer_id):
    cur = conn.cursor()
    cur.execute("SELECT *  FROM consumer_dish_count WHERE ConsumerId = %s", (consumer_id,))

    responses = cur.fetchall()

    cur.close()

    dish_count = {}

    for response in responses:
        dish_count[response[1]] = response[2]

    return dish_count

