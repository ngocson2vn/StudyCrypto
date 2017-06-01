import matplotlib.pyplot as plt
import math
import sys
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()


def fx(x):
    return x*x*x - 3*x + 2

def points_generator(n, x_coords, y_coords):
    dx = 0.0001
    x = -5
    while x <= n:
        s = fx(x)
        if s >=0:
            y = math.sqrt(s)
            x_coords.append(x)
            y_coords.append(y)
        if x <= 2:
            x = x + dx
        else:
            x = x + 1

def main():
    n = int(sys.argv[1])
    x_coords = []
    y_coords = []
    points_generator(n, x_coords, y_coords)
    plt.plot(x_coords, y_coords)
    y_coords = [-1*e for e in y_coords]
    plt.plot(x_coords, y_coords)
    plt.ylabel("y coordinate")
    plt.show()

if __name__ == "__main__":
    main()
