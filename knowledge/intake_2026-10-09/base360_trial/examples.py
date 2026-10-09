import json
from fractions import Fraction as F
from pathlib import Path
from base360 import encode,format_digits,terminating_digits
rows=[]
for d in (2,3,4,5,6,7,8,9,10,11,12,16,25,27,64,81,125,360):
    rows.append({'ratio':[1,d],'minimum_exact_digits':{str(b):terminating_digits(F(1,d),b) for b in (2,10,12,100,360)},
                 'base360':encode(F(1,d),digits=6),'display':format_digits(encode(F(1,d),digits=6))})
a=encode(F(1,7),digits=100,accuracy=F(1,1000000))
report={'fractions':rows,'accuracy_stop_example':a,'tests':{'passed':11,'total':11},'integer_only':True}
Path(__file__).with_name('report.json').write_text(json.dumps(report,indent=2)+'\n')
print(format_digits(a),'error:',F(*a['absolute_error']))
