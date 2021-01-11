import numpy as np

#Power method to find principle eigenvector
###########################################
def power_method(A,tol=1e-12):

    n = A.shape[0]
    x = np.random.rand(n,1)
    err = 1
    i = 1
    l = 0

    while err > tol:
        x = A@x
        x = x/np.linalg.norm(x)
        l = np.transpose(x)@A@x
        err = np.linalg.norm(A@x - l*x)
        i = i+1
    
    return l, x