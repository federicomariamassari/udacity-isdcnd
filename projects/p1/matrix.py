# File:         matrix.py
# Author:       Federico Maria Massari
# Date:         11/16/2022
# Description:  This Matrix class implements common matrix manipulation operations as a basic requirement to
#               handle self-driving cars. Basic optimization techniques such as pre-allocation of memory resources
#               for matrices were applied to ease comparison with the C++ code in Project 1.B.

from math import pow
import numbers


def zeros(height, width):
    """Creates a matrix of zeros.

    Example:

    > zeroes = zeros(2, 3)
    > print(zeroes)
      0.0  0.0  0.0
      0.0  0.0  0.0
    """
    g = [[0. for _ in range(width)] for __ in range(height)]
    return Matrix(g)


def identity(n):
    """Creates an (n * n) identity matrix.

    Example:

    > eye = identity(2)
    > print(eye)
      1.0  0.0
      0.0  1.0
    """
    I = zeros(n, n)
    for i in range(n):
        I.g[i][i] = 1.

    return I


class Matrix:

    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    def determinant(self) -> float:
        """Calculates the determinant of matrices up to 3x3.

           References: https://mathworld.wolfram.com/Determinant.html (minors, cofactors, submatrices).
        """
        def get_submatrix(matrix: list, col: int) -> Matrix:
            """Returns submatrix formed by deleting first row, j-th column
               (col) of input matrix.
            """
            submatrix = []
            for i in range(1, len(matrix)):
                row = [matrix[i][j] for j in range(len(matrix[0])) if j != col]
                submatrix.append(row)

            return Matrix(submatrix)

        def get_minor(submatrix: Matrix) -> float:
            """Returns the minor (i.e., determinant) of an input submatrix."""
            a, b, c, d = submatrix[0][0], submatrix[0][1], submatrix[1][0], submatrix[1][1]
            return (a * d) - (b * c)

        if not self.is_square():
            raise ValueError('Cannot calculate determinant of non-square matrix.')

        if self.h > 3:
            raise NotImplementedError('Calculating determinant not implemented for matrices larger than 3x3.')

        if self.h == 1:
            return self.g[0][0]

        elif self.h == 2:
            return get_minor(self.g)

        else:
            det = 0

            # In matrix algebra rows and columns start from index 1, which is convenient to get sign (-1)**(i+j)
            for j in range(1, self.w+1):
                submatrix = get_submatrix(self.g, (j-1))

                # Always use first row to compute matrix cofactor; i=1 used to calculate sign (-1)**(i+j)
                det += pow(-1, 1+j) * self.g[0][j-1] * get_minor(submatrix)

            return det

    def trace(self) -> float:
        """Calculates the trace of a matrix (sum of diagonal entries).

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix.trace()
          5
        """
        if not self.is_square():
            raise ValueError('Cannot calculate the trace of a non-square matrix.')

        return sum([self[i][i] for i in range(self.h)])

    def inverse(self):
        """Calculates the inverse of matrices up to 3x3.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > inverse  = my_matrix.inverse()
        > print(inverse)
          -2.0  1.0
          1.5  -0.5

        References: https://en.wikipedia.org/wiki/Invertible_matrix (Cayley-Hamilton formulae).
        """
        if not self.is_square():
            raise ValueError('Non-square Matrix does not have an inverse.')

        if self.h > 3:
            raise NotImplementedError('Inversion is not implemented for matrices larger than 3x3.')

        det = self.determinant()
        if det == 0:
            raise ValueError('Inverse does not exist for singular matrices (determinant == 0).')

        if self.h == 1:
            return Matrix([[pow(det, -1)]])

        elif self.h == 2:
            # Cayley-Hamilton decomposition of a 2*2 matrix
            return pow(det, -1) * (self.trace() * identity(self.h) - self)

        else:
            # Cayley-Hamilton decomposition of a 3*3 matrix
            return pow(det, -1) * (0.5 * (pow(self.trace(), 2) - (self*self).trace()) * identity(self.h) -
                                   self.trace() * self + (self*self))

    def T(self):
        """Returns a transposed copy of this Matrix.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > transpose  = my_matrix.T()
        > print(transpose)
          1  3
          2  4
        """
        # Create a self.h * self.w matrix of zeros
        transpose = zeros(self.w, self.h)

        # Traverse each element in the matrix
        for i in range(self.h):
            for j in range(self.w):
                transpose.g[j][i] = self.g[i][j]

        return transpose

    def is_square(self):
        """Test if the number of rows and columns of a matrix are the same."""
        return self.h == self.w

    def __getitem__(self, idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """Defines the behavior of calling print on an instance of this class."""
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"

        return s

    def __add__(self, other):
        """Defines the behavior of the + operator.

        Example:

        > A = Matrix([ [1, 2], [3, 4] ])
        > B = Matrix([ [5, 6], [7, 8] ])
        > matrix_sum = A + B
        > print(matrix_sum)
          6  8
          10  12
        """
        if self.h != other.h or self.w != other.w:
            raise ValueError('Matrices can only be added if their dimensions are the same.')

        matrix_sum = zeros(self.h, self.w)

        for i in range(self.h):
            for j in range(self.w):
                matrix_sum.g[i][j] = self.g[i][j] + other.g[i][j]

        return matrix_sum

    def __neg__(self):
        """Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1  -2
          -3  -4
        """
        matrix_neg = zeros(self.h, self.w)

        for i in range(self.h):
            for j in range(self.w):
                matrix_neg.g[i][j] = -self.g[i][j]

        return matrix_neg

    def __sub__(self, other):
        """Defines the behavior of - operator (as subtraction).

        Example:

        > A = Matrix([ [1, 2], [3, 4] ])
        > B = Matrix([ [5, 6], [7, 8] ])
        > matrix_diff = A - B
        > print(matrix_diff)
          -2  -2
          -2  -2
        """
        matrix_diff = zeros(self.h, self.w)

        for i in range(self.h):
            for j in range(self.w):
                matrix_diff.g[i][j] = self.g[i][j] - other.g[i][j]

        return matrix_diff

    def __mul__(self, other):
        """Defines the behavior of * operator (matrix multiplication).

        Example:

        > A = Matrix([ [1, 2], [3, 4] ])
        > B = Matrix([ [5, 6], [7, 8] ])
        > matrix_mul = A * B
        > print(matrix_mul)
          19  22
          43  50
        """
        def dot_product(a: list, b: list) -> float:
            return sum([a[k] * b[k] for k in range(len(a))])

        if self.w != other.h:
            raise ValueError('Number or columns in left matrix does not match number of rows in right matrix.')

        matrix_mul = zeros(self.h, other.w)
        other_transpose = other.T()

        for i in range(self.h):
            for j in range(other.w):
                matrix_mul.g[i][j] = dot_product(self.g[i], other_transpose.g[j])

        return matrix_mul

    def __rmul__(self, other):
        """Called when the object on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2  0
          0  2
        """
        if isinstance(other, numbers.Number):

            matrix_rmul = zeros(self.h, self.w)

            for i in range(self.h):
                for j in range(self.w):
                    matrix_rmul.g[i][j] = self.g[i][j] * other

            return matrix_rmul

        else:
            raise ValueError('Can only reverse multiply a matrix by a matrix or scalar.')
