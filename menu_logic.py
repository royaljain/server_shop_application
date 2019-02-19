import image_processing
import db_interface
import json
from utils import safe_run
from gcloud import storage
from datetime import datetime
import pytz
import shutil
import logging
import uuid

def shop_server_request(store_id, order_id, consumer_id, list_of_dishes, selling_prices):

    texts = []

    dish_mapping = db_interface.get_dish_mapping(store_id)

    for i in range(0, len(list_of_dishes)):
        texts.append("{} : {}".format(dish_mapping[list_of_dishes[i]], selling_prices[i]))

    total = sum(list(map(lambda x: float(x), selling_prices)))

    texts.append("Total : {}".format(total))


    file_path = "./static/images/consumers/{}.png".format(consumer_id)
    text = "<br>".join(texts)
    return {"image_link": file_path, "text": text, "order_id": order_id}


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


@safe_run
def store_order(order_id, store_id, consumer_id, list_of_dishes, actual_prices, selling_prices, order_time):


    time_stamp = float(order_time) / 1000.0
    time_stamp = datetime.fromtimestamp(time_stamp, tz=pytz.utc)
    tz = pytz.timezone('Asia/Kolkata')
    time_stamp = time_stamp.astimezone(tz)

    selling_prices = list(map(lambda x: float(x), selling_prices))
    actual_prices = list(map(lambda x: float(x), actual_prices))


    discount_saved = sum(actual_prices) - sum(selling_prices)
    money_spent = sum(selling_prices)
    db_interface.add_consumer_attributes(consumer_id, money_spent, discount_saved, time_stamp)
    db_interface.store_order_details(order_id, store_id, consumer_id, list_of_dishes, actual_prices, selling_prices, time_stamp)

    return json.dumps({'status': 'Success'})


def compute_dish_position(consumer_id):
    dish_count = db_interface.get_dish_count(consumer_id)
    return dish_count


def apply_coupon(coupon_id):

    discount = db_interface.find_coupon(coupon_id)

    if discount == -1:
        return json.dumps({'success': 'False', 'discount': 0})
   
    return json.dumps({'success': 'True', 'discount': discount[0]})



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

    rand_str = str(uuid.uuid1())
    tmp_file_path = "./tmp/consumers/{}.png".format(rand_str)
    #file_stream.save(tmp_file_path)


    encodings = image_processing.get_encodings(file_stream)

    if len(encodings) == 0:
        return json.dumps({'proceedToMenu': False, 'customerId': -1, 'dishList': [], 'validImage': False})

    

    consumer_id, new_user = db_interface.find_closest_face_in_db(encodings)
    default_menu = db_interface.get_default_menu(store_id)


    new_file_path =  "./static/images/consumers/{}.png".format(consumer_id)
    #shutil.move(tmp_file_path, new_file_path)

    logging.info("CONSUMER : "  + consumer_id)

    dishes = list(map(lambda x: x['dishId'], default_menu))

    default_discount = get_default_discount(dishes)

    proceedToMenu = True

    if new_user:
        proceedToMenu = False

    return json.dumps({'proceedToMenu': proceedToMenu, 'customerId': consumer_id, 'dishList': default_discount, 'validImage': True})

    company_id = db_interface.get_consumer_company(consumer_id)
    discount_dictionary = {}

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

    return json.dumps({'proceedToMenu': proceedToMenu, 'customerId': consumer_id, 'dishList': response, 'validImage': True})
