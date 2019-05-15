from enum import Enum
from bitstring import BitArray

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

def changing_direction(facing, turning):
    facing = convert(facing)
    turning = convert(turning)
    temp = int(facing) + int(turning)
    temp = BitArray(bin(temp))
    result = str(temp[-2:])
    result = result[2:]
    if (len(result) == 1):
        result = "0" + result
    print(result)
    return bit_convert(result)

def get_turning(facing, direction):
    facing = convert(facing)
    print(facing)
    direction = convert(direction)
    print(direction)
    print("start")
    temp = int(direction) - int(facing)
    if (temp < 0):
        temp += 4
    print(temp)
    print(bin(temp))
    temp = BitArray(bin(temp))
    print(temp)
    result = str(temp[-2:])
    result = result[2:]
    if (len(result) == 1):
        result = "0" + result
    print(result)
    return bit_convert(result)

def changing_position(x, y, direction):
    if (direction == "north"):
        y += 1
    elif (direction == "east"):
        x += 1
    elif (direction == "south"):
        y -= 1
    elif (direction == "west"):
        x -= 1
    else:
        return 1

    print(x)
    print(y)
    return 0

if __name__ == "__main__":
    x = 0
    y = 1 
    changing_position(x, y, "east")
    print(x)
    print(y)