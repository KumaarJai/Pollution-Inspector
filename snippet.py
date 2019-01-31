'''
Created on Jan 19, 2019

@author: Kumaar Jai
'''
import time
from datetime import datetime
from datetime import timedelta


def a():
    c = time.strptime("2002-03-14 17:12:00", "%Y-%m-%d %H:%M:%S")
    t = time.mktime(c)
    print(t)
    # 1016098920.0
    t = t + 30  # 30 minutes is 1800 secs
    print(t)
    # 1016100720.0
    x = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    print(x)
    # '2002-03-14 18:12:00'


def b():
    print('xxxx')
#     a = b'\x02\x03\x00\x00\x00\x01\x84\x39'
#     input = b'\x05d\x05\xc0\x00\x01\x00\x0c'
#     print(CRCCCITT().calculate(a))


if __name__ == '__main__':
    next_time = 0
    while True:
        if next_time != 0 and datetime.now() >= next_time:
            print('*********Not initial step : ',next_time)
            next_time = next_time + timedelta(seconds=10) 
    
        elif next_time == 0:
            print('This is initial step : ',next_time)
            next_time = datetime.now() + timedelta(seconds=10) 
            print('Added 10 sec initially', next_time)
        
        for i in range(0,5):
            print('processing device - ',i)
            time.sleep(1)

            
        print('\n initiating next cycle')
        print('_____________________________________________________________________________\n')
