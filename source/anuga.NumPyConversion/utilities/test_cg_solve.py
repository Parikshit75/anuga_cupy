#!/usr/bin/env python

import exceptions
class TestError(exceptions.Exception): pass
import unittest


from numpy import dot, allclose, array, transpose, arange, ones, float
from anuga.utilities.cg_solve import *
from anuga.utilities.cg_solve import _conjugate_gradient
from anuga.utilities.sparse import Sparse, Sparse_CSR


class Test_CG_Solve(unittest.TestCase):

    def test_sparse_solve(self):
        """Solve Small Sparse Matrix"""

        A = [[2.0, -1.0, 0.0, 0.0 ],
             [-1.0, 2.0, -1.0, 0.0],
             [0.0, -1.0, 2.0, -1.0],
             [0.0,0.0, -1.0, 2.0]]

        A = Sparse(A)

        xe = [0.0, 1.0, 2.0, 3.0]
        b  = A*xe
        x =  [0.0, 0.0, 0.0, 0.0]

        x = conjugate_gradient(A,b,x,iprint=0)

        assert allclose(x,xe)

    def test_max_iter(self):
        """Test max iteration Small Sparse Matrix"""

        A = [[2.0, -1.0, 0.0, 0.0 ],
             [-1.0, 2.0, -1.0, 0.0],
             [0.0, -1.0, 2.0, -1.0],
             [0.0,0.0, -1.0, 2.0]]

        A = Sparse(A)

        xe = [0.0, 1.0, 2.0, 3.0]
        b  = A*xe
        x =  [0.0, 0.0, 0.0, 0.0]

        try:
            x = conjugate_gradient(A,b,x,iprint=0,imax=2)
        except ConvergenceError:
            pass
        else:
            msg = 'Should have raised exception'
            raise TestError, msg


    def test_solve_large(self):
        """Standard 1d laplacian """

        n = 50
        A = Sparse(n,n)

        for i in arange(0,n):
            A[i,i] = 1.0
            if i > 0 :
                A[i,i-1] = -0.5
            if i < n-1 :
                A[i,i+1] = -0.5

        xe = ones( (n,), float)

        b  = A*xe
        x = conjugate_gradient(A,b,b,tol=1.0e-5,iprint=1)

        assert allclose(x,xe)

    def test_solve_large_2d(self):
        """Standard 2d laplacian"""

        n = 20
        m = 10

        A = Sparse(m*n, m*n)

        for i in arange(0,n):
            for j in arange(0,m):
                I = j+m*i
                A[I,I] = 4.0
                if i > 0  :
                    A[I,I-m] = -1.0
                if i < n-1 :
                    A[I,I+m] = -1.0
                if j > 0  :
                    A[I,I-1] = -1.0
                if j < m-1 :
                    A[I,I+1] = -1.0

        xe = ones( (n*m,), float)

        b  = A*xe
        x = conjugate_gradient(A,b,b,iprint=0)

        assert allclose(x,xe)

    def test_solve_large_2d_csr_matrix(self):
        """Standard 2d laplacian with csr format
        """

        n = 100
        m = 100

        A = Sparse(m*n, m*n)

        for i in arange(0,n):
            for j in arange(0,m):
                I = j+m*i
                A[I,I] = 4.0
                if i > 0  :
                    A[I,I-m] = -1.0
                if i < n-1 :
                    A[I,I+m] = -1.0
                if j > 0  :
                    A[I,I-1] = -1.0
                if j < m-1 :
                    A[I,I+1] = -1.0

        xe = ones( (n*m,), float)

        # Convert to csr format
        #print 'start covert'
        A = Sparse_CSR(A)
        #print 'finish covert'
        b = A*xe
        x = conjugate_gradient(A,b,b,iprint=20)

        assert allclose(x,xe)


    def test_solve_large_2d_with_default_guess(self):
        """Standard 2d laplacian using default first guess"""

        n = 20
        m = 10

        A = Sparse(m*n, m*n)

        for i in arange(0,n):
            for j in arange(0,m):
                I = j+m*i
                A[I,I] = 4.0
                if i > 0  :
                    A[I,I-m] = -1.0
                if i < n-1 :
                    A[I,I+m] = -1.0
                if j > 0  :
                    A[I,I-1] = -1.0
                if j < m-1 :
                    A[I,I+1] = -1.0

        xe = ones( (n*m,), float)

        b  = A*xe
        x = conjugate_gradient(A,b)

        assert allclose(x,xe)


    def test_vector_shape_error(self):
        """Raise VectorShapeError"""

        A = [[2.0, -1.0, 0.0, 0.0 ],
             [-1.0, 2.0, -1.0, 0.0],
             [0.0, -1.0, 2.0, -1.0],
             [0.0,0.0, -1.0, 2.0]]

        A = Sparse(A)

        xe = [[0.0,2.0], [1.0,3.0], [2.0,4.0], [3.0,2.0]]

        try:
            x = _conjugate_gradient(A,xe,xe,iprint=0)
        except VectorShapeError:
            pass
        else:
            msg = 'Should have raised exception'
            raise TestError, msg


    def test_sparse_solve_matrix(self):
        """Solve Small Sparse Matrix"""

        A = [[2.0, -1.0, 0.0, 0.0 ],
             [-1.0, 2.0, -1.0, 0.0],
             [0.0, -1.0, 2.0, -1.0],
             [0.0,0.0, -1.0, 2.0]]

        A = Sparse(A)

        xe = [[0.0, 0.0],[1.0, 1.0],[2.0 ,2.0],[3.0, 3.0]]
        b = A*xe
        x = [[0.0, 0.0],[0.0, 0.0],[0.0 ,0.0],[0.0, 0.0]]
        x = conjugate_gradient(A,b,x,iprint=0)

        assert allclose(x,xe)

#-------------------------------------------------------------
if __name__ == "__main__":
     suite = unittest.makeSuite(Test_CG_Solve,'test')
     #runner = unittest.TextTestRunner(verbosity=2)
     runner = unittest.TextTestRunner(verbosity=1)
     runner.run(suite)

