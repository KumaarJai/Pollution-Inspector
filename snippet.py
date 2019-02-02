'''
Created on Jan 19, 2019

@author: Kumaar Jai
'''
import time
from datetime import datetime
from datetime import timedelta
from ctypes import *
import struct
from PyCRC.CRC16 import CRC16
from serial.tools.hexlify_codec import hex_decode

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

 
def hex2float(s):
    bins = ''.join(chr(int(s[x:x+2], 16)) for x in range(0, len(s), 2))
    return struct.unpack('>f', bins)[0]


def convert(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float


def trial():
    val = "41973336"
    val_arr = [val[4:6], val[6:8], val[0:2], val[2:4]]
    s=''
    for item in val_arr:
        s=s+item
    print(s)
    print(val_arr)



if __name__ == '__main__':
    
    #import requests
    
    from PyCRC.CRC16 import CRC16
    a = b'\x02\x03\x00\x00\x00\x01' #\x84\x39
    
    x2= format(6000,'#04x').replace('0x','')
    x1= format(0,'#04x').replace('0x','\\x')
    x1= format(0,'#04x').replace('0x','\\x')
    x1= format(0,'#04x').replace('0x','\\x')
    bb= format(0,'#04x').replace('0x','\\x') + format(2,'#04x').replace('0x','\\x')
    
    print(len(x2), x2)
    s=''
    if len(x2) < 4:
        s = '\\x0'+x2[0:1] +'\\x'+x2[1:3]
    elif len(x2) == 4:
        s = '\\x'+x2[0:2] + '\\x'+x2[2:4]
    print(s) 
#     print(CRC16().calculate(a))
#     print(int("8439",16))
#     print(int("8836",16))