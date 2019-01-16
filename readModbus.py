



import serial
from . import configuration as CONF


def connectToDevice():
	ser = serial.Serial(CONF.PORT, CONF.BAUD_RATE,timeout=CONF.TIMEOUT)
	if(ser.isOpen()):
	    print(ser.name + ' is open--------------------------------------------')

	while True:
		for i in range(0, CONF.DEVICES_COUNT):
		device = CONF.DEVICE_LIST[i]
		readModbusData(ser, device)




def readModbusData(ser, device):
	print('Connecting to device : '+device["MAC_ID"])
	outData = []
	ser.write(b''+device["HEX_INPUT_STRING"])
	out = ser.readline()
	print(out)
	for byte in out:
		outData.append(byte)

	 
	if isOutputAligned(device, outData):
		extractData(device, outData)
	

def extractData(device, outData):
	print('Extracting data...')
	outDataBytesCount = outData[3]
	bytesPerParam = outDataBytesCount/device["PARAM_COUNT"]

	for i in range(3,len(outData)-2):
		#continue code here


def isOutputAligned(device, outData):
	if outData[0] == device["SLAVE_ID"] 
	&& outData[1] == device["FUNCTION_ID"] 
	&& generateCRC(outData) == generateCRC(device["HEX_INPUT_STRING"]) #incomplete logic
	return True


def generateCRC(data):
	#incomplete logic
	return data


def readSerialData():
	print(device["MAC_ID"]+' : Initiating serial data read...')



if __name__ == '__main__':
	readModbusData(ser)

	# if device["PROTOCOL"] == "MODBUS":
	# 		readModbusData(device)
	# 	elif device["PROTOCOL"] == "SERIAL":
	# 		readSerialData(device)