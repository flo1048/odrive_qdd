from __future__ import print_function

import odrive
from odrive.enums import *
import time

def calibrate_motor(motor):
    ''' 
    Calibrate motor and wait for it to finish.
    Input argument looks like this: odrive.axis0 
    '''
    print("Calibrating motor...")
    motor.requested_state = AxisState.FULL_CALIBRATION_SEQUENCE
    while motor.current_state != AxisState.IDLE:
        time.sleep(0.1)
    print("Motor calibrated.")
    motor.requested_state = AxisState.CLOSED_LOOP_CONTROL

def print_GPIO_voltage(odrv):
    ''' 
    Print the voltage on GPIO pinS.
    Input arguments look like this: my_drive (odrive object)
    '''
    for i in [1,2,3,4]:
        print('voltage on GPIO{} is {} Volt'.format(i, odrv.get_adc_voltage(i)))

def find_one_odrive():
    ''' 
    Find a connected ODrive (this will block until you connect one)
    '''
    print("finding an odrive...")
    odrv = odrive.find_any()
    print("Odrive found!")
    odrv.clear_errors()
    time.sleep(0.5)
    return odrv

def find_all_odrives():
    '''
    if you want to use more than one odrive
    to use the object, you can do this:
    my_drive0 = find_all_odrives()[0]
    '''
    #print(type(odrive.find_any())) # : <class 'fibre.libfibre.anonymous_interface_2380363422560'>

    # we use find_any because it will start a background thread that handles the backend,
    # so in the end we can access odrive.connected_devices
    odrive.find_any()
    od_list = []
    for i in range(len(odrive.connected_devices)):
        odrv = odrive.connected_devices[i]
        od_list.append(odrv)

    return od_list

def check_voltage(odrv, voltage:float =20.0):
    ''' 
    Check if the voltage is high enough to run the motor.
    Input argument looks like this: my_drive (odrive object), voltage (float)
    '''
    print("Bus voltage is " + str(odrv.vbus_voltage) + " V")
    if odrv.vbus_voltage < voltage:
        print("vbus voltage is too low! Please connect a power supply to the ODrive")
        while odrv.vbus_voltage < voltage:
            time.sleep(2)
            print("...")

def check_errors(odrv, want_to_clear_errors: bool = False):
    ''' 
    Check if there are errors on the ODrive and clear them if necessary.
    Input arguments look like this: my_drive (odrive object), want_to_clear_errors (bool)
    '''
    odrv.utils.dump_errors(odrv, want_to_clear_errors)
    print(odrv.utils.dump_errors(odrv))
    