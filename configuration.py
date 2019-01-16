
#Device Serial Port Connectivity Details ----------------------------------------------:

PORT='COM3'
BAUD_RATE=9600
BIT_RATE=2
TIMEOUT=3


#CLIENT Details ----------------------------------------------:

CLIENT_NAME='CLIENTXX_001'
CLIENT_ID='CL_001'
DEVICES_COUNT = 3
DEVICE_LIST = [DEVICE_1, DEVICE_2, DEVICE_3] 

#DEVICE_1 Details ----------------------------------------------:

DEVICE_1 = {
	"MAC_ID" : "MACABCXX0001",
	"PROTOCOL" : "MODBUS",
	"PARAM_COUNT" : 2,
	"HEX_INPUT_STRING" : '\x02\x03\x00\x00\x00\x01\x84\x39',
	"PARAMS_LIST" : ['NO','O2'],
	"OUT_TYPE" : "INTEGER"
}

DEVICE_2 = {
	"MAC_ID" : "MACABCXX0002",
	"PROTOCOL" : "MODBUS",
	"PARAM_COUNT" : 2,
	"HEX_INPUT_STRING" : '\x02\x03\x00\x00\x00\x01\x84\x39',
	"PARAMS_LIST" : ['NO','O2'],
	"OUT_TYPE" : "INTEGER"
}

DEVICE_3 = {
	"MAC_ID" : "MACABCXX0003",
	"PROTOCOL" : "MODBUS",
	"PARAM_COUNT" : 2,
	"HEX_INPUT_STRING" : '\x02\x03\x00\x00\x00\x01\x84\x39',
	"PARAMS_LIST" : ['NO','O2'],
	"OUT_TYPE" : "INTEGER"
}

#DEVICE_1 = ['MAC_ID', PROTOCOL, SLAVE_ID, PARAM_COUNT, START_REGISTER, NUM_REGISTERS_TO_READ]
#DEVICE_1 = ['MAC_ID', PROTOCOL, PARAM_COUNT, 'INPUT_STRING_IN_HEX', PARAMS_LIST]
#DEVICE_1 = ['MACABCXX0001', 'MODBUS', 1, '\x02\x03\x00\x00\x00\x01\x84\x39', ]
