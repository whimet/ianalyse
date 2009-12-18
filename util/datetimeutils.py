from datetime import datetime,timedelta
import re
import time

def days_ago(days = 0, now = datetime.now()) :
    start = datetime.min.replace(year = now.year, month = now.month, day = now.day)
    return (start - timedelta(days))

def begining_of_the_day(now = datetime.now()) :
    return datetime.min.replace(year = now.year, month = now.month, day = now.day)

def days_ago_not_before(days = 0, now = datetime.now(), not_before_date = None) :
    ago = days_ago(days, now)
    if ago < not_before_date :
        return not_before_date
    else :
        return ago

def to_unix_timestamp(day_of_start):
    return time.mktime(day_of_start.timetuple()) 

def cctimestamp_to_unix_timestamp(cctimestamp) :
    ccdate = datetime.strptime(cctimestamp, "%Y%m%d%H%M%S")
    return to_unix_timestamp(ccdate)

def time_delta_as_str(timedelta_param):
    if timedelta_param > timedelta(days=30):
        return "More than 1 month"
    
    if timedelta_param >= timedelta(hours=24):
        return str(timedelta_param.days) + " Days"

    if timedelta_param < timedelta(hours=24) and timedelta_param > timedelta(hours=1):
        return str(timedelta_param.seconds / 3600) + " Hours"
    
    if timedelta_param < timedelta(hours=1):
        return "Less than 1 hour"

def cctimestamp_as_date(cctimestamp):
    pattern = "log([0-9]*).*.xml"
    return datetime.strptime(re.match(pattern, cctimestamp).group(1), "%Y%m%d%H%M%S")

def evaluate_time_to_seconds(time_str) :
    left = re.compile('\(')
    right = re.compile('\)')
    second = re.compile('second')
    minute = re.compile('minute')
    hour = re.compile('hour')
    s = re.compile('s')
    trailing_plus = re.compile('\+$')
    result = s.sub('', hour.sub("*3600 + ",  minute.sub('*60 + ', second.sub( '', time_str))))
    result = trailing_plus.sub('', result)
    result = right.sub('', left.sub('', result))
    return eval(str(result))


