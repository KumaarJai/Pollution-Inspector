'''
Created on Jan 30, 2019
@author: Ajay_Rabidas
'''
from modbus_python import configuration as CONF
import pymysql
import sys
import os

def tsv_to_mysql(load_sql, host, user, password):
    try:
        con = pymysql.connect(host=host, user=user, password=password, autocommit=True, local_infile=1)
        print('Connected to DB: {}'.format(host))
        # Create cursor and execute Load SQL
        cursor = con.cursor()
        uploadedFlag = cursor.execute(load_sql)
        print('Succuessfully loaded the table from tsv.')
        print('uploadedFlag', uploadedFlag)
        con.close()
        
    except Exception as e:
        print('Error: {}'.format(str(e)))
        #sys.exit(1) 

def getListOfFilesToUpload(): 
    return os.listdir(CONF.OUTPUT_PATH) 

def initiateDataLoad():
    #file = "D:/AJAY_545732/PROJECTS/Dektos/output/data.tsv"
    host = 'cdotsdb.cc0wiogqy5qv.ap-northeast-2.rds.amazonaws.com'
    user = 'cdotsmasterdba'
    password = 'master.cdots'
    
    listOfFiles = getListOfFilesToUpload()
    print(listOfFiles)
    
    load_sql=""
    for i in range(0, len(listOfFiles)):
        file = ""+CONF.OUTPUT_PATH + listOfFiles[i]
        #print(file)
        load_sql = "LOAD DATA LOCAL INFILE '{}' \
                    INTO TABLE cdotsdb.demo_data FIELDS \
                    TERMINATED BY '\t' \
                    LINES TERMINATED BY '\n' \
                    (@col1,@col2) set mac_id=@col1,dev_data=@col2;".format(file)
        print(load_sql)
        tsv_to_mysql(load_sql, host, user, password)
        load_sql=""
   

def chkdatetime():
    import datetime
    datetimeFormat = '%Y-%m-%d#%H-%M'
    date1 = '2016-04-16#10-01'
    date2 = '2016-04-16#10-01'
    date3 = '2016-04-16#10-30'
    diff = datetime.datetime.strptime(date3, datetimeFormat) - datetime.datetime.strptime(date1, datetimeFormat)
    print(diff) 
    print(date3 > date1)
    
if __name__ == '__main__':
    initiateDataLoad()
    #chkdatetime()
    #print(getListOfFilesToUpload()) 
    
    