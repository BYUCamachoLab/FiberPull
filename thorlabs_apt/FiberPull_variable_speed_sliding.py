# equipment: 3 KDC101 DC Servo Motor Controllers
#            connected to PT1-Z8 25mm motorized translation stages

# Full fiber pulling err_code
# Simply light the torch and then execute this file in the Anaconda Prompt

# January 4, 2019
# Matthew Simmons
# P: (949)910-2223

''' 
From Kinesis: Settings > Device startup Settings > Actuator settings
These parameters are from Kinesis, under (stock) settings.
I just copied and pasted to be sure the device parameters are not exceeded; very important.

Z825

General

Name =
Stage ID = 99
Axis ID = Single axis

Home Settings

Home Direction = Reverse
Home Limit Switch Mode = Reverse (Hard)
Home Velocity = 1
Home Zero Offset = 0.3

Jog Settings

Jog Mode = Single step
Jog Step = 0.1
Jog Minimum Velocity = 0
Jog Maximum Velocity = 2
Jog Acceleration = 2
Jog Stop Mode = Profiled stop

Control Settings

Default Minimum Velocity = 0 mm/s
Default Maximum Velocity = 2.2 mm/s
Default Acceleration = 1.5 mm/s/s

Limit Settings

Clockwise Hard Limit mode = Switch Makes
Counter Clockwise Hard Limit mode = Switch Makes
Clockwise Soft Limit = 3
Counter Clockwise Soft Limit = 1
Soft Limit Mode = Ignore
Software Limits Approach PolicyMode = Complete moves only

Physical Settings

Use Device Units = False
Travel Mode = Linear
Direction Sense = Reverse
Minimum Achievable Incremental Movement = .05 um
Minimum Repeatable Incremental Movement = .2 um
Minimum Position = 0 mm
Maximum Position = 25 mm
Maximum Velocity = 2.6 mm/s
Maximum Acceleration = 4 mm/s/s
MM to Unit factor = 1
Units = mm

Misc. Settings

Backlash Distance = 0.025
Move Factor = 100
Rest Factor = 20

MMI Settings

Wheel Mode = Jog
Wheel Max Velocity = 1
Wheel Acceleration = 2
Wheel Direction Sense = Forward
Prest Position 1 = 0
Preset Position 2 = 0
Display Intensity = 60
Display Timeout = 10
Display Dim Intensity = 2

Trigger Config Settings

Trigger 1 Mode = Disabled
Trigger 1 Polarity = Trigger High
Trigger 2 Mode = Disabled
Trigger 2 Polarity = Trigger High

Trigger Params Settings

Trigger Start Position Fwd = 0
Trigger Interval Fwd = 0
Trigger Pulse Count Fwd = 1
Trigger Start Position Rev = 0
Trigger Interval Rev = 0
Trigger Pulse Count Rev = 1
Trigger Pulse Width = 50
Cycle Count = 1

DC Motor Settings

Use Device Units = False
Travel Mode = Linear
Direction Sense = Reverse
Minimum Position = 0
Maximum Position = 25
Maximum Velocity = 2.6
Maximum Acceleration = 4
MM to Unit factor = 1
Units = mm
Pitch Size = 1
Steps per revolution = 512
Gearbox Ratio = 67

DC Servo Settings

DC Servo Enabled = 1
DC Proportional Constant = 435
DC Integral Constant = 195
DC Differential Constant = 993
DC Integral Limit = 195
'''

import thorlabs_apt as apt
import time
import numpy as np

motorTorch = apt.Motor(27003356) #serial number of the stage with the torch on it
motorLeft = apt.Motor(27003323) #serial number of the left stage
motorRight = apt.Motor(27003363) #serial number of the right stage

# Maximum Velocity = 2.6
# Maximum Acceleration = 4
motorTorch.set_hardware_limit_switches(2,2)
motorTorch.set_motor_parameters(512,67)
motorTorch.set_stage_axis_info(0.0,25.0,1,1.0)
motorTorch.set_move_home_parameters(2,1,2.3,0.3)
motorTorch.set_velocity_parameters(1.0,4.0,2.6) # min, acceleration, max ---mm/s/s

