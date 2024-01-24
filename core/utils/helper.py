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

def get_previous_monthYear(monthYear):
    # Convert input string to a datetime object
    date_object = datetime.strptime(monthYear, "%Y-%m")

    # Calculate the first day of the current month
    first_day_of_current_month = date_object.replace(day=1)

    # Calculate the last day of the previous month
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

    return last_day_of_previous_month.strftime("%Y-%m")


def get_start_and_end_date(monthYear):
    start_date_string = f"{monthYear}-01 00:00:00"
    year, month = map(int, monthYear.split('-'))
    last_day = calendar.monthrange(year, month)[1]
    end_date_string = f"{monthYear}-{last_day:02} 23:59:59"

    # Convert strings to datetime objects
    start_datetime = datetime.strptime(start_date_string, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(end_date_string, "%Y-%m-%d %H:%M:%S")

    return start_datetime, end_datetime

def get_monthYear_range(monthYear):
    previous_monthYear = get_previous_monthYear(monthYear)
    current_start_date, current_end_date = get_start_and_end_date(monthYear)
    previous_start_date, previous_end_date = get_start_and_end_date(previous_monthYear)

    return current_start_date, current_end_date, previous_start_date, previous_end_date

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

def calculate_percentage_increase(current_expenses, previous_expenses):
    if previous_expenses == 0:
        # Avoid division by zero if expenses were zero in the previous month
        return float('inf')
    
    percentage_increase = ((current_expenses - previous_expenses) / previous_expenses) * 100
    return percentage_increase