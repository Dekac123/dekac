import serial
import time


ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600, timeout=1) 
time.sleep(60)

#waiting for robot to be ready

while(not ser.inWaiting()):
    print('Waiting for robot to be ready: \n')
ser.flushInput()
with open('Levi_portrait/gcode', 'r') as gcode_file:

    for gcode_line in gcode_file:
        print(gcode_line)
        ser.write(gcode_line.encode())
        ser.flushOutput()
        time.sleep(1)
        while(not ser.inWaiting()):
            print(ser.inWaiting())
        ser.flushInput()
        


