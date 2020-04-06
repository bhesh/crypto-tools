#!/usr/bin/sage

import sys

def main(args):

    # Get command line arguments
    sn = list()
    if len(args) == 1:
        sn = [int(x) for x in args[0]]
    elif len(args) == 2:
        pn = [int(x) for x in args[0]]
        cn = [int(x) for x in args[1]]
        sn = [(x + y) % 2 for x, y in zip(pn, cn)]
    else:
        print_usage_and_exit(1)

    # Run Berlekamp-Massey
    L, C = berlekamp_massey(sn)

    print('LFSR Size: {}'.format(L))
    print('LFSR     : {}'.format(C))


def berlekamp_massey(sn):
    verbose = True
    n = len(sn)
    T = None
    C.<D> = GF(2)[]
    B.<D> = GF(2)[]
    L, m, N = 0, -1, 0
    C = 0*D + 1
    B = 0*D + 1
    debug('{:2s}|{:2s}|{:20s}|{:20s}|{:2s}|{:2s}|{:20s}|{:2s}'
            .format('Sn', 'd', 'T(D)', 'C(D)', 'L', 'm', 'B(D)', 'N'), verbose)
    debug('-'*77, verbose)
    while N < n:
        d = (sn[N] + sum([
                x * y for x, y in zip(C.list()[1:L+1], ((sn[:N+1])[::-1])[1:L+1])
            ])) % 2
        if d == 1:
            T, C = C, C + (B * D^(N-m))
            if L <= int(N/2):
                L, m, B = N + 1 - L, N, T
        debug('{:2s}|{:2s}|{:20s}|{:20s}|{:2s}|{:2s}|{:20s}|{:2s}'
                .format(repr(sn[N]), repr(d), repr(T), repr(C), repr(L),
                    repr(m), repr(B), repr(N)), verbose)
        N = N + 1
    return L, C


def debug(msg, verbose=False):
    if verbose:
        print(msg)


def print_usage_and_exit(code=0):
    print('USAGE: {} <plaintext> <ciphertext>'.format(sys.argv[0]))
    print('       {} <lfsr-key>'.format(sys.argv[0]))
    print('')
    print('NOTE: Arguments expected in binary format')
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

