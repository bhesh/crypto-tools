#!/usr/bin/python3

from __future__ import print_function
import sys, getopt

def main(argv):

    # Set defaults
    f = sys.stdin

    # If a file was specified...
    if len(argv) > 0:
        f = open(argv[0], 'r')

    # Concatenate ciphertext and store into string
    ciphertext = str()
    for line in f:
        for c in line.upper():
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                ciphertext += c

    if len(argv) > 0:
        f.close()

    print(ciphertext)
    sys.exit(0)

    # Do stuff
    patterns = {}
    for start in range(len(ciphertext) - 6):
        pattern = ciphertext[start:start+3]
        for end in range(start + 3, len(ciphertext) - 3):
            item = ciphertext[end:end+3]
            if pattern == item:
                if pattern not in patterns:
                    patterns[pattern] = [start]
                if end not in patterns[pattern]:
                    patterns[pattern].append(end)
    for p in patterns:
        print(p, patterns[p])


def print_usage_and_exit(exitcode):
    print('USAGE: {} [file]'.format(sys.argv[0]))
    print('')
    print('If file is not specified, input is taken from stdin.')
    sys.exit(exitcode)


if __name__ == '__main__':
    main(sys.argv[1:])
