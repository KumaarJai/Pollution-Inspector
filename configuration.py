'''
Created on Jan 15, 2019
Config file uniquely generated for each client
@author: Ajay Rabidas
'''

#Host File System details
#BASE_PATH = 'G:\\work\\vasthi\\vasthi_pydev\\logs\\'
BASE_PATH = 'D:/AJAY_545732/PROJECTS/Dektos/'
OUTPUT_PATH = BASE_PATH+'output/'
ARCHIVE_PATH = BASE_PATH+'archived/'

#Device Serial Port Connectivity Details ----------------------------------------------:
PORT='COM5'
BAUD_RATE=9600
BIT_RATE=2
TIMEOUT=3
DATA_BYTES_START_INDEX = 3

#CLIENT Details ----------------------------------------------:
CLIENT_NAME='CLIENTXX_001'
CLIENT_ID='CL_001'
DEVICES_COUNT = 3
DATA_UPLOAD_INTERVAL = 30

#DATABASE DETAILS
DB_HOST_URL = 'cdotsdb.cc0wiogqy5qv.ap-northeast-2.rds.amazonaws.com'
DB_USER = 'cdotsmasterdba'
DB_PASSWORD = 'master.cdots'

 
 
#DEVICE Details ----------------------------------------------:
DEVICE_1 = {
    "MAC_ID" : "MACABCXX0001",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "PARAM_COUNT" : 2,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ["NO","O2", "S2"],
    "OUT_TYPE" : "INTEGER"
}

DEVICE_2 = {
    "MAC_ID" : "MACABCXX0002",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "PARAM_COUNT" : 2,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ["NO","O2", "S2"],
    "OUT_TYPE" : "INTEGER"
}

DEVICE_3 = {
    "MAC_ID" : "MACABCXX0003",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "PARAM_COUNT" : 2,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ["NO","O2", "S2"],
    "OUT_TYPE" : "INTEGER"
}

DEVICE_LIST = [DEVICE_1, DEVICE_2, DEVICE_3] 

#DEVICE_1 = ['MAC_ID', PROTOCOL, SLAVE_ID, PARAM_COUNT, START_REGISTER, NUM_REGISTERS_TO_READ]
#DEVICE_1 = ['MAC_ID', PROTOCOL, PARAM_COUNT, 'INPUT_STRING_IN_HEX', PARAMS_LIST]
#DEVICE_1 = ['MACABCXX0001', 'MODBUS', 1, '\x02\x03\x00\x00\x00\x01\x84\x39', ]
