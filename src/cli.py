#!/usr/bin/python

import sys


def main():
    if len(sys.argv) > 1:
        print(f"hello {sys.argv[1]}!")
    else:
        print("hello")


if __name__ == "__main__":
    sys.exit(main())
