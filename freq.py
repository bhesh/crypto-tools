#!/usr/bin/python3

from __future__ import print_function
import sys, getopt

def main(argv):

    # Set defaults
    f = sys.stdin
    count = 1

    # Parse options
    try:
        oplist, args = getopt.getopt(argv, 'hc:')
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)

    for o, a in oplist:
        if o == '-h':
            print_usage_and_exit(0)
        elif o == '-c':
            count = int(a)
        else:
            assert False, 'Unhandled option'

    # If a file was specified...
    if len(args) > 0:
        f = open(args[0], 'r')

    # do stuff
    total, res = count_freq(count, f)
    ic = {c: sum(x*(x-1) for x in res[c].values())/(total*(total-1)) for c in range(count)}
    for col in range(count):
        print("--------------------------------------------------------------")
        print("Column {}".format(col))
        print("--------------------------------------------------------------")
        for c in range(ord('A'), ord('Z') + 1):
            if res[col][chr(c)] > 0:
                print("{}: {}".format(chr(c), res[col][chr(c)]))
        print("--------------------------------------------------------------")
        print("IC: {:0.4f}".format(ic[col]))
        print("MR: {:0.4f}".format(ic[col]-(1/26)))
        print("--------------------------------------------------------------")
        print('')
    print("--------------------------------------------------------------")
    print("SUMMARY")
    print("--------------------------------------------------------------")
    print("Average IC: {:0.4f}".format(sum(x for x in ic.values())/count))
    print("Average MR: {:0.4f}".format((sum(x for x in ic.values())/count)-(1/26)))
    print("--------------------------------------------------------------")

    if len(args) > 0:
        f.close()


def count_freq(c, f):
    "Counts the number of times each character pops up in a column"
    res = []
    for i in range(c):
        res.append({chr(c): 0 for c in range(ord('A'), ord('Z') + 1)})
    i = 0
    for line in f:
        for c in line.upper():
            if ord(c) >= ord('A') and ord(c) <= ord('Z'):
                res[i % len(res)][c] += 1
                i += 1
    return i, res


def print_usage_and_exit(exitcode):
    print('USAGE: {} [OPTIONS] [file]'.format(sys.argv[0]))
    print('')
    print('If file is not specified, input is taken from stdin.')
    print('')
    print('  -h\t\tPrint this message')
    print('  -c ARG\tColumns')
    sys.exit(exitcode)


if __name__ == '__main__':
    main(sys.argv[1:])
