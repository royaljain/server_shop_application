from flask import Flask, jsonify, request, redirect
import config
import menu_logic
from attendance_management import identify_employee

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

from utils import timeit


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
@app.route('/process_employee_image', methods=['POST'])
def process_employee_image():
    # Check if a valid image file was uploaded

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']



    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # The image file seems valid! Detect faces and return the result.
        
        return identify_employee(file)

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
