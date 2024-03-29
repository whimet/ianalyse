import os
import shutil          
import re 
import util.datetimeutils
from datetime import datetime
import base64

def touch(path):
    makedirs_p(os.path.dirname(path))
    f = open(path, 'w')
    f.close()

def makedirs_p(path):
    if not os.access(path, os.F_OK):
        os.makedirs(path)

def rmdir_p(path):
    if not os.path.exists(path):
        return
    shutil.rmtree(path, True)

def write_to_file(path, content, mode='w'):
    makedirs_p(os.path.dirname(path))
    f = open(path, mode)
    try:
        f.write(content)
    finally:
        f.close() 
                                                                   
def list_matched_files(root, pattern=None):     
    files = []
    if pattern == None:
        pattern = '.*'
    for file in os.listdir(root):
        m = re.match(pattern, file)
        if m != None:
            files.append(file)
    return files
    
def sort_by_rule(root, rule, order):   
    files = list();
    all_files = list_matched_files(root, rule)
    return sorted(all_files, eval('compare_files_' + order)) 

def filter_by_days(root, rule, days):
    if days == None or days == 0:
        return []
    files = os.sort_by_rule(root, rule, 'asc');
    ndays_before = __ndays_before__(files[len(files) - 1], days)
    
    filtered = []
    for file in files:
        current_date =  util.datetimeutils.cctimestamp_as_date(file)

        if current_date >= ndays_before:
            filtered.append(file)
    return filtered
    
def __ndays_before__(file, days):
    cc_date =  util.datetimeutils.cctimestamp_as_date(file)
    n_days_ago = util.datetimeutils.days_ago(days, cc_date)
    beging_of_n_days_ago = util.datetimeutils.begining_of_the_day(n_days_ago)
    return beging_of_n_days_ago
    

def __compare_files(file1, file2, order):
    pattern = "log([0-9]*).*.xml"
    m1 = re.match(pattern, file1)
    date1 = datetime.strptime(m1.group(1), "%Y%m%d%H%M%S")
    m2 = re.match(pattern, file2)
    date2 = datetime.strptime(m2.group(1), "%Y%m%d%H%M%S")

    if order == 'desc':                                   
        return cmp(date2, date1)
    else:                                                  
        return cmp(date1, date2)
        
def compare_files_asc(file1, file2):
    return __compare_files(file1, file2, 'asc')

def compare_files_desc(file1, file2):
    return __compare_files(file1, file2, 'desc')                                      

    
def write_base64_as_binary(file, data):
    data = data.replace(u'\a\b\t\n\v\f\r',  u'abtnvfr')
    data = data.replace(' ', '+')
    write_to_file(file, base64.b64decode(data), 'wb')

os.write_to_file = write_to_file
os.touch = touch
os.makedirs_p = makedirs_p
os.rmdir_p = rmdir_p
os.sort_by_rule = sort_by_rule
os.list_matched_files = list_matched_files
os.filter_by_days = filter_by_days
os.write_base64_as_binary = write_base64_as_binary
