'''
Created on Jan 19, 2019

@author: Kumaar Jai
'''

if __name__ == '__main__':
    from PyCRC.CRCCCITT import CRCCCITT
    a = b'\x02\x03\x00\x00\x00\x01\x84\x39'
    input = b'\x05d\x05\xc0\x00\x01\x00\x0c'
    print(CRCCCITT().calculate(a))