#!/usr/bin/python

###
# Brian Hession
#
# A tool to do a bunch of different ECC calculations
#

from __future__ import print_function
import sys, getopt

# Polynomial types
simple = 1
supersingular = 2
nonsupersingular = 3

def main(argv):

    global verbose
    verbose = False
    case = 0
    polytype = simple
    alpha = -1
    beta = -1
    gamma = -1
    modulo = -1

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hva:b:c:p:123')
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit(0)
        elif o == '-v':
            verbose = True
        elif o == '-a':
            alpha = int(a)
        elif o == '-b':
            beta = int(a)
        elif o == '-c':
            gamma = int(a)
        elif o == '-p':
            modulo = int(a)
        elif o == '-1':
            polytype = simple
        elif o == '-2':
            polytype = supersingular
        elif o == '-3':
            polytype = nonsupersingular
        else:
            assert False, 'Unhandled option'

    # Parse out command and arguments
    if len(args) == 0:
        print_usage_and_exit(1)
    command = args[0]
    args = args[1:]

    # Modular multiplicative inverse
    if command == "modinverse":
        if len(args) != 2:
            print_usage_and_exit(1)
        k = int(args[0])
        p = int(args[1])
        kinv = modinverse(k, p)
        assert k * kinv % p == 1
        print('{} * {} = 1 mod {}'.format(k, kinv, p))
        sys.exit(0)

    # Build polynomial
    poly = None
    if polytype == simple:
        if alpha < 0 or beta < 0 or modulo < 0:
            print('ERROR: Expected polynomial coefficients/modulo', file=sys.stderr)
            sys.exit(1)
        poly = ECCSimplePoly(alpha, beta, modulo)
    elif polytype == supersingular:
        assert False, 'Unimplemented polynomial type'
    elif polytype == nonsupersingular:
        assert False, 'Unimplemented polynomial type'
    else:
        assert False, 'Invalid polynomial type'

    # List group
    if command == "listgroup":
        if len(args) != 2:
            print_usage_and_exit(1)
        x = int(args[0])
        y = int(args[1])
        elements = poly.calc_elements((x, y))
        for i in range(len(elements)):
            print('{:3d}: ({:3d}; {:3d})'.format(i + 1, elements[i][0], elements[i][1]))

    # Scalar multiplication
    elif command == "multiply":
        if len(args) != 3:
            print_usage_and_exit(1)
        x = int(args[0])
        y = int(args[1])
        scalar = int(args[2])
        ret_x, ret_y = poly.eccmul((x, y), scalar)
        print('{} * ({}; {}) = ({}; {})'.format(scalar, x, y, ret_x, ret_y))

    # Add points
    elif command == "add":
        if len(args) != 4:
            print_usage_and_exit(1)
        x1 = int(args[0])
        y1 = int(args[1])
        x2 = int(args[2])
        y2 = int(args[3])
        ret_x, ret_y = poly.eccadd((x1, y1), (x2, y2))
        print('({}; {}) + ({}; {}) = ({}; {})'.format(x1, y1, x2, y2, ret_x, ret_y))

    # Polynomial multiplicative inverse
    elif command == "polyinverse":
        if len(args) != 3:
            print_usage_and_exit(1)
        x = int(args[0])
        y = int(args[1])
        k = int(args[2])
        elements = poly.calc_elements((x, y))
        kinv = modinverse(k, len(elements))
        assert poly.eccmul((x, y), k * kinv) == (x, y)
        print('{} * {} * ({}; {}) = ({}, {})'.format(k, kinv, x, y, x, y))

    # Else error
    else:
        print('ERROR: Invalid command `{}`'.format(command), file=sys.stderr)


#####################################################################
# Helping functions
#####################################################################

def log(message):
    if verbose:
        print(message)

def euclidean(a, b):
    """Returns (gcd, x, y) where a * x + b * y = gcd"""
    x2, x1 = 0, 1
    y2, y1 = 1, 0
    r2, r1 = b, a
    while r2 != 0:
        q = r1 / r2
        r1, r2 = r2, r1 - (q * r2)
        x1, x2 = x2, x1 - (q * x2)
        y1, y2 = y2, y1 - (q * y2)
    return r1, x1, y1

def modinverse(n, p):
    """Returns ninv where n * ninv = 1 mod p"""
    gcd, x, y = euclidean(n, p)
    assert (n * x + p * y) % p == gcd
    assert gcd == 1, 'No modular multiplicative inverse exists'
    return x % p

#####################################################################
# ECC Polynomial Classes
#####################################################################

def simple_eccdouble(poly, p):
    if not isinstance(poly, ECCSimplePoly):
        assert False, 'Invalid eccdouble function'
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        assert False, 'Invalid point type'

    alpha = int(poly.coefficients[0])
    beta = int(poly.coefficients[1])
    modulo = int(poly.modulo)
    x, y = int(p[0]), int(p[1])

    # Special case for infinity
    if x < 0 or y < 0:
        return p

    slope_top = (3 * (x * x) + alpha) % modulo
    slope_bottom = (2 * y) % modulo
    if slope_bottom == 0:
        return (-1, -1)

    slope = (slope_top * modinverse(slope_bottom, modulo)) % modulo
    ret_x = ((slope * slope) - (2 * x)) % modulo
    ret_y = ((slope * (x - ret_x)) - y) % modulo

    return (ret_x, ret_y)

