'''
Created on Jan 23, 2019
@author: Ajay_Rabidas
'''
# from PyCRC.CRCCCITT import CRCCCITT
#     input = b'\x02\x03\x00\x00\x00\x01'
#     print(CRCCCITT().calculate(input))

import json
import csv
from datetime import datetime, timedelta
import re, uuid 
from ctypes import *
import modbus_python.configuration as CONF
macid= ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def getMacId():
    return macid

def HexToFloat(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value 


def extractData(demoArr):
    print('Extracting data...')
    PARAMS_LIST = ["NO","O2", "S2"]
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
        outputParamMap[str(PARAMS_LIST[count])] = int(val,16)
        
        count = count+1
        start = start + bytesPerParam
        end = end +bytesPerParam
        
    paramMapJSON = json.dumps(outputParamMap)
    writetoFile(paramMapJSON) 
    
    
def writetoFile(paramMapJSON):
    
    uniqueIdentifier = datetime.now().strftime('%Y-%m-%d#%H-%M')
    #print(datetime.now().strftime('%Y-%m-%d#%H-%M'))
    #print((datetime.now() + timedelta(minutes=30)).strftime('%Y-%m-%d#%H-%M') ) 
    file = 'data_'+uniqueIdentifier+'.tsv'
    
    targetFile = open(CONF.OUTPUT_PATH + file, 'a')
    csvWriter = csv.writer(targetFile, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, quotechar='' )
    csvWriter.writerow([getMacId(), paramMapJSON, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    targetFile.close()


if __name__ == '__main__':
    demoArr = [2,3,6,2,52,33,52,22,22,1,1]
    print(demoArr)
    while True:
        extractData(demoArr)
    