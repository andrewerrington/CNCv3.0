import fcntl
import sys
import os
import time
import tty
import termios
import pigpio

# Quickly hacked way of turning servos on and off, and watching
# the state of the inputs, to allow setting up and adjusting
# the Cardboard CNC model.

# by Andrew Errington 17 November 2016

# Non-blocking stdin from
# http://ballingt.com/nonblocking-stdin-in-python-3

class raw(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

class nonblocking(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()
    def __enter__(self):
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)


def openclose(state):
    return "Open" if state else "Closed"


# Constants for servo control
CENTRE = 1500  # stop
INWARD = 1800  # clockwise, draw the carriage closer
OUTWARD = 1000 # anticlockwise, push the carriage away

#GPIO pins for rotation sensor, limit switch and servo PWM
SENSOR_X = 24
SWITCH_X = 25
SERVO_X = 23
            
SENSOR_Y = 17
SWITCH_Y = 27
SERVO_Y = 22

SENSOR_Z = 5
SWITCH_Z = 6
SERVO_Z = 13

# Set up a pigpio object
pi = pigpio.pi()

# Set up GPIO pins.  Turn on pullups for switch inputs.
pi.set_mode(SENSOR_X, pigpio.INPUT)
pi.set_pull_up_down(SENSOR_X, pigpio.PUD_UP)
pi.set_mode(SWITCH_X, pigpio.INPUT)
pi.set_pull_up_down(SWITCH_X, pigpio.PUD_UP)
pi.set_mode(SERVO_X, pigpio.OUTPUT)

pi.set_mode(SENSOR_Y, pigpio.INPUT)
pi.set_pull_up_down(SENSOR_Y, pigpio.PUD_UP)
pi.set_mode(SWITCH_Y, pigpio.INPUT)
pi.set_pull_up_down(SWITCH_Y, pigpio.PUD_UP)
pi.set_mode(SERVO_Y, pigpio.OUTPUT)

pi.set_mode(SENSOR_Z, pigpio.INPUT)
pi.set_pull_up_down(SENSOR_Z, pigpio.PUD_UP)
pi.set_mode(SWITCH_Z, pigpio.INPUT)
pi.set_pull_up_down(SWITCH_Z, pigpio.PUD_UP)
pi.set_mode(SERVO_Z, pigpio.OUTPUT)


with raw(sys.stdin):
    with nonblocking(sys.stdin):
        while True:
            c = sys.stdin.read(1)

            if c:
                print(c)
            else:
                print("No key")

            print ("\n\nCNC v3.0 tester")
            print ("X = move X outward")
            print ("x = move X inward")
            print ("Y = move Y outward")
            print ("y = move Y inward")
            print ("Z = move Z outward")
            print ("z = move Z inward")
            print ("Qq = Quit")

            key = c

            if key == 'X':
                print("                X outward")
                pi.set_servo_pulsewidth(SERVO_X, OUTWARD)

            elif key == 'x':
                print("                X inward")
                pi.set_servo_pulsewidth(SERVO_X, INWARD)

            elif key == 'Y':
                print("                Y outward")
                pi.set_servo_pulsewidth(SERVO_Y, OUTWARD)

            elif key == 'y':
                print("                Y inward")
                pi.set_servo_pulsewidth(SERVO_Y, INWARD)

            elif key == 'Z':
                print("                Z outward")
                pi.set_servo_pulsewidth(SERVO_Z, OUTWARD)

            elif key == 'z':
                print("                Z inward")
                pi.set_servo_pulsewidth(SERVO_Z, INWARD)

            elif key == 'Q' or key == 'q':
                break
            else:
                print("                Stop")
                pi.set_servo_pulsewidth(SERVO_X, 0)
                pi.set_servo_pulsewidth(SERVO_Y, 0)
                pi.set_servo_pulsewidth(SERVO_Z, 0)

            # Show the state of the switches on the machine.
            X_limit = pi.read(SWITCH_X)
            X_rotation = pi.read(SENSOR_X)
            Y_limit = pi.read(SWITCH_Y)
            Y_rotation = pi.read(SENSOR_Y)
            Z_limit = pi.read(SWITCH_Z)
            Z_rotation = pi.read(SENSOR_Z)

            print("X limit: %s"%openclose(X_limit))
            print("X rotation: %s"%openclose(X_rotation))

            print("Y limit: %s"%openclose(Y_limit))
            print("Y rotation: %s"%openclose(Y_rotation))

            print("Z limit: %s"%openclose(Z_limit))
            print("Z rotation: %s"%openclose(Z_rotation))

            time.sleep(0.1)

        # Tidy up
        print("Finished")
        pi.set_servo_pulsewidth(SERVO_X, 0)
        pi.set_servo_pulsewidth(SERVO_Y, 0)
        pi.set_servo_pulsewidth(SERVO_Z, 0)
