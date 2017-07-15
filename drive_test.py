#!/usr/bin/python3
#MIT License

#Copyright (c) [2017] [Kevin Gray]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#If you want to add a lot of lines of code to your script try the GNU license ;)

import time
import brickpi3
from oldschool import *
BP = brickpi3.BrickPi3()

#PORT 4: Left Ultrasonic Sensor
#PORT 2: Right Ultrasonic Sensor
#PORT 1: Front Ultrasonic Sensor

#Initializes all of the sensors.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_ULTRASONIC)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.NXT_ULTRASONIC)
time.sleep(3)

def scanner(scan):
    """Gets data from all Sensors and returns them in an array."""
    ports = [BP.PORT_2, BP.PORT_4, BP.PORT_1]
    x = 0
    for i in range(0, 3):
        scan.append(get_ultrasonic(ports[x]))
        x += 1 
        if x > 3:
            break
        else:
            pass
    return scan

def get_ultrasonic(port):
    """Robust method for getting data from sensors"""
    readings = []
    for x in range(0, 2):
        for i in range(0, 1000):
            if i > 100:
                time.sleep(0.01)
            else:
                time.sleep(0.0001)
            try:
                readings.append(BP.get_sensor(port))
            except:
                pass

    average_reading = (readings[0] + readings[1]) / 2
    return average_reading

def main():
    init()
    #The following variables are for the PID Loop
    iteration_time = 0.0001
    Kp = 3
    Ki = 0
    Kd = -2
    desired_value = 0
    target_error = 0
    error_prior = 1 
    integral = 1
    #This defines the maxe Degrees Per Second the motor can go at. The Pid Loop will only take away from this number, not add.
    base_dps = 200
    turning_direction = None
    while True:
        scan_array = []
        scan_array = scanner(scan_array)
        actual_value = abs(scan_array[0] - scan_array[1])
        error = desired_value - actual_value
        integral = integral + (error*iteration_time)
        derivative = (error - error_prior) / iteration_time
        output = Kp*error + Ki*integral + Kd*derivative
        output = float("{0:.10f}".format(output))


        time.sleep(iteration_time)
        error_prior = error
        
        #This limits how far the PID Loop can go. Optimally I shouldn't need this, but here it is. 
        if abs(output) > base_dps:
            output = base_dps
        else:
            pass
        
        #Not sure why this here, It's on my todo list to fix.
        if abs(output) < 10 and scan_array[0] > scan_array[1] and error > 10:
            output = base_pwr
        elif abs(output) < 10 and scan_array[1] > scan_array[0] and error > 10:
            output = base_pwr
        else:
            pass

        #Compares the sensor readings and turns a left if the Left sensor reads more than the Right and vice versa. 
        #If neither are greater than each other it will drive forwards, this is there not because the PID Loop demands it,
        #but because it is logically required.   
        if scan_array[0] > scan_array[1]:
            turning_direction = 'right'
            BP.set_motor_dps(BP.PORT_D, -base_dps + abs(output))
            BP.set_motor_dps(BP.PORT_A, -base_dps)
            #actual_value = get_ultrasonic()
        elif scan_array[0] < scan_array[1]:
            turning_direction = 'left'
            BP.set_motor_dps(BP.PORT_D, -base_dps)
            BP.set_motor_dps(BP.PORT_A, -base_dps + abs(output))
        else:
            turning_direction = 'forwards'
            BP.set_motor_dps(BP.PORT_D, -base_dps)
            BP.set_motor_dps(BP.PORT_A, -base_dps)
        #Updates the output.
        update(0, 0, scan_array[1], scan_array[0], turning_direction, error, output, 0, 0)
        time.sleep(iteration_time)
        output = 0

try:
    main()
except Exception as Inst:
    reset()
    print(Inst)
except KeyboardInterrupt:
    pass
BP.reset_all()
reset()

#And the program lived happily ever after.
#THE END
#To be continued ...
