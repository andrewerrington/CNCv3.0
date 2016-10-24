# CNCv3.0
Python version of Homofaciens CNC v3.0 cardboard CNC machine.

This is intended to run on a Raspberry Pi with the PiGPIO daemon.  The
servos and switches are connected to the Pi GPIO lines, and the software
plots characters on the CNC model in the same way as the Arduino code.

The best way to run the program is to use the 'cnc' bash script.  At
the command line type:

./cnc

This will start the pigpio server and then run the CNC program.  If the
program encounters an error (or CTRL-C is pressed) then it will exit and
the bash script will stop the pigpio server, which will stop any servos
that are running.
