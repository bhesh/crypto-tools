#!/usr/bin/sage

import sys, getopt

def main(argv):

    modulo = None
    alpha = None
    beta = None
    verbose = False
    factorbase = list()
    
    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hvm:a:b:')
    except getopt.GetoptError as err:
        print(err)
        return

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit(0)
        elif o == '-v':
            verbose = True
        elif o == '-m':
            modulo = int(a)
        elif o == '-a':
            alpha = int(a)
        elif o == '-b':
            beta = int(a)
        else:
            assert False, 'Unhandled option'

    # Parse out command and arguments
    if not modulo or not alpha or not beta or len(args) == 0:
        print_usage_and_exit(1)
    for a in args:
        factorbase.append(int(a))
    val = indexcalculus(modulo, alpha, beta, factorbase, verbose)
    print(val)


def is_smooth(factors, factorbase):
    if len(factors) == 0:
        return False
    for f in factors:
        if f[0] not in factorbase:
            return False
    return True


def is_linear_independent(vector, matrix):
    tM = Matrix(matrix + [vector])
    eM = tM.echelon_form()
    for r in eM.rows():
        is_zero = True
        for v in r:
            if int(v) != 0:
                is_zero = False
                break
        if is_zero:
            return False
    return True


def calc_relations(m, a, factorbase, verbose=False):

    relations = list()

    # Populate matrix
    k = 1
    while len(relations) <= len(factorbase) and k < m:
        gk = int(mod(a^k, m))
        factors = factor(gk)
        if is_smooth(list(factors), factorbase):
            vector = [0 for f in factorbase]
            for f in list(factors):
                vector[factorbase.index(f[0])] = f[1]
            vector.append(k)
            if is_linear_independent(vector, relations):
                debug("{}\t{}\t{}".format(k, gk, factors), verbose)
                relations.append(vector)
        k += 1
    return relations


def indexcalculus(m, a, b, factorbase, verbose=False):
    relations = calc_relations(m, a, factorbase, verbose)
    if len(relations) != len(factorbase) + 1:
        print("Failed")
        return None
    M = Matrix(relations)
    debug("Matrix", verbose)
    debug(M, verbose)
    debug("Echelon Form", verbose)
    eM = M.echelon_form()
    debug(eM, verbose)
    for s in xrange(1, m):
        gsh = int(mod(a^s * b, m))
        factors = factor(gsh)
        debug("{}\t{}\t{}".format(s, gsh, factors), verbose)
        if is_smooth(list(factors), factorbase):
            fs = list(factors)
            val = 0
            for f in factors:
                dl = eM.rows()[factorbase.index(f[0])][-1]
                val = int(mod(val + (f[1] * dl), m))
            return int(mod(val - s, m))
    print("Failed")
    return None


def debug(msg, verbose=False):
    if verbose:
        print(msg)


def print_usage_and_exit(code=0):
    print('USAGE: {} -m modulo -a alpha -b beta factor1 factor2...'.format(sys.argv[0]))
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

