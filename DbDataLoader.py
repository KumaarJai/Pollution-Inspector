'''
Created on Jan 30, 2019
@author: Ajay_Rabidas
'''
import logging as LOGGER
import os
import sys
#sys.path.append('C:/Users/psingh06/Desktop/AKR/')
sys.path.append("/".join(os.getcwd().split('\\')[0:-1]))

from modbusInterface import configuration as CONF
import pymysql
import os
import shutil
from datetime import datetime, timedelta


LOG_FILENAME = CONF.BASE_PATH+'log/dbUpload.log'
#LOGGER.basicConfig(filename=LOG_FILENAME,level=LOGGER.DEBUG)

LOGGER.basicConfig(
    level=LOGGER.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        LOGGER.FileHandler("{0}.log".format(LOG_FILENAME)),
        LOGGER.StreamHandler()
    ])

LOGGER.debug('Log file initiated, System starting up...') 


def tsv_to_mysql(load_sql, host, user, password):
    try:
        con = pymysql.connect(host=host, user=user, password=password, autocommit=True, local_infile=1)
        LOGGER.info('Connected to DB: {}'.format(host))
        cursor = con.cursor()
        uploadedFlag = cursor.execute(load_sql)
        LOGGER.info('Succuessfully loaded the table from tsv.')
        con.close()
        return uploadedFlag
    
    except Exception as e:
        LOGGER.info('Error: {}'.format(str(e)))
        #sys.exit(1) 
        return 0


def initiateDataLoad():
    try:
        host = CONF.DB_HOST_URL
        user = CONF.DB_USER
        password = CONF.DB_PASSWORD
        readyFileList = getReadyToUploadFiles()
        uploadedFilesList = []
        LOGGER.info(readyFileList)
        load_sql=""
        if len(readyFileList) > 0:
            for i in range(0, len(readyFileList)):
                file = ""+CONF.OUTPUT_PATH + readyFileList[i]
                #print(file)
                load_sql = "LOAD DATA LOCAL INFILE '{}' \
                            INTO TABLE cdotsdb.demo_data FIELDS \
                            TERMINATED BY '\t' \
                            LINES TERMINATED BY '\n' \
                            (@col1,@col2) set mac_id=@col1,dev_data=@col2;".format(file)
                #print(load_sql)
                uploadedFlag = tsv_to_mysql(load_sql, host, user, password)
                if(uploadedFlag > 0):
                    uploadedFilesList.append(file)
                load_sql=""
            for i in range(0,len(uploadedFilesList)):
                LOGGER.info('Archiving file : ' + file)
                archiveFile(uploadedFilesList[i])
        else:
            LOGGER.info('readyFileList is empty, retrying in 120 seconds...')
    except Exception as e:
        LOGGER.info('Error in Data Upload')
        LOGGER.info(e)
        time.sleep(20)
        initiateDataLoad()

 
def getReadyToUploadFiles():
    readyFileList = []
    datetimeFormat = '%Y-%m-%d#%H-%M'
    listOfFiles = os.listdir(CONF.OUTPUT_PATH) 
    #LOGGER.info(listOfFiles)
    
    for i in range(0, len(listOfFiles)):
        fileName = listOfFiles[i]                                               # data_2019-01-30#17-28.tsv
        seperator_position = fileName.index('_')
        file_extention_position = fileName.index('.')
        current_file_date = fileName[seperator_position+1:file_extention_position]      # 2019-01-30#17-28
        last_valid_timestamp = (datetime.now() - timedelta(minutes=2)).strftime(datetimeFormat) 
        print(current_file_date, last_valid_timestamp) 
        
        if datetime.strptime(current_file_date, datetimeFormat) <= datetime.strptime(last_valid_timestamp, datetimeFormat):
            readyFileList.append(fileName)
    LOGGER.info(readyFileList)
    return readyFileList



def deleteFile(file):
    os.remove(file)

def archiveFile(file):
    shutil.move(file, CONF.ARCHIVE_PATH)
 
 
def chkdatetime():
    datetimeFormat = '%Y-%m-%d#%H-%M'
    date1 = datetime.now().strftime(datetimeFormat)
    date2 = (datetime.now() - timedelta(minutes=30)).strftime(datetimeFormat)
    date3 = '2020-01-30#17-29'
    diff = datetime.strptime(date3, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
    print(diff)
    print(date1, date2, date3) 
    print(datetime.strptime(date3, datetimeFormat) > datetime.strptime(date1, datetimeFormat))
    
    
    
if __name__ == '__main__':
    import time
    print('Started db load process...')
    while True:
        time.sleep(20)
        initiateDataLoad()
    #getReadyToUploadFiles()
    
    