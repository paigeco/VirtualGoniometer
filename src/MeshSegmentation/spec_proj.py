import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

def spec_proj(W,k,alg=3):
    n = W.shape[0]
    deg = sp.spdiags(np.sum(W,1).T,0,n,n)
    L = deg - W
    
    if alg == 1:
        E,V = eigsh(L,k,sigma=-1,tol=1e-6,return_eigenvectors=True)
        V1 = V
    elif alg == 2:
        E,V = eigsh(L,k,deg,sigma=-1,tol=1e-6,return_eigenvectors=True)
        V1 = V
    else:
        Dinv2 = sp.spdiags(np.power(np.sum(W,1),(-1/2)).T,0,n,n) 
        Lsym = Dinv2@L@Dinv2
        
        E,V1 = eigsh(Lsym,k,sigma=-1,tol=1e-6,return_eigenvectors=True)
        T = sp.spdiags(np.power(np.sum(np.multiply(V1,V1),1).T,(-1/2)),0,n,n)
        V = T@V1
        D = sp.spdiags(E,0,k,k).toarray()    
    return V, D, V1
