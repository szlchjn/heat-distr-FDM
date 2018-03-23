"""Contains Environment class
This class creates matrix of nodes as a domain for later 
evaluation by FDM module.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Environment(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.h = 1
        self._input_matrix = []
        self.cols = 0
        self.rows = 0

    @property
    def input_matrix(self):
        return self._input_matrix

    def mesh(self, h):
        """Discretize the domain
        Returns empty matrix of size 'width' by 'height' with nodes spaced
        by given 'h'.
        """
        self.h = h
        # Size of the input matrix
        self.cols = round(self.width / h) + 1
        self.rows = round(self.height / h) + 1
        # Create empty input matrix
        self._input_matrix = [None] * self.rows
        for i in range(self.rows):
            self._input_matrix[i] = [None] * self.cols

    def boundary_conditons(self, up, right, down, left):
        """Set boundary conditions
        Applies Dirichlet conditions to the edges of the domain.
        Parameters can be either constant or a function.
        """
        if len(self._input_matrix) == 0:
            self.mesh(1)

        rows = len(self._input_matrix)
        cols = len(self._input_matrix[0])
        for i in range(rows):
            self._input_matrix[i][-1] = right(i) if callable(right) else right
            self._input_matrix[i][0] = left(i) if callable(left) else left
        for j in range(cols):
            self._input_matrix[0][j] = up(j) if callable(up) else up
            self._input_matrix[-1][j] = down(j) if callable(down) else down
#        self._input_matrix[0][0] = (up + left) / 2
#        self._input_matrix[0][-1] = (up + right) / 2
#        self._input_matrix[-1][0] = (down + left) / 2
#        self._input_matrix[-1][-1] = (down + right) / 2

    def show(self, output):
        # 2D plot
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        ax.set_title('Temperature Map')
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.imshow(np.array(output), interpolation='bilinear')
        plt.set_cmap('hsv')
        plt.colorbar(orientation='vertical')
        plt.show()
        # 3D plot
        z = np.array(output)
        length = z.shape[0]
        width = z.shape[1]
        x, y = np.meshgrid(np.arange(length), np.arange(width))
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_title('Temperature Graph')
        ax.set_xlabel('Height')
        ax.set_ylabel('Width')
        ax.set_zlabel('Temperature')
        ax.plot_surface(x, y, np.transpose(z), cmap=plt.cm.hsv)
        plt.show()
        # Cross sections
        plt.plot(output[round(0.1*self.height/self.h)], label='0.1 width')
        plt.plot(output[round(0.25*self.height/self.h)], label='0.25 width')
        plt.plot(output[round(0.5*self.height/self.h)], label='0.5 width')
        plt.legend(loc='upper center', shadow=True, fontsize='large')
        plt.ylabel('Temperature')
        plt.xlabel('Width')
        plt.title('Lenghtwise cross sections')
        plt.show()