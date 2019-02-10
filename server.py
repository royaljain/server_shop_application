from flask import Flask, jsonify, request, redirect, render_template
import config
import menu_logic
from attendance_management import employee_sign_in, employee_sign_out, identify_employee, add_employee_to_db
import uuid
import json
from base64 import decodestring
import base64
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

from utils import timeit
import os




@app.route('/add_employee_page', methods=['GET'])
def load_index():

    return render_template('index.html')


@app.route('/add_employee', methods=['POST'])
def add_employee():

    try: 
        if not os.path.exists('./tmp/'):
            os.mkdir('./tmp/')

        employee_id = str(uuid.uuid1())
        employee_id = employee_id.replace('-','')
        token = request.json

        img_data = token['image'].replace("data:image/png;base64,","")
        file_path = "./tmp/{}.png".format(employee_id)
        with open(file_path, "wb") as fh:
            fh.write(base64.decodebytes(img_data.encode()))


        name = token['name']
        manager = token['manager']
        phone = token['phone']
        store = token['store']
        entry_time = token['time_in']
        exit_time = token['time_out']

        return add_employee_to_db(employee_id, file_path, name, manager, store, entry_time, exit_time, phone)

    except Exception as e:
        print(e)
        return json.dumps({'employeeAddition': False, 'employeeId': '-1'})


    finally:
        try:
            pass
            #os.remove(file_path)
        except:
            pass




@timeit
@app.route('/process_image', methods=['POST'])
def process_image():
    # Check if a valid image file was uploaded

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # The image file seems valid! Detect faces and return the result.
        store_id = request.args.get('storeId')
        response = menu_logic.compute_menu_response(file, store_id)
        print(response)


        return response

@timeit
@app.route('/employee_sign_in', methods=['POST'])
def process_employee_signin():
    # Check if a valid image file was uploaded

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        sign_in_time = request.args.get('timestamp')

        return employee_sign_in(file, sign_in_time)


@timeit
@app.route('/employee_sign_out', methods=['POST'])
def process_employee_signout():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        sign_out_time = request.args.get('timestamp')
        return employee_sign_out(file, sign_out_time)




@timeit
@app.route('/store_details', methods=['POST'])
def store_details():
    store_id = request.args.get('storeId')
    response = menu_logic.compute_menu_response(file, store_id)

    return response

@timeit
@app.route('/apply_coupon', methods=['POST'])
def process_coupons():
    coupon_id = request.args.get('coupon')
    response = menu_logic.apply_coupon(coupon_id)

    return response


@timeit
@app.route('/default_menu', methods=['GET', 'POST'])
def get_default_menu():
    store_id = request.args.get('storeId')
    return menu_logic.get_default_menu(store_id)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
