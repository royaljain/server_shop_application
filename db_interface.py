
import config
import psycopg2
import uuid
from datetime import datetime, date
from utils import safe_run


conn = psycopg2.connect(database=config.DATABASE, user = config.USER, 
    password = config.PASSWORD, host = config.HOST)



def find_coupon(coupon_id):
    cur = conn.cursor()
    cur.execute("SELECT discount from coupon_attributes WHERE couponId=%s", (coupon_id,))
    response = cur.fetchone()
    if response is None:
        return -1
    return response



@safe_run
def add_dish_to_menu(dish_id, url, store_id, dish_name, dish_desc, dish_tag, dish_price, dish_position, dish_cat):

    cur = conn.cursor()

    cur.execute("SELECT * from dish_attributes WHERE dishId=%s", (dish_id,))
    response = cur.fetchone()

    if response is None:
        cur.execute("INSERT INTO  dish_attributes VALUES (%s)", (dish_id,))


    cur.execute("INSERT INTO store_menu VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 4.3, %s)", (store_id, dish_id, dish_name, dish_desc, url, dish_cat, dish_price, dish_tag, dish_position))
    cur.close()

    conn.commit()
    return {'status': 'Success'}


    

def add_consumer(string_encoding):

    cur = conn.cursor()
    consumer_id = str(uuid.uuid1()).replace("-","")
    cur.execute("INSERT INTO consumer_attributes VALUES (%s, NULL, 0, 0, 0, NULL)", (consumer_id,));
    cur.execute("INSERT INTO consumer_faces VALUES (%s, %s)", (consumer_id, string_encoding))
    cur.close()

    conn.commit()
    return consumer_id


def add_employee_in_db(employee_id, encodings, name, manager, store_id, number, entry_time, working_hour):


    cur = conn.cursor()
    string_encoding = list(encodings)

    entry_time = '{:02d}:00:00'.format(int(entry_time))
    cur.execute("INSERT INTO employee_attributes VALUES (%s, %s, %s, %s, %s, 0, 0, %s)", (employee_id, name, manager, store_id, entry_time, working_hour));

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

@safe_run
def add_consumer_attributes(consumer_id, money_spent, discount_saved, order_time):
 
    cur = conn.cursor()
    dt = order_time.date()

    cur.execute("SELECT * from  consumer_attributes where consumerId= %s", (consumer_id,))

    consumerid, lastvisit, numberofvisits, moneyspent, discountsaved, companyid = cur.fetchone()

    moneyspent += money_spent
    discountsaved += discount_saved
    numberofvisits += 1
    lastvisit = dt 

    cur.execute("UPDATE consumer_attributes SET moneyspent=%s, discountsaved=%s, numberofvisits=%s, lastvisit=%s where consumerId=%s", (moneyspent, discountsaved, numberofvisits, lastvisit, consumerid));

    cur.close()
    conn.commit()


    return {'status': 'Success'}


@safe_run
def store_order_details(store_id, consumer_id, list_of_dishes, actual_prices, selling_prices, order_time):
 
    cur = conn.cursor()
    order_date = order_time.date()
    order_time = order_time.time()

    order_id = str(uuid.uuid1())

    for i, dish_id in enumerate(list_of_dishes):
        cur.execute("INSERT INTO order_details VALUES (%s, %s, %s, %s, %s, %s, NULL, %s, %s);", (order_id, consumer_id, store_id, dish_id, selling_prices[i], actual_prices[i]-selling_prices[i], order_date, order_time));

    cur.close()
    conn.commit()


    return {'status': 'Success'}


def employee_sign_in(employee_id, time_stamp):

    cur = conn.cursor()
    dt = time_stamp.date()
    tm = time_stamp.time()

    cur.execute("SELECT timein from employee_attributes WHERE employeeId=%s", (employee_id,))

    scheduled_time = cur.fetchone()[0]
    is_late = 0


    if tm > scheduled_time:
        is_late = 1

    cur.execute("INSERT INTO employee_register VALUES (%s, %s, %s, NULL, %s, NULL, NULL)", (employee_id, dt, tm, is_late));

    cur.close()
    conn.commit()
    return employee_id


def diff_times_in_hours(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( t2_secs - t1_secs)/3600.0



def employee_sign_out(employee_id, time_stamp):
 
    cur = conn.cursor()
    dt = time_stamp.date()
    tm = time_stamp.time()


    
    is_overtime = 0

    cur.execute("SELECT timein, workinghour, numberofdaysworking, averageworkinghour from employee_attributes WHERE employeeId=%s", (employee_id,))

    timein, scheduledhours, numberofdaysworking, averageworkinghour = cur.fetchone()
 
    cur.execute("SELECT intime from employee_register WHERE employeeId=%s and entrydate=%s", (employee_id, dt))

    intime = cur.fetchone()[0]

    work_time_interval = datetime.combine(date.min, tm) - datetime.combine(date.min, intime)

    work_time = work_time_interval.total_seconds()/3600.0

    if work_time > scheduledhours:
        is_overtime = 1

    new_numberofdaysworking = numberofdaysworking + 1
    new_averageworkinghour = (numberofdaysworking*averageworkinghour + work_time) / new_numberofdaysworking

    cur.execute("UPDATE employee_register SET outtime=%s, isovertime=%s, hoursworked=%s WHERE employeeId=%s and entrydate=%s", (tm, is_overtime,work_time_interval, employee_id, dt));
    cur.execute("UPDATE employee_attributes SET numberofdaysworking=%s, averageworkinghour=%s WHERE employeeId=%s", (new_numberofdaysworking, new_averageworkinghour, employee_id));


    cur.close()
    conn.commit()

    return employee_id


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
        discount_dictionary[response[1]] = response[2]

    return discount_dictionary


def get_consumer_discount(consumer_id):

    cur = conn.cursor()
    cur.execute("SELECT *  FROM consumer_discount WHERE ConsumerId = %s", (consumer_id,))

    responses = cur.fetchall()

    cur.close()

    discount_dictionary = {}

    for response in responses:
        discount_dictionary[response[1]] = response[2]

    return discount_dictionary


def get_company_discount(company_id):

    if company_id is None:
        return 0

    cur = conn.cursor()
    cur.execute("SELECT *  FROM company_discount WHERE companyId=%s", (company_id,))

    response = cur.fetchone()

    if response is None:
        return 0

    cur.close()

    discount = response[0]

    return discount


def get_dish_count(consumer_id):
    cur = conn.cursor()
    cur.execute("SELECT dishId, COUNT(*) from order_details WHERE consumerId=%s GROUP BY dishId;", (consumer_id,))

    responses = cur.fetchall()

    cur.close()

    dish_count = {}

    for response in responses:
        dish_count[response[0]] = response[1]

    return dish_count

