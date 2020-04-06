#!/usr/bin/python3

from __future__ import print_function
import sys, getopt

def main(argv):

    # Set defaults
    func = encode
    f = sys.stdin
    keys = []

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hk:ed')
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit(0)
        elif o == '-k':
            for k in a.split(':'):
                try:
                    keys.append(int(k))
                except:
                    keys.append(ord(k.upper()) - ord('A'))
        elif o == '-e':
            func = encode
        elif o == '-d':
            func = decode
        else:
            assert False, 'Unhandled option'

    # Check if keys were specified
    if len(keys) == 0:
        print_usage_and_exit(1)

    # If a file was specified...
    if len(args) > 0:
        f = open(args[0], 'r')

    # do stuff
    resp = func(keys, f)
    print(resp)

    if len(args) > 0:
        f.close()


def encode(keys, f):
    "Encodes the vigenere cipher"
    ciphertext = ''
    i = 0
    for line in f:
        for c in line.upper():
            val = ord(c) - ord('A')
            if val >= 0 and val <= 26:
                nval = (val + keys[i % len(keys)]) % 26
                ciphertext += chr(nval + ord('A'))
                i += 1
    return ciphertext


def decode(keys, f):
    "Decodes the vigenere cipher"
    message = ''
    i = 0
    for line in f:
        for c in line.upper():
            val = ord(c) - ord('A')
            if val >= 0 and val <= 26:
                nval = (val - keys[i % len(keys)]) % 26
                message += chr(nval + ord('A'))
                i += 1
    return message


def print_usage_and_exit(exitcode):
    print('USAGE: {} [OPTIONS] [file]'.format(sys.argv[0]))
    print('')
    print('If file is not specified, input is taken from stdin.')
    print('')
    print('  -h\t\tPrint this message')
    print('  -k ARG\tkey1:key2:key3:...:keyN')
    print('  -e\t\tEncode')
    print('  -d\t\tDecode')
    sys.exit(exitcode)


if __name__ == '__main__':
    main(sys.argv[1:])
