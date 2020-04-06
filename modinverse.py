#!/usr/bin/python3

import sys, getopt

def main(argv):

    m = None

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hm:')
    except getopt.GetoptError as err:
        print(err)
        return

    for op, arg in oplist:
        if op == '-h':
            print_usage_and_exit()
        elif op == '-m':
            m = int(arg)
        else:
            assert False, 'Unhandled option'

    for arg in args:
        a = int(arg)
        print('{}^-1 mod {} = {}'.format(a, m, modular_inverse(a, m)))


def euclidean(a, b, verbose=False):
    """Returns (gcd, x, y) where a * x + b * y = gcd"""
    x2, x1 = 0, 1
    y2, y1 = 1, 0
    r2, r1 = b, a
    while r2 != 0:
        q = int(r1 / r2)
        r1, r2 = r2, r1 - (q * r2)
        x1, x2 = x2, x1 - (q * x2)
        y1, y2 = y2, y1 - (q * y2)
    return r1, x1, y1


def modular_inverse(n, p, verbose=False):
    """Returns ninv where n * ninv = 1 mod p"""
    gcd, x, y = euclidean(n, p, verbose)
    assert (n * x + p * y) % p == gcd
    assert gcd == 1, 'No modular multiplicative inverse exists gcd({}, {}) = {}'.format(n, p, gcd)
    return x % p


if __name__ == '__main__':
    main(sys.argv[1:])
