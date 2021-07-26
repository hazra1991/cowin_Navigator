# cowin_Navigator

* To find the cowin vaccination slots /generate report and monitor  

## Usage
```
python cowin_Navigator --help

Find the cowin slot availability

optional arguments:
  -h, --help            show this help message and exit
  -p, --bypin           search via Pin
  -bd, --bydistrict     search by state and district name
  --all-pin  <filename/filepath>
                        get the pin list to check from a file
  -m, --monitor         monitors periodicaly
  -a , --age-limit      Specify the age [+default 1 & 2}]
  --date                Date format 'dd-mm-yy' [ + Default is today ]
  --dose                Specify the dose to to searched[+ default is all]
 ```
### Example :- 

```
python cowin_navigator --dose 1 -a 18 -bd
```
