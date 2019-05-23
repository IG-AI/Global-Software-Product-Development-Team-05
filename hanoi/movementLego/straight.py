from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, MediumMotor
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.led import Leds
import time

lmLeft = LargeMotor('outB')
lmRight = LargeMotor('outC')
mm = MediumMotor('outA')

cs = ColorSensor()
cs.mode = "RGB-RAW"
gs = GyroSensor()

RSPEED = 100
MSPEED = 50
SSPEED = 30
LSPEED = 10

def go_straight():
    state = 0
    lmRight.on(speed = SSPEED)
    lmLeft.on(speed = SSPEED)
    while True:
        red = cs.value(0)
        green = cs.value(1)
        blue = cs.value(2)
        
        if (red in range(0,80) and blue in range(0,80) and green in range(0,80)):
            state = 1
        
        if (red > 150 and green > 150 and blue > 150):
            lmRight.off()
            lmLeft.off()
            print("white")
            break
            
        if (green > 150 and red in range(0, 150) and blue in range(0, 150) and state == 1):
            lmRight.off()
            lmLeft.off()
            print("green")
            break
            
        print(state)
            
    finish_move()
    return 0
    #while cs not COLOR_GREEN:
        #lmLeft.on(speed = RSPEED)
        #lmRight.on(speed = RSPEED)

def detect():
    red = cs.value(0)
    green = cs.value(1)
    blue = cs.value(2)
    print(red)
    print(green)
    print(blue)

def correct_left():
    while True:
        red = cs.value(0)
        green = cs.value(1)
        blue = cs.value(2)
        
        if (red > 150 and green >150 and blue > 150):
            lmLeft.on(speed = -LSPEED)
            
        if (red in range(0,80) and blue in range(0,80) and green in range(0,80)):
            lmLeft.off()
            break
    
    return 0

def correct_move():
    red = cs.value(0)
    green = cs.value(1)
    blue = cs.value(2)
    while True:
         degree = 5
         current_degree = gs.value()
         lmLeft.on(speed = -LSPEED)
         if (gs.value() - current_degree) < -degree:
             lmLeft.on(speed = LSPEED)
             degree = degree*2
             current_degree = gs.value()
             
         if (gs.value() - current_degree) > degree:
             lmLeft.on(speed = -LSPEED)
             degree = degree*2
             current_degree = gs.value()
             
         if (red in range(0,80) and blue in range(0,80) and green in range(0,80)):
            lmLeft.off()
            break
    return 0
    
def correct_right():
    while True:
        red = cs.value(0)
        green = cs.value(1)
        blue = cs.value(2)
        
        if (red > 150 and green > 150 and blue > 150):
            lmLeft.on(speed = LSPEED)
            
        if (red in range(0,80) and blue in range(0,80) and green in range(0,80)):
            lmLeft.off()
            break
    
    return 0    
    
    #check if blaack color

def turn_left():
    current_degree = gs.value()
    #lmRight.on(speed = MSPEED)
    lmLeft.on(speed = -MSPEED)
    while (gs.value() - current_degree) > -90:
        {}
    lmLeft.off()
    lmRight.off()
    #correct_move()

def turn_right():
    current_degree = gs.value()
    #lmRight.on(speed = -MSPEED)
    lmLeft.on(speed = MSPEED)
    while (gs.value() - current_degree) < 90:
        {}
    lmLeft.off()
    lmRight.off()
    #correct_move()

def turn_back():
    current_degree = gs.value()
    #lmRight.on(speed = -MSPEED)
    lmLeft.on(speed = MSPEED)
    while (gs.value() - current_degree) < 180:
        {}
    lmLeft.off()
    lmRight.off()
    #correct_move()
    
def finish_move():
    lmLeft.on(speed = LSPEED)
    lmRight.on(speed = LSPEED)
    time.sleep(1.8)
    lmLeft.off()
    lmRight.off()

def go_left():
    turn_left()
    correct_move()
    go_straight()

def go_right():
    turn_right()
    correct_move()
    go_straight()

def go_back():
    turn_back()
    correct_move()
    go_straight()    

    

if __name__ == "__main__":
    correct_move()