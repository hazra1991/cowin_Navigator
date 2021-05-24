from scedules import getCalenderByPin ,FindRecordByDistrict,getCentersByPin
from datetime import timedelta,datetime


def getCalenderAvailability(pin=None,state=None,district=None,from_date=None,min_age=None):
    try:
        if not from_date:
            from_date = datetime.now().date()
        else:
            from_date = datetime.strptime(from_date,'%d-%m-%Y').date()
            if (from_date - datetime.now().date()).days < 0:
                raise Exception('\nProvidede date cannot be in past ,should be from today')
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
    # import pprint
    avaialble_dict = {}
    for i in center_list:
        for j in i['sessions']:
            if j['available_capacity'] > 0 and (min_age ==None  or j['min_age_limit'] == min_age):
                avaialble_dict.setdefault(j['date'],[]).append({"center_name":i['name'],"center_id":i['center_id'],"address":i['address'],
                "vaccine":j['vaccine'],"dose1":j['available_capacity_dose1'],"dose2":j['available_capacity_dose2'],"min_age_limit":j['min_age_limit'],
                "fee_type":i['fee_type'],"available_capacity":j["available_capacity"],'slots':j["slots"]})
                
    del center_list
    # pprint.pprint(avaialble_dict)
    # pprint.pprint(center_list)
    print (f"Vaccination available for dates {avaialble_dict.keys()}")
    return avaialble_dict


if __name__ == '__main__':

    # getCalenderAvailability(state='karnataka',district='bangalore urban',from_date='23-5-2021')
    getCalenderAvailability(pin=110001,from_date='23-5-2021')

