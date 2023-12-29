from datetime import datetime
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
    print("start date", "end date", start_datetime, end_datetime)

    return start_datetime, end_datetime