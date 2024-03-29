
# This file was *autogenerated* from the file ./berlekamp-massey.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_77 = Integer(77)#!/usr/bin/sage

import sys

def main(args):

    # Get command line arguments
    sn = list()
    if len(args) == _sage_const_1 :
        sn = [int(x) for x in args[_sage_const_0 ]]
    elif len(args) == _sage_const_2 :
        pn = [int(x) for x in args[_sage_const_0 ]]
        cn = [int(x) for x in args[_sage_const_1 ]]
        sn = [(x + y) % _sage_const_2  for x, y in zip(pn, cn)]
    else:
        print_usage_and_exit(_sage_const_1 )

    # Run Berlekamp-Massey
    L, C = berlekamp_massey(sn)

    print('LFSR Size: {}'.format(L))
    print('LFSR     : {}'.format(C))


def berlekamp_massey(sn):
    verbose = True
    n = len(sn)
    T = None
    C = GF(_sage_const_2 )['D']; (D,) = C._first_ngens(1)
    B = GF(_sage_const_2 )['D']; (D,) = B._first_ngens(1)
    L, m, N = _sage_const_0 , -_sage_const_1 , _sage_const_0 
    C = _sage_const_0 *D + _sage_const_1 
    B = _sage_const_0 *D + _sage_const_1 
    debug('{:2s}|{:2s}|{:20s}|{:20s}|{:2s}|{:2s}|{:20s}|{:2s}'
            .format('Sn', 'd', 'T(D)', 'C(D)', 'L', 'm', 'B(D)', 'N'), verbose)
    debug('-'*_sage_const_77 , verbose)
    while N < n:
        d = (sn[N] + sum([
                x * y for x, y in zip(C.list()[_sage_const_1 :L+_sage_const_1 ], ((sn[:N+_sage_const_1 ])[::-_sage_const_1 ])[_sage_const_1 :L+_sage_const_1 ])
            ])) % _sage_const_2 
        if d == _sage_const_1 :
            T, C = C, C + (B * D**(N-m))
            if L <= int(N/_sage_const_2 ):
                L, m, B = N + _sage_const_1  - L, N, T
        debug('{:2s}|{:2s}|{:20s}|{:20s}|{:2s}|{:2s}|{:20s}|{:2s}'
                .format(repr(sn[N]), repr(d), repr(T), repr(C), repr(L),
                    repr(m), repr(B), repr(N)), verbose)
        N = N + _sage_const_1 
    return L, C


def debug(msg, verbose=False):
    if verbose:
        print(msg)


def print_usage_and_exit(code=_sage_const_0 ):
    print('USAGE: {} <plaintext> <ciphertext>'.format(sys.argv[_sage_const_0 ]))
    print('       {} <lfsr-key>'.format(sys.argv[_sage_const_0 ]))
    print('')
    print('NOTE: Arguments expected in binary format')
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[_sage_const_1 :])


