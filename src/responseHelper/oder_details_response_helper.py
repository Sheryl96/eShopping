import datetime
from dateutil.relativedelta import relativedelta


class OrderDetailsResponseHelper:

    def __init__(self, order_details, start_date, end_date):
        self.order_details = order_details
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    def group_by_date(self, limit, offset, fields):
        start = self.start_date.date()
        end = self.end_date.date()
        response_list = []
        freq = {}

        # Fill map with dates to be returned
        while (start <= end):
            freq[start] = []
            start += datetime.timedelta(days=1)
        

        # Add orders to relevant dates in map
        for detail in self.order_details:
            orderDate = detail['OrderDate'].date()
            freq[orderDate].append({ required_key: detail[required_key] for required_key in fields})

        # Add to final list 
        for item in freq.items():
            date_map = {}
            date_map['date'] = item[0]
            date_map['productsSold'] = item[1]
            response_list.append(date_map)

        return response_list
    
    def group_by_month(self, limit, offset, fields):
        start = self.start_date
        end = self.end_date
        response_list = []
        freq = {}

        # initialize map with months that fall in range
        while (start <= end):
            freq[start.strftime("%B")] = []
            start += relativedelta(months=1)
        freq[end.strftime("%B")] = [] # enddate might be earlier than one month increment

        # Add order details to relavant month in map
        for detail in self.order_details:
            orderDate = detail['OrderDate'].strftime("%B")
            freq[orderDate].append({ required_key: detail[required_key] for required_key in fields})

        # Add result to final list
        for item in freq.items():
            date_map = {}
            date_map['month'] = item[0]
            date_map['productsSold'] = item[1]
            response_list.append(date_map)

        return response_list

    def group_by_week(self, limit, offset, fields):
        start = self.start_date
        end = self.end_date
        response_list = []
        freq = {}

        # Create map with week numbers in date range
        while (start <= end):
            freq[start.strftime("%U")] = []
            start += datetime.timedelta(days=7)
        freq[end.strftime("%U")] = [] # making sure we capture the week number of enddate
        
        # Populate map with order details
        for detail in self.order_details:
            orderDate = detail['OrderDate'].strftime("%U")
            freq[orderDate].append({ required_key: detail[required_key] for required_key in fields})

        # Add info to final list
        for item in freq.items():
            date_map = {}
            date_map['weekNumber'] = item[0]
            date_map['productsSold'] = item[1]
            response_list.append(date_map)

        return response_list