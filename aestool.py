#!/usr/bin/python

from __future__ import print_function
import sys, getopt

inverse = 1
log = 2
subbytes = 3
invsubbytes = 4
shiftrows = 5
invshiftrows = 6
mixcolumns = 7
invmixcolumns = 8
genttables = 9

def main(argv):

    case = 0

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hialsSrRmMtT')
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit(0)
        elif o == '-i':
            case = inverse
        elif o == '-a':
            case = inverse
        elif o == '-l':
            case = log
        elif o == '-s':
            case = subbytes
        elif o == '-S':
            case = invsubbytes
        elif o == '-r':
            case = shiftrows
        elif o == '-R':
            case = invshiftrows
        elif o == '-m':
            case = mixcolumns
        elif o == '-M':
            case = invmixcolumns
        elif o == '-t':
            case = genttables
        elif o == '-T':
            print_usage_and_exit(0)
        else:
            assert False, 'Unhandled option'

    # Inverse/Alog
    if case == inverse:
        if len(args) < 1:
            print_usage_and_exit(1)
        invtable = geninvtable()
        for a in args:
            b = int(a, 16)
            print('inv({:02x}) = {:02x}'.format(b, invtable[b]))

    # Log
    elif case == log:
        if len(args) < 1:
            print_usage_and_exit(1)
        invtable = geninvtable()
        iargs = list()
        for a in args:
            iargs.append(int(a, 16))
        for i in range(len(invtable)):
            if invtable[i] in iargs:
                print('log({:x}) = {:x}'.format(invtable[i], i))

    # SubBytes
    elif case == subbytes:
        if len(args) < 1:
            print_usage_and_exit(1)
        invtable = geninvtable()
        for a in args:
            b = int(a, 16)
            s = sbox(invtable[b])
            print('SBox {:02x}: {:02x}'.format(b, s))

    # InvSubBytes
    elif case == invsubbytes:
        if len(args) < 1:
            print_usage_and_exit(1)
        invtable = geninvtable()
        for a in args:
            s = int(a, 16)
            b = invtable[invsbox(s)]
            print('InvSBox {:02x}: {:02x}'.format(s, b))

    # ShiftRows
    elif case == shiftrows:
        if len(args) != 16:
            print_usage_and_exit(1)
        b = []
        b.append(int(args[0], 16))
        b.append(int(args[1], 16))
        b.append(int(args[2], 16))
        b.append(int(args[3], 16))
        b.append(int(args[4], 16))
        b.append(int(args[5], 16))
        b.append(int(args[6], 16))
        b.append(int(args[7], 16))
        b.append(int(args[8], 16))
        b.append(int(args[9], 16))
        b.append(int(args[10], 16))
        b.append(int(args[11], 16))
        b.append(int(args[12], 16))
        b.append(int(args[13], 16))
        b.append(int(args[14], 16))
        b.append(int(args[15], 16))
        bshift = b[0:4] + rotla(b[4:8], 1) + rotla(b[8:12], 2) + rotla(b[12:], 3)
        print(('{:02x} '*4).format(*bshift[0:4]))
        print(('{:02x} '*4).format(*bshift[4:8]))
        print(('{:02x} '*4).format(*bshift[8:12]))
        print(('{:02x} '*4).format(*bshift[12:]))

    # InvShiftRows
    elif case == invshiftrows:
        if len(args) < 16:
            print_usage_and_exit(1)
        b = []
        b.append(int(args[0], 16))
        b.append(int(args[1], 16))
        b.append(int(args[2], 16))
        b.append(int(args[3], 16))
        b.append(int(args[4], 16))
        b.append(int(args[5], 16))
        b.append(int(args[6], 16))
        b.append(int(args[7], 16))
        b.append(int(args[8], 16))
        b.append(int(args[9], 16))
        b.append(int(args[10], 16))
        b.append(int(args[11], 16))
        b.append(int(args[12], 16))
        b.append(int(args[13], 16))
        b.append(int(args[14], 16))
        b.append(int(args[15], 16))
        bshift = b[0:4] + rotla(b[4:8], 3) + rotla(b[8:12], 2) + rotla(b[12:], 1)
        print(('{:02x} '*4).format(*bshift[0:4]))
        print(('{:02x} '*4).format(*bshift[4:8]))
        print(('{:02x} '*4).format(*bshift[8:12]))
        print(('{:02x} '*4).format(*bshift[12:]))

    # MixColumns
    elif case == mixcolumns:
        if len(args) < 4:
            print_usage_and_exit(1)

        A = []
        A.append(int(args[0], 16))
        A.append(int(args[1], 16))
        A.append(int(args[2], 16))
        A.append(int(args[3], 16))
        print('A =' + (' {:02x}'*4).format(*A))

        B = [3, 1, 1, 2]

        C = []
        C.append(mixcolumns(A, rotla(B, 3)))
        C.append(mixcolumns(A, rotla(B, 2)))
        C.append(mixcolumns(A, rotla(B, 1)))
        C.append(mixcolumns(A, B))
        print('C =' + (' {:02x}'*4).format(*C))

    # InvMixColumns
    elif case == invmixcolumns:
        if len(args) < 4:
            print_usage_and_exit(1)

        C = []
        C.append(int(args[0], 16))
        C.append(int(args[1], 16))
        C.append(int(args[2], 16))
        C.append(int(args[3], 16))
        print('C =' + (' {:02x}'*4).format(*C))

        S = [0xb, 0xd, 0x9, 0xe]

        A = []
        A.append(invmixcolumns(C, rotla(S, 3)))
        A.append(invmixcolumns(C, rotla(S, 2)))
        A.append(invmixcolumns(C, rotla(S, 1)))
        A.append(invmixcolumns(C, S))
        print('A =' + (' {:02x}'*4).format(*A))

    # GenTTables
    elif case == genttables:
        T0 = genttables([2, 1, 1, 3])
        T1 = genttables([3, 2, 1, 1])
        T2 = genttables([1, 3, 2, 1])
        T3 = genttables([1, 1, 3, 2])
        if len(args) > 0:
            for a in args:
                v = int(a, 16)
                print(('{:02x}:' + ' {:08x}'*4).format(v, T0[v], T1[v], T2[v], T3[v]))
        else:
            for i in range(0, 0x100):
                print(('{:02x}:' + ' {:08x}'*4).format(i, T0[i], T1[i], T2[i], T3[i]))


