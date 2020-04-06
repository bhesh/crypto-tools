#!/usr/bin/python3

from __future__ import print_function
import sys, getopt

def main(argv):

    # Set defaults
    func = encode
    f = sys.stdin
    k1 = -1
    k2 = -1

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'ha:b:ed')
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit(0)
        elif o == '-a':
            k1 = int(a)
        elif o == '-b':
            k2 = int(a)
        elif o == '-e':
            func = encode
        elif o == '-d':
            func = decode
        else:
            assert False, 'Unhandled option'

    # Check if k1 and k2 were specified
    if k1 == -1 or k2 == -1:
        print_usage_and_exit(1)

    # If a file was specified...
    if len(args) > 0:
        f = open(args[0], 'r')

    # do stuff
    resp = func(k1, k2, f)
    print(resp)

    if len(args) > 0:
        f.close()


def encode(k1, k2, f):
    "Encodes the affine cipher"
    ciphertext = ''
    for line in f:
        for c in line.upper():
            val = ord(c) - ord('A')
            if val >= 0 and val <= 26:
                nval = (k1 * val + k2) % 26
                ciphertext += chr(nval + ord('A'))
    return ciphertext


def decode(k1, k2, f):
    "Decodes the affine cipher"
    k1_inv = get_inverse(26, k1)
    message = ''
    for line in f:
        for c in line.upper():
            val = ord(c) - ord('A')
            if val >= 0 and val <= 26:
                nval = ((val - k2) * k1_inv) % 26
                message += chr(nval + ord('A'))
    return message


def get_inverse(a, b):
    "Returns the inverse assuming gcd(a, b) = 1"
    x1, x2 = 0, 1
    q = int(a / b)
    r1, r2 = b, a % b
    while r2 > 0:
        x1, x2 = x2, x1 - (q * x2)
        q = int(r1 / r2)
        r1, r2 = r2, r1 % r2
    return x2 % 26 # This works for negatives in Python!


def print_usage_and_exit(exitcode):
    print('USAGE: {} [OPTIONS] [file]'.format(sys.argv[0]))
    print('')
    print('If file is not specified, input is taken from stdin.')
    print('')
    print('  -h\t\tPrint this message')
    print('  -a ARG\tkey 1')
    print('  -b ARG\tkey 2')
    print('  -e\t\tEncode')
    print('  -d\t\tDecode')
    sys.exit(exitcode)


if __name__ == '__main__':
    main(sys.argv[1:])
