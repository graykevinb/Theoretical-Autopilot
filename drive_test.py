#!/usr/bin/python3

import time
import brickpi3
from oldschool import *
BP = brickpi3.BrickPi3()

#PORT 4: Left Ultrasonic Sensor
#PORT 2: Right Ultrasonic Sensor
#PORT 1: Front Ultrasonic Sensor

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
<<<<<<< HEAD
    averaged_reading = (readings[0] + readings [1]) / 2
    return averaged_reading
=======
    average_reading = (readings[0] + readings[1]) / 2
    return average_reading
>>>>>>> efc8d746d98d01f7f8032d4455bf8244fe3a2c20

def main():
    init()
    iteration_time = 0.0001
    Kp = 3
    Ki = 0
    Kd = -2
    desired_value = 0
    target_error = 0
    error_prior = 1 
    integral = 1
    base_pwr = 200
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
        if abs(output) > base_pwr:
            output = base_pwr
        else:
            pass
        if abs(output) < 10 and scan_array[0] > scan_array[1] and error > 10:
            output = base_pwr
        elif abs(output) < 10 and scan_array[1] > scan_array[0] and error > 10:
            output = base_pwr
        else:
            pass

            
        if scan_array[0] > scan_array[1]:
            turning_direction = 'right'
            BP.set_motor_dps(BP.PORT_D, -base_pwr + abs(output))
            BP.set_motor_dps(BP.PORT_A, -base_pwr)
            #actual_value = get_ultrasonic()
        elif scan_array[0] < scan_array[1]:
            turning_direction = 'left'
            BP.set_motor_dps(BP.PORT_D, -base_pwr)
            BP.set_motor_dps(BP.PORT_A, -base_pwr + abs(output))
        else:
            turning_direction = 'forwards'
            BP.set_motor_dps(BP.PORT_D, -base_pwr)
            BP.set_motor_dps(BP.PORT_A, -base_pwr)
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
