"""Contains simple console UI and times execution of the algorithm.
Specify domain, heat transfer coefficients and grid size.
"""
from environment import Environment
from fdm import FiniteDifferenceMethod
import numpy as np
from time import time


def main():
    np.set_printoptions(threshold=100)

    width = float(input('Width: '))
    height = float(input('Height: '))
    kx = input('k1(x): ')
    ky = input('k2(y): ')

    input1 = Environment(width, height)

    h = float(input('Grid size: '))
    input1.mesh(h)

    bound = lambda x: round(400 * np.sin((np.pi * x) / (height / h)), 5)
    input1.boundary_conditons(0, bound, 0, bound)

    fdm1 = FiniteDifferenceMethod(input1, lambda x: eval(kx), lambda y: eval(ky))

    start = time()
    output1 = fdm1.solve()
    end = time()
    elapsed = round(end-start, 3)

    input1.show(output1)
    print('\nFinished in: {0} seconds'.format(elapsed))


if __name__ == '__main__':
    main()
