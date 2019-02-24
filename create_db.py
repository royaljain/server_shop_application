from glob import glob
from random import randint
import datetime
import menu_logic
from attendance_management import employee_sign_in, employee_sign_out, add_employee_to_db
import uuid
import names
import time
from random import shuffle

queries = []


stores = ['store1', 'store2', 'store3']
companies = ['company1', 'company2']
dishes = ['dish1', 'dish2', 'dish3', 'dish4', 'dish5', 'dish6', 'dish7', 'dish8']
actual_prices = ['100', '66', '43', '56', '59','98','44','67']
selling_prices = ['90', '56', '23', '46', '57','88','34','57']

employee_photos = glob('employees/*')
print(employee_photos)

'''
for photo in employee_photos:
    employee_id = str(uuid.uuid1())
    name = names.get_first_name()
    manager =  names.get_first_name()
    store = stores[randint(0, 2)]
    ntime = randint(1, 10)
    working_hours = randint(8, 12)
    phone = str(uuid.uuid1())
    add_employee_to_db(employee_id, photo, name, manager, store, ntime, working_hours, phone)
'''


for photo in employee_photos:

    for i in range(1, 28):

        if randint(0, 7) >= 6:
            continue

        dt_sign_in = datetime.datetime(2019, 2, i, randint(2, 6) ,30)
        dt_sign_out = datetime.datetime(2019, 2, i, randint(14, 18) ,30)
        dt_sign_in_ = 1000.0*time.mktime(dt_sign_in.timetuple())
        dt_sign_out_ = 1000.0*time.mktime(dt_sign_out.timetuple())

        try:        
            employee_sign_in(photo, dt_sign_in_)
            time.sleep(1)
            employee_sign_out(photo, dt_sign_out_)
        except:
            print(dt_sign_out)
            
            pass

'''
import json

consumer_photos = glob('consumers/*')



for photo in consumer_photos:
    for i in range(1, 28):

        if randint(0, 7) >= 6:
            continue

        store = stores[randint(0, 2)]
        consumer_id = json.loads(menu_logic.compute_menu_response(photo, store))['customerId']
        order_id = str(uuid.uuid1())
        order_time = datetime.datetime(2019, 2, i, randint(3, 15) ,30)
        order_time = 1000.0*time.mktime(order_time.timetuple())
        indices = list(range(0, 8))
        shuffle(indices)

        list_of_dishes, list_of_selling_prices, list_of_actual_prices = [], [], []
        
        for index in indices[:3]:
            list_of_dishes.append(dishes[index])
            list_of_actual_prices.append(actual_prices[index])
            list_of_selling_prices.append(selling_prices[index])


        menu_logic.store_order(order_id, store, consumer_id, list_of_dishes, list_of_actual_prices, 
            list_of_selling_prices, order_time)
'''
