#!/usr/bin/env python3
# coding=utf-8
# File name   : move.py
# Description : Motor Control System for RaspTank Robot
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/03/10
#
# ============================================================================
# MOTOR CONTROL SYSTEM DOCUMENTATION
# ============================================================================
#
# This module provides comprehensive motor control for the RaspTank robot using
# the Adafruit PCA9685 PWM driver. It supports multiple movement modes including:
# - Basic directional movement (forward, backward, left, right)
# - Line tracking with offset compensation
# - Computer vision tracking with differential steering
#
# Hardware Configuration:
# - Uses PCA9685 16-channel PWM driver at I2C address 0x5f
# - Controls up to 4 DC motors (M1-M4) via H-bridge connections
# - Motor layout: M1=right motor, M2=left motor (tank-style steering)
# - PWM frequency set to 50Hz for optimal motor performance
#
# Movement Logic:
# - Tank steering: differential motor speeds for turning
# - Direction values: 1=forward, -1=backward
# - Speed range: 0-100 (mapped to 0-1.0 throttle internally)
# - Turn options: "left", "right", "mid" (straight)
#
# ============================================================================

import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

# ============================================================================
# MOTOR PIN DEFINITIONS
# ============================================================================
# PCA9685 channel assignments for H-bridge motor control
# Each motor uses 2 channels (IN1/IN2) for direction control

MOTOR_M1_IN1 =  15      # Motor 1 positive pole (right motor forward)
MOTOR_M1_IN2 =  14      # Motor 1 negative pole (right motor reverse)
MOTOR_M2_IN1 =  12      # Motor 2 positive pole (left motor forward)
MOTOR_M2_IN2 =  13      # Motor 2 negative pole (left motor reverse)
MOTOR_M3_IN1 =  11      # Motor 3 positive pole (optional expansion)
MOTOR_M3_IN2 =  10      # Motor 3 negative pole (optional expansion)
MOTOR_M4_IN1 =  8       # Motor 4 positive pole (optional expansion)
MOTOR_M4_IN2 =  9       # Motor 4 negative pole (optional expansion)

# ============================================================================
# MOTOR DIRECTION CONFIGURATION
# ============================================================================
# These values control motor rotation direction
# Change these values if motors are wired in reverse
# Values: 1=normal direction, -1=reversed direction

M1_Direction   = 1      # Right motor direction multiplier
M2_Direction   = 1      # Left motor direction multiplier

# Legacy direction variables (maintained for compatibility)
left_forward   = 1      # Left motor forward state
left_backward  = 0      # Left motor backward state
right_forward  = 0      # Right motor forward state  
right_backward = 1      # Right motor backward state

# ============================================================================
# TRACKING LINE COMPENSATION
# ============================================================================
# Speed offsets for line tracking to compensate for motor differences
# These values help maintain straight line movement during line following

TL_LEFT_Offset  = 10    # Left motor speed compensation (+/- adjustment)
TL_RIGHT_Offset = 0     # Right motor speed compensation (+/- adjustment)

# ============================================================================
# PWM CONFIGURATION
# ============================================================================
# PWM control variables for motor speed regulation

pwn_A = 0               # PWM channel A value (legacy)
pwm_B = 0               # PWM channel B value (legacy)
FREQ = 50               # PWM frequency in Hz (50Hz optimal for DC motors)

# Global motor control objects (initialized in setup())
motor1, motor2, motor3, motor4, pwm_motor = None, None, None, None, None


# ============================================================================
# ROBOT PHYSICAL LAYOUT
# ============================================================================
'''
Tank-style motor configuration (viewed from above):

    FRONT
    xx  _____  xx
       |     |
       | CAM |  <- Camera/sensors
       |     |
    M2 |_____| M1    M1 = Right motor (channels 14,15)
    LEFT     RIGHT   M2 = Left motor  (channels 12,13)
    
Movement Logic:
- Forward:  M1=forward, M2=forward
- Backward: M1=reverse, M2=reverse  
- Left:     M1=forward, M2=reverse (tank turn)
- Right:    M1=reverse, M2=forward (tank turn)
'''

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def map(x, in_min, in_max, out_min, out_max):
    """
    Linear mapping function to convert values between ranges
    
    Args:
        x: Input value to be mapped
        in_min: Minimum value of input range
        in_max: Maximum value of input range  
        out_min: Minimum value of output range
        out_max: Maximum value of output range
        
    Returns:
        float: Mapped value in the output range
        
    Example:
        map(50, 0, 100, 0, 1.0) -> 0.5 (maps 50% to 0.5 throttle)
    """
    return (x - in_min)/(in_max - in_min) *(out_max - out_min) + out_min


# ============================================================================
# MOTOR INITIALIZATION
# ============================================================================

