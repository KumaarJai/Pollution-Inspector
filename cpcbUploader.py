'''
Created on May 11, 2019

@author: Ajay_Rabidas
'''
import requests
import sqlite3 as SQLITE
from modbusInterface import configuration as CONF
import json

LOCAL_DB = CONF.LOCAL_SQLITE_DB_PATH + 'cpcb.db'
ROWS_LIMIT = CONF.CPCB_DATA_UPLOAD_ROW_LIMIT

    
def readDataFromLocalDB(industry_id, station_id):
    stationData = []
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        query = "SELECT rowid, device_data FROM CPCB WHERE industry_id = '{}' AND station_id = '{}' LIMIT {}".format(industry_id, station_id, ROWS_LIMIT)
        print(query)
        c.execute(query)
        rows = c.fetchall()
        if len(rows)>0:
            for row in rows:
                stationData.append(json.loads(row[1]))
        #print(json.dumps(f))  
        else:
            raise Exception("Empty result set, retrying in 30 seconds...") 
        conn.close()
    except Exception as e:
        return e
    else:
        return stationData
    


def call_CPCB_API(industry_id, station_id):
    try:
        cpcbMap = {}
        url = CONF.CPCB_API_ENDPOINT + '/industry/{}/station/{}/data'.format(industry_id, station_id)
        print(url)
        
        cpcbMap["stationId"] = station_id
        cpcbMap["data"] = readDataFromLocalDB(industry_id, station_id)

        
        response = requests.post(url, data=json.dumps([cpcbMap]),  headers={'Content-Type': 'application/json', 'Authorization': 'Basic {}'.format(CONF.CPCB_ACCESS_TOKEN)})
        print(response.content)
    except Exception as e:
        print(e)
        pass
    

if __name__ == '__main__':
    import time
    print('Started CPCB upload process...')
    while True:
        time.sleep(30)
        #call_CPCB_API('CL_001', 'PODR_2')
        call_CPCB_API(CONF.INDUSTRY_ID, 'PODR_2')
    
    