'''
Created on Jan 15, 2019
@author: Ajay Rabidas
'''

import os
import sys
sys.path.append("/".join(os.getcwd().split('\\')[0:-1]))
from modbusInterface import configuration as CONF
from modbusInterface import dektosExternalPackageInstaller as DEKTOS_INSTALLER
from modbusInterface import dektosLogger
from modbusInterface import util as UTIL
from modbusInterface import dbUtil as DBUTIL



LOG_FILENAME = CONF.LOG_DEVICE_READER
LOGGER = dektosLogger.AppLogger(LOG_FILENAME).getLogger()
LOGGER.info('Log file initiated, System starting up...') 


try:
    LOGGER.info('Installing external python packages required to run this application..')
    DEKTOS_INSTALLER.installMandatoryPackages()
    LOGGER.info('Installation complete. System started successfully')
except Exception as e:
    LOGGER.info('Installation Failed. System will exit...')
    LOGGER.exception(e)
    sys.exit(1)

#------------------------------------------------------------------------------------------------------------------------------

import serial
import re, uuid 
import json
import csv
from datetime import datetime
from datetime import timedelta
#from PyCRC.CRC16 import CRC16



def getMacId():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def connectToDevice(mode):
    LOGGER.info('Connecting to device. PROTOCOL : '+mode)
    try:
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
                next_time = next_time + timedelta(seconds=60) 
                file = CONF.OUTPUT_PATH + 'data_'+datetime.now().strftime('%Y-%m-%d#%H-%M')+'.tsv'
                LOGGER.info("file name "+file)
                f = open(file, 'a')
                
            elif next_time == 0:
                next_time = datetime.now() + timedelta(seconds=60) 
                
            if mode == 'SERIAL':
                print('Initiating serial read...')
                readSerialData(ser.readline(), f)
                
            elif mode == 'MODBUS':        
                for i in range(0, len(CONF.DEVICE_LIST)):
                    device = CONF.DEVICE_LIST[i]
                    readModbusData(ser, device, f)
                    #readDummyData(ser, device, f)
            
            LOGGER.info('\n initiating next cycle')
            LOGGER.info('_____________________________________________________________________________\n')
    except Exception as e:
        LOGGER.info(ser.name + '  : Error occured while processing.')
        print(e)
        ser.close()
        connectToDevice(CONF.PROTOCOL)
        #exit()



def readSerialData(out, targetFile):
    device = CONF.SERIAL_DEVICE
    errC = device["ERROR_COUNT"]
    LOGGER.info(device["DEVICE_ID"]+' error count : '+str(errC))
#    outData = []
    outputParamMap = {}
    SERIAL_PARAMS_LIST = device["PARAMS_LIST"]
    SERIAL_PARAMS_INDEX = device["PARAMS_SERIAL_POS"]
    
    outData = [x for x in out.decode(encoding='UTF-8').split(',')]
    outData.pop(0)
#     for byte in out:
#         outData.append(byte)
    
    if outData == []:
        if errC >=3:
            LOGGER.info('\n\n send error data to server...........')
            errC = 0
        elif errC < 3:
            errC = errC +1
        CONF.SERIAL_DEVICE["ERROR_COUNT"] = errC   
        
    if outData !=[]:
        for i in range(0, len(SERIAL_PARAMS_LIST)):
            outputParamMap[str(SERIAL_PARAMS_LIST[i])] = outData[SERIAL_PARAMS_INDEX[i]]
        paramMapJSON = json.dumps(outputParamMap)
        writetoFile(paramMapJSON, targetFile) 
        prepareDataForCPCB(paramMapJSON, device)
    else:
        LOGGER.info('Cannot read to device data... send error to server')




def readModbusData(ser, device, targetFile):
    outData = []   
    #errC = 0 
    errC = device["ERROR_COUNT"]
    LOGGER.info(device["DEVICE_ID"]+' error count : '+str(errC))
    inputString = UTIL.generateInputString(device)
    LOGGER.info(device["DEVICE_ID"]+ ' Requesting : '+ str(inputString))
    #LOGGER.info(str(device["HEX_INPUT_STRING"]))    #just for testing the correctness of input string
    ser.write(inputString)
    out = ser.readline()
    LOGGER.info('output recieved : ')
    LOGGER.info(out)

    for byte in out:
        outData.append(byte)
    
    if outData == []:
        if errC >=3:
            LOGGER.info('\n\n send error data to server...........')
            errC = 0
        elif errC < 3:
            errC = errC +1
        device["ERROR_COUNT"] = errC

    if outData !=[]:
        if isOutputAligned(device, outData, out):
            device["ERROR_COUNT"] = 0
            extractData(device, outData, targetFile)
        else:
            errC = errC +1
            device["ERROR_COUNT"] = errC




def extractData(device, outData, targetFile):
    LOGGER.info('Extracting data..............')
    #print(outData)
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
    prepareDataForCPCB(paramMapJSON, device)
    

    
def writetoFile(paramMapJSON, targetFile):
    csvWriter = csv.writer(targetFile, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, quotechar='' )
    csvWriter.writerow([getMacId(), paramMapJSON, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    #time.sleep(2)
    #targetFile.close()



def prepareDataForCPCB(paramMapJSON, device):
    paramList = device["PARAMS_LIST"]
    unitList = device["PARAMS_UNIT"]
    diagnosticList = device["DIAGNOSTIC_PARAMS"]
    cpcbMap = {}
    params = []
    diagnostics = []
    #paramData = {}
    cpcbMap["deviceId"] = device["DEVICE_ID"]
    for i in range(0, len(paramList)):
        params.append({
                "parameter" : paramList[i],
                "value" : paramMapJSON[paramList[i]],
                "unit" : unitList[i],
                "timestamp" : UTIL.getUnixTime(),
                "flag" : device["FLAG"]
            })
    for d in range(0, len(diagnosticList)):
        diagnostics.append({
                "diagParam" : diagnosticList[d],
                "value" : 0,
                "timestamp" : UTIL.getUnixTime()
            })
    cpcbMap["params"] = params
    cpcbMap["diagnostics"] = diagnostics
    #print(json.dumps(cpcbMap))
    
    try:
        DBUTIL.loadCPCBDataToLocalDB(CONF.INDUSTRY_ID, device["STATION_ID"], json.dumps(cpcbMap))
        #loadedToLocalDB = DBUTIL.loadCPCBDataToLocalDB(CONF.INDUSTRY_ID, device["STATION_ID"], json.dumps(cpcbMap))
        #print('loadedToLocalDB', loadedToLocalDB)
    except Exception as e:
        LOGGER.exception(e)
        LOGGER.info("Couldn't load : " + cpcbMap)
        pass




def isOutputAligned(device, outData, out):
    #[48, 3, 12, 63, 87, 126, 50, 64, 13, 77, 223, 0, 0, 0, 0, 65, 4]
    LOGGER.info('checking isOutputAligned....')
    print(outData)
    interimOutString = outData[0:-2]
    outCrc = outData[-2:]
    print(interimOutString, '----' ,outCrc)
    if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"] and UTIL.verifyOutCRC(interimOutString, outCrc):
        return True
    else:
        return False


#Demo purpose only
# def readDummyData(ser, device, targetFile):
#     outData = [2,3,6,2,52,33,52,22,22,1,1]
#     extractData(device, outData, targetFile)




if __name__ == '__main__':
    #from modbusInterface import installer as INSTALLER
    #INSTALLER.generateDirectorySturcture()
    connectToDevice(CONF.PROTOCOL)

    