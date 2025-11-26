import sys
import termios
import tty

LOG_FILE = "terminal_keys.log"

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

while True:
    key = getch()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if key == " ":
            f.write(" ")
        elif key == "\n":
            f.write("\n")
        elif key == "\x7f":
            # On ignore backspace pour éviter réécriture
            pass
        else:
            f.write(key)
        f.flush()