def simple_eccadd(poly, p1, p2):
    if not isinstance(poly, ECCSimplePoly):
        assert False, 'Invalid eccadd function'
    if not isinstance(p1, (tuple, list)) or len(p1) != 2:
        assert False, 'Invalid point type'
    if not isinstance(p2, (tuple, list)) or len(p2) != 2:
        assert False, 'Invalid point type'

    alpha = int(poly.coefficients[0])
    beta = int(poly.coefficients[1])
    modulo = int(poly.modulo)
    x1, y1 = int(p1[0]), int(p1[1])
    x2, y2 = int(p2[0]), int(p2[1])

    # Special case for infinity
    if x1 < 0 or y1 < 0:
        return (x2, y2)
    if x2 < 0 or y2 < 0:
        return (x1, y1)

    # Check if doubling instead of adding (different algorithms)
    if x1 == x2 and y1 == y2:
        return simple_eccdouble(poly, p1)

    slope_top = (y2 - y1) % modulo
    slope_bottom = (x2 - x1) % modulo
    if slope_bottom == 0:
        return (-1, -1)

    slope = (slope_top * modinverse(slope_bottom, modulo)) % modulo
    ret_x = ((slope * slope) - x1 - x2) % modulo
    ret_y = ((slope * (x1 - ret_x)) - y1) % modulo

    return (ret_x, ret_y)

class ECCPoly(object):
    """ECC Polynomial Structure"""

    def __init__(self, coefficients, modulo, eccdouble, eccadd):
        self.coefficients = coefficients
        self.modulo = modulo
        self.__eccdouble = eccdouble
        self.__eccadd = eccadd

    def eccmul(self, p, s):
        if not isinstance(p, (tuple, list)) or len(p) != 2:
            assert False, 'Invalid point'
        if not isinstance(s, int):
            assert False, 'Invalid scalar data type'
        ret = (-1, -1)
        scalar = [x for x in list('{0:0b}'.format(s))]
        while len(scalar) > 0:
            log('{}: {}'.format(scalar[0], ''.join(scalar)))
            bit = int(scalar.pop(0))
            ret = self.__eccdouble(self, ret)
            log('Double: ({:3d}; {:3d})'.format(*ret))
            if bit == 1:
                ret = self.__eccadd(self, ret, p)
                log(' - Add: ({:3d}; {:3d})'.format(*ret))
            log('')
        return ret

    def eccadd(self, p1, p2):
        return self.__eccadd(self, p1, p2)

    def eccdouble(self, p):
        return self.__eccdouble(self, p)

    def calc_elements(self, p):
        elements = list()
        ret_x, ret_y = -1, -1
        while True:
            ret_x, ret_y = self.__eccadd((ret_x, ret_y), p)
            elements.append((ret_x, ret_y))
            if ret_x < 0 or ret_y < 0:
                break
        return elements

class ECCSimplePoly(ECCPoly):
    """Simple ECC Polynomial Structure: y^2 = x^3 + ax + b"""

    def __init__(self, alpha, beta, modulo):
        super(ECCSimplePoly, self).__init__(
                (beta, alpha),
                modulo,
                simple_eccdouble,
                simple_eccadd)


#####################################################################
# Main Program Stuff
#####################################################################

def print_usage_and_exit(exitcode):
    print('USAGE: {} [OPTIONS] -a alpha -b beta [-c gamma] -p modulo <action> [args...]'.format(sys.argv[0]))
    print('')
    print('Note: The point (-1, -1) is used to express the point at infinity')
    print('')
    print('ACTIONS\t\tARGS\t\tDESCRIPTION')
    print('listgroup\tx y\t\tLists the elements given the generator')
    print('multiply\tx y scalar\tMultiplies a point with a scalar')
    print('add\t\tx1 y1 x2 y2\tAdds two points')
    print('polyinverse\tx y k\t\tPolynomial multiplicative inverse')
    print('modinverse\tk p\t\tModular multiplicative inverse')
    print('')
    print('OPTIONS')
    print('  -h\t\tPrint this message')
    print('  -v\t\tSet verbose logging')
    print('  -a alpha\tAlpha coefficient')
    print('  -b beta\tBeta coefficient')
    print('  -c gamma\tGamma coefficient')
    print('  -p modulo\tPolynomial modulo')
    print('  -1\t\tSimple: y^2 = x^3 + bx + a (default)')
    print('  -2\t\tSupersingular: y^2 + cy = x^3 + bx + a')
    print('  -3\t\tNon-supersingular: y^2 + xy = x^3 + bx^2 + a')
    sys.exit(exitcode)

if __name__ == '__main__':
    main(sys.argv[1:])

