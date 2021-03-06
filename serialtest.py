import sys, serial, time
import piplates.MOTORplate as MOTOR
import threading

ser = serial.Serial("/dev/ttyS0", baudrate = 115200, timeout=1)

#globals for move
xmax = 780
ymax = 695
xcurrpos = 0
ycurrpos = 0

MOTOR_X = 'B'
MOTOR_Y = 'A'


in_message = None
out_message = None
if ser.in_waiting>0:
    ser.read(ser.in_waiting)


def drop():
    pass
    #actions for dropping leaf will go here


    

def movey(y):
    global ycurrpos
    yflag = 1
    MOTOR.stepperOFF(0, MOTOR_Y)
    newypos = int(y)

    if((newypos > ymax) or (newypos < 0)):
        print("invalid y coordinate")
        return
    else:
        print("Current y position is:", ycurrpos, " Moving to:", newypos)

    if(newypos > ycurrpos):
        MOTOR.stepperCONFIG(0, MOTOR_Y, 'CCW', 'F', 200, 0)
        # print("Turning CCW")
    elif(newypos < ycurrpos):
        MOTOR.stepperCONFIG(0, MOTOR_Y, 'CW', 'F', 200, 0)
        # print("Turning CW")
    elif(newypos == ycurrpos):
        print("same location")
        return
    else:
        print("broken")

    ysteps = abs(newypos - ycurrpos)
    MOTOR.stepperMOVE(0, MOTOR_Y, ysteps)
    while(yflag):
        time.sleep(0.1)
        stat = MOTOR.getINTflag0(0)
        if(stat & 0x10):
            yflag = 0
    MOTOR.stepperOFF(0, MOTOR_Y)
    print("Y move complete!")
    ycurrpos = newypos


def move(x,y):
    global xcurrpos
    xflag = 1
    #Reset 
    MOTOR.stepperOFF(0, MOTOR_X)
    newxpos = int(x)

    if((newxpos > xmax) or (newxpos < 0)):
        print("invalid x coordinate")
        return
    else:
        print("Current x position is:", xcurrpos, " Moving to:", newxpos)

    if(newxpos > xcurrpos):
        MOTOR.stepperCONFIG(0, MOTOR_X, 'CCW', 'F', 200, 0)
        # print("Turning CCW")
    elif(newxpos < xcurrpos):
        MOTOR.stepperCONFIG(0, MOTOR_X, 'CW', 'F', 200, 0)
        # print("Turning CW")
    elif(newxpos == xcurrpos):
        print("same location")
        return
    else:
        print("broken")

    xsteps = abs(newxpos - xcurrpos)
    MOTOR.stepperMOVE(0, MOTOR_X, xsteps)
    while(xflag):
        time.sleep(0.1)
        stat = MOTOR.getINTflag0(0)
        if(stat & 0x10):
            xflag = 0
    MOTOR.stepperOFF(0, MOTOR_X)
    xcurrpos = newxpos

    


def getCoordinates():
    ser.write(b'coords?\n')
    in_message = (ser.readline())[:-1]#.decode('utf-8')
    return eval(in_message)

#this function will return when the leaf should be dropped
#aka drop the leaf when this function returns
def blockUntilDrop():
    ser.write(b'time?\n')
    ser.timeout=10 #max time will spend waiting
    ser.readline()
    ser.timeout = 1

def actionPlaceholder(action="example_action"):
    for letter in action:
        print(letter,end='',flush=True)
        time.sleep(0.1)

def demo():    
    print("Where should I go next?")
    time.sleep(0.5)
    coordinates = getCoordinates()
    print('>',coordinates)
    time.sleep(0.5)
    move(*coordinates)
    print("\nWhen should I drop?")
    blockUntilDrop()
    print("> Now")
    actionPlaceholder("Dropping leaf\n\n")  #placeholder for where drop leaf function would go
    time.sleep(0.5)


def test():
    move(0,0)
    move(775,0)


#MAIN FUNCTION
#driver
try:
    while True:
        test()
except KeyboardInterrupt:
    print("\nKeyboard Interrupt")
    try:
        move(0,0)
    except:
        pass
    MOTOR.stepperOFF(0, MOTOR_X)
    MOTOR.stepperOFF(0, MOTOR_Y)