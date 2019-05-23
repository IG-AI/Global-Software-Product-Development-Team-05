import socket

from movement.straight import go_straight, go_left, go_right, go_back

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def hear(flag, map, flag_queue, map_queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        try:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
            #print('Received', repr(data))
                    if not data:
                        break
                    data = bytes.decode(data)
                    print(data)
                    if "map" in data:
                        #print(data)
                        map = data[4:]
                        #print(map)
                        map_queue.put(map)
                    elif data == "auto":
                        flag = 1
                        flag_queue.put(flag)
                    elif data == "button":
                        flag = 0
                        flag_queue.put(flag)
                    elif data == "north":
                        go_straight()
                    elif data == "east":
                        go_right()
                    elif data == "west":
                        go_left()
                    elif data == "south":
                        go_back()
                    elif data == "pack":
                        {}
                    elif data == "exit":
                        s.close()
                    else: {}
                    #If-else call movement function


        except:
            print("Closing socket")
            #conn.sendall(data)
        #print('Received', repr(data))
    #print('Received', repr(data))

#print('Received', repr(data))

#if __name__ == "__main__":
    #hear()