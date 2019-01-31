'''
Created on Jan 30, 2019
@author: Ajay_Rabidas
'''
from modbusInterface import configuration as CONF
import pymysql
import os
import shutil
from datetime import datetime, timedelta


def tsv_to_mysql(load_sql, host, user, password):
    try:
        con = pymysql.connect(host=host, user=user, password=password, autocommit=True, local_infile=1)
        print('Connected to DB: {}'.format(host))
        cursor = con.cursor()
        uploadedFlag = cursor.execute(load_sql)
        print('Succuessfully loaded the table from tsv.')
        con.close()
        return uploadedFlag
    
    except Exception as e:
        print('Error: {}'.format(str(e)))
        #sys.exit(1) 
        return 0


def initiateDataLoad():
    host = CONF.DB_HOST_URL
    user = CONF.DB_USER
    password = CONF.DB_PASSWORD
    readyFileList = getReadyToUploadFiles()
    print(readyFileList)
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
            print(load_sql)
            uploadedFlag = tsv_to_mysql(load_sql, host, user, password)
            if(uploadedFlag > 0):
                deleteFile(file)
            load_sql=""
    else:
        print('readyFileList is empty, retrying in 10 seconds...')
 
def getReadyToUploadFiles():
    readyFileList = []
    datetimeFormat = '%Y-%m-%d#%H-%M'
    listOfFiles = os.listdir(CONF.OUTPUT_PATH) 
    print(listOfFiles)
    
    for i in range(0, len(listOfFiles)):
        fileName = listOfFiles[i]                                               # data_2019-01-30#17-28.tsv
        seperator_position = fileName.index('_')
        file_extention_position = fileName.index('.')
        current_file_date = fileName[seperator_position+1:file_extention_position]      # 2019-01-30#17-28
        last_valid_timestamp = (datetime.now() - timedelta(minutes=30)).strftime(datetimeFormat) 
        print(current_file_date, last_valid_timestamp) 
        
        if datetime.strptime(current_file_date, datetimeFormat) <= datetime.strptime(last_valid_timestamp, datetimeFormat):
            readyFileList.append(fileName)
    print(readyFileList)
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
    
    while True:
        time.sleep(10)
        initiateDataLoad()
    #getReadyToUploadFiles()
    
    