'''
Created on Jan 15, 2019
Config file uniquely generated for each client
@author: Ajay Rabidas
'''

#Host File System details
#BASE_PATH = 'D:/AJAY_545732/PROJECTS/Dektos/APPDATA/'
BASE_PATH = 'D:/AJAY_545732/PROJECTS/Dektos/APPDATA/'
OUTPUT_PATH = BASE_PATH+'output/'
ARCHIVE_PATH = BASE_PATH+'archived/'
LOG_PATH = BASE_PATH+'log/'

LOG_DEVICE_READER = LOG_PATH+'/dektos'  #absolute log file name for deviceReader.py
LOG_DB_DATA_LOADER = LOG_PATH+'/dbUpload'     #absolute log file name for DbDataLoader.py

#Device Serial Port Connectivity Details ----------------------------------------------:
PORT='COM7'
BAUD_RATE=9600
BIT_RATE=2
TIMEOUT=8
DATA_BYTES_START_INDEX = 3  #Do not change
PROTOCOL = "MODBUS"


#CLIENT Details ----------------------------------------------:
INDUSTRY_NAME='CLIENTXX_001'
INDUSTRY_ID='CL_001'
DATA_UPLOAD_INTERVAL = 30

#DATABASE DETAILS : Do Not Touch
DB_HOST_URL = 'cdotsdb.cc0wiogqy5qv.ap-northeast-2.rds.amazonaws.com'
DB_USER = 'cdotsmasterdba'
DB_PASSWORD = 'master.cdots'

#CPCB Server Details
CPCB_API_ENDPOINT = "http://localhost:5000"
#CPCB_API_ENDPOINT = 'http://182.75.69.206:8080/v1.0'
CPCB_ACCESS_TOKEN = 'ABCD1234'

#DATA_TYPES : Do Not Touch
DATA_TYPE = ["INTEGER", "BIG_I", "LITTLE_I", "MID_BIG_I", "MID_LITTLE_I"]
 
 
 
 
 
 
#SERIAL DEVICE Details in Decimal (Only 1 serial device per config file)----------------------------------------------:
SERIAL_DEVICE = {
    "STATION_ID" : "SER_1",
    "DEVICE_ID" : "SER_DEV_1",
    "PARAMS_LIST" : ["NO","SO2","CD"],
    "PARAMS_SERIAL_POS" : [0,2,3],
    "PARAMS_UNIT" : ['Kg/m3','ppm','vol%'],
    "FLAG" : "M",
    "DIAGNOSTIC_PARAMS" : ["humidityAlert", "devTemperature"],
    "ERROR_COUNT" : 0
}
 
 
 
 
 
#MODBUS DEVICE Details in Decimal----------------------------------------------:
DEVICE_1 = {
    "STATION_ID" : "PODR_1",
    "DEVICE_ID" : "MOD_DEV_1",
    "SLAVE_ID" : 1,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 85,
    "BYTES_TO_READ" : 2,
    "PARAMS_LIST" : ["NO"],
    "PARAMS_UNIT" : ['ppm'],
    "OUT_TYPE" : DATA_TYPE[2],
    "FLAG" : "M",                #"U|C|M|F|Z|D"
    "DIAGNOSTIC_PARAMS" : ["humidityAlert"],
    "ERROR_COUNT" : 0
}

DEVICE_2 = {
    "STATION_ID" : "PODR_2",
    "DEVICE_ID" : "MOD_DEV_1",
    "SLAVE_ID" : 48,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 4096,
    "BYTES_TO_READ" : 6,
    "PARAMS_LIST" : ["NO","SO2","CD"],
    "PARAMS_UNIT" : ['Kg/m3','ppm','vol%'],
    "OUT_TYPE" : DATA_TYPE[1],
    "FLAG" : "M",
    "DIAGNOSTIC_PARAMS" : ["humidityAlert", "devTemperature"],
    "ERROR_COUNT" : 0
}

DEVICE_3 = {
    "STATION_ID" : "PODR_3",
    "DEVICE_ID" : "MOD_DEV_1",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 0,
    "BYTES_TO_READ" : 1,
    "PARAMS_LIST" : ["O2"],
    "PARAMS_UNIT" : ['ppm'],
    "OUT_TYPE" : DATA_TYPE[2],
    "FLAG" : "M",
    "DIAGNOSTIC_PARAMS" : ["devTemperature"],
    "ERROR_COUNT" : 0
}

DEVICE_4 = {
    "STATION_ID" : "PODR_1",
    "DEVICE_ID" : "MOD_DEV_1",
    "SLAVE_ID" : 1,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 85,
    "BYTES_TO_READ" : 2,
    "PARAMS_LIST" : ["NO"],
    "PARAMS_UNIT" : ['ppm'],
    "OUT_TYPE" : DATA_TYPE[2],
    "FLAG" : "M",
    "DIAGNOSTIC_PARAMS" : ["devTemperature"],
    "ERROR_COUNT" : 0
}


#DEVICE_LIST = [DEVICE_1, DEVICE_2, DEVICE_3] 
DEVICE_LIST = [DEVICE_1, DEVICE_2] 




