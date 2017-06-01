import matplotlib.pyplot as plt
import math
import sys
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()


def fx(x):
    return x*(x**2) + 2*x + 3

def points_generator(n, x_coords, y_coords):
    for x in xrange(0, n):
        y = math.sqrt(fx(x))
        x_coords.append(x)
        y_coords.append(y)

def main():
    n = int(sys.argv[1])
    x_coords = []
    y_coords = []
    points_generator(n, x_coords, y_coords)
    plt.plot(x_coords, y_coords)
    y_coords = [-1*x for x in y_coords]
    plt.plot(x_coords, y_coords)
    plt.ylabel("y coordinate")
    plt.show()

if __name__ == "__main__":
    main()
