import time

from pathfinder.pathfinder import find_path

from hanoi.speakLego import request


def neuron(flag, map, flag_queue, map_queue):
    #flag = flag_queue.get()
    while True:
        if not flag_queue.empty():
            flag = flag_queue.get()
        if not map_queue.empty():
            map = map_queue.get()        
        #map = map_queue.get()
        #flag = flag_queue.get()
        #print(flag) 
        print(map)
        if ((flag == 1) and map):
        #if not map:
            #break
        #if not map_queue.empty():
        #map = map_queue.get()
        #print(map) 
            steps = find_path(map)
            if steps == None:
                break
            print(steps[0])
                #if steps[0] == 'pack':
                    #raise Exception
            request(steps[0])
            time.sleep(3)
                #if not flag_queue.empty():
                    #flag = flag_queue.get()
                #if not map_queue.empty():
                    #map = map_queue.get()
            map = 0 
        #Auto mode
        #Auto mode off
        #map = map_queue.get()
        #print('out')

