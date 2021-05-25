from scedules import getCalenderByPin ,FindRecordByDistrict,getCentersByPin
from datetime import timedelta,datetime
import csv


def _getCalenderAvailability(pin=None,state=None,district=None,from_date=None,min_age=None,dose=None):
    try:
        if not from_date:
            from_date = datetime.now().date()
        else:
            from_date = datetime.strptime(from_date,'%d-%m-%Y').date()
            if (from_date - datetime.now().date()).days < 0:
                raise Exception('\n\n[++] Providede date cannot be in past ,should be from today')
    except ValueError as e:
        raise ValueError(f"\n{e}   --- \n\n[+][+]PLease provide an proper date format in dd-mm-yy")

    time_counter =  timedelta(days=8)
    c=4
    center_list = []
    if pin:
        get_record = "getCalenderByPin(pin,f\"{from_date.day}-{from_date.month}-{from_date.year}\")"
    else:    
        record = FindRecordByDistrict(state,district)
        get_record ='record.getCalenderByDate(f"{from_date.day}-{from_date.month}-{from_date.year}")'
    while c:
        rawlist = eval(get_record)  # eval parses the statement present in string and compiles it every tiem its called .we can use function as well to evaluate and expressions 
        if rawlist:
            center_list.extend(rawlist)
            from_date = from_date + time_counter
        else:
            break
        c -=1
    detailed_report = []
    brief_info = {}
    for i in center_list:
        for j in i['sessions']:
            if j['available_capacity'] > 0 and (min_age ==None  or j['min_age_limit'] == min_age) and (dose == None or j[f'available_capacity_dose{dose}']>0):
                detailed_report.append({"center_name":i['name'],"center_id":i['center_id'],"date":j['date'],"address":i['address'],
                "vaccine_type":j['vaccine'],"dose1":j['available_capacity_dose1'],"dose2":j['available_capacity_dose2'],"min_age_limit":j['min_age_limit'],
                "fee_type":i['fee_type'],"available_capacity":j["available_capacity"],'slots':str(j["slots"])})
                brief_info[j['date']] = brief_info.get(j['date'],0)+1
    del center_list
    return detailed_report,brief_info


def _print_and_generate_report(data,v):
    columun_name = ['center_name', 'center_id','date','vaccine_type', 'dose1', 'dose2', 'min_age_limit', 'fee_type', 'available_capacity', 'slots','address']
    if len(data) > 0:
        print(f'\nAbailable for the dates and number of centes : - {list(zip(v.keys(),v.values()))}')
        print('\nGenerating complete report-------------\n')
        with open('detailed_report.csv','w') as fd:
            writer = csv.DictWriter(fd,fieldnames=columun_name)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    else:
        print("\n\nNO centers found for the provided date.")

def monitorAvailabitily(email,**kwargs):
    import hashlib
    from time import sleep
    from utils import send_mail
    prev_hash = ""
    try:
        while True:
            details, _ = _getCalenderAvailability(**kwargs)
            curr_hex = hashlib.md5(str(details).encode()).hexdigest()
            print(prev_hash,curr_hex)
            if not (prev_hash == curr_hex):
                body = f"Abailable for the dates and number of centes : - {list(zip(_.keys(),_.values()))}"
                prev_hash = curr_hex
                send_mail(subject="Cowin-Notification",body=body,sendto=email,priority="1")
                print("notification sent")
                _print_and_generate_report(details,_)
            sleep(600)
    except KeyboardInterrupt:
        print('Monitoring exited safely ')
    

def getCalender(**kwargs):
    details,brief = _getCalenderAvailability(**kwargs)
    _print_and_generate_report(details,brief)


##--------------For testing ----------------------##

def generateRandomeString_for_testing():
    import random
    import string

    # printing lowercase
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))