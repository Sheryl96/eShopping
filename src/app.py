from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file
from datetime import datetime
import hashlib

app = Flask(__name__)

import db.rds_db as db
from responseHelper.oder_details_response_helper import OrderDetailsResponseHelper
import json

@app.route('/')
def index():
    return "Hello World"

@app.route('/orders/orderDetails/orderDate', methods=['GET'])
def products_sold():
    args = request.args 
    # Extract query params
    start_date = args['startDate']
    end_date = args['endDate']
    limit = args.get('limit', default=10) # not implemented but for future extensibility
    group_by = args['groupBy']
    offset = args.get('offset', default=0) # not implemented but for future extensibility
    fields = args.get('fields', default='').split(",")

    # Get details from DB
    result, row_headers = db.get_sold_products(start_date, end_date)
    result = list(result)

    # conver the result to a dict for easier parsing
    json_data = []
    for r in result:
        json_data.append(dict(zip(row_headers, r)))
    
    # return all fields if not passed in query
    if (len(fields) == 1 and fields[0] == ''):
        fields = row_headers


    # Parse response based on required grouping
    response_helper = OrderDetailsResponseHelper(json_data, start_date, end_date)
    if (group_by == 'day'):
        response_list = response_helper.group_by_date(limit, offset, fields)
    elif (group_by == 'month'):
        response_list = response_helper.group_by_month(limit, offset, fields)
    else:
        #defaulting to group by week
        response_list = response_helper.group_by_week(limit, offset, fields)

    final_result = {}
    final_result['groupBy'] = group_by
    final_result['startDate'] = start_date
    final_result['endDate'] = end_date
    final_result['result'] = response_list
    
    return json.dumps(final_result, default=str)

        
@app.route('/orders/userid/<int:userID>', methods=['GET'])
def get_user_orders(userID):
    # Get sort by requirement from query param
    args = request.args
    sort_by = args['sortBy']

    # Get all orders from DB
    user_orders, row_headers = db.get_user_orders(userID, sort_by)

    # Parse results to dict
    json_data=[]
    for result in user_orders:
        json_data.append(dict(zip(row_headers,result)))

    final_result = {}
    final_result['Orders'] = json_data
    return json.dumps(final_result, default=str)


@app.route('/order/placeOrder',methods=['POST'])
def create_order_for_user():
    body = request.json

    # extract details from body        
    user_id = body['userID']
    products_list = body['orderList']

    # Get list of product IDs
    product_id_list = [a_dict['productID'] for a_dict in products_list]

    # Get price for all products from DB
    unit_prices = db.get_product_details(product_id_list)

    # Add price to products list
    for p in products_list:
        productID = p['productID']
        for item in unit_prices:
            if item[0] == productID:
                p['price'] = item[1]
                break

    # Generate order ID hash
    order_id_hash_input = str(user_id) + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    order_id = hashlib.md5(order_id_hash_input.encode()).hexdigest()

    #insert into db
    db.add_order(user_id, order_id, products_list)
    
    json_response = {}
    json_response['success'] = True
    return json_response


if __name__ == "__main__":
    
    app.run(debug=True)