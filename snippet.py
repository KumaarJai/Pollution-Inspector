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


def restapi():
    import requests
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = {  "title": "AKR",    "body": "bar",   "userId": 1007   }

    response = requests.post(url, data=data)
    print(response, response.content)


if __name__ == '__main__':
    import libscrc
#     restapi()
    from PyCRC.CRC16 import CRC16
#     print(hex(CRC16().calculate(y)))
#     print(format(CRC16().calculate(x),'#04x') )
#      
#     input = b'\x05d\x05\xc0\x00\x01\x00\x0c'
#     print(CRC16().calculate(input))
#     print(bytearray.fromhex('030900'))
#     
    a = b'\x02\x03\x00\x00\x00\x01' #\x84\x39
    x = b'\x02\x03\x02\x02\x52' #\x7c\xd9
    y = b'\x01\x03\x00\x00\x00\x02' #\xD4\x1B

    crc16 = libscrc.modbus(a)  # Calculate HEX of modbus
    crc16x = libscrc.modbus(x)  # Calculate HEX of modbus
    print(crc16, crc16x)
    
    print(CRC16().calculate(a), CRC16().calculate(x))


    
    
    