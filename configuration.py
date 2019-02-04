'''
Created on Jan 15, 2019
Config file uniquely generated for each client
@author: Ajay Rabidas
'''

#Host File System details
#BASE_PATH = 'G:\\work\\vasthi\\vasthi_pydev\\logs\\'
BASE_PATH = 'G:/work/vasthi/'
OUTPUT_PATH = BASE_PATH+'output/'
ARCHIVE_PATH = BASE_PATH+'archived/'

#Device Serial Port Connectivity Details ----------------------------------------------:
PORT='COM8'
BAUD_RATE=57600
BIT_RATE=2
TIMEOUT=5
DATA_BYTES_START_INDEX = 3

#CLIENT Details ----------------------------------------------:
CLIENT_NAME='CLIENTXX_001'
CLIENT_ID='CL_001'
DATA_UPLOAD_INTERVAL = 30

#DATABASE DETAILS
DB_HOST_URL = 'cdotsdb.cc0wiogqy5qv.ap-northeast-2.rds.amazonaws.com'
DB_USER = 'cdotsmasterdba'
DB_PASSWORD = 'master.cdots'

 
#DATA_TYPES
DATA_TYPE = ["INTEGER", "BIG_I", "LITTLE_I", "MID_BIG_I", "MID_LITTLE_I"]
 
#DEVICE Details ----------------------------------------------:
DEVICE_1 = {
    "MAC_ID" : "MACABCXX0001",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 1,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 55,
    "BYTES_TO_READ" : 2,
    "HEX_INPUT_STRING" : b'\x01\x03\x00\x55\x00\x02\xD4\x1B',
    "PARAMS_LIST" : ["NO"],
    "OUT_TYPE" : DATA_TYPE[2]
}

DEVICE_2 = {
    "MAC_ID" : "MACABCXX0002",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 0,
    "BYTES_TO_READ" : 1,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ["NO"],
    "OUT_TYPE" : DATA_TYPE[1]
}

DEVICE_3 = {
    "MAC_ID" : "MACABCXX0003",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 0,
    "BYTES_TO_READ" : 1,
    "HEX_INPUT_STRING" : b'\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ["O2"],
    "OUT_TYPE" : DATA_TYPE[2]
}

#DEVICE_LIST = [DEVICE_1, DEVICE_2, DEVICE_3] 
DEVICE_LIST = [DEVICE_1] 

#DEVICE_1 = ['MAC_ID', PROTOCOL, SLAVE_ID, PARAM_COUNT, START_REGISTER, NUM_REGISTERS_TO_READ]
#DEVICE_1 = ['MAC_ID', PROTOCOL, PARAM_COUNT, 'INPUT_STRING_IN_HEX', PARAMS_LIST]
#DEVICE_1 = ['MACABCXX0001', 'MODBUS', 1, '\x02\x03\x00\x00\x00\x01\x84\x39', ]
