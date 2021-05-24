from entrypoint import getCalenderAvailability
from argparse import ArgumentParser,Action

my_args = ArgumentParser(description='Find the cowin slot availability',prog='Cowin Nvigator')

# myargs.add_argument('variable',help ='intiget')
mygroup = my_args.add_mutually_exclusive_group( required=True)
mygroup.add_argument("-p","--bypin",action = 'store_true', help='search via Pin')
mygroup.add_argument('-di','--bydistrict',action='store_true',help='search by state and district name')
my_args.add_argument('-m','--monitor',action='store_true',help='monitors periodicaly')
my_args.add_argument('-a','--age-limit',action="store",metavar='',dest='age_limit',type=int,help='Specify the age [by default considers everything]')
my_args.add_argument('--date',metavar='\'dd-mm-yy\'',type = str,help='Date which is needed to be concidered [ + Default is today ]')

args = my_args.parse_args()
pin=state=district = None

if args.bypin:
    pin = input('Please enter the pin number :- ')
elif args.bydistrict:
    state = input('Please enter the state name:- ')
    district =input('Please enter the district name:- ')
user_args = {'pin':pin,'state':state,'district':district,'min_age':args.age_limit,'from_date':args.date}
getCalenderAvailability(**user_args)

