#!/usr/bin/python3

import sys, getopt

def main(argv):

    p = None
    a = None
    b = None
    c = None
    verbose = False
    users = list()

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hvp:a:b:c:')
    except getopt.GetoptError as err:
        print(err)
        return

    for op, arg in oplist:
        if op == '-h':
            print_usage_and_exit()
        elif op == '-v':
            verbose = True
        elif op == '-p':
            p = int(arg)
        elif op == '-a':
            a = int(arg)
        elif op == '-b':
            b = int(arg)
        elif op == '-c':
            c = int(arg)
        else:
            assert False, 'Unhandled option'

    if not p or not a or not b or not c or len(args) == 0:
        print_usage_and_exit(1)
    for arg in args:
        users.append(int(arg))
    keys = genKeys(p, a, b, c, users, verbose)
    print(keys)
    if not testKeys(p, keys, verbose):
        print('Failed')
    print('Success')


def testKeys(p, keys, verbose):
    for i in range(len(keys)):
        gu, fgu = keys[i]
        for j in range(i + 1, len(keys)):
            gv, fgv = keys[j]
            kuv = (fgu[0] + (fgu[1] * gv)) % p
            debug('{} + {}*{} = {}'.format(fgu[0], fgu[1], gv, kuv), verbose)
            kvu = (fgv[0] + (fgv[1] * gu)) % p
            debug('{} + {}*{} = {}'.format(fgv[0], fgv[1], gu, kvu), verbose)
            if kuv != kvu:
                return False
    return True


def genKeys(p, a, b, c, users, verbose=False):
    keys = list()
    for u in users:
        priv = ((a + (b * u)) % p, (b + (c * u)) % p)
        debug('{0} + {1}*{2} + ({1} + {3}*{2})x mod {4} = {5} + {6}x'
                .format(a, b, u, c, p, priv[0], priv[1]), verbose)
        keys.append((u, priv))
    return keys


def debug(msg, verbose=False):
    if verbose:
        print(msg)


def print_usage_and_exit(code=0):
    print('Usage: {} -p prime -a a -b b -c c "user1 user2..."'.format(sys.argv[0]))
    sys.exit(code)


if __name__ == '__main__':
    main(sys.argv[1:])

