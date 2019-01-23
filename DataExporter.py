'''
Created on Jan 23, 2019

@author: Kumaar Jai
'''
import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='mydb')
cursor = mydb.cursor()

csv_data = csv.reader(file('students.csv'))
for row in csv_data:

    cursor.execute('INSERT INTO testcsv(names, \
          classes, mark )' \
          'VALUES("%s", "%s", "%s")', 
          row)
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"



def csv_to_mysql(load_sql, host, user, password):
    '''
    This function load a csv file to MySQL table according to
    the load_sql statement.
    '''
    try:
        con = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                autocommit=True,
                                local_infile=1)
        print('Connected to DB: {}'.format(host))
        # Create cursor and execute Load SQL
        cursor = con.cursor()
        cursor.execute(load_sql)
        print('Succuessfully loaded the table from csv.')
        con.close()
        
    except Exception as e:
        print('Error: {}'.format(str(e)))
        sys.exit(1)

# Execution Example
load_sql = "LOAD DATA LOCAL INFILE '/tmp/city.csv' INTO TABLE usermanaged.city\
 FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;"
host = 'host url'
user = 'username'
password = 'password'
csv_to_mysql(load_sql, host, user, password)



if __name__ == '__main__':
    pass