#!/usr/bin/sage

import sys, getopt

def main(argv):

    p = None
    verbose = False
    poly = list()
    users = list()
    doSolve = None

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hvp:gs')
    except getopt.GetoptError as err:
        print(err)
        return

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit()
        elif o == '-v':
            verbose = True
        elif o == '-p':
            p = int(a)
        elif o == '-g':
            doSolve = False
        elif o == '-s':
            doSolve = True
        else:
            assert False, 'Unhandled option'

    if not p or doSolve == None:
        print_usage_and_exit(1)
    if not doSolve:
        if len(args) != 2:
            print_usage_and_exit(1)
        for a in args[0].split():
            poly.append(int(a))
        for u in args[1].split():
            users.append(int(u))
        debug('Threshold: {} - coefficients: {}'.format(len(poly), poly), verbose)
        debug('Users: {} - public keys: {}'.format(len(users), users), verbose)

        P.<a> = PolynomialRing(GF(p))
        P = P(poly)
        debug('Polynomial: {}'.format(P), verbose)
        userkeys = shamirs(p, P, users, verbose)
        print(userkeys)
    else:
        if len(args) == 0:
            print_usage_and_exit(1)
        points = list()
        for a in args:
            points.append([int(c) for c in a.split()])
        debug('User keys: {}'.format(points), verbose)
        a0 = solve_shamirs(points, p, verbose)
        print(a0)


def shamirs(p, P, users, verbose=False):
    userkeys = list()
    for key in users:
        userkeys.append((key, P(key)))
    debug('User points: {}'.format(userkeys), verbose)
    return userkeys


def modular_inverse(n, p):
    return n**(p-2) % p


def solve_shamirs(userkeys, p, verbose=False):
    a0 = 0
    for i in xrange(len(userkeys)):
        xi, yi = userkeys[i]

        js = range(len(userkeys))
        js.remove(i)
        debug(js, verbose)

        prod = 1
        for j in js:
            xj = userkeys[j][0]
            inverse = modular_inverse(xj - xi, p)
            innerprod = mod(xj * inverse, p)
            prod = mod(prod * innerprod, p)
            debug('{0}/({0}-{1}) = {0}*{2} = {3}'.format(xj, xi, inverse, innerprod), verbose)
        atmp = mod(a0 + (yi * prod), p)
        debug('{} + ({} * {}) = {}'.format(a0, yi, prod, atmp), verbose)
        a0 = atmp
    return a0


def debug(msg, verbose=False):
    if verbose:
        print(msg)


def print_usage_and_exit(code=0):
    print('Usage: {} -p prime -g "a0 a1..." "user1 user2..."'.format(sys.argv[0]))
    print('Usage: {} -p prime -s "user1-x user1-y" "user2-x user2-y"'.format(sys.argv[0]))
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

