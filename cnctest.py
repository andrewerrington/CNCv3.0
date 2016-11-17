import time

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)  # Change to select()?
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch()
        else:
            return None

def openclose(state):
    if state:
        return "Open"
    else:
        return "Closed"


if __name__=="__main__":

    getch = _Getch()

    while True:
        print ("\n\nCNC v3.0 tester")
        print ("X = move X outward")
        print ("x = move X inward")
        print ("Y = move Y outward")
        print ("y = move Y inward")
        print ("Z = move X outward")
        print ("z = move X inward")
        print ("Qq = Quit")


        key = getch()
        if key == b'X':
            print("                X outward")
        elif key == b'x':
            print("                X inward")
        elif key == b'Y':
            print("                Y outward")
        elif key == b'y':
            print("                Y inward")
        elif key == b'Z':
            print("                Z outward")
        elif key == b'z':
            print("                Z inward")
        elif key == b'Q' or key == b'q':
            break
        else:
            print("                Stop")

        # Show the state of the switches on the machine.
        X_limit = True
        X_rotation = True
        Y_limit = True
        Y_rotation = True
        Z_limit = True
        Z_rotation = True

        print("X limit: %s"%openclose(X_limit))
        print("X rotation: %s"%openclose(X_rotation))

        print("Y limit: %s"%openclose(Y_limit))
        print("Y rotation: %s"%openclose(Y_rotation))

        print("Z limit: %s"%openclose(Z_limit))
        print("Z rotation: %s"%openclose(Z_rotation))

        time.sleep(0.2)


    # Tidy up
    print("Finished")
    

        
    
