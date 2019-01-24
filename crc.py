'''
Created on Jan 23, 2019

@author: Ajay_Rabidas
'''
# from PyCRC.CRCCCITT import CRCCCITT
#     input = b'\x02\x03\x00\x00\x00\x01'
#     print(CRCCCITT().calculate(input))

import json
from ctypes import *

def HexToFloat(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value 


def extractData(demoArr):
    print('Extracting data...')
    PARAMS_LIST = ['NO','O2', 'S2']
    outputParamMap = {}
    dataBytesStartIndex = 3
    NumberOfOutDataBytesRecieved = demoArr[2]
    paramCount = len(PARAMS_LIST)
    bytesPerParam = int(NumberOfOutDataBytesRecieved/paramCount)
    count = 0
    
    start = dataBytesStartIndex
    end = dataBytesStartIndex + bytesPerParam
    while(count < paramCount):
        val=''
        for i in range(start,end):
            val=val + str(demoArr[i])
        print(val)
        outputParamMap[PARAMS_LIST[count]] = int(val,16)
        
        count = count+1
        start = start + bytesPerParam
        end = end +bytesPerParam
            
    
    print(json.dumps(outputParamMap)) 


if __name__ == '__main__':
    demoArr = [2,3,6,2,52,33,52,22,22,1,1]
    print(demoArr)
    extractData(demoArr)
    