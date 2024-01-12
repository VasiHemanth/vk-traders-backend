from datetime import datetime
import calendar
import copy
from .config import *
from .helper import number_with_commas

def convert_date_time_string_to_datetime(date_string):
    date_format = "%Y-%m-%dT%H:%M"
    return datetime.strptime(date_string, date_format)

def multi_orders_expense_calculator(order_expense):
    amount = 0
    for expense in order_expense:
        each_order_expense = expense['freight_amount'] - expense['total_expenses'] - expense['driver_amount'] 
        amount += each_order_expense

    print("amount", amount)
    return amount

def trip_data_config(trip_data):
    trip_metrics = copy.deepcopy(trip_metrics_config)
    if trip_data['submit_status']:
        for key, value in trip_data.items():
            if key in trip_metrics_key:
                index = trip_metrics_key.index(key)
                # print("index", key, value, index)
                if value != None:
                    if key in ['kilometers', 'diesel','mileage']:
                        trip_metrics[index]["value"] = value
                    elif key == 'reading':
                        trip_metrics[index]["value"] = number_with_commas(value, False)
                    else:
                        trip_metrics[index]["value"] = "₹" + number_with_commas(value)
        return trip_metrics
    else:
        return trip_metrics

def order_data_config(order_data):
    order_details = copy.deepcopy(order_details_config)
    if order_data['order_submit_status']:
        for index, detail in enumerate(order_details_key):
            if detail not in ['from_field', 'to', 'grade', 'quantity', 'order_id', 'party_name']:
                order_details[index]['value'] = "₹" + number_with_commas(order_data[detail])
            else:
                order_details[index]['value'] = order_data[detail]

        return order_details
    else:
        order_details_data = order_details[0:7]
        print("order_details", order_details_data)
        for index, detail in enumerate(order_details_key_):
            if detail=='advance':
                order_details_data[index]['value'] = "₹" + number_with_commas(order_data[detail])
            else:
                order_details_data[index]['value'] = order_data[detail]
        return order_details_data


def vitals_data_config(vitals):
    vitals_config = copy.deepcopy(vital_detials_config)
    for vital in vitals_config:
        # print(vital['title'], vitals[vital['title']])
        if vitals[vital['title']] != None:
            vital['value']=vitals[vital['title']]

            if vital['title'] == 'Frieght Amount':
                if vital['value'] > 400000 and vital['value'] < 500000:
                    vital['color'] = 'yellow'
                elif vital['value'] < 400000:
                    vital['color'] = 'red'

    return vitals_config


def expenses_data_config(expenses):
    expenses_config = copy.deepcopy(total_expenditure_config)
    for expense in expenses_config:
        expense['value'] = expenses[expense['label']]
            

    return expenses_config
        
        