#####################################################################
# Helping Functions
#####################################################################

def rotl8(x, shift):
    return ((x << shift) | (x >> (8 - shift))) & 0xFF


def rotla(l, shift):
    return l[shift:] + l[0:shift]


def xtime(a):
    b = a << 1
    if a >= 0x80:
        b = (b & 0xFF) ^ 0x1B
    return b


def geninvtable():
    Sbox = [0x00]
    for i in range(1, 0x100):
        Sbox.append(0)
    p, q = 1, 1
    while True:
        p = p ^ xtime(p)
        q ^= q << 1
        q ^= q << 2
        q ^= q << 4
        q &= 0xFF
        if q >= 0x80:
            q ^= 0x09
        Sbox[p] = q
        if (p == 1):
            break
    return Sbox


#####################################################################
# AES Functions
#####################################################################

def sbox(b):
    return b ^ rotl8(b, 1) ^ rotl8(b, 2) ^ rotl8(b, 3) ^ rotl8(b, 4) ^ 0x63


def invsbox(s):
    return rotl8(s, 1) ^ rotl8(s, 3) ^ rotl8(s, 6) ^ 0x5


def mixcolumns(A, B):
    ret = []
    for i in range(0, 4):
        t0 = A[i]
        t1 = xtime(t0)
        if B[i] == 1:
            ret.append(t0)
        elif B[i] == 2:
            ret.append(t1)
        elif B[i] == 3:
            ret.append(t1 ^ t0)
    return ret[0] ^ ret[1] ^ ret[2] ^ ret[3]


def invmixcolumns(A, B):
    ret = []
    for i in range(0, 4):
        t0 = A[i]
        t1 = xtime(t0)
        t2 = xtime(t1)
        t3 = xtime(t2)
        if B[i] == 0x9:
            ret.append(t3 ^ t0)
        elif B[i] == 0xb:
            ret.append(t3 ^ t1 ^ t0)
        elif B[i] == 0xd:
            ret.append(t3 ^ t2 ^ t0)
        elif B[i] == 0xe:
            ret.append(t3 ^ t2 ^ t1)
    return ret[0] ^ ret[1] ^ ret[2] ^ ret[3]


def genttables(B):
    ret = []
    invtable = geninvtable()
    for i in range(0, 0x100):
        s = sbox(invtable[i])
        a = [s, s, s, s]
        c = []
        for j in range(0, 4):
            t0 = s 
            t1 = xtime(t0)
            if B[j] == 1:
                c.append(t0)
            elif B[j] == 2:
                c.append(t1)
            elif B[j] == 3:
                c.append(t1 ^ t0)
        ret.append((c[0] << 24) | (c[1] << 16) | (c[2] << 8) | c[3])
    return ret


#####################################################################
# Main Program Stuff
#####################################################################

def print_usage_and_exit(exitcode):
    print('USAGE: {} [OPTIONS]'.format(sys.argv[0]))
    print('')
    print('All numerical values are read as base16')
    print('')
    print('  -h\t\t\tPrint this message')
    print('  -i b1, ...\t\tInverse')
    print('  -a b1, ...\t\tAlog')
    print('  -l b1, ...\t\tLog')
    print('  -s b1, ...\t\tSubBytes')
    print('  -S s1, ...\t\tInvSubBytes')
    print('  -r b1...b16\t\tShiftRows')
    print('  -R b1...b16\t\tInvShiftRows')
    print('  -m a1 a2 a3 a4\tMixColumns')
    print('  -M c1 c2 c3 c4\tInvMixColumns')
    print('  -t\t\t\tGenerate T-Table')
    sys.exit(exitcode)


if __name__ == '__main__':
    main(sys.argv[1:])