def setup():
    """
    Initialize the motor control system
    
    This function must be called before any motor operations.
    It sets up:
    - I2C communication with PCA9685 PWM driver
    - Motor control objects for each DC motor
    - PWM frequency configuration
    - Motor decay mode for smooth operation
    
    Hardware Setup:
    - PCA9685 PWM driver at I2C address 0x5f
    - 4 DC motors connected via H-bridge circuits
    - Each motor uses 2 PWM channels for directional control
    
    Raises:
        I2C communication errors if hardware not connected
    """
    global motor1, motor2, motor3, motor4, pwm_motor
    
    # Initialize I2C communication bus
    i2c = busio.I2C(SCL, SDA)
    
    # Create PCA9685 PWM controller instance at address 0x5f
    # Note: Default PCA9685 address is 0x40, but this board uses 0x5f
    pwm_motor = PCA9685(i2c, address=0x5f)

    # Set PWM frequency for optimal motor control
    pwm_motor.frequency = FREQ

    # Initialize DC motor objects using PCA9685 channels
    # Each motor uses 2 channels for H-bridge directional control
    motor1 = motor.DCMotor(pwm_motor.channels[MOTOR_M1_IN1], pwm_motor.channels[MOTOR_M1_IN2])
    motor1.decay_mode = (motor.SLOW_DECAY)  # Smooth motor operation
    
    motor2 = motor.DCMotor(pwm_motor.channels[MOTOR_M2_IN1], pwm_motor.channels[MOTOR_M2_IN2])
    motor2.decay_mode = (motor.SLOW_DECAY)  # Reduces motor noise and heat
    
    motor3 = motor.DCMotor(pwm_motor.channels[MOTOR_M3_IN1], pwm_motor.channels[MOTOR_M3_IN2])
    motor3.decay_mode = (motor.SLOW_DECAY)  # Optional expansion motor
    
    motor4 = motor.DCMotor(pwm_motor.channels[MOTOR_M4_IN1], pwm_motor.channels[MOTOR_M4_IN2])
    motor4.decay_mode = (motor.SLOW_DECAY)  # Optional expansion motor


# ============================================================================
# MOTOR CONTROL FUNCTIONS
# ============================================================================

def motorStop():
    """
    Emergency stop function - immediately stops all motors
    
    This function sets all motor throttles to 0, causing immediate停止
    Used for:
    - Emergency stops
    - End of movement commands  
    - Safety shutdown
    - Transition between movement modes
    
    Safety: This function should be called before any major mode changes
    """
    global motor1,motor2,motor3,motor4
    motor1.throttle = 0
    motor2.throttle = 0
    motor3.throttle = 0
    motor4.throttle = 0

def Motor(channel,direction,motor_speed):
    # channel,1~4:M1~M4
  if motor_speed > 100:
    motor_speed = 100
  elif motor_speed < 0:
    motor_speed = 0

  speed = map(motor_speed, 0, 100, 0, 1.0)

  # setup() 
  pwm_motor.frequency = FREQ
  # Prevent the servo from affecting the frequency of the motor
  if direction == -1:
    speed = -speed
  if channel == 1:
    motor1.throttle = speed
  elif channel == 2:
    motor2.throttle = speed
  elif channel == 3:
    motor3.throttle = speed
  elif channel == 4:
    motor4.throttle = speed

def move(speed, direction, turn, radius=0.6):
    """
    Main robot movement function with tank-style steering
    
    This is the primary movement control function that handles all basic
    robot movements using differential motor control (tank steering).
    
    Args:
        speed (int): Motor speed percentage (0-100)
        direction (int): Movement direction (1=forward, -1=backward)
        turn (str): Turn direction ("left", "right", "mid" for straight)
        radius (float): Turn radius modifier (0-1, currently unused)
    
    Movement Logic:
        - Forward: Both motors rotate forward
        - Backward: Both motors rotate backward  
        - Left turn: Right motor forward, left motor backward (tank turn)
        - Right turn: Left motor forward, right motor backward (tank turn)
    
    Examples:
        move(50, 1, "mid")    # Move forward at 50% speed
        move(30, 1, "left")   # Turn left while moving forward at 30%
        move(80, -1, "no")    # Move backward at 80% speed
        move(0, 0, "mid")     # Stop all motors
        
    Note: This function uses the global direction multipliers (M1_Direction, 
          M2_Direction) to handle motor wiring variations.
    """
    if speed == 0:
        motorStop()  # Safety stop for zero speed
    else:
        if direction == 1:              # FORWARD MOVEMENT
            if turn == 'left':          # Forward + Left turn (tank style)
                Motor(1, -M1_Direction, speed)  # Right motor reverse
                Motor(2, M2_Direction, speed)   # Left motor forward
            elif turn == 'right':       # Forward + Right turn (tank style)
                Motor(1, M1_Direction, speed)   # Right motor forward  
                Motor(2, -M2_Direction, speed)  # Left motor reverse
            else:                       # Straight forward (turn == "mid")
                Motor(1, M1_Direction, speed)   # Both motors forward
                Motor(2, M2_Direction, speed)
        elif direction == -1: 		# backward
            Motor(1, -M1_Direction, speed)
            Motor(2, -M2_Direction, speed)

