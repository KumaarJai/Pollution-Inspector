'''
Created on Jan 15, 2019
Config file uniquely generated for each client
@author: Ajay Rabidas
'''


#Device Serial Port Connectivity Details ----------------------------------------------:
PORT='COM5'
BAUD_RATE=9600
BIT_RATE=2
TIMEOUT=3


#CLIENT Details ----------------------------------------------:
CLIENT_NAME='CLIENTXX_001'
CLIENT_ID='CL_001'
DEVICES_COUNT = 3

#DEVICE_1 Details ----------------------------------------------:
DEVICE_1 = {
    "MAC_ID" : "MACABCXX0001",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "PARAM_COUNT" : 2,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ['NO','O2'],
    "OUT_TYPE" : "INTEGER"
}

DEVICE_2 = {
    "MAC_ID" : "MACABCXX0002",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "PARAM_COUNT" : 2,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ['NO','O2'],
    "OUT_TYPE" : "INTEGER"
}

DEVICE_3 = {
    "MAC_ID" : "MACABCXX0003",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "PARAM_COUNT" : 2,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ['NO','O2'],
    "OUT_TYPE" : "INTEGER"
}

DEVICE_LIST = [DEVICE_1, DEVICE_2, DEVICE_3] 

#DEVICE_1 = ['MAC_ID', PROTOCOL, SLAVE_ID, PARAM_COUNT, START_REGISTER, NUM_REGISTERS_TO_READ]
#DEVICE_1 = ['MAC_ID', PROTOCOL, PARAM_COUNT, 'INPUT_STRING_IN_HEX', PARAMS_LIST]
#DEVICE_1 = ['MACABCXX0001', 'MODBUS', 1, '\x02\x03\x00\x00\x00\x01\x84\x39', ]


return 19255 0x4B37 '''
import numpy as np

def crc16(data: bytes):
    '''
    CRC-16-ModBus Algorithm
    '''
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)

    return np.uint16(crc)
    
    
print(crc16(b'\x31\x32\x33\x34\x35\x36\x37\x38\x39'))