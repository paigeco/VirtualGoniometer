#import numpy.random as rand

import numpy as np
import scipy.sparse as sp
from src.MeshSegmentation.conjgrad import conjgrad

def poisson_learning(W, g, I):
    k = len(np.unique(g))
    n = W.shape[0]
    m = len(I)
    I = I - 1
    g = g.T - 1

    F = np.zeros((n, k))
    for i in range(m):
        F[I[i], g[i]] = 1
    c = np.ones((1, n)) @ F / len(g)
    F[I] -= c
    
    deg = np.sum(W, 1)
    D = sp.spdiags(deg.T, 0, n, n)
    L = D-W #Unnormalized graph laplacian matrix
    
    #Preconditioning
    Dinv2 = sp.spdiags(np.power(np.sum(W, 1), -1/2).T, 0, n, n) 
    Lnorm = Dinv2 @ L @ Dinv2
    F = Dinv2 @ F
    
    #Conjugate Gradient Solver
    u, i = conjgrad(Lnorm,  F,  np.zeros((n, k)), 1e5,  np.sqrt(n)*1e-10)
    
    #Undo preconditioning
    u = Dinv2 @ u
    return u
