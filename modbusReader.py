'''
Created on Jan 15, 2019
@author: Ajay Rabidas
'''

import logging as LOGGER
from modbusInterface import configuration as CONF
from modbusInterface import dektosExternalPackageInstaller as DEKTOS_INSTALLER

LOG_FILENAME = CONF.BASE_PATH+'dektos.log'
LOGGER.basicConfig(filename=LOG_FILENAME,level=LOGGER.DEBUG)
LOGGER.debug('Log file initiated, System starting up...')

LOGGER.debug('Installing external python packages required to run this application..')
DEKTOS_INSTALLER.installPackage('pyserial')
DEKTOS_INSTALLER.installPackage('PyCRC')
LOGGER.debug('Installation complete. System started successfully')

import serial
import time
from PyCRC.CRCCCITT import CRCCCITT




def connectToDevice():
    try:
        ser = serial.Serial(CONF.PORT, CONF.BAUD_RATE,timeout=CONF.TIMEOUT)
        if(ser.isOpen()):
            print(ser.name + ' is open--------------------------------------------')
            LOGGER.debug(ser.name + ' is open--------------------------------------------')
    except:
        print(ser.name + ' : Failed to open')
        LOGGER.debug(ser.name + '  : Failed to open')
        ser.close()
        exit()
    
    try:
        next_time = 0
        fileName = 'G:\\work\\vasthi\\out\\dektos_'+str(time.clock())+'.txt'
        f = open(fileName, 'a')
        print("-------new file ",fileName)
        while True:
            if time.clock() >= next_time and next_time>0:
                f.close()
                next_time = time.time()+20
                fileName = 'G:\\work\\vasthi\\out\\dektos_'+str(time.clock())+'.txt'
                print("file name ",fileName)
            f = open(fileName, 'a')
            
            for i in range(0, CONF.DEVICES_COUNT):
                device = CONF.DEVICE_LIST[i]
                readModbusData(ser, device, f)
            
            print('\n initiating next cycle')
            print('_____________________________________________________________________________\n')
    except:
        print(ser.name + ' : Error occured while processing. Exiting application')
        LOGGER.debug(ser.name + '  : Error occured while processing. Exiting application')
        ser.close()
        exit()



def readModbusData(ser, device, targetFile):
    outData = []
    print(device["MAC_ID"], ' Requesting : ', device["HEX_INPUT_STRING"])
    targetFile.write(device["MAC_ID"]+ ' Requesting : '+ device["HEX_INPUT_STRING"])
    ser.write(device["HEX_INPUT_STRING"])
    out = ser.readline()
    for byte in out:
        outData.append(byte)
        
    if outData !=[]:
        if isOutputAligned(device, outData):
            extractData2(device, outData, targetFile)


def extractData(device, outData):
    print('Extracting data...')
    outDataBytesCount = outData[3]
    bytesPerParam = outDataBytesCount/device["PARAM_COUNT"]
    bytePosition = 0
    for i in range(3,len(outData)-2):
        bytePosition = i
        for j in range(0,bytesPerParam):
            #some logic here
            print("some logic here...")


def extractData2(device, outData, targetFile):
    #print("printing data in extractData2")
    print('Reply : ',outData)
    print('\n')
    
    targetFile.write('Reply : '+outData)
    targetFile.write('\n')


def isOutputAligned(device, outData):
#     if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"] and generateCRC(outData)==generateCRC(device["HEX_INPUT_STRING"]):
    if outData[0]==device["SLAVE_ID"] and outData[1]==device["HOLDING_REGISTER"]:
        return True



def generateCRC(data):
    #incomplete logic
    return data



def readSerialData(device):
    print(device["MAC_ID"]+' : Initiating serial data read...')


def readModbus(ser):
    count = 0
    if(ser.isOpen()):
        print(ser.name + ' is open---------------------------------------------------')
    
    while count <2:
        outData = []
        print('Sending...')
        ser.write(b'\x02\x03\x00\x00\x00\x01\x84\x39')
        out = ser.readline()
        print(out)
        count=count+1
        for byte in out:
            outData.append(byte)
        print(outData) # present ascii
    ser.close()

if __name__ == '__main__':
    connectToDevice()
    
    