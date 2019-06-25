'''
Created on Jan 25, 2019

@author: Ajay_Rabidas
'''

import os
import sys
sys.path.append("/".join(os.getcwd().split('\\')[0:-1]))

from modbusInterface import dbUtil as DBUTIL
from modbusInterface import configuration as CONF
def generateDirectorySturcture():
    try:
        print("Creating Archive path : "+ CONF.ARCHIVE_PATH)
        os.makedirs(CONF.ARCHIVE_PATH, exist_ok=True)
        
        print("Creating Output path : "+ CONF.ARCHIVE_PATH)
        os.makedirs(CONF.OUTPUT_PATH, exist_ok=True)
        
        print("Creating Log path : "+ CONF.ARCHIVE_PATH)
        os.makedirs(CONF.LOG_PATH, exist_ok=True)
        
        print("Creating Local DB path : "+ CONF.LOCAL_SQLITE_DB_PATH)
        os.makedirs(CONF.LOCAL_SQLITE_DB_PATH, exist_ok=True)
        
        print('Creating CPCB Table in Local DB')
        flag, error = DBUTIL.createLocalSQLiteDB()
        
        if flag == True:
            print('table created successfully...')
        else:
            print(error)
            raise Exception('failed to create Local DB, check logs for details')
        
    except Exception as e:
        print('Error generating directory structure, Please retry...')
        print(e)
        exit()
    else:
        print("All Set...! Directory structure successfully generated...")



if __name__ == '__main__':
    generateDirectorySturcture()