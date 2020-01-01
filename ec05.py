import matplotlib.pyplot as plt
import math
import sys


def fx(x):
    return x*x*x - x + 1

def scan(s, n):
    ret = []
    for y in range(n + 1):
        if y*y % n == s:
            ret.append(y)

    return ret
        

def points_generator(n, x_coords, y_coords):
    dx = 1
    x = 0
    while x < n:
        s = fx(x)
        if s >= 0:
            s = s % n
            ret = scan(s, n)
            for y in ret:
                print(x, y)
                x_coords.append(x)
                y_coords.append(y)

        x = x + dx

def main():
    n = int(sys.argv[1])
    x_coords = []
    y_coords = []
    points_generator(n, x_coords, y_coords)
   
    if len(x_coords) > 0:
        #plt.plot(x_coords, y_coords)
        plt.scatter(x_coords, y_coords, color='blue', s=10)
        #y_coords = [-1*e for e in y_coords]
        #plt.plot(x_coords, y_coords)
        #plt.scatter(x_coords, y_coords, color='red', s=10)
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

if __name__ == "__main__":
    main()
