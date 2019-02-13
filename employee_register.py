import subprocess
from glob import glob
from random import randint
from db_interface import employee_sign_in, employee_sign_out
from datetime import datetime, time
import pytz

employee_ids = ['f555de482d1611e99ae542010a8a0003', '73c4c0be2d1711e99ae542010a8a0003', '3fa94a342d1711e99ae542010a8a0003', 'b15749882d1711e99ae542010a8a0003']


def populate(dt):

    print(dt)

    for employee_id in employee_ids[1:]:
   

        t = time(randint(8, 11), 00, 00)
        ts = datetime.combine(dt, t)

        print(ts)
        print(dt, ':', t, ':', employee_sign_in(employee_id, ts))    
 

        tout = time(randint(19, 21), 00, 00)
        tsout = datetime.combine(dt, tout)
   
        print(tsout)
        print(dt, ':', tout, ':', employee_sign_out(employee_id, tsout))


for days in range(1, 21):
    #dt = datetime.date.fromisoformat('2019-02-{%2d}'.format(days))
    dt = datetime.strptime('Feb {} 2019  1:30PM'.format(days), '%b %d %Y %I:%M%p').date()
    populate(dt)


