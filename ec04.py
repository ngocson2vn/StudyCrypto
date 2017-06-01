import math
import sys


def fx(x):
    return x*x*x + 2*x + 3

def main():
    x = int(sys.argv[1])
    ret = fx(x)
    print "fx = %d" % ret
    print "fx mod 263 = %d" % (ret % 263)
    L = -30420
    for i in xrange(L, L + 10):
        ys = ret + i * 263
        if ys > 0:
            print math.sqrt(ys)

if __name__ == "__main__":
    main()
