import matplotlib.pyplot as plt
import math
import sys

p = 487

def lx():
    retx = []
    rety = []
    for x in xrange(p):
        retx.append(x)
        y = (4*x + 83) % p
        rety.append(y)

    return retx, rety

def fx(x):
    return x*x*x - x + 1

def scan(s, n):
    ret = []
    for y in xrange(n):
        if y*y % n == s:
            ret.append(y)

    return ret 

def points_generator(n, x_coords, y_coords):
    dx = 1
    x = 0
    while x <= n:
        s = fx(x)
        if s >= 0:
            s = s % n
            ret = scan(s, n)
            for y in ret:
                print x, y 
                x_coords.append(x)
                y_coords.append(y)

        x = x + dx

def main():
    n = p
    x_coords = []
    y_coords = []
    points_generator(n, x_coords, y_coords)
   
    if len(x_coords) > 0:
        plt.scatter(x_coords, y_coords, color='blue', s=20)
        #plt.plot(x_coords, y_coords)

    #x, y = lx()
    #plt.scatter(x, y, color='red', s=40, facecolors='none', edgecolors='r')
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

if __name__ == "__main__":
    main()
