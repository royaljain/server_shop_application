import image_processing
import db_interface
import json
from utils import safe_run
from gcloud import storage


def add_dish(file_path, dish_id, store_ids, dish_name, dish_desc, dish_tag, dish_price, dish_position, dish_cat):
    bucket_name = 'digital_menu'
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)


    for store_id in store_ids.split(','):
        object_name = 'testing/{}/{}'.format(store_id, dish_id)
        blob = bucket.blob(object_name)
        blob.upload_from_filename(file_path, content_type='image/jpeg')
        blob.make_public()
        url = "https://storage.googleapis.com/%s/%s" % (bucket_name, object_name)

        db_interface.add_dish_to_menu(dish_id, url, store_id, dish_name, dish_desc, dish_tag, dish_price, dish_position, dish_cat)

    return dish_id



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


def store_order(store_id, consumer_id, list_of_dishes, actual_prices, selling_prices, order_time):

    discount_saved = sum(actual_prices)
    money_spent = sum(selling_prices)
    return db_interface.add_consumer_attributes(consumer_id, money_spent, discount_saved, order_time)


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
