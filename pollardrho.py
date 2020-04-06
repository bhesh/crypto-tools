#!/usr/bin/python3

import sys, getopt, random, math

def main(argv):

    global verbose
    verbose = False
    alpha = None
    beta = None
    modulo = None
    
    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hva:b:m:')
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
        elif o == '-m':
            modulo = int(a)
        else:
            assert False, 'Unhandled option'

    # Parse command and arguments
    if len(args) == 0:
        pass
    else:
        command = args[0]
        args = args[1:]

        if command == 'solve':
            assert alpha and beta and modulo, 'Invalid alpha/beta/modulo'
            a0, b0 = 1, 1
            if len(args) == 2:
                a0, b0 = int(args[0]), int(args[1])
            elif len(args) != 0:
                print_usage_and_exit(1)
            z = solve(alpha, beta, modulo, a0, b0)
            print(z)

        elif command == 'subgroup':
            assert alpha and modulo, 'Invalid alpha/modulo'
            group = gen_subgroup(alpha, modulo)
            for i in range(len(group)):
                print('{}\t{}'.format(i, group[i]))

        elif command == 'genrand':
            assert alpha and beta and modulo, 'Invalid alpha/beta/modulo'
            a0, b0 = 1, 1
            if len(args) == 2:
                a0, b0 = int(args[0]), int(args[1])
            elif len(args) != 0:
                print_usage_and_exit(1)
            group = gen_subgroup(alpha, modulo)
            for params in standard_rand(alpha, beta, modulo, group, a0, b0):
                xi, x2i = params[:2]
                aj, bj, a2j, b2j = [j % len(group) for j in params[2:]]
                print('{}\t{}\t{},{}\t{},{}'.format(xi, x2i, aj, bj, a2j, b2j))

        elif command == 'test':
            assert alpha and beta and modulo, 'Invalid alpha/beta/modulo'
            if len(args) != 1:
                print_usage_and_exit(1)
            x = int(args[0])
            if (alpha**x) % modulo == beta % modulo:
                print('Pass')
            else:
                print('Fail')
        else:
            print('Invalid command `{}`'.format(command))


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


def gen_subgroup(alpha, modulo):
    group = [1]
    element = alpha
    while element not in group:
        group.append(element)
        element = (element * alpha) % modulo
    return group


def split_group(group):
    s1 = [x for x in group if x % 3 == 1]
    s2 = [x for x in group if x % 3 == 0]
    s3 = [x for x in group if x % 3 == 2]
    return s1, s2, s3


def next_x(x, a, b, alpha, beta, modulo, subgroups):
    if x in subgroups[0]:
        debug('beta*x, a, b+1')
        return (beta * x) % modulo, a, b + 1
    elif x in subgroups[1]:
        debug('x*x, 2a, 2b')
        return (x * x) % modulo, a * 2, b * 2
    elif x in subgroups[2]:
        debug('alpha*x, a+1, b')
        return (alpha * x) % modulo, a + 1, b
    else:
        assert False, 'Unknown x'


def standard_rand(alpha, beta, modulo, group, a0, b0):
    debug('a = {}, b = {}'.format(a0, b0))
    subgroups = split_group(group)
    #xi, aj, bj = next_x(((alpha**a0)*(beta**b0)) % modulo, a0, b0,
    #        alpha, beta, modulo, subgroups)
    xi, aj, bj = next_x(1, a0, b0, alpha, beta, modulo, subgroups)
    debug('xi = {}'.format(xi))
    x2i, a2j, b2j = next_x(xi, aj, bj, alpha, beta, modulo, subgroups)
    debug('x2i = {}'.format(x2i))
    for i in range(len(group)):
        yield xi, x2i, aj, bj, a2j, b2j
        xi, aj, bj = next_x(xi, aj, bj, alpha, beta, modulo, subgroups)
        debug('xi+1 = {}'.format(xi))
        x2i, a2j, b2j = next_x(x2i, a2j, b2j, alpha, beta, modulo, subgroups)
        debug('x2i+1 = {}'.format(x2i))
        x2i, a2j, b2j = next_x(x2i, a2j, b2j, alpha, beta, modulo, subgroups)
        debug('x2i+2 = {}'.format(x2i))
        debug('xi = {}, x2i = {}'.format(xi, x2i))


def solve(alpha, beta, modulo, a0=1, b0=1):
    group = gen_subgroup(alpha, modulo)
    debug('Subgroups: {}'.format(group))
    vals = list()
    for a in range(1, len(group)):
        for b in range(2, len(group)):
            vals.append((a, b))
    r = random.SystemRandom()
    r.shuffle(vals)
    while len(vals) > 0:
        for params in standard_rand(alpha, beta, modulo, group, a0, b0):
            debug('testing {}'.format(params))
            xi, x2i, aj, bj, a2j, b2j = params
            if xi == x2i:
                l = (bj - b2j) % len(group)
                r = (a2j - aj) % len(group)
                z = (modular_inverse(l, len(group)) * r) % len(group)
                debug('(bj - b2j)^-1 * (a2j - aj) mod len(subgroup) = {}'.format(z))
                if z == 0:
                    continue
                return z
        a0, b0 = vals.pop()
    assert False, 'Could not solve the equation'


def debug(msg):
    if verbose:
        print(msg)


def print_usage_and_exit(code=0):
    print('USAGE: {} -a <alpha> -b <beta> -m <modulo> [command]'
            .format(sys.argv[0]))
    print('')
    print('Solves for x in the equation: a^x = b mod m')
    print('')
    print('COMMANDS')
    print('solve [a0 b0]\tSolves for x')
    print('subgroup\tGenerates the subgroup given alpha (generator)')
    print('genrand [a0 b0]\tGenerates the `random` x sequence')
    print('test x\t\tTests a^x = b mod m')
    print('')
    print('OPTIONS')
    print('  -a #\t\tAlpha')
    print('  -b #\t\tBeta')
    print('  -m #\t\tModulo')
    print('  -f [NAME]\tRandomize function')
    print('     standard\t(default)')
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