motorLeft.set_hardware_limit_switches(2,2)
motorLeft.set_motor_parameters(512,67)
motorLeft.set_stage_axis_info(0.0,25.0,1,1.0)
motorLeft.set_move_home_parameters(2,1,2.3,0.3)
motorLeft.set_velocity_parameters(1.0,1.0,1.0)

motorRight.set_hardware_limit_switches(2,2)
motorRight.set_motor_parameters(512,67)
motorRight.set_stage_axis_info(0.0,25.0,1,1.0)
motorRight.set_move_home_parameters(2,1,2.3,0.3)
motorRight.set_velocity_parameters(1.0,1.0,1.0)


# Home the stages:
print("homing the stages")
motorTorch.move_home()
motorLeft.move_home()
motorRight.move_home()
time.sleep(1)

#wait while they move
while motorTorch.is_in_motion: 
    pass
while motorLeft.is_in_motion: 
    pass
while motorRight.is_in_motion: 
    pass

print('Stage homing complete')

'''
When ready and the torch is lit, press "enter" on the keyboard
This will begin the rest of the fiber pulling sequence
'''
input("Place fiber and light torch, then press enter to continue")
PullSpeed = float(input("Enter the desired pull speed: ")) #easily changeable pull speed
pullLength = float(input("Enter the desired pull length: ")) #distance each stage should move when pulling the fiber
sliding = int(input("Sliding hot spot desired? (0 or 1): ")) #use a sliding or stationary hot spot
#move the torch into position:
torch_on_fiber = 10.0 #distance stage holding the torch needs to move so that the torch is heating the fiber

if sliding is 1:
     motorTorch.move_to(torch_on_fiber) #move the stage holding the torch 20 mm to be on the fiber
    time.sleep(1)



else:
    motorTorch.move_to(torch_on_fiber) #move the stage holding the torch 20 mm to be on the fiber
    time.sleep(1)
    while motorTorch.is_in_motion: #wait till it's done moving
        pass

    print('Torch moved to fiber')

    wait_pullFiber=15 #the amount of time (seconds) to wait before the stages start to pull the fiber
    time.sleep(wait_pullFiber)

    #pull the fiber:


    motorLeft.set_velocity_parameters(0.001,4.0,PullSpeed)
    motorRight.set_velocity_parameters(0.001,4.0,PullSpeed)
    motorLeft.move_to(pullLength/2)
    motorRight.move_to(pullLength/2)
    while motorLeft.is_in_motion: 
        pass
    while motorRight.is_in_motion: 
        pass
print('Fiber stretched')


print("Fiber pulling complete, home torch stage")
torch_off_fiber = 1
motorTorch.move_to(torch_off_fiber) #move the stage holding the torch off of the fiber
time.sleep(1)
while motorTorch.is_in_motion:
    pass 
print("moved off fiber")


tensionLength = .025
moveLength = 2


while True:
    command = input('t (u) to (un)tension, r to move right, l to move left, q to quit: ')
    if command is 't':
        motorLeft.move_by(tensionLength)
        motorRight.move_by(tensionLength)
        while motorLeft.is_in_motion: 
            pass
        while motorRight.is_in_motion: 
            pass
    elif command is 'u':
        motorLeft.move_by(-tensionLength)
        motorRight.move_by(-tensionLength)
        while motorLeft.is_in_motion: 
            pass
        while motorRight.is_in_motion: 
            pass
    elif command is 'r':
        motorLeft.move_by(moveLength)
        motorRight.move_by(-moveLength)
        while motorLeft.is_in_motion: 
            pass
        while motorRight.is_in_motion: 
            pass
    elif command is 'l':
        motorLeft.move_by(-moveLength)
        motorRight.move_by(moveLength)
        while motorLeft.is_in_motion: 
            pass
        while motorRight.is_in_motion: 
            pass
        while motorTorch.is_in_motion:
            pass
    elif command is 'q':
        break

motorTorch.move_home()
time.sleep(1)

print('Torch stage homing complete')
