'''
Created on Feb 2, 2019
Utility module
@author: Kumaar Jai
'''
from ctypes import cast, pointer, c_int, c_float, POINTER
from modbusInterface import configuration as CONF
from modbusInterface import dektosCRC
from builtins import str
DATA_TYPE = CONF.DATA_TYPE


def getConvertedData(val, dtype):
    if dtype == DATA_TYPE[0]:     #INTEGER
        return int(val,16)
    
    elif dtype == DATA_TYPE[1]:   #ABCD - BIG_I
        return hexToFloat(val)
    
    elif dtype == DATA_TYPE[2]:   #DCBA - LITTLE_I
        val_arr = [val[6:8], val[4:6], val[2:4], val[0:2]]
        strval=''
        for item in val_arr:
            strval=strval+item
        return hexToFloat(strval)
    
    elif dtype == DATA_TYPE[3]:   #BADC - MID_BIG_I
        val_arr = [val[2:4], val[0:2], val[6:8], val[4:6]]
        strval=''
        for item in val_arr:
            strval=strval+item
        return hexToFloat(strval)
    
    elif dtype == DATA_TYPE[4]:   #CDAB - MID_LITTLE_I
        val_arr = [val[4:6], val[6:8], val[0:2], val[2:4]]
        strval=''
        for item in val_arr:
            strval=strval+item
        return hexToFloat(strval)
    
    

def hexToFloat(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float


def handleByteAbove255(val):
    if len(val) < 4:
        val = '0'+val
    return val



def generateInputString(device):
    slaveId= format(device["SLAVE_ID"],'#04x').replace('0x','')
    holdingRegister= format(device["HOLDING_REGISTER"],'#04x').replace('0x','')
    start = ''
    bytesToRead = ''
    if device["START_REGISTER"] > 255:
        start = handleByteAbove255(format(device["START_REGISTER"],'#04x').replace('0x',''))
    else:
        start = start + '00' + format(device["START_REGISTER"],'#04x').replace('0x','')
    
    
    if device["BYTES_TO_READ"] > 255:
        bytesToRead = handleByteAbove255(format(device["BYTES_TO_READ"],'#04x').replace('0x',''))
    else:
        bytesToRead = bytesToRead + '00' + format(device["BYTES_TO_READ"],'#04x').replace('0x','')
    
    interimn_input_string = slaveId + holdingRegister + start + bytesToRead
    final_input_string = interimn_input_string + dektosCRC.CRC16_BIG_INDIAN(bytes.fromhex(interimn_input_string).decode('utf-8'))
    
    
#    Testing functionality
#    print(final_input_string, bytes.fromhex(final_input_string), bytes.fromhex(final_input_string).decode('latin-1') == device["HEX_INPUT_STRING"])
#    print(device["HEX_INPUT_STRING"], bytes.fromhex(final_input_string).decode('latin-1') == device["HEX_INPUT_STRING"])
    return bytes.fromhex(final_input_string)






if __name__ == '__main__':
    DEVICE_2 = {
    "MAC_ID" : "MACABCXX0001",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 1,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 85,
    "BYTES_TO_READ" : 2,
    "HEX_INPUT_STRING" : '\x01\x03\x00\x55\x00\x02\xD4\x1B',
    "PARAMS_LIST" : ["NO"],
    "OUT_TYPE" : DATA_TYPE[2]
    }
    
    DEVICE_1 = {
    "MAC_ID" : "MACABCXX0001",
    "PROTOCOL" : "MODBUS",
    "SLAVE_ID" : 2,
    "HOLDING_REGISTER" : 3,
    "START_REGISTER" : 0,
    "BYTES_TO_READ" : 1,
    "HEX_INPUT_STRING" : '\x02\x03\x00\x00\x00\x01\x84\x39',
    "PARAMS_LIST" : ["NO"],
    "OUT_TYPE" : DATA_TYPE[2]
    }

    generateInputString(DEVICE_1)
    generateInputString(DEVICE_2)
    #print(dektosCRC.CRC16_BIG_INDIAN(d))

#     val = "79d33e44"
#     print(getConvertedData(val, DATA_TYPE[1]))
#     print(getConvertedData(val, DATA_TYPE[2]))
#     print(getConvertedData(val, DATA_TYPE[3]))
#     print(getConvertedData(val, DATA_TYPE[4]))

