'''
Created on Jan 15, 2019
Config file uniquely generated for each client
@author: Ajay Rabidas
'''

#Host File System details
#BASE_PATH = 'G:\\work\\vasthi\\vasthi_pydev\\logs\\'
BASE_PATH = 'C:/Users/psingh06/Desktop/AKR/vasthi/'
OUTPUT_PATH = BASE_PATH+'output/'
ARCHIVE_PATH = BASE_PATH+'archived/'

#Device Serial Port Connectivity Details ----------------------------------------------:
PORT='COM7'
BAUD_RATE=9600
BIT_RATE=2
TIMEOUT=8
DATA_BYTES_START_INDEX = 3
PROTOCOL = "MODBUS"


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
    "SLAVE_ID" : 1,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 85,
    "BYTES_TO_READ" : 2,
    "PARAMS_LIST" : ["NO"],
    "OUT_TYPE" : DATA_TYPE[2],
    "ERROR_COUNT" : 0
}

DEVICE_2 = {
    "MAC_ID" : "MACABCXX0002",
    "SLAVE_ID" : 48,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 4096,
    "BYTES_TO_READ" : 6,
    "PARAMS_LIST" : ["NO","AB","CD"],
    "OUT_TYPE" : DATA_TYPE[1],
    "ERROR_COUNT" : 0
}

DEVICE_3 = {
    "MAC_ID" : "MACABCXX0003",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 0,
    "BYTES_TO_READ" : 1,
    "PARAMS_LIST" : ["O2"],
    "OUT_TYPE" : DATA_TYPE[2],
    "ERROR_COUNT" : 0
}

#DEVICE_LIST = [DEVICE_1, DEVICE_2, DEVICE_3] 
DEVICE_LIST = [DEVICE_2] 

#DEVICE_1 = ['MAC_ID', PROTOCOL, SLAVE_ID, PARAM_COUNT, START_REGISTER, NUM_REGISTERS_TO_READ]
#DEVICE_1 = ['MAC_ID', PROTOCOL, PARAM_COUNT, 'INPUT_STRING_IN_HEX', PARAMS_LIST]
#DEVICE_1 = ['MACABCXX0001', 'MODBUS', 1, '\x02\x03\x00\x00\x00\x01\x84\x39', ]
