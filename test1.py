import sys
import termios
import tty
from contextlib import contextmanager

LOG_FILE = "terminal_keys.log"


@contextmanager
def raw_mode(fd):
    """Context manager pour le mode raw du terminal."""
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def getch(fd):
    """Lit un caractère depuis stdin."""
    return sys.stdin.read(1)


def main():
    fd = sys.stdin.fileno()
    
    try:
        with raw_mode(fd), open(LOG_FILE, "a", encoding="utf-8", buffering=1) as f:
            while True:
                key = getch(fd)
                
                # Gestion des touches spéciales
                if key == "\x03":  # Ctrl+C
                    break
                elif key == "\x7f":  # Backspace - ignoré
                    continue
                elif key == "\x1b":  # Séquence d'échappement (flèches, etc.)
                    # Lire et ignorer les caractères suivants
                    sys.stdin.read(2)
                    continue
                
                # Écriture immédiate
                f.write(key)
                    
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main() 
