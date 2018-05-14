"""Contains simple console API and times execution of the algorithm.
Specify domain, heat transfer coefficients and grid size.
"""
from environment import Environment
from fdm import FiniteDifferenceMethod
import numpy as np
from time import time


def main():
    np.set_printoptions(threshold=100)

    width = 1.5 #float(input('Width: '))
    height = 1 #float(input('Height: '))
    k1 = '1.245*np.log2(x)+1 if x!=0 else 1' #input('k1(x): ')
    k2 = '1' #input('k2(y): ')

    input1 = Environment(width, height)

    h = 0.025 #float(input('Grid size: '))
    input1.mesh(h)

    bound_Y = lambda y: round(500 * np.sin((np.pi * y) / (height / h)), 5)
    bound_X = lambda x: round(500 * np.sin((np.pi * x) / (width / h)), 5)
    input1.boundary_conditons(left=bound_Y)
                                                                                             #MAP           #PLOT
    fdm1 = FiniteDifferenceMethod(input1, lambda x: eval(k1), lambda y: eval(k2))

    start = time()
    output1 = fdm1.solve()
    end = time()
    elapsed = round(end-start, 3)

    print('\nFinished in: {0} seconds'.format(elapsed))
    input1.show(output1)


if __name__ == '__main__':
    main()
