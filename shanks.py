#!/usr/bin/python3

import sys, getopt, math

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
        assert alpha and beta and modulo, 'Invalid alpha/beta/modulo'
        x = solve(alpha, beta, modulo)
        print(x)
    elif len(args) == 1:
        command = args[0]

        if command == 'solve':
            assert alpha and beta and modulo, 'Invalid alpha/beta/modulo'
            x = solve(alpha, beta, modulo)
            print(x)
        elif command == 'itable':
            assert alpha and beta and modulo, 'Invalid alpha/beta/modulo'
            m = calc_m(modulo)
            itable = calc_itable(alpha, beta, m, modulo)
            for i in range(m):
                print('{}\t\t{}'.format(i, itable[i]))
        elif command == 'jtable':
            assert alpha and modulo, 'Invalid alpha/modulo'
            m = calc_m(modulo)
            jtable = calc_jtable(alpha, m, modulo)
            for j in sorted(jtable.keys()):
                print('{}\t\t{}'.format(j, jtable[j]))
        elif command == 'mu':
            assert alpha and modulo, 'Invalid alpha/modulo'
            m = calc_m(modulo)
            print(modular_inverse((alpha**m) % modulo, modulo))
        elif command == 'ceilsqrt':
            assert modulo, 'Invalid modulo'
            print(calc_m(modulo))
        else:
            print('Invalid command `{}`'.format(command))
    else:
        print_usage_and_exit(1)


def modular_inverse(a, m):
    return (a**(m - 2)) % m


def calc_m(modulo):
    res = int(math.sqrt(modulo))
    while res * res < modulo:
        res = res + 1
    return res


def calc_itable(alpha, beta, m, modulo):
    mu = modular_inverse((alpha**m) % modulo, modulo)
    itable = {0: beta}
    res = beta
    for i in range(1, m):
        res = (res * mu) % modulo
        itable[i] = res
    return itable


def calc_jtable(alpha, m, modulo):
    jtable = {1: 0}
    res = 1
    for i in range(1, m):
        res = (res * alpha) % modulo
        jtable[res] = i
    return jtable


def solve(alpha, beta, modulo):
    m = calc_m(modulo)
    jtable = calc_jtable(alpha, m, modulo)
    itable = calc_itable(alpha, beta, m, modulo)
    i, j = -1, -1
    for i in range(m):
        if itable[i] in jtable:
            i, j = i, jtable[itable[i]]
            break
    assert (i >= 0 and j >= 0), 'No (i, j) pair found'
    return ((i * m) + j) % modulo


def print_usage_and_exit(code=0):
    print('USAGE: {} -a <alpha> -b <beta> -m <modulo> [command]'
            .format(sys.argv[0]))
    print('')
    print('Solves for x in the equation: a^x = b mod m')
    print('')
    print('COMMANDS')
    print('solve\t\tSolves for x')
    print('itable\t\tBuilds and outputs the i-table')
    print('jtable\t\tBuilds and outputs the j-table')
    print('mu\t\tCalculates mu')
    print('ceilsqrt\tCalculates optimal m')
    print('')
    print('OPTIONS')
    print('  -a #\tAlpha')
    print('  -b #\tBeta')
    print('  -m #\tModulo')
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

