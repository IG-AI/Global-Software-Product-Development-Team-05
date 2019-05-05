from enum import Enum
from bitstring import BitArray

class Direction(Enum):
    NORTH = BitArray('0b00000000')
    EAST = BitArray('0b00000001')
    SOUTH = BitArray('0b00000010')
    WEST = BitArray('0b00000011')

def convert(direction): 
    switcher = { 
        "north": "0b00000000", 
        "east": "0b00000001", 
        "south": "0b00000010",
        "west": "0b00000011"
    } 

    return switcher.get(direction, None)

def int(direction):
    bitarray = BitArray(direction)
    return bitarray.int

def bit_convert(binarystring):
    switcher = { 
        "00": "north", 
        "01": "east", 
        "10": "south",
        "11": "west"
    } 

    return switcher.get(binarystring, None)

def changing_direction(direction, turning):
    direction = convert(direction)
    turning = convert(turning)
    temp = int(direction) + int(turning)
    temp = BitArray(bin(temp))
    result = str(temp[-2:])
    result = result[2:]
    if (len(result) == 1):
        result = "0" + result
    print(result)
    return bit_convert(result)

if __name__ == "__main__":
    changing_direction("north", "east")