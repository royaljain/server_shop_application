from flask import Flask, jsonify, request, redirect, render_template
import config
#import menu_logic
#from attendance_management import employee_sign_in, employee_sign_out, identify_employee, add_employee_to_db
import uuid
import json
from base64 import decodestring
import base64
import logging
import sys
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request
from random import random
from time import sleep
from threading import Thread, Event
from utils import timeit
import os
from flask import send_from_directory


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()



list_of_orders = []

dictionary_of_orders = {}

empty_div1, empty_div2, empty_div3 = True, True, True

def give_next_order():

    global list_of_orders
    global dictionary_of_orders

    order_id = list_of_orders[0]
    order = dictionary_of_orders[order_id]
    image_link = order['image_link']
    text = order['text']
    return image_link, text

def delete_order():

    global list_of_orders
    global dictionary_of_orders

    order_id = list_of_orders[0]
    order = dictionary_of_orders[order_id]
                        
    list_of_orders = list_of_orders[1:]
    del dictionary_of_orders[order_id]


class RandomThread(Thread):
    def __init__(self):
        self.delay = 5
        super(RandomThread, self).__init__()

    def orderPush(self):
        ctr = 0

        global empty_div1
        global empty_div2
        global empty_div3


        while True:
            
            if len(list_of_orders) > 0:

                if empty_div1:
                        image_link, text = give_next_order()                        
                        socketio.emit('my-image-event1', {'image_link': image_link}, namespace='/test')
                        socketio.emit('my-text-event1', {'text': text}, namespace='/test')
                        delete_order()
                        empty_div1 = False

                elif empty_div2:
                        image_link, text = give_next_order()                        
                        socketio.emit('my-image-event2', {'image_link': image_link}, namespace='/test')
                        socketio.emit('my-text-event2', {'text': text}, namespace='/test')
                        delete_order()
                        empty_div2 = False

                elif empty_div3:
                        image_link, text = give_next_order()                        
                        socketio.emit('my-image-event3', {'image_link': image_link}, namespace='/test')
                        socketio.emit('my-text-event3', {'text': text}, namespace='/test')
                        delete_order()
                        empty_div3 = False



            sleep(self.delay)

    def run(self):
        self.orderPush()

@socketio.on('empty_div_1', namespace='/test')
def func_empty_div1():
    global empty_div1
    empty_div1 = True

@socketio.on('empty_div_2', namespace='/test')
def func_empty_div2():
    global empty_div2
    empty_div2 = True

@socketio.on('empty_div_3', namespace='/test')
def func_empty_div3():
    global empty_div3
    empty_div3 = True


@app.route('/completed_orders_page')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('shopkeeper.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@app.route('/add_order', methods=['POST'])
def add_order():
    content = request.json
    print(content)
    image_link = content['image_link']
    text = content['text']
    order_id = content['order_id']

    list_of_orders.append(order_id)
    dictionary_of_orders[order_id] = {'image_link': image_link, 'text': text}

    return json.dumps({'status': 'Success'})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/images/icons'), 'favicon.ico')


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5002)
    #app.run(host='0.0.0.0', port=5001, debug=True)
