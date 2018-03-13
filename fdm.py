"""Contains finite difference algorithm
This class applies finite difference method to previously discretized by
Environment class domain.
Material can be nonhomogeneous along x-axis but must heat transfer coefficient
must be constant along y-axis.
"""
import numpy as np
from copy import deepcopy

class FiniteDifferenceMethod(object):
    def __init__(self, other, kx, ky):
        """Initialize instance of FDM
        'other' is instance of Environment class
        'kx' and 'ky' are heat transfer coefficient in directions perpendicular
        to both axes of the domain respectively.
        """
        self.cols = other.cols
        self.rows = other.rows
        self.kx = kx
        self.ky = ky

        self.input_matrix = deepcopy(other.input_matrix)
        self.unknown_vector = []
        self.neighbours = {}
        self.boundaries = {}
        self.coefficient_matrix = []
        self.boundary_vector = []
        self.result_vector = []
        self.rv_list = []

    def create_uv(self):
        """Count unknown nodes and create unknown vector"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.input_matrix[i][j] is None:
                    self.unknown_vector.append((i, j))
                    self.input_matrix[i][j] = self.unknown_vector[-1]

    def count_neighbours(self):
        """Count neighbours and sum the boundary values for each node"""
        self.neighbours = {node:[] for node in self.unknown_vector}
        self.boundaries = {node:0 for node in self.unknown_vector}

        for i in range(self.rows):
            for j in range(self.cols):

                # Upper node (i-1, j)
                if isinstance(self.input_matrix[i][j], tuple) and \
                             isinstance(self.input_matrix[i-1][j], tuple):
                    self.neighbours[self.input_matrix[i][j]].append(('U',) \
                                   + self.input_matrix[i-1][j])
                elif isinstance(self.input_matrix[i][j], tuple):
                    self.boundaries[self.input_matrix[i][j]] \
                                   += self.input_matrix[i-1][j] * self.ky(1)

                # Right node (i, j+1)
                if isinstance(self.input_matrix[i][j], tuple) and \
                             isinstance(self.input_matrix[i][j+1], tuple):
                    self.neighbours[self.input_matrix[i][j]].append(('R',) \
                                   + self.input_matrix[i][j+1])
                elif isinstance(self.input_matrix[i][j], tuple):
                    self.boundaries[self.input_matrix[i][j]] += \
                                   self.input_matrix[i][j+1] \
                                   * (self.kx(j) + ((self.kx(j + 1) \
                                   - self.kx(j - 1)) / 4))

                # Lower node (i+1, j)
                if isinstance(self.input_matrix[i][j], tuple) and \
                             isinstance(self.input_matrix[i+1][j], tuple):
                    self.neighbours[self.input_matrix[i][j]].append(('D',) \
                                   + self.input_matrix[i+1][j])
                elif isinstance(self.input_matrix[i][j], tuple):
                    self.boundaries[self.input_matrix[i][j]] \
                                   += self.input_matrix[i+1][j] * self.ky(1)

                # Left node (i, j-1)
                if isinstance(self.input_matrix[i][j], tuple) and \
                             isinstance(self.input_matrix[i][j-1], tuple):
                    self.neighbours[self.input_matrix[i][j]].append(('L',) \
                                   + self.input_matrix[i][j-1])
                elif isinstance(self.input_matrix[i][j], tuple):
                    self.boundaries[self.input_matrix[i][j]] += \
                                   self.input_matrix[i][j-1] \
                                   * (self.kx(j) + ((self.kx(j - 1) \
                                   - self.kx(j + 1)) / 4))

    def create_cm(self):
        """Create and populate coefficient matrix"""
        d = [float(-2*self.kx(node[1])-2*self.ky(node[0])) for node in
             self.unknown_vector]
        self.coefficient_matrix = np.diag(d, 0)

        row = -1
        for node in self.neighbours:  # Iterate over list of nodes
            row += 1
            for neighbour in self.neighbours[node]:  # Iterate over neighbours
                column = self.unknown_vector.index(neighbour[1:])
                if neighbour[0] == 'U':
                    self.coefficient_matrix[row][column] = self.ky(1)
                elif neighbour[0] == 'R':
                    self.coefficient_matrix[row][column] = self.kx(int(node[1])) \
                                              + ((self.kx(int(node[1]) + 1) \
                                              - self.kx(int(node[1]) - 1)) / 4)
                elif neighbour[0] == 'D':
                    self.coefficient_matrix[row][column] = self.ky(1)
                elif neighbour[0] == 'L':
                    self.coefficient_matrix[row][column] = self.kx(int(node[1])) \
                                              + ((self.kx(int(node[1]) - 1) \
                                              - self.kx(int(node[1]) + 1)) / 4)

    def create_bv(self):
        # Create boundary vector
        bound_vals = [-value for value in self.boundaries.values()]
        self.boundary_vector = np.array(bound_vals).reshape((len(bound_vals), 1))

    def create_sm(self):
        solved_matrix = deepcopy(self.input_matrix)
        for i in range(self.rows):
            for j in range(self.cols):
                if isinstance(self.input_matrix[i][j], tuple):
                    node = self.unknown_vector.index(solved_matrix[i][j])
                    solved_matrix[i][j] = self.rv_list[node]
        return solved_matrix

    def symmetry(self):
        zeros = self.coefficient_matrix - np.transpose(self.coefficient_matrix)
        return not np.any(zeros)

    def solve(self):
        self.create_uv()
        self.count_neighbours()
        self.create_cm()
        self.create_bv()
        self.result_vector = np.linalg.solve(self.coefficient_matrix,
                                             self.boundary_vector)
        self.rv_list = [round(item, 2) for sublist in
                        self.result_vector.tolist() for item in sublist]
        return self.create_sm()