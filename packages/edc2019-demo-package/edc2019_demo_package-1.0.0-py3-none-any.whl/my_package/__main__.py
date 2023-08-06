import sys
from . import echo

def main():
    if len(sys.argv) == 3:
        echo(sys.argv[1], sys.argv[2])
    else:
        echo()

if __name__ == '__main__':
    main()
