from datetime import datetime, timedelta
import calendar

def number_with_commas(value, decimal=True):
    if value is not None:
        raw_value = ''.join(c for c in str(value) if c.isdigit() or c == '.')
        if decimal:
            return '{:,.2f}'.format(float(raw_value))
        else:
            return '{:,}'.format(int(float(raw_value)))
    return value

def get_monthYear_range(monthYear):
    start_date_string = f"{monthYear}-01 00:00:00"
    year, month = map(int, monthYear.split('-'))
    last_day = calendar.monthrange(year, month)[1]
    end_date_string = f"{monthYear}-{last_day:02} 23:59:59"

    # Convert strings to datetime objects
    start_datetime = datetime.strptime(start_date_string, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(end_date_string, "%Y-%m-%d %H:%M:%S")

    return start_datetime, end_datetime

def get_last_six_monthYear(monthYear):
    input_date = datetime.strptime(monthYear, '%Y-%m')

    # Calculate the start date of the last 6 months
    start_date = input_date - timedelta(days=input_date.day - 1)
    start_date -= timedelta(days=180)

    # Generate a list of the last 6 months
    last_six_months = [(start_date + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(6)]

    last_six_months.append(monthYear)

    return last_six_months

def get_strp_time(montYear):
    input_date = datetime.strptime(montYear, '%Y-%m')

    # Convert to the desired format 'Month YYYY'
    formatted_date = input_date.strftime('%b %Y')

    return formatted_date