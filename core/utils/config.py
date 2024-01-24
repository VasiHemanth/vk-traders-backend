
trip_metrics_key = ['reading', 'kilometers', 'diesel', 'diesel_amount', 'ad_blue', 'mileage', 'balance_amount']

trip_metrics_config = [
    {
        "label": "Reading",
        "value": "N/A" 
    },
    {
        "label": "Kilometers",
        "value": "N/A"
    },
    {
        "label": "Diesel",
        "value": "N/A" 
    },
    {
        "label": "Diesel Amount",
        "value": "N/A" 
    },
    {
        "label": "AdBlue",
        "value": "N/A"
    },
    {
        "label": "Mileage",
        "value": "N/A" 
    },
    {
        "label": "Balance Amount",
        "value": "N/A"
    },
]


order_details_key_ = [
    'from_field', 
    'to', 
    'grade', 
    'quantity', 
    'order_id', 
    'party_name', 
    'advance'
]

order_details_key = ['from_field', 'to', 'grade', 'quantity', 'order_id', 'party_name', 
    'advance', 'loading', 'unloading', 'toll_gate', 'rto_pcl', 'freight', 'total_expenses',
    'freight_amount','driver_freight', 'driver_amount'
]

order_details_config = [
      { 'label': "From", 'value': "" },
      { 'label': "To", 'value': "" },
      { 'label': "Grade", 'value': "" },
      { 'label': "Quantity", 'value': "" },
      { 'label': "Shipment Number", 'value': "" },
      { 'label': "Party Name", 'value': "" },
      {
        'label': "Advance",
        'value': "",
      },
      { 'label': "Loading", 'value': "" },
      { 'label': "UnLoading", 'value':"" },
      { 'label': "Toll Gate", 'value': "" },
      { 'label': "RTO & PC", 'value': "" },
      { 'label': "Freight", 'value': "" },
      { 'label': "Expenses", 'value': "" },
      { 'label': "Freight Amount", 'value': "" },
      { 'label': "Driver Freight", 'value': "" },
      { 'label': "Driver Amount", 'value': "" },
]

vital_detials_config = [
    {
    "title": "Frieght Amount",
    "value": "",
    "description": "",
    "icon": "/rupees.svg",
    "details": False,
    "color": "",
    },
    {
    "title": "Total Expenditure",
    "value": "",
    "description": "",
    "icon": "/total-expenses.svg",
    "details": True,
    "color": "",
    },
    {
    "title": "EMI",
    "value": "",
    "description": "",
    "icon": "/loan.svg",
    "details": False,
    "color": "",
    },
    {
    "title": "Kilometers",
    "value": "",
    "description": "",
    "icon": "/kilometers.svg",
    "details": False
    },
    {
    "title": "Maintenance",
    "value": "",
    "description": "",
    "icon": "/maintenance.svg",
    "details": True,
    "color": "",
    },{
    "title": "Quantity",
    "value": "",
    "description": "",
    "icon": "/quantity.svg",
    "details": False,
    "color": "",
    },
    {
    "title": "Balance",
    "value": "",
    "description": "",
    "icon": "/balance.svg",
    "details": False,
    "color": "",
    },
]

total_expenditure_config = [
    { "label": "Loading", "value": "N/A" },
    { "label": "UnLoading", "value":"N/A" },
    { "label": "Toll Gate", "value": "N/A" },
    { "label": "RTO & PC", "value": "N/A" },
    {
        "label": "Diesel Amount",
        "value": "N/A" 
    },
    {
        "label": "AdBlue",
        "value": "N/A"
    },
    { "label": "Driver Amount", "value": "N/A" },
]

calculate_percentage = ['Frieght Amount', 'Total Expenditure', 'Maintenance', 'Quantity']

entire_trip_column_names =['DATE', 'FROM', 'TO', 'QTY', 'ADVANCE', 'LOADING', 'UNLOADING', 
    'RTO & PC', 'TOLLGATE', 'READING', 'KMS', 'DIESEL', 'DIESEL AMT', 'ADBLUE',
     'TOTAL EXPENSES', 'MILEAGE', 'FREIGHT', 'FRIEGHT AMT','DRIVER FRIEGHT', 'DRIVER AMT',
    'BALANCE AMT', 'GST AMT', 'BALANCE AMT (+GST)'
]

each_trip_details = {
    'DATE': 'N/A',
    "FROM": "N/A",
    "TO": "N/A",
    "QTY": "N/A",
    "ADVANCE": "N/A",
    "LOADING": "N/A",
    "UNLOADING": "N/A",
    "TOLLGATE": "N/A",
    "RTO & PC": "N/A",
    "READING": None,
    "KMS": None,
    "DIESEL": None,
    "DIESEL AMT":None,
    "ADBLUE": None,
    'TOTAL EXPENSES': None,
    "MILEAGE": None,
    "FREIGHT": "N/A",
    "FRIEGHT AMT": 'N/A',
    "DRIVER FRIEGHT": "N/A",
    "DRIVER AMT": "N/A",
    "BALANCE AMT": None,
    'GST AMT': None,
    'BALANCE AMT (+GST)': None,
}

total_trip_details = {
    'DATE': 'Total',
    "FROM": None,
    "TO": None,
    "QTY": 0,
    "ADVANCE": 0,
    "LOADING": 0,
    "UNLOADING": 0,
    "RTO & PC": 0,
    "TOLLGATE": 0,
    "READING": None,
    "KMS": 0,
    "DIESEL": 0,
    "DIESEL AMT":0,
    "ADBLUE": 0,
    'TOTAL EXPENSES': 0,
    "MILEAGE": 0,
    "FREIGHT": 0,
    "FRIEGHT AMT": 0,
    "DRIVER FRIEGHT": 0,
    "DRIVER AMT": 0,
    "BALANCE AMT": 0,
    "GST AMT": 0,
    'BALANCE AMT (+GST)': 0
}

not_included_in_total = ['DATE','FROM', 'TO', 'READING']