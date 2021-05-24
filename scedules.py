import requests,pickle
# from endpoints import *


# Any  User-Agent hving the word python or the programming language name will not the accepted by the API setu ,
# normally the User-Agent is python-request/15.2.0. We can use any randome name as useragent as long as it dont have "python"
# to find the prepared request data we can use the 'res.request.headers' syntax  

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept-Language':'en_US'}

findByPin ="/v2/appointment/sessions/public/findByPin"
calendarByPin = "/v2/appointment/sessions/public/calendarByPin"
calendarByDistrict = "/v2/appointment/sessions/public/calendarByDistrict"
calendarByCenter = "/v2/appointment/sessions/public/calendarByCenter"
statesApi = "/v2/admin/location/states"
districtsApi = "/v2/admin/location/districts/"
findCenterByDistrict = "/v2/appointment/sessions/public/findByDistrict"
url = "https://cdn-api.co-vin.in/api"

class FindRecordByDistrict:

    # TODO need to handel exception noreefficiently and get rid of the state save code

    def __init__(self,s_name,d_name):
        self.state_name = s_name.lower()
        self.district_name = d_name.lower()
        try:
            with open("info_state.pkl",'rb') as fd:
                self.state_list = pickle.load(fd)
                if self.state_name in self.state_list:
                    self.district_Id = self.__get_district_id(self.state_list[self.state_name],self.district_name)
                else:
                    raise ValueError
        except (FileNotFoundError,ValueError):
            self.state_list = self.__createStateFile()
            if self.state_name in self.state_list:
                 self.district_Id = self.__get_district_id(self.state_list[self.state_name],self.district_name)
            else:
                raise Exception(f"++ state  '{s_name}'  not found")    
        self.state_Id =  self.state_list[self.state_name]        

    def __createStateFile(self):
        res = requests.get(f"{url}{statesApi}",headers=headers)
        st_dict = {}
        for i in res.json()['states']:
            st_dict[i['state_name'].lower()] = i['state_id']
        with open("info_state.pkl","wb") as fd:
            pickle.dump(st_dict,fd)
        return st_dict
        

    def __get_district_id(self,state_id,district_name):
        res =  requests.get(f"{url}{districtsApi}{state_id}",headers=headers)
        for d in res.json()['districts']:
            if district_name == d['district_name'].lower():
                return d['district_id']
        raise Exception(f"Disctrict {district_name} not found")

    def getAllCentersOnDate(self,date:str):
        print(self.state_Id)
        res = requests.get(f'{url}{findCenterByDistrict}',params={"district_id":self.district_Id,"date":date},headers=headers)
        return res.json()['sessions']
        

    def getCalenderByDate(self,date):
        res = requests.get(f"{url}{calendarByDistrict}",params={'district_id':self.district_Id,'date':date},headers= headers)
        if res.status_code ==200:
            return res.json()['centers']
        raise Exception(f"{res.text}\nError occured")

    def getCalendarByCenterAndDate(self,center_Id,date):
        res = requests.get(f"{url}{calendarByCenter}",params={'center_id':center_Id,'date':date},headers=headers)
        return res
        


def getCalenderByPin(p,d):

    res = requests.get(f"{url}{calendarByPin}",params={"pincode":p,"date":d},headers=headers)
    if res.status_code == 200:
        return res.json()['centers']
    elif res.status_code == 400:
        raise Exception(res.json()['error'])

def getCentersByPin(pin,date):
    res = requests.get(f"{url}{findByPin}",params={"pincode":pin,"date":date},headers=headers)
    if res.status_code ==200:
        return res.json()['sessions']
    else:
        raise Exception(res.text)
