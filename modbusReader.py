'''
Created on Jan 15, 2019
@author: Ajay Rabidas
'''

import logging as LOGGER
import sys

from modbusInterface import configuration as CONF
from modbusInterface import dektosExternalPackageInstaller as DEKTOS_INSTALLER
from modbusInterface import util as UTIL

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
    LOGGER.info('Installing external python packages required to run this application..')
    DEKTOS_INSTALLER.installMandatoryPackages()
    LOGGER.info('Installation complete. System started successfully')
except Exception as e:
    LOGGER.info('Installation Failed. System will exit...')
    LOGGER.exception(e)
    sys.exit(1)


import serial
import re, uuid 
import json
import csv
from datetime import datetime
from datetime import timedelta
#from PyCRC.CRC16 import CRC16


def getMacId():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def connectToDevice():
    try:
        #ser = ''
        ser = serial.Serial(CONF.PORT, CONF.BAUD_RATE,timeout=CONF.TIMEOUT)
        if(ser.isOpen()):
            LOGGER.info(ser.name + ' is open--------------------------------------------')
    except:
        LOGGER.info(ser.name + '  : Failed to open')
        ser.close()
        exit()
    
    try:
        next_time = 0
        file = CONF.OUTPUT_PATH + 'data_'+datetime.now().strftime('%Y-%m-%d#%H-%M')+'.tsv'
        f = open(file, 'a')
        LOGGER.info("-------new file "+file)
        
        while True:
            if next_time != 0 and datetime.now() >= next_time:
                print(next_time)
                f.close()
                next_time = next_time + timedelta(seconds=30) 
                file = CONF.OUTPUT_PATH + 'data_'+datetime.now().strftime('%Y-%m-%d#%H-%M')+'.tsv'
                LOGGER.info("file name "+file)
                f = open(file, 'a')
                
            elif next_time == 0:
                next_time = datetime.now() + timedelta(seconds=30) 
                
                
            for i in range(0, len(CONF.DEVICE_LIST)):
                device = CONF.DEVICE_LIST[i]
                readModbusData(ser, device, f)
                #readDummyData(ser, device, f)
            
            LOGGER.info('\n initiating next cycle')
            LOGGER.info('_____________________________________________________________________________\n')
    except Exception as e:
        LOGGER.info(ser.name + '  : Error occured while processing. Exiting application')
        print(e)
        ser.close()
        exit()




def readModbusData(ser, device, targetFile):
    outData = []
    LOGGER.info(device["MAC_ID"]+ ' Requesting : '+ str(device["HEX_INPUT_STRING"]))
    #targetFile.write(device["MAC_ID"]+ ' Requesting : '+ str(device["HEX_INPUT_STRING"]))
    #ser.write(device["HEX_INPUT_STRING"])
    ser.write(UTIL.generateInputString(device))
    out = ser.readline()
    for byte in out:
        outData.append(byte)
    
    if outData !=[]:
        if isOutputAligned(device, outData):
            extractData(device, outData, targetFile)






def extractData(device, outData, targetFile):
    print('Extracting data...')
    print(outData)
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
            #print(format(outData[i],'#04x').replace('0x',''))
            val = val + format(outData[i],'#04x').replace('0x','')  #convert to HEX and remove 0x
        #print(val)
        finalValue = UTIL.getConvertedData(val, device["OUT_TYPE"])
        outputParamMap[str(PARAMS_LIST[count])] = finalValue
        
        count = count+1
        start = start + bytesPerParam
        end = end +bytesPerParam
        
    paramMapJSON = json.dumps(outputParamMap)
    writetoFile(paramMapJSON, targetFile) 
    
    
def writetoFile(paramMapJSON, targetFile):
    csvWriter = csv.writer(targetFile, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, quotechar='' )
    csvWriter.writerow([getMacId(), paramMapJSON, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    #time.sleep(2)
    #targetFile.close()
    

def isOutputAligned(device, outData):
#     if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"] and generateCRC(outData)==generateCRC(device["HEX_INPUT_STRING"]):
    if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"]:
        return True



#Demo purpose only
def readDummyData(ser, device, targetFile):
    outData = [2,3,6,2,52,33,52,22,22,1,1]
    LOGGER.info(device["MAC_ID"]+ ' Requesting : '+ str(device["HEX_INPUT_STRING"]))
    #targetFile.write(device["MAC_ID"]+ ' Requesting : '+ str(device["HEX_INPUT_STRING"]))
    extractData(device, outData, targetFile)






if __name__ == '__main__':
    connectToDevice()
    
    