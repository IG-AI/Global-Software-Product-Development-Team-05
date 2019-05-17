def save(map):
    fo = open("map.txt", "w+")
    fo.write(map)
    fo.close()

def load():
    fo = open("map.txt", "r+")
    map = fo.read()
    fo.close()
    return map

if __name__ == "__main__":
    map = "E E E E E\nE E E E E\nE E E E E\nE E E E E"
    save(map)
    map = load()
    print(map)
