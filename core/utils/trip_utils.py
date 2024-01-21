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

def maintenance_config(maintenance):
    monthYear = []
    activities= []
  
    for service in maintenance:
        formatted_monthYear = service['maintenance_date'].strftime("%B %Y")
        if formatted_monthYear not in monthYear:
            monthYear.append(formatted_monthYear)
            activities.append({
                formatted_monthYear: [
                    {
                        'activity_name': service['maintenance_name'],
                        'charges' : service['charges']
                    }
                ]
            })
            
        else:
            for activity in activities:
                if formatted_monthYear in activity:
                    activity[formatted_monthYear].append({
                        'activity_name': service['maintenance_name'],
                        'charges' : service['charges']
                    })
    
    return {
        'monthYear': monthYear,
        'activities': activities
    }


def maintenance_data_config(services):
    maintenance = []
    total_maintenance = 0
    for service in services:
        maintenance.append({
            'label': service['maintenance_name'],
            'value': service['charges']
        })
        total_maintenance += service['charges']

    return total_maintenance, maintenance
        
        

def entire_trip_details_data_config(trips, order_to_trips, orders):
    all_trips = {
        'column_names': entire_trip_column_names,
        'column_values': [],
        'row_span': [],
        'total': {},
    }
        
    trip_totals = copy.deepcopy(total_trip_details)
    for order in orders:
        trip_detail = copy.deepcopy(each_trip_details)
        for trip_order in order_to_trips:
            if str(order['id']) == trip_order['order_id']:
                for trip in trips:
                    if str(trip['id']) == trip_order['trip_id']:
                        if trip['trip_date'].date() == order['date'].date():
                            trip_detail['READING'] = trip['reading']

                            trip_detail['KMS'] = trip['kilometers']
                            trip_totals['KMS'] += trip['kilometers']

                            trip_detail['DIESEL'] = trip['diesel']
                            trip_totals['DIESEL'] += trip['diesel']
                            
                            trip_detail['DIESEL AMT'] = trip['diesel_amount']
                            trip_totals['DIESEL AMT'] += trip['diesel_amount']
                            
                            trip_detail['MILEAGE'] = trip['mileage']
                            trip_totals['MILEAGE'] += trip['mileage']

                            trip_detail['ADBLUE'] = trip['ad_blue']
                            trip_totals['ADBLUE'] += trip['ad_blue']

                            trip_detail['BALANCE AMT'] = trip['balance_amount']
                            trip_totals['BALANCE AMT'] += trip['balance_amount']

                            all_trips['row_span'].append(trip['no_of_trips'])
                        else:
                            all_trips['row_span'].append(None)

                        trip_detail['DATE'] = order['date'].date()
                        # print("excuted trip_detail", trip_detail)
        trip_detail['FROM'] = order['from_field']
        trip_detail['TO'] = order['to']

        trip_detail['QTY'] = order['quantity']
        trip_totals['QTY'] += order['quantity']

        trip_detail['ADVANCE'] = order['advance']
        trip_totals['ADVANCE'] += int(order['advance'])

        trip_detail['LOADING'] = order['loading']
        trip_totals['LOADING'] += order['loading']

        trip_detail['UNLOADING'] = order['unloading'] 
        trip_totals['UNLOADING'] += order['unloading']

        trip_detail['TOLLGATE'] = order['toll_gate']
        trip_totals['TOLLGATE'] += order['toll_gate']

        trip_detail['RTO & PC'] = order['rto_pcl'] 
        trip_totals['RTO & PC'] += order['rto_pcl']

        trip_detail['FREIGHT'] = order['freight']
        trip_totals['FREIGHT'] += order['freight']

        trip_detail['FRIEGHT AMT'] = order['freight_amount']
        trip_totals['FRIEGHT AMT'] += order['freight_amount']

        trip_detail['DRIVER FRIEGHT'] = order['driver_freight']
        trip_totals['DRIVER FRIEGHT'] += order['driver_freight']

        trip_detail['DRIVER AMT'] = order['driver_amount']
        trip_totals['DRIVER AMT'] += order['driver_amount']

        trip_detail['GST'] = order['gst_amount']
        trip_totals['GST'] += order['gst_amount']

        all_trips['column_values'].append(trip_detail)                    

    print('entire trips', all_trips['column_values'])

    trip_totals['FREIGHT'] = trip_totals['FREIGHT'] / len(all_trips['column_values'])
    trip_totals['DRIVER FRIEGHT'] = trip_totals['DRIVER FRIEGHT'] / len(all_trips['column_values'])
    trip_totals['MILEAGE'] = trip_totals['MILEAGE'] / len(trips)

    print("trip totals", trip_totals)

    all_trips['total'] = trip_totals


    return all_trips