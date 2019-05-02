'''
Created on May 2, 2019

@author: Ajay_Rabidas
'''

import multiprocessing 
import os 
import time
  
def worker1(i): 
    # printing process id
    print('worker1 starts', i)
    time.sleep(5) 
    print("ID of process running worker1: {}".format(os.getpid())) 
  
def worker2(i): 
    # printing process id 
    print('worker2 starts', i)
    time.sleep(8) 
    print("ID of process running worker2: {}".format(os.getpid())) 

async def doIt(i):
    print('\n\n Interation', i)
    print("ID of main process: {}".format(os.getpid())) 
      
    # creating processes 
    p1 = multiprocessing.Process(target=worker1(i)) 
    p2 = multiprocessing.Process(target=worker2(i)) 
    
    # starting processes 
    p1.start() 
    p2.start() 
    
    # process IDs 
    print("ID of process p1: {}".format(p1.pid)) 
    print("ID of process p2: {}".format(p2.pid)) 
    
    # wait until processes are finished 
    #         p1.run()
    #         p2.run() 
    
    # both processes finished 
    print("Both processes finished execution!") 
    
    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive()))

if __name__ == "__main__": 
    # printing main program process id 
    import asyncio
    #loop = asyncio.get_event_loop()
    #tasks = []
    
    i = 0
    while i<5:
        #tasks.append(doIt(i))
        asyncio.run(doIt(i))
        i += 1
        
    #asyncio.create_task(tasks)
    
    


