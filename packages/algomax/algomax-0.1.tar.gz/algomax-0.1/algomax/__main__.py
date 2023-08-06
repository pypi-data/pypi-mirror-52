import sys
from .algomax import algomax as a_max


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    a_max(args)


if __name__ == '__main__':
    main()
