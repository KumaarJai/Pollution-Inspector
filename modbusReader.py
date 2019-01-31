'''
Created on Jan 15, 2019
@author: Ajay Rabidas
'''

import logging as LOGGER
import sys

from modbusInterface import configuration as CONF
from modbusInterface import dektosExternalPackageInstaller as DEKTOS_INSTALLER

LOG_FILENAME = CONF.BASE_PATH+'log/dektos.log'
#LOGGER.basicConfig(filename=LOG_FILENAME,level=LOGGER.DEBUG)

LOGGER.basicConfig(
    level=LOGGER.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        LOGGER.FileHandler("{0}.log".format(LOG_FILENAME)),
        LOGGER.StreamHandler()
    ])

LOGGER.debug('Log file initiated, System starting up...') 


try:
    LOGGER.debug('Installing external python packages required to run this application..')
    DEKTOS_INSTALLER.installMandatoryPackages()
    LOGGER.info('Installation complete. System started successfully')
except Exception as e:
    LOGGER.info('Installation Failed. System will exit...')
    LOGGER.exception(e)
    sys.exit(1)


import serial
import re, uuid 
import time
import json
import csv
from datetime import datetime
from datetime import timedelta
#from PyCRC.CRC16 import CRC16


def getMacId():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def connectToDevice():
    try:
        ser = ''
#         ser = serial.Serial(CONF.PORT, CONF.BAUD_RATE,timeout=CONF.TIMEOUT)
#         if(ser.isOpen()):
#             print(ser.name + ' is open--------------------------------------------')
#             LOGGER.info(ser.name + ' is open--------------------------------------------')
    except:
        print(ser.name + ' : Failed to open')
        LOGGER.debug(ser.name + '  : Failed to open')
        ser.close()
        exit()
    
    try:
        next_time = 0
        file = CONF.OUTPUT_PATH + 'data_'+datetime.now().strftime('%Y-%m-%d#%H-%M')+'.tsv'
        f = open(file, 'a')
        print("-------new file ",file)
        
        while True:
            if next_time != 0 and datetime.now() >= next_time:
                print(next_time)
                f.close()
                next_time = next_time + timedelta(seconds=30) 
                file = CONF.OUTPUT_PATH + 'data_'+datetime.now().strftime('%Y-%m-%d#%H-%M')+'.tsv'
                print("file name ",file)
                f = open(file, 'a')
                
            elif next_time == 0:
                next_time = datetime.now() + timedelta(seconds=30) 
                
                
            for i in range(0, CONF.DEVICES_COUNT):
                device = CONF.DEVICE_LIST[i]
                #readModbusData(ser, device, f)
                readDummyData(ser, device, f)
            
            print('\n initiating next cycle')
            print('_____________________________________________________________________________\n')
    except:
        print(ser.name + ' : Error occured while processing. Exiting application')
        LOGGER.debug(ser.name + '  : Error occured while processing. Exiting application')
        ser.close()
        exit()


def readDummyData(ser, device, targetFile):
    outData = [2,3,6,2,52,33,52,22,22,1,1]
    print(device["MAC_ID"], ' Requesting : ', device["HEX_INPUT_STRING"])
    #targetFile.write(device["MAC_ID"]+ ' Requesting : '+ str(device["HEX_INPUT_STRING"]))
    extractData(device, outData, targetFile)


def readModbusData(ser, device, targetFile):
    outData = []
    print(device["MAC_ID"], ' Requesting : ', device["HEX_INPUT_STRING"])
    targetFile.write(device["MAC_ID"]+ ' Requesting : '+ str(device["HEX_INPUT_STRING"]))
    ser.write(device["HEX_INPUT_STRING"])
    out = ser.readline()
    for byte in out:
        outData.append(byte)
        
    if outData !=[]:
        if isOutputAligned(device, outData):
            extractData(device, outData, targetFile)


def extractData(device, outData, targetFile):
    print('Extracting data...')
    PARAMS_LIST = device["PARAMS_LIST"]
    dataBytesStartIndex = CONF.DATA_BYTES_START_INDEX
    outputParamMap = {}
    
    NumberOfOutDataBytesRecieved = outData[2]
    paramCount = len(PARAMS_LIST)
    bytesPerParam = int(NumberOfOutDataBytesRecieved/paramCount)
    
    start = dataBytesStartIndex
    end = dataBytesStartIndex + bytesPerParam
    count = 0
    
    while(count < paramCount):
        val=''
        for i in range(start,end):
            val=val + str(outData[i])
        #print(val)
        outputParamMap[str(PARAMS_LIST[count])] = int(val,16)
        
        count = count+1
        start = start + bytesPerParam
        end = end +bytesPerParam
        
    paramMapJSON = json.dumps(outputParamMap)
    writetoFile(paramMapJSON, targetFile) 
    
    
def writetoFile(paramMapJSON, targetFile):
    csvWriter = csv.writer(targetFile, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, quotechar='' )
    csvWriter.writerow([getMacId(), paramMapJSON, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    time.sleep(2)
    #targetFile.close()
    

def isOutputAligned(device, outData):
#     if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"] and generateCRC(outData)==generateCRC(device["HEX_INPUT_STRING"]):
    if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"]:
        return True




if __name__ == '__main__':
    connectToDevice()
    
    