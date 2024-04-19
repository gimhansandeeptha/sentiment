from datetime import datetime, timedelta
import pytz

def get_query_param(start=0, page_size=5)->dict:
    #Get the yesterday date value
    utc_time = datetime.now(pytz.utc)
    utc_date = utc_time.date()
    yesterday = utc_date - timedelta(days=1)

    # Put 'yesterday' varibale for actual production. 
    query_params = {
        "startDate": "2024-03-19", # yesterday 
        "endDate": "2024-03-19", # yesterday
        "page_size": page_size,
        "start" : start
    }

    return query_params

