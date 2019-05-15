import json
from util.echo_client import send

#'{"map": "E E E E E\\nE E E E E\\nE E E E E\\nE E E E E"}'
map = 'E E E E E\nE E E R E\nE G E E E\nE E E E E'
HOST = '192.168.43.159'
PORT = 5000



def process(map, x, y, shell):
    #global map
    #print(map)
    #data = str(map)
    #print(data)
    #data = json.loads(data)
    #print(data)
    #data = data['map']
    print(map)
    line = map.splitlines()
    br = line[-y].split(' ')
    br[x] = shell
    line[-y-1] = ' '.join(br)
    map = '\n'.join(line)
    #print('\n')
    print(map)
    return map

def convert_map(map):
    i = 0    
    line = map.splitlines()
    #print(len(line))
    while i < len(line):
        #print(line[i])
        br = line[i].split(' ')
        j = 0
        while j < len(br):
            #print(br[j])
            if br[j] == 'R':
                br[j] = 'O'
            elif br[j] == 'G':
                br[j] = 'E'
            #elif br = 'P':
                #br = 'O'
            j += 1
            #print(br)
        line[i] = ' '.join(br)
        #print(line[i])
        i += 1        
    map = '\n'.join(line)
    #print(map)
    return map

if __name__ == "__main__":
    print(map)
    map = convert_map(map)
    print(map)
    #send(HOST, PORT, bytes('heelo', 'utf-8'))