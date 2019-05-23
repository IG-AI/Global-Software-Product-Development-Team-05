import queue
import threading

from neuronLego import neuron

from hanoi.hostLego import hear
from hanoi.speakLego import register


def func1(num, q):
    while num < 100000000:
        num =  num**2
        q.put(num)

def func2(num, q):
    while num < 100000000:
        num = q.get()
        print(num)

flag = 0
map = ''
flag_queue = queue.Queue()
map_queue = queue.Queue()

thread_host = threading.Thread(target = hear, args = (flag, map, flag_queue, map_queue), daemon = True)
thread_neuron = threading.Thread(target = neuron, args = (flag, map, flag_queue, map_queue), daemon = True)
print ('setup')


if __name__ == "__main__":
    register()
    thread_host.start()
    thread_neuron.start()
    while True:
        {}
