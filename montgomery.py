#!/usr/bin/python3

import sys, getopt, math

VERBOSE = False
NONE = 0
FORM = 1
REDC = 2
MULT = 3

def main(argv):

    global VERBOSE
    m = None
    R = None
    operation = NONE

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hvm:R:trx')
    except getopt.GetoptError as err:
        print(err)
        return

    for op, arg in oplist:
        if op == '-h':
            print_usage_and_exit()
        elif op == '-v':
            VERBOSE = True
        elif op == '-m':
            m = int(arg)
        elif op == '-R':
            R = int(arg)
        elif op == '-t':
            operation = FORM
        elif op == '-r':
            operation = REDC
        elif op == '-x':
            operation = MULT
        else:
            assert False, 'Unhandled option'

    if not m or not R or operation == NONE:
        print_usage_and_exit(1)
    values = [int(a) for a in args]
    if operation == FORM:
        if len(values) < 1:
            print_usage_and_exit(1)
        ret = [MP(v, (R*R) % m, m, R) for v in values]
        print(ret)
        ret = [MP(v, 1, m, R) for v in ret]
        print(ret)
    elif operation == REDC:
        if len(values) < 1:
            print_usage_and_exit(1)
        mont = [MPReduce(v, m, R) for v in values]
        print('Montgomery Reduction: {}'.format(mont))
    elif operation == MULT:
        if len(values) < 2:
            print_usage_and_exit(1)
        debug('Transform into Montgomery domain - MP(v, R*R % m, m)')
        mont = [MP(v, (R*R) % m, m, R) for v in values]
        print('Montgomery values: {}'.format(mont))
        ret = mont[0]
        for v in mont[1:]:
            ret = MP(ret, v, m, R)
        print('Montgomery product: {}'.format(ret))
        debug('Transform into Integer domain - MP(v, 1, m)')
        print(MP(ret, 1, m, R))


def euclidean(a, b, verbose=False):
    """Returns (gcd, x, y) where a * x + b * y = gcd"""
    x2, x1 = 0, 1
    y2, y1 = 1, 0
    r2, r1 = b, a
    debug('{}\t{}\t{}\t{}'.format('-', r2, x2, y2), verbose)
    while r2 != 0:
        q = int(r1 / r2)
        r1, r2 = r2, r1 - (q * r2)
        x1, x2 = x2, x1 - (q * x2)
        y1, y2 = y2, y1 - (q * y2)
        debug('{}\t{}\t{}\t{}'.format(q, r2, x2, y2), verbose)
    return r1, x1, y1


def modular_inverse(n, p, verbose=False):
    """Returns ninv where n * ninv = 1 mod p"""
    gcd, x, y = euclidean(n, p, verbose)
    assert (n * x + p * y) % p == gcd
    assert gcd == 1, 'No modular multiplicative inverse exists gcd({}, {}) = {}'.format(n, p, gcd)
    return x % p


def MPReduce(T, m, R):
    assert R > m, 'Cannot transform: R must get greater than m'
    assert math.gcd(R, m) == 1, 'Cannot transform: gcd(R, m) != 1'
    Rinv = modular_inverse(R, m)
    debug('R^-1 mod m = {}'.format(Rinv))
    minv = modular_inverse(m, R)
    debug('m^-1 mod R = {}'.format(minv))
    mprime = (-minv) % R
    debug('m\' mod R = {}'.format(mprime))
    U = (T * mprime) % R
    debug('U = {} * m\' mod R = {}'.format(T, U))
    TRinv = ((T + (U*m)) * Rinv) % m
    debug('{} * R^-1 mod m = {}'.format(T, TRinv))
    t = (TRinv * R) % m
    debug('{} * R mod m = {}'.format(TRinv, t))
    return TRinv


def MP(X, Y, m, R):
    assert R > m, 'Cannot transform: R must get greater than m'
    assert math.gcd(R, m) == 1, 'Cannot transform: gcd(R, m) != 1'
    Rinv = modular_inverse(R, m)
    debug('R^-1 = {}'.format(Rinv))
    A = (X * Y * Rinv) % m
    debug('{} * {} * R^-1 mod m = {}'.format(X, Y, A))
    return A


def debug(msg, verbose=None):
    if verbose != None and verbose:
        print(msg)
    elif verbose == None and VERBOSE:
        print(msg)


def print_usage_and_exit(code=0):
    print('Usage: {} -m modulus -b wordsize -R mont-modulus [-x] x1 x2 [x3...]'.format(sys.argv[0]))
    print('       {} -m modulus -b wordsize -R mont-modulus -t x1 [x2...]'.format(sys.argv[0]))
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

