from entrypoint import getCalender,monitorAvailabitily , getFromPincodeList
from argparse import ArgumentParser
from requests.exceptions import ConnectionError

my_args = ArgumentParser(description='Find the cowin slot availability',prog='Cowin Nvigator')
mygroup = my_args.add_mutually_exclusive_group( required=True)
mygroup.add_argument("-p","--bypin",action = 'store_true', help='search via Pin')
mygroup.add_argument('-bd','--bydistrict',action='store_true',help='search by state and district name')
mygroup.add_argument('--all-pin',metavar=" <filename/filepath> ",dest="all_pin_file",action='store',type = str,help='get the pin list to check from a file')
my_args.add_argument('-m','--monitor',action='store_true',help='monitors periodicaly')
my_args.add_argument('-a','--age-limit',action="store",metavar='',choices=[18,45],dest='age_limit',type=int,help='Specify the age [+default 1 & 2}]')
my_args.add_argument('--date',metavar='',type = str,help='Date format \'dd-mm-yy\' [ + Default is today ]')
my_args.add_argument('--dose',metavar = '',action='store',choices=['1','2'],help='Specify the dose to to searched[+ default is all]')

args = my_args.parse_args()
user_args = {'min_age':args.age_limit,'from_date':args.date,'dose':args.dose}
pin=state=district = None
try:

    if args.bypin:
        pin = input('Please enter the location pin number :- ').strip()
        user_args.update({'pin':pin})
    elif args.bydistrict:
        state = input('Please enter the state name:- ').strip()
        district =input('Please enter the district name:- ').strip()
        user_args.update({'state':state,'district':district})
    elif args.all_pin_file and not args.monitor:
        getFromPincodeList(args.all_pin_file,user_args)
        exit()
    else:
        print("\n\n[**] Cannot monitor(-m,--monitor) with --all-pin flag else use -p or -bd or dissable th -m param")
        exit()

    if not args.monitor:
        getCalender(**user_args)
        
    else:
        email = input("Please specify the email address to sent notification to :-- ")
        print('\t\t\-----Monitoring-------------- ')
        monitorAvailabitily(email,**user_args)
except ConnectionError:
    print('\n\n[[++]] Could not establish connection , Pleas check the internet connection')


