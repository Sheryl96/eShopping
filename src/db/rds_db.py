import pymysql
import json
from datetime import datetime

conn = pymysql.connect(
        host = 'eshopping.cize1zswnc9n.us-east-2.rds.amazonaws.com',
        port = 3306,
        user = 'admin',
        password = 'adminadmin',
        db = 'eShopping',

        )

def get_details():
    cur = conn.cursor()
    cur.execute("SELECT * FROM eShopping.Users")
    details = cur.fetchall()
    return details

def get_sold_products(start_date, end_date):
    cur = conn.cursor()
    cur.execute("SELECT * FROM eShopping.OrderDetails AS od INNER JOIN eShopping.Order AS O ON od.OrderID=O.OrderID WHERE OrderDate BETWEEN %s AND %s;", (start_date, end_date))
    row_headers=[x[0] for x in cur.description]
    # print row_headers
    sold_products = cur.fetchall()
    return sold_products, row_headers

def get_user_orders(userID, order_by):
    cur = conn.cursor()
    cur.execute("SELECT * FROM eShopping.Order WHERE UserID=%s ORDER BY %s ", (userID, order_by))
    row_headers=[x[0] for x in cur.description]
    orders = cur.fetchall()
    return orders, row_headers


def get_product_details(product_list):
    # product id is a list
    product_list = [str(element) for element in product_list]
    products = ",".join(product_list)
    cur = conn.cursor()
    query = "SELECT ProductID, UnitPrice FROM eShopping.Products WHERE ProductID in ({});".format(products)
    cur.execute(query)
    product_details = cur.fetchall()
    return product_details

def add_order(user_id, order_id, order_details):
    cur = conn.cursor()
    query1 = "INSERT INTO eShopping.Order (OrderID, UserID, OrderDate) VALUES ('{0}',{1},'{2}');".format(order_id,user_id,datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for order_detail in order_details:
        query2 = "INSERT INTO eShopping.OrderDetails (OrderDetailsID,OrderID,ProductID,Quantity,UnitPrice,Status,ShipDate) VALUES ({0},'{1}',{2},{3},{4},'{5}',{6});".format("null",order_id,order_detail['productID'],order_detail['quantity'], order_detail['price'],"in progress","null")
    cur.execute(query1)
    cur.execute(query2)
    conn.commit()
