# Basic REST API application 

## Desciption
### Create a very basic REST API application where a customer can have an order that is made up of products.

## Project setup
### The project is using Python framework, Flask with AWS RDS database (MySQL) for storing the database details. 

<img src="ER diagram.png" alt="ER diagram" />

## Installation instruction
1. Install pip: python3 -m pip install --user --upgrade pip
2. 'cd' into the root dir of the project (dir: eShopping). 
3.  source venv/bin/activate   \
3.a. If you run into issues, run: python3 -m pip install --user virtualenv  \
3.b. After installing virtual environment, activate venv again using command in step 3.
4. brew install openssl 
5. pip3 install -r requirments.txt
6. 'cd' into src dir of the project
7. Run command: flask run 

## Assumptions
### 
1. Before placing the order using ProductID, assumed that the Product table is populated.
2. All requests are valid/correct (request body and query params have valid data inline with the API contract outlined below).
3. DB set up is not required to run the app since RDS is being used.
4. Auth is not required for the endpoints.
5. Server has Python3 installed.
6. Installation instructions have been tried on a Mac. Slight variations would be required for Linux/Windows.


## Endpoints

### 
### 1. An API endpoint that accepts a date range and a day, week, or month and returns a breakdown of products sold by quantity per day/week/month: 
Endpoint: <b> /orders/orderDetails/orderDate </b> \
Query Parameters: startDate, endDate, limit, groupBy, offset, fields \
Method: GET \
Response code: 200 \
Response body: Json response. Samples given below

Option 1: By day \
Sample request : http://localhost:5000/orders/orderDetails/orderDate?startDate=2021-06-10&&endDate=2021-06-15&&groupBy=day&&fields=ProductID,Quantity \
Sample Response Body: \
```
{
  "groupBy": "day",
  "startDate": "2021-06-10",
  "endDate": "2021-06-15",
  "result": [
    {
      "date": "2021-06-10",
      "productsSold": []
    },
    {
      "date": "2021-06-11",
      "productsSold": []
    },
    {
      "date": "2021-06-12",
      "productsSold": []
    },
    {
      "date": "2021-06-13",
      "productsSold": []
    },
    {
      "date": "2021-06-14",
      "productsSold": [
        {
          "ProductID": 2,
          "Quantity": 2
        }
      ]
    },
    {
      "date": "2021-06-15",
      "productsSold": []
    }
  ]
}
```

Option 2: By month \
Sample request : http://localhost:5000/orders/orderDetails/orderDate?startDate=2021-06-10&&endDate=2021-06-15&&groupBy=month&&fields=ProductID,Quantity \
Sample Response Body: \
```
{
  "groupBy": "month",
  "startDate": "2021-06-10",
  "endDate": "2021-06-15",
  "result": [
    {
      "month": "June",
      "productsSold": [
        {
          "ProductID": 2,
          "Quantity": 2
        }
      ]
    }
  ]
}
```

Option 3: By week 
Sample request : http://localhost:5000/orders/orderDetails/orderDate?startDate=2021-06-10&&endDate=2021-06-15&&groupBy=week&&fields=ProductID,Quantity \
Sample Response Body: \
```
{
  "groupBy": "week",
  "startDate": "2021-06-10",
  "endDate": "2021-06-15",
  "result": [
    {
      "weekNumber": "23",
      "productsSold": []
    },
    {
      "weekNumber": "24",
      "productsSold": [
        {
          "ProductID": 2,
          "Quantity": 2
        }
      ]
    }
  ]
}
```
 
### 2. An API endpoint that returns all orders for a customer sorted by date: 
Endpoint:<b>  /orders/userid/<int:userID> </b> \
Query Parameters: sortBy  \
Method: GET  \
Response code: 200

Sample request : http://localhost:5000/orders/userid/1?sortBy=%272020-09-09%27 \
Sample Response Body: \
```{
  "Orders": [
    {
      "OrderID": "1",
      "UserID": 1,
      "OrderDate": "2020-09-23 00:00:00"
    },
    {
      "OrderID": "ca9775b3e549aecc2aeb1d39440f8979",
      "UserID": 1,
      "OrderDate": "2021-06-14 18:38:18"
    }
  ]
}
```

### 3. An API endpoint to create an Order for a Customer where input products can be specified by Product IDs: 
Endpoint: <b> /order/placeOrder </b>  \
Method: POST  \
Sample Request Body: \
```{
    "userID": 1,
    "orderList": [{
        "productID": 1,
        "quantity": 3.0
    },
    {
        "productID": 2,
        "quantity": 2.0
    }]
}
```
Response code: 200 \
Response Body: 
```
{
    sucess: true
}
```

## Things not covered as part of project
### 
1. Query parameters are case sensitive. Would had made them case insensitive.
2. Better handling of request params, request body and passing of that info all the way to db.
4. Would have added more checks for error handling.
5. Would have added user authentication, in order to make the website more secure.
6. I have used MySQL as my database. However, could have used a hybrid approach for a more sofisticated system. NoSQL for full text searches and browsing session data storage for predictive analysis, and SQL for transactional nature of the server. 
7. The endpoints are extensible but some things are not implemented. Like the option of pagination using limit and offset for the first endpoint.

