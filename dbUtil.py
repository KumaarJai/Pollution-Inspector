'''
Created on May 10, 2019

Separate DB stuff here. 
Re-factoring to increase readability and modularity

@author: Ajay_Rabidas
'''
import requests
import sqlite3 as SQLITE
from modbusInterface import configuration as CONF

LOCAL_DB = CONF.LOCAL_SQLITE_DB_PATH + 'cpcb.db'


def createLocalSQLiteDB():
    success = False
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS CPCB(
                        industry_id text, 
                        station_id text, 
                        device_data text, 
                        uploaded INTEGER,
                        time_stamp text)
                ''')
        conn.commit()
        conn.close()
        success = True
    except Exception as e:
        return success, e
    else:
        return success, ''


def loadCPCBDataToLocalDB(industry_id, station_id, cpcbMap):
    success = False
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        query = "INSERT INTO CPCB VALUES ('{}','{}','{}',0,DATETIME('now'))".format(industry_id, station_id, cpcbMap)
        #print(query)
        c.execute(query)
        conn.commit()
        conn.close()
        success = c.rowcount>0
    except Exception as e:
        return e
    else:
        return success

    
def readDataFromLocalDB():
    success = False
    try:
        conn = SQLITE.connect(LOCAL_DB)
        c = conn.cursor()
        query = "INSERT INTO CPCB VALUES ('{}','{}','{}',0,DATETIME('now'))".format()
        #print(query)
        c.execute(query)
        conn.commit()
        conn.close()
        success = c.rowcount>0
    except Exception as e:
        return e
    else:
        return success
    
    
    

def call_CPCB_API(industry_id, station_id, cpcbMap):
    url = CONF.CPCB_API_ENDPOINT + '/industry/{}/station/{}/data'.format(industry_id, station_id)
    print(url, cpcbMap)
    response = requests.post(url, data=cpcbMap,  headers={'Content-Type': 'application/json', 'Authorization': 'Basic {}'.format(CONF.CPCB_ACCESS_TOKEN)})
    print(response.content)
    

if __name__ == '__main__':
    pass