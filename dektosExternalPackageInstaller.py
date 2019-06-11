'''
Created on Jan 23, 2019

@author: Ajay Rabidas
Description: This script installs the external python packages required to run this application
'''

import subprocess
import sys

def installPackage(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def installMandatoryPackages():
    installPackage('pyserial')
    installPackage('pymysql')
    #installPackage('sqlite3')

if __name__ == '__main__':
    print("Dektos Msg : Installing mandatory python packages manually")
    installMandatoryPackages()