def destroy():
    motorStop()
    pwm_motor.deinit()

def trackingMove(speed, direction, turn, radius=0.6):
    """
    Line tracking movement function with motor compensation
    
    This function is specifically designed for line following operations
    and includes speed offsets to compensate for motor differences that
    could cause the robot to drift during straight-line tracking.
    
    Args:
        speed (int): Base motor speed percentage (0-100)
        direction (int): Movement direction (1=forward, -1=backward)
        turn (str): Turn direction ("left", "right", "mid")
        radius (float): Unused parameter (maintained for compatibility)
        
    Key Differences from move():
        - Applies TL_LEFT_Offset and TL_RIGHT_Offset for drift compensation
        - Uses Motor(channel, 0, speed) to stop one motor during tight turns
        - Optimized for precise line following with minimal overshoot
        
    Offset System:
        - TL_LEFT_Offset: Compensates for left motor power differences
        - TL_RIGHT_Offset: Compensates for right motor power differences
        - These values help maintain straight tracking on lines
    """
    if speed == 0:
        motorStop()  # Stop all motors for zero speed
    else:
        if direction == 1:              # FORWARD TRACKING
            if turn == 'left':          # Track left turn
                Motor(1, -M1_Direction, speed + TL_LEFT_Offset)   # Right motor reverse
                Motor(2, 0, speed + TL_RIGHT_Offset)              # Left motor stop
            elif turn == 'right':       # Track right turn  
                Motor(1, 0, speed)                                # Right motor stop
                Motor(2, -M2_Direction, speed + TL_RIGHT_Offset)  # Left motor reverse
            else:                       # Track straight (turn == "mid")
                Motor(1, M1_Direction, speed + TL_LEFT_Offset)    # Both motors forward
                Motor(2, M2_Direction, speed + TL_RIGHT_Offset)   # with compensation
        elif direction == -1:           # BACKWARD TRACKING
            Motor(1, -M1_Direction, speed + TL_LEFT_Offset)       # Both motors reverse
            Motor(2, -M2_Direction, speed + TL_RIGHT_Offset)      # with compensation


# ============================================================================
# COMPUTER VISION TRACKING FUNCTIONS
# ============================================================================

def video_Tracking_Move(speed, direction, turn, radius=0):
    """
    Advanced movement function for computer vision tracking
    
    This function provides smooth, proportional turning for vision-based
    tracking systems. It uses differential motor speeds to create smooth
    curves rather than sharp tank-style turns.
    
    Args:
        speed (int): Base motor speed percentage (0-100)
        direction (int): Movement direction (1=forward, -1=backward)
        turn (str): Turn direction ("left", "right", "mid")
        radius (float): Turn sharpness factor (0-1)
                       0 = sharp turn, 1 = gentle curve
                       
    Key Features:
        - Proportional turning: Inner wheel speed = speed * radius
        - Smooth vision tracking: Reduces jerky movements during object following  
        - Camera-friendly: Minimizes rapid direction changes that confuse CV
        - Line following: Gentle corrections for video-based line tracking
        
    Examples:
        video_Tracking_Move(50, 1, "left", 0.3)   # Sharp left turn
        video_Tracking_Move(60, 1, "right", 0.8)  # Gentle right curve
        video_Tracking_Move(40, 1, "mid", 0)      # Straight forward
    """
    if speed == 0:
        motorStop()  # Safety stop for zero speed
    else:
        if direction == 1:              # FORWARD VISION TRACKING
            if turn == 'left':          # Smooth left turn
                Motor(1, -M1_Direction, speed)              # Right motor full speed
                Motor(2, M2_Direction, speed * radius)      # Left motor proportional
            elif turn == 'right':       # Smooth right turn
                Motor(1, M1_Direction, speed * radius)      # Right motor proportional
                Motor(2, -M2_Direction, speed)
            else: 					# forward  (mid)
                Motor(1, M1_Direction, speed)
                Motor(2, M2_Direction, speed)
        elif direction == -1: 		# backward
            Motor(1, -M1_Direction, speed)
            Motor(2, -M2_Direction, speed)
            

if __name__ == '__main__':
    try:
        speed_set = 20
        setup()
        move(speed_set, -1, 'mid', 0.8)
        time.sleep(3)
        motorStop()
        time.sleep(1)
        move(speed_set, 1, 'mid', 0.8)
        time.sleep(3)
        motorStop()
    except KeyboardInterrupt:
        destroy()

