from entrypoint import getCalender,monitorAvailabitily
from argparse import ArgumentParser

my_args = ArgumentParser(description='Find the cowin slot availability',prog='Cowin Nvigator')
mygroup = my_args.add_mutually_exclusive_group( required=True)
mygroup.add_argument("-p","--bypin",action = 'store_true', help='search via Pin')
mygroup.add_argument('-bd','--bydistrict',action='store_true',help='search by state and district name')
my_args.add_argument('-m','--monitor',action='store_true',help='monitors periodicaly')
my_args.add_argument('-a','--age-limit',action="store",metavar='',choices=['18','45'],dest='age_limit',type=int,help='Specify the age [+default 1 & 2}]')
my_args.add_argument('--date',metavar='',type = str,help='Date format \'dd-mm-yy\' [ + Default is today ]')
my_args.add_argument('--dose',metavar = '',action='store',choices=['1','2'],help='Specify the dose to to searched[+ default is all]')

args = my_args.parse_args()
pin=state=district = None
if args.bypin:
    pin = input('Please enter the location pin number :- ')
elif args.bydistrict:
    state = input('Please enter the state name:- ')
    district =input('Please enter the district name:- ')
user_args = {'pin':pin,'state':state,'district':district,'min_age':args.age_limit,'from_date':args.date,'dose':args.dose}
if not args.monitor:
    getCalender(**user_args)
    
else:
    email = input("Please specify the email address to sent notification to :-- ")
    print('\t\t\-----Monitoring-------------- ')
    monitorAvailabitily(email,**user_args)

