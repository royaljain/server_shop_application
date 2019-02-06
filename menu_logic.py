import image_processing
import db_interface
import json

def compute_dish_discount(consumer_id, company_id, store_id):
    store_discount = db_interface.get_store_discount(store_id)
    consumer_discount = db_interface.get_consumer_discount(consumer_id)
    company_discount = db_interface.get_company_discount(company_id)

    discount_dictionary = {}

    for k in list(consumer_discount.keys()) + list(store_discount.keys()):
        default_discount = 0
        
        if k in consumer_discount:
            default_discount = max(consumer_discount[k], default_discount)
        if k in store_discount:
            default_discount = max(store_discount[k], default_discount)
        
        default_discount = max(company_discount, default_discount)

    return discount_dictionary


def compute_dish_position(consumer_id):
    dish_count = db_interface.get_dish_count(consumer_id)
    return dish_count


def apply_coupon(coupon_id):
    return json.dumps({'Valid': 'Success', 'Discount': 7})



def get_default_menu(store_id):

    dish_list = db_interface.get_default_menu(store_id)
    response = {"storeId": store_id,
                "dishList": dish_list}

    return json.dumps(response)


import random
from random import shuffle


def get_default_discount(dishes):
    

    indices = list(range(0, len(dishes)))
    shuffle(indices)

    ctr = 0

    response = []

    for dish in dishes:

        discount = random.randint(0, 20)
        response.append({'dishId': dish, 'discount': discount,'position': indices[ctr]})
        ctr += 1

    return response


def compute_menu_response(file_stream, store_id):
    encodings = image_processing.get_encodings(file_stream)
    consumer_id, new_user = db_interface.find_closest_face_in_db(encodings)
    default_menu = db_interface.get_default_menu(store_id)

    dishes = list(map(lambda x: x['dishId'], default_menu))

    default_discount = get_default_discount(dishes)

    return json.dumps({'customerId': consumer_id, 'dishList': default_discount})

    company_id = db_interface.get_consumer_company(consumer_id)
    discount_dictionary = {}

    if not new_user:
        discount_dictionary = compute_dish_discount(consumer_id, company_id, store_id)

    dish_count = compute_dish_position(consumer_id)

    for dish in default_menu:
        dish_id = dish['dishId']
        if not (dish_id in dish_count):
            dish_count[dish_id] = 0 

    sorted_dishes = sorted(list(dish_id.keys()), key=lambda x: dish_count[x])

    dish_position = {}

    for i, dish_id in enumerate(sorted_dishes):
        dish_position[dish_id] = i

    response = []


    for dish in default_menu:
        dish_id = dish['dishId']
        dish_dic = {'dishId': dish_id}

        if dish_id in discount_dictionary:
            dish_dic['discount'] = discount_dictionary[dish_id]
        else:
            dish_dic['discount'] = 0

        dish_dic['position'] = dish_position[dish_id]


        response.append(dish_dic)

    return json.dumps(response)
