'''
Created on May 11, 2019

@author: Ajay_Rabidas
'''
import requests
import sqlite3 as SQLITE
from modbusInterface import configuration as CONF
from modbusInterface import dektosLogger
import json


LOG_FILENAME = CONF.LOG_CPCB_UPLOADER
LOGGER = dektosLogger.AppLogger(LOG_FILENAME).getLogger()
LOGGER.info('Log file initiated, System starting up...') 


LOCAL_DB = CONF.LOCAL_SQLITE_DB_PATH + 'cpcb.db'
ROWS_LIMIT = CONF.CPCB_DATA_UPLOAD_ROW_LIMIT


def getFormattedRowIds(rowIds):
    return ','.join(str(x) for x in rowIds)

    
def readDataFromLocalDB(industry_id, station_id):
    stationData = []
    rowIds = []
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        query = "SELECT rowid, device_data FROM CPCB WHERE industry_id = '{}' AND station_id = '{}' AND uploaded = 0 LIMIT {}".format(industry_id, station_id, ROWS_LIMIT)
        #LOGGER.info(query)
        c.execute(query)
        rows = c.fetchall()
        if len(rows)>0:
            for row in rows:
                stationData.append(json.loads(row[1]))
                rowIds.append(row[0])
        #LOGGER.info(json.dumps(f))  
        else:
            LOGGER.info("Empty result set for STATION_ID : {}, retrying in next cycle (30 seconds) ...".format(station_id))
        conn.close()
    except Exception as e:
        return e
    else:
        return rowIds, stationData
    

    
def updateFlagsInLocalDB(industry_id, station_id, rowIds):  #updates successfully uploaded rows in local db (sqlite) 
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        rowsToUpdate = getFormattedRowIds(rowIds)
        query = "UPDATE CPCB SET uploaded = 1 WHERE industry_id = '{}' AND station_id = '{}' AND rowid IN ({})".format(industry_id, station_id, rowsToUpdate)
        LOGGER.info(query)
        c.execute(query)
        conn.commit()
        LOGGER.info("{} rows updated".format(c.rowcount))
        conn.close()
    except Exception as e:
        LOGGER.info('Error updating flags in local db after successful CPCB API response, '+e)




def deleteUploadedRowsFromLocalDB(industry_id, station_id, rowIds):  #Deletes successfully uploaded rows in local db (sqlite) 
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        rowsToUpdate = getFormattedRowIds(rowIds)
        query = "DELETE FROM CPCB WHERE industry_id = '{}' AND station_id = '{}' AND rowid IN ({})".format(industry_id, station_id, rowsToUpdate)
        LOGGER.info(query)
        c.execute(query)
        conn.commit()
        LOGGER.info("{} rows deleted".format(c.rowcount))
        conn.close()
    except Exception as e:
        LOGGER.info('Error deleting flags in local db after successful CPCB API response, trying to update flags [uploaded = 1] to avoid duplicate CPCB API Call, '+e)




def call_CPCB_API(industry_id, station_id):
    try:
        cpcbMap = {}
        url = CONF.CPCB_API_ENDPOINT + '/industry/{}/station/{}/data'.format(industry_id, station_id)
        rowIds, stationData = readDataFromLocalDB(industry_id, station_id)
        
        if stationData == [] or rowIds == []:
            return
        
        cpcbMap["stationId"] = station_id
        cpcbMap["data"] = stationData
        
        LOGGER.info('URL : '+url)
        LOGGER.info('Data : '+json.dumps([cpcbMap]))
        
        response = requests.post(url, data=json.dumps([cpcbMap]),  headers={'Content-Type': 'application/json', 'Authorization': 'Basic {}'.format(CONF.CPCB_ACCESS_TOKEN)})
        LOGGER.info('Response : '+str(response.content))
        
        if isResponseSuccess(response):
            if CONF.LOCAL_SQLITE_DB_SUCCESSUPLOADS_ACTION == "UPDATE":
                updateFlagsInLocalDB(industry_id, station_id, rowIds)
                
            elif CONF.LOCAL_SQLITE_DB_SUCCESSUPLOADS_ACTION == "DELETE":
                deleteUploadedRowsFromLocalDB(industry_id, station_id, rowIds)
        
    except Exception as e:
        LOGGER.info(e)
        pass


def isResponseSuccess(response):
    success = False
    jsonResponse = json.loads(response.text)
    print(response.status_code, jsonResponse["msg"], jsonResponse["status"])
    if response.status_code == 200 and jsonResponse["msg"] == "success" and jsonResponse["status"] == 1:
        success = True
    return success



def sendEachDeviceDataToCPCB():
    try: 
        if CONF.PROTOCOL == 'MODBUS':
            for modbusDevice in CONF.DEVICE_LIST:
                call_CPCB_API(CONF.INDUSTRY_ID, modbusDevice["STATION_ID"])
                
        elif CONF.PROTOCOL == "SERIAL":
            call_CPCB_API(CONF.INDUSTRY_ID, CONF.SERIAL_DEVICE["STATION_ID"])
            
    except Exception as e:
        LOGGER.info(e)
        time.sleep(5)
        sendEachDeviceDataToCPCB()
 


if __name__ == '__main__':
    import time
    LOGGER.info('Started CPCB upload process...')
    while True:
        time.sleep(5)
        sendEachDeviceDataToCPCB()
    
    