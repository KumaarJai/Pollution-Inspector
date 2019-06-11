'''
Created on May 15, 2019
Refactoring code to seperate logger
@author: Ajay_Rabidas
'''

import logging as LOGGER

class AppLogger:
    def __init__(self, fileName):
        self.fileName = fileName

    def getLogger(self):
        LOGGER.basicConfig(
        level=LOGGER.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            LOGGER.FileHandler("{0}.log".format(self.fileName)),
            LOGGER.StreamHandler()
        ])
        return LOGGER



if __name__ == '__main__':
    LOGGER = AppLogger('test').getLogger()
    LOGGER.info('This is testing log file generation')